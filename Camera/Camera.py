import time
import picamera
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import pygame
from pygame.local import *

# Set camera resolution
width = 1920
height = 1080

# Button Size
button = 100

# Initialize overlay
image_array = np.zeros((height, width, 4), np.uint8)
image = Image.fromarray(image_array)
draw = ImageDraw.Draw(image)

# Initialize camera
camera = picamera.PiCamera()
camera.resolution = (width, height)
camera.framerate = 30
camera_array = np.asarray(image)
overlay = camera.add_overlay(bytes(memoryview(camera_array)), format='rgba', layer=3)
camera.start_preview()
end = 0

pygame.init()
windowSurfaceObj = pygame.display.set_mode((width, height), pygame.FULLSCREEN)


def on_press(key):
    global end, overlay
    if key == pygame.K_ESCAPE:
        camera.remove_overlay(overlay)
        camera.close()
        pygame.disply.quit()
        end = 1
        exit()
    elif key == pygame.K_ENTER:
        camera.capture("test.png")

while end == 0 :
    time.sleep(0.1)
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            key = event.key
            on_press(key)
