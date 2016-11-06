#!/usr/bin/env python2
# -.- coding: utf-8

import socket, time
from PIL import Image, ImageFont, ImageDraw
import sys
import fileinput
import threading

UDPHOST="flipdot.openlab.lan"
UDPPORT=2323

FPS = 13
STEPS = 1
INVERT=True

DISPLAY_SIZE = (80, 16)
FONT_SIZE = 16
FONT_OFFSET= (1, -1)

C_BLACK = (0, 0, 0)
C_WHITE = (255, 255, 255)

finished = False
framebuffer = []

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def list2byte(l):
    byte = 0
    i = 0
    for i in range(8):
        byte += 2**(7-i) if l[i] else 0
    return byte

def array2packet(a):
    return str(bytearray([list2byte(a[i*8:i*8+8]) for i in range(len(a)/8)]))

def str2array(s):
    font = ImageFont.load_default()

    img_width = font.getsize(s)[0]
    image     = Image.new("RGBA", (img_width,DISPLAY_SIZE[1]), C_BLACK)
    draw      = ImageDraw.Draw(image)
    draw.fontmode = "1" # no AA

    draw.text(FONT_OFFSET, s, font=font, fill=C_WHITE)

    imgmap = []
    for pixel in image.getdata():
        r, g, b, a = pixel
        if r == 255:
            imgmap.append(0 if INVERT else 1)
        else:
            imgmap.append(1 if INVERT else 0)
    return imgmap

def render_frames(imgmap):
    global framebuffer
    global finished

    framebuffer = []

    finished = False

    display_width  = DISPLAY_SIZE[0]
    display_heigth = DISPLAY_SIZE[1]

    imgmap_width    = len(imgmap) / display_heigth
    scrollimg_width = imgmap_width + 2*display_width

    scroll_imgmap = [1 if INVERT else 0] * (scrollimg_width * display_heigth)

    # expand imgmap
    for row in range(display_heigth):
        for col in range(imgmap_width):
            scroll_imgmap[display_width-STEPS + row*scrollimg_width + col] = imgmap[col+row*imgmap_width]

    # scroll img
    curr_frame = [0] * display_width * display_heigth

    for offset in range(0, scrollimg_width-display_width, STEPS):
        for row in range(display_heigth):
            for col in range(display_width):
                    curr_frame[col+row*display_width] = scroll_imgmap[col+row*scrollimg_width + offset]

        framebuffer.append(array2packet(curr_frame))

    finished = True


def send_frames():
    global framebuffer
    global finished
    frame_pos = 0

    def frames_left(frame_pos, framebuffer):
        return frame_pos < len(framebuffer)

    while not finished or frames_left(frame_pos, framebuffer):
        if frames_left(frame_pos, framebuffer):
            sock.sendto(framebuffer[frame_pos], (UDPHOST, UDPPORT))
            time.sleep(1.0/FPS)
            frame_pos += 1
        else:
            continue

try:
    while True:
        text = sys.stdin.readline().decode('utf-8').strip()
        if text == "":
            break
        imgmap = str2array(text)

        renderer = threading.Thread(target=render_frames,args=(imgmap,))
        sender = threading.Thread(target=send_frames)

        renderer.start()
        sender.start()

        sender.join()

except KeyboardInterrupt:
    print("Exited due to Ctrl-C")
    sys.exit(0)
