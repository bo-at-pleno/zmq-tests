import asyncio
import logging
import time

import aiozmq.rpc
import zmq

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s")


async def pub():
    stream = await aiozmq.stream.create_zmq_stream(
        zmq_type=zmq.PUB,
        bind="tcp://127.0.0.1:5556",
    )

    while True:
        await asyncio.sleep(1)
        msg = [str(time.time()).encode()]
        logging.info(f"write {msg}")
        stream.write(msg)


async def sub(name: str):
    stream = await aiozmq.stream.create_zmq_stream(
        zmq_type=zmq.SUB,
        connect="tcp://127.0.0.1:5556",
    )
    stream.transport.subscribe(b"")

    while True:
        logging.info(f"{name} waiting ...")
        msg = await stream.read()
        logging.info(f"{name} received {msg}")


def main():
    # task group
    async def do():
        async with asyncio.TaskGroup() as g:
            g.create_task(pub())
            g.create_task(sub(name="sub1"))
            g.create_task(sub(name="sub2"))
            await asyncio.sleep(10)
            await g.cancel_remaining()

    asyncio.run(do())
    logging.info("DONE")


if __name__ == "__main__":
    main()
