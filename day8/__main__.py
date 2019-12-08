import numpy as np
from matplotlib import pyplot as plt

from utils import get_data

pixels = list(map(int, get_data(test=False).strip()))
# flat image
fimage = np.array(pixels, dtype=int)

w = 25
h = 6
n = fimage.size // (w * h)
# vstacked image
vimage = fimage.reshape((h * n, w))
# dstacked images
image = np.dstack(tuple((vimage[h * i : h * (i + 1), :]) for i in range(n)))

# Find layer with the fewers number of zeros, calc checksum
n_zero = (image == 0).astype(int).sum(1).sum(0)
min_z_layer = np.argmin(n_zero)
n_ones = (image[..., min_z_layer] == 1).sum()
n_twos = (image[..., min_z_layer] == 2).sum()
print(f"Layer number {min_z_layer} has the fewest zeros. Checksum: {n_ones * n_twos}")

# Decode image
# Find the first layer with non-transparent pixel for each coordinate
layers = np.argmax((image != 2).astype(int), axis=2)
# Create tuple of indices for these pixels
r_idx = np.indices(layers.shape)[0]
c_idx = np.indices(layers.shape)[1]
pix_idx = (r_idx, c_idx, layers)
image = image[pix_idx]
print("====== Decoded image =======")
# Make it a bit more human readable
im_out = np.chararray(image.shape)
for row in image:
    print("".join(("#" if p == 1 else " " for p in row)))
