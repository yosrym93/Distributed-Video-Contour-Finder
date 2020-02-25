import cv2


def extract_video(path):
    """
    this function takes a video path and extract frames
    :param path: path to the video.
    :return: returns frames of the given video in the parameters
    """
    vcap = cv2.VideoCapture(path)
    frames = []
    if vcap.isOpened():
        success, frame = vcap.read()
        # loop until no frames can be extracted from the video
        while success:
            # append frame extracted in the lis of frames and extract another one
            frames.append(frame)
            success, frame = vcap.read()
        vcap.release()
    return frames
