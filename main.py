import cv2
import numpy as np

# Read image
cap = cv2.VideoCapture(1)
while True:
    ret, frame = cap.read()
    # Define the coordinates of the rectangle
    r_x, r_y, r_width, r_height = 0, 0, 400, 300

    # Draw a rectangle around the ROI
    cv2.rectangle(frame, (r_x, r_y), (r_x + r_width, r_y + r_height), (255, 0, 0), 2)

    # Crop the frame to the defined ROI
    roi_frame = frame[r_y:r_y + r_height, r_x:r_x + r_width]

    # Convert image to grayscale
    gray = cv2.cvtColor(roi_frame, cv2.COLOR_BGR2GRAY)

    # Use canny edge detection
    edges = cv2.Canny(gray, 50, 150, apertureSize=3)

    # Maintain a list of already displayed lines
    displayed_lines = []

    # Apply HoughLinesP method to
    # to directly obtain line end points
    lines_list = []
    lines = cv2.HoughLinesP(
        edges,  # Input edge image
        1,  # Distance resolution in pixels
        np.pi / 180,  # Angle resolution in radians
        threshold=50,  # Min number of votes for valid line
        minLineLength=5,  # Min allowed length of line
        maxLineGap=1000  # Max allowed gap between line for joining them
    )

    # Iterate over points
    if lines is not None:
        for line in lines:
            # Extracted points nested in the list
            x1, y1, x2, y2 = line[0]

            # Check if line endpoints are within a certain distance from the edges of the ROI
            edge_margin = 10
            if (edge_margin < x1 < r_width - edge_margin and
                    edge_margin < x2 < r_width - edge_margin and
                    edge_margin < y1 < r_height - edge_margin and
                    edge_margin < y2 < r_height - edge_margin):

                # Check if the line is too close to already displayed lines
                too_close = False
                for disp_line in displayed_lines:
                    dist1 = np.linalg.norm(np.array([x1, y1]) - np.array(disp_line[0]))
                    dist2 = np.linalg.norm(np.array([x2, y2]) - np.array(disp_line[1]))
                    if dist1 < 10 or dist2 < 10:
                        too_close = True
                        break

                # If the line is not too close, draw it and add it to the displayed lines list
                if not too_close:
                    cv2.line(roi_frame, (x1, y1), (x2, y2), (0, 255, 0), 5)
                    lines_list.append(((x1, y1), (x2, y2)))
                    displayed_lines.append(((x1, y1), (x2, y2)))

    # Calculate average midpoint of detected lines
    if len(lines_list) > 0:
        avg_midpoint = np.mean([[(x1 + x2) / 2, (y1 + y2) / 2] for line in lines_list for (x1, y1), (x2, y2) in [line]], axis=0)
        avg_midpoint = avg_midpoint.astype(int)

        # Draw a line parallel to the detected lines passing through the average midpoint
        for line in lines_list:
            (x1, y1), (x2, y2) = line
            # Calculate the direction vector of the detected line
            direction_vector = np.array([x2 - x1, y2 - y1])
            # Calculate the endpoint of the midline based on the direction vector and the average midpoint
            midline_endpoint = avg_midpoint + direction_vector
            # Draw the midline
            cv2.line(roi_frame, tuple(avg_midpoint), tuple(midline_endpoint), (255, 255, 0), 2)

        # Extend the midline to the edges of the ROI
        if direction_vector[0] != 0:
            # Calculate the slope of the midline
            avg_slope = direction_vector[1] / direction_vector[0]
            # Calculate the y-intercept using the average midpoint
            b = avg_midpoint[1] - avg_slope * avg_midpoint[0]
            # Calculate the intersection points with the left and right edges of the ROI
            left_edge_y = int(avg_slope * 0 + b)
            right_edge_y = int(avg_slope * r_width + b)
            # Draw the extended midline
            cv2.line(roi_frame, (0, left_edge_y), (r_width, right_edge_y), (255, 255, 0), 2)

    # Save the result image
    cv2.imshow('detectedLines', frame)
    cv2.imshow('edge', edges)
    cv2.waitKey(1)
