import cv2
import pytesseract
import numpy as np
import easyocr
import tensorflow as tf
import matplotlib.pyplot as plt

mnist_model = tf.keras.models.load_model('mnist_model.h5')

reader = easyocr.Reader(['en'])
image = cv2.imread('7d92e460-6bfa-40af-8615-2c64253c7fac.jpg')
image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
results = reader.readtext(image_rgb)
for i, (bbox, text, confidence) in enumerate(results):
    (x1, y1), (x2, y2), (x3, y3), (x4, y4) = bbox  
    x_min, y_min = min(x1, x2, x3, x4), min(y1, y2, y3, y4)
    x_max, y_max = max(x1, x2, x3, x4), max(y1, y2, y3, y4)
    x_min, y_min, x_max, y_max = map(int, [x_min, y_min, x_max, y_max])
    cropped_image = image[y_min:y_max, x_min:x_max]
    # print(type(cropped_image))

    gray = cv2.cvtColor(cropped_image, cv2.COLOR_RGB2GRAY)
    # print(type(gray))
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    dilated = cv2.dilate(thresh, kernel, iterations=1)
    contours, _ = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=lambda ctr: cv2.boundingRect(ctr)[0])

    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        # cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
        digit = gray[y:y + h, x:x + w]

        # _, binary = cv2.threshold(digit, 150, 255, cv2.THRESH_BINARY_INV)

        # Resize to 28x28 like MNIST (optional)
        # mnist_like = cv2.resize(binary, (28, 28), interpolation=cv2.INTER_AREA)

        digit = cv2.resize(digit, (28, 28))
        digit = cv2.bitwise_not(digit) 
        processed = digit.astype('float32').reshape(1, 28, 28, 1) / 255.0
        # prediction = mnist_model.predict(processed, verbose=0)
        prediction = mnist_model.predict(processed, verbose=0)
        # print(prediction.shape)
        predicted_num= np.argmax(prediction)
        # print(predicted_num.shape)
        print(predicted_num)

        probability = prediction[0][predicted_num]
        result = None


        if probability > 0.5:

            result = predicted_num
            plt.figure(figsize=(5, 5))
            plt.imshow(digit)
            plt.title(f"Cropped {i+1} - {result}")
            plt.axis("off")
            plt.show()
        else:
            result = None
        
        
    

        

        

        
        
