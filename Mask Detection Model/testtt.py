import cv2 

haad = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

def face_detect(img):
    coord = haad.detectMultiScale(img)
    return coord

cap = cv2.VideoCapture(0)


while True:
    ret, frame = cap.read()
    coords = face_detect(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY))

    for x,y,w,h in coords:
        cv2.rectangle(frame, (x,y), (x+w, y+h), (0,255,0), 3)


    cv2.imshow('frame', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


cap.release()

cv2.destroyAllWindows()