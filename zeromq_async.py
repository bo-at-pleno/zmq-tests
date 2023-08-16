"""ZeroMQ has its own asyncio impl of context
"""

import asyncio

import zmq
import zmq.asyncio

ctx = zmq.asyncio.Context()


async def pub():
    sock = ctx.socket(zmq.PUB)
    sock.bind("inproc://example")

    i = 0
    while True:
        await sock.send(f"Hello from publisher {i}".encode("utf-8"))
        await asyncio.sleep(1)
        i += 1


async def sub():
    sock = ctx.socket(zmq.SUB)
    sock.connect("inproc://example")
    sock.setsockopt_string(zmq.SUBSCRIBE, "")

    while True:
        msg = await sock.recv()
        print(f"Received: {msg.decode('utf-8')}")
        await asyncio.sleep(1)


async def async_main():
    tg = asyncio.gather(pub(), sub())
    await tg


def main():
    asyncio.run(async_main())
    print("DONE")


if __name__ == "__main__":
    main()
