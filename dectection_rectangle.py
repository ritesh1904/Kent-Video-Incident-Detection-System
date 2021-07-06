import numpy as np
import cv2

confidenceThreshold = 0.5
NMSThreshold = 0.3

modelConfiguration = '/Users/riteshrana36gmail.com/Documents/Kent Internship May - June 2021/internship-1/YOLO-v3-Object-Detection-master/cfg/yolov3.cfg'
modelWeights = 'yolov3.weights'

labelsPath = 'coco.names'
labels = open(labelsPath).read().strip().split('\n')

np.random.seed(10)
COLORS = np.random.randint(0, 255, size=(len(labels), 3), dtype="uint8")

net = cv2.dnn.readNetFromDarknet(modelConfiguration, modelWeights)

image = cv2.imread('/Users/riteshrana36gmail.com/Documents/Kent Internship May - June 2021/internship-1/YOLO-v3-Object-Detection-master/images/person.jpg')

start_point = (50, 50)
end_point = (400, 500)
color = (0, 0, 0)
thickness = 1

mid_point = ((50+400)/2,(50+500)/2)
start_point_line = (50, 275)
end_point_line = (400, 275)

image = cv2.line(image, start_point_line, end_point_line, color, thickness)
crop_image = image[50:500,50:400]
(H, W) = crop_image.shape[:2]

#Determine output layer names
layerName = net.getLayerNames()
layerName = [layerName[i[0] - 1] for i in net.getUnconnectedOutLayers()]

blob = cv2.dnn.blobFromImage(crop_image, 1 / 255.0, (416, 416), swapRB = True, crop = False)
net.setInput(blob)
layersOutputs = net.forward(layerName)

boxes = []
confidences = []
classIDs = []

for output in layersOutputs:
    for detection in output:
        scores = detection[5:]
        classID = np.argmax(scores)
        confidence = scores[classID]
        if confidence > confidenceThreshold:
            box = detection[0:4] * np.array([W, H, W, H])
            (centerX, centerY,  width, height) = box.astype('int')
            x = int(centerX - (width/2))
            y = int(centerY - (height/2))

            boxes.append([x, y, int(width), int(height)])
            confidences.append(float(confidence))
            classIDs.append(classID)

#Apply Non Maxima Suppression
detectionNMS = cv2.dnn.NMSBoxes(boxes, confidences, confidenceThreshold, NMSThreshold)

if(len(detectionNMS) > 0):
    for i in detectionNMS.flatten():
        (x, y) = (boxes[i][0], boxes[i][1])
        (w, h) = (boxes[i][2], boxes[i][3])

        color = [int(c) for c in COLORS[classIDs[i]]]
        cv2.rectangle(crop_image, (x, y), (x + w, y + h), color, 2)
        text = '{}: {:.4f}'.format(labels[classIDs[i]], confidences[i])
        cv2.putText(crop_image, text, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

cv2.imshow('Image', image)
cv2.waitKey(0)
