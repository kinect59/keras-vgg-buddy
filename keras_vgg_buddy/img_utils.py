import numpy as np
from scipy.misc import imread, imresize

from . import vgg16


# util function to open, resize and format pictures into appropriate tensors
def load_image(image_path):
    return imread(image_path , mode='RGB')  # NOTE: this mode kwarg requires v0.17


# util function to open, resize and format pictures into appropriate tensors
def preprocess_image(x, img_width, img_height):
    img = imresize(x, (img_height, img_width), interp='bicubic').astype('float32')
    img = vgg16.img_to_vgg(img)
    img = np.expand_dims(img, axis=0)
    return img


def load_and_preprocess_image(path, width=None, square=False):
    img = load_image(path)
    n_channels, n_rows, n_cols = img.shape[::-1]
    if width:
        n_rows = int(float(width) / n_cols * n_rows)
        n_cols = width
    if square:
        n_rows = n_cols
    img = preprocess_image(img, n_cols, n_rows)[0]
    return img


# util function to convert a tensor into a valid image
def deprocess_image(x, contrast_percent=0.0, resize=None):
    x = vgg16.img_from_vgg(x)
    if contrast_percent:
        min_x, max_x = np.percentile(x, (contrast_percent, 100 - contrast_percent))
        x = (x - min_x) * 255.0 / (max_x - min_x)
    x = np.clip(x, 0, 255)
    if resize:
        x = imresize(x, resize, interp='bicubic')
    return x.astype('uint8')