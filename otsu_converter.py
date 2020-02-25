import zmq
from skimage.filters import threshold_otsu
from skimage.color import rgb2gray
import cv2
import sys
import pickle


def consumer(port_send, port_rec):
    print("Otsu converter started sending on port "+ port_send + " Listening to port " + port_rec)
    context = zmq.Context()
    # receive socket setup
    consumer_receiver = context.socket(zmq.PULL)
    consumer_receiver.connect("tcp://127.0.0.1:"+port_rec)
    # send socket setup
    consumer_sender = context.socket(zmq.PUSH)
    consumer_sender.connect("tcp://127.0.0.1:"+port_send)

    while True:
        message = {}
        # receive message and transform it into grayscale
        message = pickle.loads(consumer_receiver.recv())
        index, frame = message['fnumber'], message['frame']
        gray = rgb2gray(frame)
        # get suitable threshold using otsu algorithm
        threshold = threshold_otsu(gray)
        # applying threshold on the grayscale image and convert it to binary
        binary_frame = (gray > threshold).astype(int)
        message = {'fnumber': index, 'frame': binary_frame}
        # send message to collector stage 1
        consumer_sender.send(pickle.dumps(message))


def main():
    if len(sys.argv) != 3:
        print("Wrong arguments")
        exit()
    else:
        _,port_send, port_rec = sys.argv
        consumer(port_send, port_rec)


if __name__ == '__main__':
    main()
