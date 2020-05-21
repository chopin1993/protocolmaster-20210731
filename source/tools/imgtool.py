import scipy
import io
import colorcet as cc
import scipy.misc
import numpy as np

color_map = np.array(cc.linear_bgy_10_95_c74)*255


def numpy2color(gray_array, min_value=10.0, max_value=40.0):
    rows, cols = gray_array.shape
    gray_array = np.copy(gray_array)
    gray_array[np.where(gray_array < min_value)] = min_value
    gray_array[np.where(gray_array > max_value)] = max_value
    raw_byte = (gray_array - min_value)/(max_value - min_value)*255
    raw_byte = raw_byte.astype(np.int)
    color_array = np.zeros((rows, cols, 3), np.uint8)
    for i in range(0, rows):
        for j in range(0, cols):
            color_array[i, j] = color_map[raw_byte[i,j]]
    return color_array


def color2jpg(color):
    buf = io.BytesIO()
    img = scipy.misc.imresize(color, (240,320), interp='nearest')
    scipy.misc.imsave(buf, img, format="jpeg")
    data = buf.getvalue()
    buf.close()
    return data


def numpy2jpg(gray_array, min_value=12.0, max_value=37.0):
    data = numpy2color(gray_array, min_value=min_value, max_value=max_value)
    return color2jpg(data)