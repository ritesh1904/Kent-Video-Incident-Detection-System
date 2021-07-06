import cv2
image = cv2.imread('/Users/riteshrana36gmail.com/Documents/Internship/internship-1/YOLO-v3-Object-Detection-master/images/toll.jpeg')


start_point = (900, 50)
end_point = (500, 500)
color = (0, 0, 0)
thickness = 1
image_rectangle = cv2.rectangle(image, start_point, end_point, color, thickness)

crop = image[50:500,500:900]
cv2.imshow('Image', crop)
cv2.waitKey(0) 