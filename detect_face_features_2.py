import numpy as np
import cv2 as cv

f_img = '52346.jpg'
im_cv = cv.imread(f_img)

# grab the dimensions of the image
(h, w, _) = im_cv.shape

# set up the x and y maps as float32
flex_x = np.zeros((h, w), np.float32)
flex_y = np.zeros((h, w), np.float32)

# create map with the barrel pincushion distortion formula
for y in range(h):
    delta_y = scale_y * (y - center_y)
    for x in range(w):
        # determine if pixel is within an ellipse
        delta_x = scale_x * (x - center_x)
        distance = delta_x * delta_x + delta_y * delta_y
        if distance >= (radius * radius):
            flex_x[y, x] = x
            flex_y[y, x] = y
        else:
            factor = 1.0
            if distance > 0.0:
                factor = math.pow(math.sin(math.pi * math.sqrt(distance) / radius / 2), -amount)
            flex_x[y, x] = factor * delta_x / scale_x + center_x
            flex_y[y, x] = factor * delta_y / scale_y + center_y

# do the remap  this is where the magic happens
dst = cv.remap(im_cv, flex_x, flex_y, cv.INTER_LINEAR)

cv.imshow('src', im_cv)
cv.imshow('dst', dst)

cv.waitKey(0)
cv.destroyAllWindows()