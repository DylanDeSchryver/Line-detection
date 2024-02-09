import cv2
import numpy as np

# Read image
cap = cv2.VideoCapture(0)
#img = cv2.imread('Parallellines.png')
slopes = {}
while True:
    ret, frame = cap.read()

    # Define the coordinates of the rectangle
    r_x, r_y, r_width, r_height = 300, 300, 640, 480

    # Draw a rectangle around the ROI
    cv2.rectangle(frame, (r_x, r_y), (r_x + r_width, r_y + r_height), (255, 0, 0), 2)

    # Crop the frame to the defined ROI
    roi_frame = frame[r_y:r_y + r_height, r_x:r_x + r_width]

    # Convert image to grayscale
    # Convert image to grayscale
    gray = cv2.cvtColor(roi_frame, cv2.COLOR_BGR2GRAY)

    # Use canny edge detection
    edges = cv2.Canny(gray, 200, 500, apertureSize=3)

    # Apply HoughLinesP method to
    # to directly obtain line end points
    lines_list = []
    lines = cv2.HoughLinesP(
        edges,  # Input edge image
        1,  # Distance resolution in pixels
        np.pi / 180,  # Angle resolution in radians
        threshold=10,  # Min number of votes for valid line
        minLineLength = 580,  # Min allowed length of line
        maxLineGap= 100000000# Max allowed gap between line for joining them
    )

    # Iterate over points
    if lines is not None:

        for points in lines:
            # Extracted points nested in the list
            x1, y1, x2, y2 = points[0]
            # Draw the lines joing the points
            # On the original image
            print('hi1')

            for x in lines_list:
                #see if lines are too close
                print('hi')

                if x[0][0] - 10 <= x1 <= x[0][0] + 10:
                    print('x', x[0][0], x1)
                    x1 = 0
                    y1 = 0
                    x2 = 0
                    y2 = 0
                elif x[0][1] - 10 <= y1 <= x[0][1] + 10:
                    print('y', x[0][1], y2)
                    x1 = 0
                    y1 = 0
                    x2 =0
                    y2=0


            print('points are not close')
            cv2.line(roi_frame, (x1, y1), (x2, y2), (0, 255, 0), 5)
            # Maintain a simple lookup list for points
            lines_list.append([(x1, y1), (x2, y2)])




    # Save the result image
    cv2.imshow('detectedLines', frame)
    #cv2.imshow('dfggdf', edges)
    cv2.waitKey(15)
