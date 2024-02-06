import cv2
import numpy as np

# Read image
cap = cv2.VideoCapture(0)
slopes = {}
while True:
    ret, frame = cap.read()
    # Convert image to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Use canny edge detection
    edges = cv2.Canny(gray, 50, 150, apertureSize=3)

    # Apply HoughLinesP method to
    # to directly obtain line end points
    lines_list = []


    lines = cv2.HoughLinesP(
        edges,  # Input edge image
        1,  # Distance resolution in pixels
        np.pi / 180,  # Angle resolution in radians
        threshold=100,  # Min number of votes for valid line
        minLineLength=5,  # Min allowed length of line
        maxLineGap=10  # Max allowed gap between line for joining them

    )

    if lines is not None:

        # Iterate over points
        for points in lines:
            # Extracted points nested in the list
            x1, y1, x2, y2 = points[0]

            slope = (y2 - y1)/(x2 - x1)
            slopes[points] = slope

            print(slopes)

            # Draw the lines to connect points
            cv2.line(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            # Maintain a simples lookup list for points
            lines_list.append([(x1, y1), (x2, y2)])

        # Save the result image
        cv2.imshow('detectedLines', frame)
        cv2.waitKey(1)
