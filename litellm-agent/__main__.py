import hypercorn
import asyncio
import restate

from app.chaining import call_chaining_svc

app = restate.app(
    services=[
        call_chaining_svc,
    ]
)

if __name__ == "__main__":
    conf = hypercorn.Config()
    conf.bind = ["0.0.0.0:9080"]
    asyncio.run(hypercorn.asyncio.serve(app, conf))
