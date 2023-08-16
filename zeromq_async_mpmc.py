"""ZeroMQ has its own asyncio impl of context
"""

import asyncio
import random

import zmq
import zmq.asyncio

ctx = zmq.asyncio.Context()


async def pub(publisher_id):
    sock = ctx.socket(zmq.PUB)
    sock.bind("tcp://127.0.0.1:5555")
    topics = ["topic1", "topic2", "topic3"]

    while True:
        topic = topics[random.randint(0, len(topics) - 1)]
        message = f"Message from Pub {publisher_id} on {topic}".encode("utf-8")
        await sock.send_multipart([topic.encode("utf-8"), message])
        await asyncio.sleep(1)


async def sub(subscriber_id):
    sock = ctx.socket(zmq.SUB)
    for pub_id in range(3):
        sock.connect("tcp://127.0.0.1:5555")
    sock.setsockopt_string(zmq.SUBSCRIBE, "")

    while True:
        topic, message = await sock.recv_multipart()
        print(f"Subscriber {subscriber_id} received [{topic.decode('utf-8')}]: {message.decode('utf-8')}")


async def async_main():
    num_publishers = 1
    num_subscribers = 3

    publishers = [pub(i) for i in range(num_publishers)]
    subscribers = [sub(i) for i in range(num_subscribers)]

    await asyncio.gather(*publishers, *subscribers)


def main():
    asyncio.run(async_main())
    print("DONE")


if __name__ == "__main__":
    main()
