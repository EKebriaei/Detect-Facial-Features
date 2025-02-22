# import the necessary packages
from collections import OrderedDict
import numpy as np
import cv2
import argparse
import dlib
import imutils

facial_features_cordinates = {}

# define a dictionary that maps the indexes of the facial
# landmarks to specific face regions
FACIAL_LANDMARKS_INDEXES = OrderedDict([
    ("Mouth", (48, 68)),
    ("Right_Eyebrow", (17, 22)),
    ("Left_Eyebrow", (22, 27)),
    ("Right_Eye", (36, 42)),
    ("Left_Eye", (42, 48)),
    ("Nose", (27, 35)),
    ("Jaw", (0, 17))
])

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-p", "--shape-predictor", required=True,
	help="path to facial landmark predictor")
ap.add_argument("-i", "--image", required=True,
	help="path to input image")
ap.add_argument("-t", "--threshold", required=False,
	help="Threshold number")
args = vars(ap.parse_args())


def shape_to_numpy_array(shape, dtype="int"):
    # initialize the list of (x, y)-coordinates
    coordinates = np.zeros((68, 2), dtype=dtype)

    # loop over the 68 facial landmarks and convert them
    # to a 2-tuple of (x, y)-coordinates
    for i in range(0, 68):
        coordinates[i] = (shape.part(i).x, shape.part(i).y)

    # return the list of (x, y)-coordinates
    return coordinates


def visualize_facial_landmarks(image, shape, colors=None, alpha=0.75):
    # create two copies of the input image -- one for the
    # overlay and one for the final output image
    overlay = image.copy()
    output = image.copy()

    # if the colors list is None, initialize it with a unique
    # color for each facial landmark region
    if colors is None:
        colors = [(19, 199, 109), (79, 76, 240), (230, 159, 23),
                  (168, 100, 168), (158, 163, 32),
                  (163, 38, 32), (180, 42, 220)]

    # loop over the facial landmark regions individually
    for (i, name) in enumerate(FACIAL_LANDMARKS_INDEXES.keys()):
        # grab the (x, y)-coordinates associated with the
        # face landmark
        (j, k) = FACIAL_LANDMARKS_INDEXES[name]
        pts = shape[j:k]
        # if name == 'Left_Eye':
        # if name == 'Nose':
        #     width = int(src.shape[1] * scale_percent / 100)
        #     height = int(src.shape[0] * scale_percent / 100)

        facial_features_cordinates[name] = pts

        # check if are supposed to draw the jawline
        # if name == "Jaw":
        #     # since the jawline is a non-enclosed facial region,
        #     # just draw lines between the (x, y)-coordinates
        #     for l in range(1, len(pts)):
        #         ptA = tuple(pts[l - 1])
        #         ptB = tuple(pts[l])
        #         cv2.line(overlay, ptA, ptB, colors[i], 2)

        # otherwise, compute the convex hull of the facial
        # landmark coordinates points and display it
        # else:
        #     hull = cv2.convexHull(pts)
        #     cv2.drawContours(overlay, [hull], -1, colors[i], -1)
        if name != "Jaw" and name == "Left_Eye" or name == "Nose":
            minX = min(pts[:,0])
            maxX = max(pts[:,0])
            minY = min(pts[:,1])
            maxY = max(pts[:,1]) 

            rect = []
            rect.append([minX, minY])
            rect.append([minX, maxY])
            rect.append([maxX, minY])
            rect.append([maxX, maxY])
            rect = np.array(rect)

            hull = cv2.convexHull(rect)
            # print(hull)
            # output = cv2.resize(overlay, dsize)
            # print(overlay[minX:maxX,minY:maxX,:])
            tmp = overlay[minY:maxY, minX:maxX, :]
            print(tmp.shape)
            s = 2

            Affine_Mat_w = [s, 0, tmp.shape[0]/2.0 - s*tmp.shape[0]/2.0]
            Affine_Mat_h = [0, s, tmp.shape[1]/2.0 - s*tmp.shape[1]/2.0]


            M = np.c_[ Affine_Mat_w, Affine_Mat_h].T 

            tmp = cv2.warpAffine(tmp, M, (tmp.shape[1], tmp.shape[0]))

            # width = int(tmp.shape[1] * s / 100)
            # height = int(tmp.shape[0] * s / 100)
            # dim = (width, height)

            # resized = cv2.resize(tmp, (width, height), interpolation = cv2.INTER_CUBIC)
            # tmp = cv2.resize(resized, (tmp.shape[1], tmp.shape[0]), interpolation = cv2.INTER_CUBIC)

            # print(tmp.shape)
   
            
            overlay[minY:maxY, minX:maxX, :] = tmp
            # cv2.drawContours(overlay, [hull], -1, colors[i], -1)
    # apply the transparent overlay
    # cv2.addWeighted(overlay, alpha, output, 1 - alpha, 0, output)

    # return the output image
    # print(facial_features_cordinates)
    return overlay

# initialize dlib's face detector (HOG-based) and then create
# the facial landmark predictor
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(args["shape_predictor"])

# load the input image, resize it, and convert it to grayscale
image = cv2.imread(args["image"])
image = imutils.resize(image, width=500)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# detect faces in the grayscale image
rects = detector(gray, 1)

# loop over the face detections
for (i, rect) in enumerate(rects):
    # determine the facial landmarks for the face region, then
    # convert the landmark (x, y)-coordinates to a NumPy array
    shape = predictor(gray, rect)
    shape = shape_to_numpy_array(shape)

    output = visualize_facial_landmarks(image, shape)
    print(output.shape)
    cv2.imshow("Image", output)
    cv2.waitKey(0)
