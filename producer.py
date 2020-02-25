import zmq
from extract_video import extract_video
import sys
import pickle
import config


def producer(port):
    context = zmq.Context()
    # send socket setup
    zmq_socket = context.socket(zmq.PUSH)
    zmq_socket.bind("tcp://127.0.0.1:"+port)
    # extract given imput frames to send it
    frames = extract_video(config.sample_video_path)
    message = {}
    print("Producer started sending on "+port)
    for index in range(len(frames)):
        message = {'fnumber': index, 'frame': frames[index]}
        zmq_socket.send(pickle.dumps(message))


def main():
    if len(sys.argv) != 2:
        print("Wrong arguments")
        exit()
    else:
        _,port_send = sys.argv
        producer(port_send)


if __name__ == '__main__':
    main()
