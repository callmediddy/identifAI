from PIL import Image
import numpy as np
import scipy.fftpack

def to_hash_string(difference):
    decimal_value = 0
    hex_string = []
    for index, value in enumerate(difference):
        if value:
            decimal_value += 2**(index % 8)
        if (index % 8) == 7:
            hex_string.append(hex(decimal_value)[2:].rjust(2, '0'))
            decimal_value = 0
    return ''.join(hex_string)

def difference_hash(image, hash_size = 8):
    # Resizing image to (9 x 8) box in order to calculate frequencies
    image = image.convert('L').resize((hash_size + 1, hash_size), Image.ANTIALIAS)
    pixels = list(image.getdata())
    difference = []
    for row in range(hash_size):
        for col in range(hash_size):
            pixel_left = image.getpixel((col, row))
            pixel_right = image.getpixel((col + 1, row))
            difference.append(pixel_left > pixel_right)
    return to_hash_string(difference)

def average_hash(image, hash_size = 8):
    image = image.convert("L").resize((hash_size, hash_size), Image.ANTIALIAS)
    pixels = np.array(image.getdata()).reshape((hash_size, hash_size))
    average = pixels.mean()
    difference = []
    for row in range(hash_size):
        for col in range(hash_size):
            pixel = image.getpixel((col, row))
            difference.append(pixel > average)
    return to_hash_string(difference)

def hamming_distance(hash_to_check, hash_against, distance):
    hash_to_check_bin = bin(int.from_bytes(hash_to_check.encode(), 'big'))
    hash_against_bin =  bin(int.from_bytes(hash_against.encode(), 'big'))
    hamm_distance = int(hash_against_bin[2:]) ^ int(hash_to_check_bin[2:])
    if(hamm_distance <= distance):
        return True
    else:
        return False