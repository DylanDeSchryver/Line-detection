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
    gray = cv2.cvtColor(roi_frame, cv2.COLOR_BGR2GRAY)

    #blur = cv2.GaussianBlur(gray, (1,1), 0)

    # Use canny edge detection
    edges = cv2.Canny(gray, 200, 600, apertureSize=3)

    # Apply HoughLinesP method to
    # to directly obtain line end points
    lines_list = []


    lines = cv2.HoughLinesP(
        edges,  # Input edge image
        1,  # Distance resolution in pixels
        np.pi / 180,  # Angle resolution in radians
        threshold=100,  # Min number of votes for valid line
        minLineLength=250,  # Min allowed length of line9
        maxLineGap=100  # Max allowed gap between line for joining them

    )

    if lines is not None:

        # Iterate over points
        for points in lines:
            # Extracted points nested in the list
            x1, y1, x2, y2 = points[0]

            slope = (y2 - y1)/(x2 - x1)
            slopes[slope] = x1, y1, x2, y2

            print(slopes[slope])

            for x in slopes:
                if x == slope:
                    matching = slopes[x]
                    print('found match')
                    # # Draw the lines to connect points
                    cv2.line(roi_frame, (x1, y1), (x2, y2), (0, 255, 0), 9) #original line green
                    print('green')
                    cv2.line(roi_frame, (matching[0], matching[1]), (matching[2], matching[3]), (255, 0, 0), 9) #new line blue
                    print("blue")
                    midpointx1 = int((x1 + matching[0])/2)
                    midpointy1 = int((y1 + matching[1])/2)
                    midpointx2 = int((x2 + matching[2])/2)
                    midpointy2 = int((y2 + matching[3])/2)




                    print('hello')

                    cv2.line(roi_frame, (midpointx1, midpointy1), (midpointx2, midpointy2), (255, 0, 255), 4)  # mid line pink
                    print('pink')


                    # # Maintain a simples lookup list for points
                    lines_list.append([(x1, y1), (x2, y2)])
                    lines_list.append([(matching[0], matching[1]), (matching[2], matching[3])])
                    if len(lines_list) >= 8:
                        print(len(lines_list))
                        break
                        
                    
               

                # if len(lines_list) >= 5:
                #     break

            else:
                print("slopes do not match")

            # # Draw the lines to connect points
            # cv2.line(cap, (x1, y1), (x2, y2), (0, 255, 0), 1)
            # # Maintain a simples lookup list for points
            # lines_list.append([(x1, y1), (x2, y2)])

        # Save the result image
        cv2.imshow('detectedLines', roi_frame)
        #cv2.imshow('dfggdf', edges)
        cv2.waitKey(15)
