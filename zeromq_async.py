import asyncio

import aiozmq


async def process1():
    ctx = await aiozmq.create_zmq_context()
    socket = await ctx.socket(aiozmq.ZMQ_PUB)
    await socket.bind("tcp://127.0.0.1:5555")  # Bind to a specific address

    # Simulate generating work items (messages) and sending them
    work_items = ["Work Item 1", "Work Item 2", "Work Item 3"]
    for item in work_items:
        await socket.send_string(item)
        print(f"Process 1 sent: {item}")

    # Send a termination signal to process2
    await socket.send_string("TERMINATE")
    print("Process 1 sent termination signal")

    # Close the socket and context
    await socket.close()
    await ctx.destroy()
    print("Process 1 complete.")


async def process2():
    ctx = await aiozmq.create_zmq_context()
    socket = await ctx.socket(aiozmq.ZMQ_SUB)
    await socket.connect("tcp://127.0.0.1:5555")  # Connect to the same address as process1
    await socket.setsockopt_string(aiozmq.ZMQ_SUBSCRIBE, "")  # Subscribe to all topics

    print("Starting to receive messages...")
    while True:
        message = await socket.recv_string()
        if message == "TERMINATE":
            break

        print(f"Process 2 received: {message}")

    # Close the socket and context
    await socket.close()
    await ctx.destroy()


async def main():
    task1 = asyncio.create_task(process1())
    task2 = asyncio.create_task(process2())

    await asyncio.gather(task1, task2)


if __name__ == "__main__":
    asyncio.run(main())
