from wand.image import Image
import numpy as np
import cv2

with Image(filename='52346.jpg') as img:
    img.virtual_pixel = 'black'
    img.implode(0.5)
    img.save(filename='emad_implode.jpg')
    # convert to opencv/numpy array format
    img_implode_opencv = np.array(img)
    img_implode_opencv = cv2.cvtColor(img_implode_opencv, cv2.COLOR_RGB2BGR)

with Image(filename='52346.jpg') as img:
    img.virtual_pixel = 'black'
    img.implode(-0.5 )
    img.save(filename='emad_explode.jpg')
    # convert to opencv/numpy array format
    img_explode_opencv = np.array(img)
    img_explode_opencv = cv2.cvtColor(img_explode_opencv, cv2.COLOR_RGB2BGR)

# display result with opencv
cv2.imshow("IMPLODE", img_implode_opencv)
cv2.imshow("EXPLODE", img_explode_opencv)
cv2.waitKey(0)