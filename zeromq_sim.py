import time
from multiprocessing import Process

import zmq as pyzmq


def process1():
    ctx = pyzmq.Context()
    socket = ctx.socket(pyzmq.PUB)
    socket.bind("tcp://127.0.0.1:5555")  # Bind to a specific address
    time.sleep(0.5)
    work_items = ["Work Item 1", "Work Item 2", "Work Item 3"]
    for item in work_items:
        socket.send_string(item)
        print(f"Process 1 sent: {item}\n")

    # Send a termination signal to process2
    socket.send_string("TERMINATE")
    print("Process 1 sent termination signal\n")

    # Close the socket and context
    socket.close()
    ctx.term()
    print("Process 1 complete.\n")


def process2():
    ctx = pyzmq.Context()
    socket = ctx.socket(pyzmq.SUB)
    socket.connect("tcp://127.0.0.1:5555")  # Connect to the same address as process1
    socket.setsockopt_string(pyzmq.SUBSCRIBE, "")  # Subscribe to all topics

    print("Starting to receive messages...\n")
    while True:
        message = socket.recv_string()
        if message == "TERMINATE":
            break

        print(f"Process 2 received: {message}\n")

    # Close the socket and context
    socket.close()
    ctx.term()


def main():
    p1 = Process(target=process1)
    p2 = Process(target=process2)

    p1.start()
    p2.start()

    print("Started P1 and P2")

    p1.join()
    print("Joined P1")
    p2.join()
    print("Joined P2")


if __name__ == "__main__":
    main()
