import zmq
import cv2
import sys
import pickle
import numpy as np


def collector_stage1(port_send, port_rec):
    print("Collector stage 1 started sending on port "+port_send + " Listening to port " + port_rec)
    context = zmq.Context()
    # receive socket setup
    collector_receiver = context.socket(zmq.PULL)
    collector_receiver.bind("tcp://127.0.0.1:"+port_rec)
    # send socket setup
    collector_sender = context.socket(zmq.PUSH)
    collector_sender.bind("tcp://*:"+port_send)
    # main loop
    while True:
        # receive message
        message = pickle.loads(collector_receiver.recv())
        index, frame = message['fnumber'], message['frame']
        # saving the frames received by collector
        cv2.imwrite("frames_machine1/frame%d.jpeg" % index, frame*255)
        frame = frame.astype(np.uint8)
        message = {'fnumber': index, 'frame': frame}
        collector_sender.send(pickle.dumps(message))


def main():
    if len(sys.argv) != 3:
        print("Wrong arguments")
        exit()
    else:
        _,port_send, port_rec = sys.argv
        collector_stage1(port_send,port_rec)


if __name__ == '__main__':
    main()
