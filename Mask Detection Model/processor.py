import tensorflow 
from tensorflow import keras
from tensorflow.keras.models import load_model
import cv2

model = load_model('mask_detector.h5')


def predict(img):
  img = cv2.imread(img)
  img = cv2.resize(img, (224, 224))
  img = img.reshape(1, 224, 224, 3)
  y_pred = model.predict(img)
  return y_pred[0][0]


def draw_label(img, text, pos, bg_color):
  text_size = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 1, cv2.FILLED)
  end_x = pos[0] +  text_size[0][0] + 2
  end_y = pos[1] +  text_size[0][1] - 2    
  
  cv2.rectangle(img, pos, (end_x, end_y), bg_color, cv2.FILLED)
  cv2.putText(img, text, pos, cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 1, cv2.LINE_AA) 
