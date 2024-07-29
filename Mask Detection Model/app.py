import cv2
import numpy as np
from tensorflow.keras.models import load_model

# Load the model
model = load_model('asif_face_mask_model.h5')
print('Model Loaded Successfully')





def predict(img):
    img = cv2.resize(img, (224, 224))
    
    img = img.reshape(1, 224, 224, 3)
    
    y_pred = model.predict(img)
    
    return y_pred[0][0]


# ---- Face Detection Module Start Here ----


haad = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

def face_detect(img):
    coord = haad.detectMultiScale(img)
    return coord

# ---- Face Detection Module End Here ----


cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()

    # This Section of the code calls the face detection module
    coords = face_detect(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY))

    for x,y,w,h in coords:
        cv2.rectangle(frame, (x,y), (x+w, y+h), (0,255,0), 3)

    # ----- Ends here ------

    # This Section of the code calls the mask detection module

    y_pred = predict(frame)    
    label = 'Mask Detected' if y_pred > 0.5 else 'No Mask Detected'
    color = (0, 255, 0) if y_pred > 0.5 else (0, 0, 255)
    cv2.putText(frame, label, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2, cv2.LINE_AA)
    
    cv2.imshow('Labeled Window', frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
