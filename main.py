import numpy as np
from PIL import Image
import cv2
import curses
import os
import sys

C = " .'`^\",:;Il!i~+_-?][}{1)(|/tfjrxnuvczXYUJCLQ0OZwmqpdbkhao*#MW&8%B@$"
L = len(C)


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


def frame_to_text(frame, max_height, max_width):
    img = Image.fromarray(frame).convert('L')
    img = img.resize((max_width, max_height))
    arr = np.array(img)
    return '\n'.join(''.join(C[int(p / 255 * (L - 1))] for p in row) for row in arr)


def video_to_ascii(screen, video_path):
    cap = cv2.VideoCapture(video_path)
    ret, frame = cap.read()

    max_height, max_width = curses.LINES - 1, curses.COLS - 1

    while ret:
        ret, frame = cap.read()
        if not ret:
            break

        ascii_frame = frame_to_text(frame, max_height, max_width)

        screen.clear()
        screen.addstr(0, 0, ascii_frame)
        screen.refresh()

    cap.release()


if __name__ == '__main__':

    video_file = input("Enter the name of the video file (with extensions, for example: video.mp4).): ").strip()

    if not os.path.isfile(resource_path(video_file)):
        print(f"Error: file '{video_file}' not found!")
    else:
        curses.wrapper(video_to_ascii, resource_path(video_file))
