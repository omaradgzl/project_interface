import os
import cv2
import time

def funkMain(givenName):
    numOfPhotos=40
    vid=cv2.VideoCapture(0)
    givenName = givenName[:-1]
    os.mkdir("data/people/{}".format(givenName))
    
    def shootPhotos(count):
        for i in range(count):
            ret,frame=vid.read()
            cv2.imwrite("data/people/{}".format(givenName) + "/{photo}_".format(photo=givenName)+str(i)+".jpg",frame)  # save the image
            
            time.sleep(0.1)    
            
    
    while True:                              
        ret,frame=vid.read()
        frame=cv2.flip(frame,1)
        cv2.imshow("Cam",frame)
        time.sleep(5)
        shootPhotos(numOfPhotos)         
        break                            
    
    vid.release()
    cv2.destroyAllWindows()







