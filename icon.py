import os
import pygame

def load(image, color):
	filename = os.path.join("images", image)
	surface = pygame.image.load(filename).convert_alpha()
	pixel_array = pygame.PixelArray(surface)
	pixel_array.replace((255,255,255), color)
	pixel_array.close()
	return surface
