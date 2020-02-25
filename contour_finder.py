import numpy as np
from skimage.measure import find_contours
import skimage.io as io
import zmq
import sys
import pickle


def init_connection(receive_address, receive_port, send_port):
    context = zmq.Context.instance()

    send_socket = context.socket(socket_type=zmq.PUSH)
    send_socket.connect("tcp://127.0.0.1:{}".format(send_port))

    receive_socket = context.socket(socket_type=zmq.PULL)
    receive_socket.connect('tcp://{0}:{1}'.format(receive_address, receive_port))
    return send_socket, receive_socket


def get_contours(binary_img):
    contours = np.array(find_contours(binary_img, 0.8))
    bounding_boxes = []
    for contour in contours:
        x_min = np.min(contour[:, 1]).astype(int)
        x_max = np.max(contour[:, 1]).astype(int)
        y_min = np.min(contour[:, 0]).astype(int)
        y_max = np.max(contour[:, 0]).astype(int)
        bounding_boxes.append([x_min, x_max, y_min, y_max])

    return bounding_boxes


def send_contours(send_socket, frame_number, bounding_boxes):
    frame_contours = {'fnumber': frame_number, 'bounding_boxes': bounding_boxes}
    send_socket.send(pickle.dumps(frame_contours))


def main():
    if len(sys.argv) != 4:
        print('Wrong number of arguments')
        exit()
    _, receive_address, receive_port, send_port = sys.argv
    send_socket, receive_socket = init_connection(receive_address, receive_port, send_port)
    print('Contour finder started, connected to Collector on port {0}, '
          'listening on {1}:{2}..'.format(send_port, receive_address, receive_port))
    while True:
        frame = pickle.loads(receive_socket.recv())
        frame_number, frame_data = frame['fnumber'], frame['frame']
        io.imsave('frames/frame{}.jpg'.format(frame_number), (frame_data*255).astype(np.uint8))
        print('Frame {} received'.format(frame_number))
        bounding_boxes = get_contours(frame_data)
        send_contours(send_socket, frame_number, bounding_boxes)


if __name__ == '__main__':
    main()
