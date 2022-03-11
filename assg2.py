
import requests
import cv2
import numpy as np
import imutils
import collections
def empty(a):
    pass
# Replace the below URL with your own. Make sure to add "/shot.jpg" at last.
url = "http://10.42.0.168:8080/shot.jpg"
# cv2.namedWindow("Trackbars")
# cv2.resizeWindow("Trackbars",640,240)
# cv2.createTrackbar("Hue min","Trackbars",0,179,empty)
# cv2.createTrackbar("Hue max","Trackbars",0,179,empty)
# cv2.createTrackbar("sat min","Trackbars",0,255,empty)
# cv2.createTrackbar("sat max","Trackbars",0,255,empty)
# cv2.createTrackbar("val min","Trackbars",0,255,empty)
# cv2.createTrackbar("val max","Trackbars",0,255,empty)

# While loop to continuously fetching data from the Url
lower = [30,57,43]
upper = [80,170,222]
points = [collections.deque(maxlen=1024)]
index = 0
cap = cv2.VideoCapture(0)
cap.set(3,600)
cap.set(4,400)
cap.set(10,100)
while True:
    
    # img_resp = requests.get(url)
    # img_arr = np.array(bytearray(img_resp.content), dtype=np.uint8)
    # img = cv2.imdecode(img_arr, -1)
    # img = imutils.resize(img, width=1000, height=1800)
    success,img = cap.read()
    img = cv2.flip(img, 1)
    # image = cv2.rotate(img, cv2.cv2.ROTATE_90_CLOCKWISE)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    # rand_array = ["Hue min","sat min","val min"]
    # rand_array2 = ["Hue max","sat max","val max"]
    # for i,j in zip(rand_array,rand_array2):
    #     lower.append(cv2.getTrackbarPos(i,"Trackbars"))
    #     upper.append(cv2.getTrackbarPos(j,"Trackbars"))
    # print(lower,upper)
    mask = cv2.inRange(hsv,np.array(lower),np.array(upper))
    contrs,hierc = cv2.findContours(mask.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    center = None
    if len(contrs)!=0:
        for contour in contrs:
            if cv2.contourArea(contour)>300:
                ((x, y), radius) = cv2.minEnclosingCircle(contour)
                cv2.circle(img, (int(x), int(y)), int(radius), (0, 255, 255), 2)
                M = cv2.moments(contour)
                center = (int(M['m10'] / M['m00']), int(M['m01'] / M['m00']))
                # cv2.circle(img,(int(x), int(y)),1,(0,0,255),20)
                points[index].appendleft(center)
    else:
           points.append(collections.deque(maxlen=512)) 
           index+=1        
    for i in range(len(points)):
        for j in range(1,len(points[i])):
            if points[i][j-1] is None or points[i][j] is None:
                    continue  
            cv2.line(img, points[i][j-1], points[i][j], (0,0,255), 2)          
    cv2.imshow("mask",mask)
    cv2.imshow("Android_cam", img)
  
    # Press Esc key to exit
    if cv2.waitKey(1) == 27:
        break
        
cv2.destroyAllWindows()