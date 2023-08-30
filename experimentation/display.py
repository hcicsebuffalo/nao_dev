import yolov5
from pathlib import Path
import torch
from PIL import Image
import cv2


# # or load custom model
# model = yolov5.load('YOLOV5/best.pt')


# # set model parameters
# model.conf = 0.40  # NMS confidence threshold
# model.iou = 0.45  # NMS IoU threshold
# model.agnostic = False  # NMS class-agnostic 
# model.max_det = 1000  # maximum number of detections per image


# cap = cv2.VideoCapture(0)

# while True:
#     # Capture frame-by-frame
#     ret, frame = cap.read()
#     print(frame)
#     # results = model(frame)
# # # Get detected objects
# # detected_objects = results.pred[0]
# # boxes = detected_objects[:, :4] # x1, y1, x2, y2
# # scores = detected_objects[:, 4]
# # categories = detected_objects[:, 5]
# # boxes = boxes.squeeze(0)
#     # img_with_boxes = results.render()[0]
#     # Display the frame
#     cv2.imshow('Live Video Feed', frame)

#     # Exit the loop when 'q' is pressed
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# # Release the camera and close the window
# cap.release()
# cv2.destroyAllWindows()


import cv2

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()

    cv2.imshow('Camera Feed in WSL 2', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
