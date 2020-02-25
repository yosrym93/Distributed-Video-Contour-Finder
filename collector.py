import zmq
import os
import sys
import pickle

output_file = 'output.txt'


def init_connection(receive_port):
    context = zmq.Context.instance()
    receive_socket = context.socket(socket_type=zmq.PULL)
    receive_socket.bind('tcp://*:{}'.format(receive_port))
    return receive_socket


def write_bounding_boxes(frame_number, bounding_boxes):
    file = open(output_file, 'a')
    print('frame number: {}'.format(frame_number), file=file)
    for bounding_box in bounding_boxes:
        print('x_min: {0}, x_max: {1}, y_min: {2}, y_max: {3}'.format(*bounding_box), file=file)
    file.close()
    print('Data written')


def main():
    try:
        os.remove(output_file)
    except FileNotFoundError:
        pass

    if len(sys.argv) != 2:
        print('Wrong number of arguments')
        exit()
    _, receive_port = sys.argv
    receive_socket = init_connection(receive_port)
    print('Collector started, listening on port {}..'.format(receive_port))
    while True:
        received_data = pickle.loads(receive_socket.recv())
        frame_number, bounding_boxes = received_data['fnumber'], received_data['bounding_boxes']
        write_bounding_boxes(frame_number, bounding_boxes)


if __name__ == '__main__':
    main()
