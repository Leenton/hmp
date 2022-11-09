
import asyncio
import json
from datetime import datetime, timedelta
from wsgiref.simple_server import make_server
from falcon.asgi import App, SSEvent


async def thing(wait):
    print('waiting for', wait)
    await asyncio.sleep(wait)
    return {'ok': 1}


class Res:
    async def on_get_stream(self, req, resp):
        print('on_get_stream')
        # works:
        async def wait_for_result_and_yield_keepalives():
            awaitable = thing(wait := req.get_param_as_int('wait', default=10))
            while True:
                done, pending = await asyncio.wait((awaitable,), timeout=wait // 10)
                if not done:
                    print('sending keep-alive')
                    awaitable = pending.pop()
                    yield b' '
                    continue
                break
            result = done.pop().result()
            print(f'scan done {result=}')
            yield json.dumps(result).encode('utf-8')

        resp.stream = wait_for_result_and_yield_keepalives()

    async def on_get_event(self, req, resp):
        print('on_get_event')
        # does not work (will get stuck):
        async def wait_for_result_and_yield_keepalives():
            awaitable = thing(wait := req.get_param_as_int('wait', default=10))
            start = datetime.utcnow()
            end = start + timedelta(seconds=wait)
            yield SSEvent(event='scheduled', json={'end': end.isoformat()})
            while True:
                done, pending = await asyncio.wait(
                    (awaitable,), timeout=min(wait // 10, 30)
                )
                if not done:
                    print('sending keep-alive')
                    awaitable = pending.pop()
                    eta = end - datetime.utcnow()
                    yield SSEvent(event='keep-alive', json={'eta': eta.total_seconds()})
                    # yield SSEvent(event='keep-alive')
                    continue
                break
            result = done.pop().result()
            print(f'scan done {result=}')
            yield SSEvent(event='result', json=result)

        resp.sse = wait_for_result_and_yield_keepalives()


app = App()
res = Res()
app.add_route('/stream', res, suffix='stream')
app.add_route('/event', res, suffix='event')

with make_server('',80,handler) as httpd:
    httpd.serve_forever()