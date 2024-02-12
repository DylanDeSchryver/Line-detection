import cv2
import numpy as np

# Read image from camera
cap = cv2.VideoCapture(1)

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Define the coordinates of the region of interest (ROI)
    r_x, r_y, r_width, r_height = 0, 0, 400, 300

    # Draw a rectangle around the ROI
    cv2.rectangle(frame, (r_x, r_y), (r_x + r_width, r_y + r_height), (255, 0, 0), 2)

    # Crop the frame to the defined ROI
    roi_frame = frame[r_y:r_y + r_height, r_x:r_x + r_width]

    # Convert the cropped image to grayscale
    gray = cv2.cvtColor(roi_frame, cv2.COLOR_BGR2GRAY)

    # Apply Gaussian blur to reduce noise
    blurred = cv2.blur(gray, (1, 1))

    # Use Canny edge detection to detect edges
    edges = cv2.Canny(blurred, 50, 150, apertureSize=3)

    # Maintain a list of already displayed lines
    displayed_lines = []

    # Apply HoughLinesP method to directly obtain line end points
    lines_list = []
    lines = cv2.HoughLinesP(
        edges,              # Input edge image
        1,                  # Distance resolution in pixels
        np.pi / 180,        # Angle resolution in radians
        threshold=75,       # Min number of votes for a valid line
        minLineLength=200,  # Min allowed length of a line
        maxLineGap=500      # Max allowed gap between line segments for joining them
    )

    # Iterate over detected lines
    if lines is not None:
        for line in lines:
            # Extract line endpoints
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

                # If the line is not too close to already displayed lines, draw it
                if not too_close:
                    if x1 == x2:  # Vertical line
                        new_x1, new_y1 = x1, r_y
                        new_x2, new_y2 = x2, r_y + r_height
                    else:  # Non-vertical line
                        m = (y2 - y1) / (x2 - x1)
                        new_x1 = int((r_y - y1 + m * x1) / m) if m != 0 else x1
                        new_y1 = r_y
                        new_x2 = int((r_y + r_height - y1 + m * x1) / m) if m != 0 else x1
                        new_y2 = r_y + r_height

                    # Draw the extended line on the original frame
                    cv2.line(roi_frame, (new_x1, new_y1), (new_x2, new_y2), (0, 255, 0), 8)

                    # Store the line endpoints and add them to the displayed lines list
                    lines_list.append(((x1, y1), (x2, y2)))
                    displayed_lines.append(((x1, y1), (x2, y2)))

    # Calculate the average midpoint of detected lines
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
            cv2.line(roi_frame, (0, left_edge_y), (r_width, right_edge_y), (255, 255, 0), 5)

    # Display the result images
    cv2.imshow('detectedLines', frame)
    cv2.imshow('edge', edges)

    # Wait for 1 millisecond and check for key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture object and close all windows
cap.release()
cv2.destroyAllWindows()
