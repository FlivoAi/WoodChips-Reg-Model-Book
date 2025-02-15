# -*- coding: utf-8 -*-
"""woodchiprecognition.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1T8EWzmtes_CIX-xu8G8QdQZ1XHfaaYTd
"""

import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense,Dropout
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import numpy as np
import matplotlib.pyplot as plt
import os
from google.colab import drive
drive.mount('/content/drive')

data_dir = '/content/drive/MyDrive/wooddataset'
train_dir = os.path.join(data_dir, 'train')
test_dir = os.path.join(data_dir, 'test')

class1_dir = os.path.join(train_dir, 'cipher')
class2_dir = os.path.join(train_dir, 'pino patula')

# Set up the ImageDataGenerator for data augmentation
train_datagen = ImageDataGenerator(rescale=1./255, # Normalize pixel values
                                  rotation_range=20, # Rotate images
                                  zoom_range=0.2, # Zoom in on images
                                  horizontal_flip=True) # Flip images horizontally

test_datagen = ImageDataGenerator(rescale=1./255) # Only normalize test data

# Load the training and test data
train_generator = train_datagen.flow_from_directory(
    train_dir,
    target_size=(224, 224), # Resize images to 224x224
    batch_size=32,
    class_mode='binary')

test_generator = test_datagen.flow_from_directory(
    test_dir,
    target_size=(224, 224),
    batch_size=32,
    class_mode='binary')

# Define the CNN model
model = Sequential()
model.add(Conv2D(32, (3, 3), activation='relu', input_shape=(224, 224, 3)))
model.add(MaxPooling2D((2, 2)))
model.add(Conv2D(64, (3, 3), activation='relu'))
model.add(MaxPooling2D((2, 2)))
model.add(Conv2D(128, (3, 3), activation='relu'))
model.add(MaxPooling2D((2, 2)))
model.add(Flatten())
model.add(Dense(128, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(1, activation='sigmoid'))

# Compile the model
model.compile(optimizer='adam',
              loss='binary_crossentropy',
              metrics=['accuracy'])

# Train the model
epochs = 20
model.fit(train_generator,
          epochs=epochs,
          validation_data=test_generator)

# Evaluate the model on the test data
test_loss, test_acc = model.evaluate(test_generator)
print('Test accuracy:', test_acc)

data_dir2 = '/content/drive/My Drive/color code'


img_height, img_width = 128, 128

images = []
labels = []

from tensorflow.keras.preprocessing.image import ImageDataGenerator, load_img, img_to_array

for filename in os.listdir(data_dir2):
    if filename.endswith('.png'):
        img_path = os.path.join(data_dir2, filename)
        image = load_img(img_path, target_size=(img_height, img_width))
        image = img_to_array(image)
        images.append(image)
        labels.append(filename.split('.')[0])  # Extract color code from filename

images = np.array(images) / 255.0

import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from tensorflow.keras.preprocessing.image import ImageDataGenerator, load_img, img_to_array

from sklearn.model_selection import RandomizedSearchCV
from sklearn.preprocessing import LabelEncoder
label_encoder = LabelEncoder()
labels_encoded = label_encoder.fit_transform(labels)
labels_categorical = tf.keras.utils.to_categorical(labels_encoded, num_classes=31)  # Assuming 10 color codes

# Data augmentation
datagen = ImageDataGenerator(
    rotation_range=40,
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True,
    fill_mode='nearest'
)

colormodel = Sequential([
    Conv2D(32, (3, 3), activation='relu', input_shape=(img_height, img_width, 3)),
    MaxPooling2D(pool_size=(2, 2)),
    Conv2D(64, (3, 3), activation='relu'),
    MaxPooling2D(pool_size=(2, 2)),
    Conv2D(128, (3, 3), activation='relu'),
    MaxPooling2D(pool_size=(2, 2)),
    Flatten(),
    Dense(512, activation='relu'),
    Dropout(0.5),
    Dense(31, activation='softmax')  # Assuming you have 10 color codes
])

colormodel.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# Train the model
epochs = 50
colormodel.fit(
    datagen.flow(images, labels_categorical, batch_size=32),
    epochs=epochs
)

import numpy as np
new_image_path="/content/drive/MyDrive/WhatsApp Image 2024-07-02 at 15.29.08_0b2e04cf.jpg"
# Preprocess the new image for the wood model
new_image_wood = load_img(new_image_path, target_size=(224, 224))
new_image_wood = img_to_array(new_image_wood)
new_image_wood = new_image_wood / 255.0
new_image_wood = new_image_wood.reshape(1, 224, 224, 3)

# Preprocess the new image for the color model
new_image_color = load_img(new_image_path, target_size=(img_height, img_width))
new_image_color = img_to_array(new_image_color)
new_image_color = new_image_color / 255.0
new_image_color = np.expand_dims(new_image_color, axis=0)

# Predict the wood type for the new image
wood_prediction = model.predict(new_image_wood)
wood_class = np.argmax(wood_prediction)
wood_class_name = "cipher" if wood_class == 0 else "pino patula"
print(f"Predicted wood type: {wood_class_name}")

# Predict the color code for the new image
color_prediction = colormodel.predict(new_image_color)
color_class = np.argmax(color_prediction)
print(f"Predicted color code: {color_class}")

# a dictionary to map wood types and color codes to values
wood_color_values = {
    ("cipher", 1): 100,
    ("cipher", 2): 200,
    ("cipher", 3): 300,
    ("cipher", 4): 400,
    ("cipher", 5): 500,
    ("cipher", 6): 600,
    ("cipher", 7): 700,
    ("cipher", 8): 800,
    ("cipher", 9): 900,
    ("cipher", 10): 1000,
    ("cipher", 11): 1100,
    ("cipher", 12): 1200,
    ("cipher", 13): 1300,
    ("cipher", 14): 1400,
    ("cipher", 15): 1500,
    ("cipher", 16): 1600,
    ("cipher", 17): 1700,
    ("cipher", 18): 1800,
    ("cipher", 19): 1900,
    ("cipher", 20): 2000,
    ("cipher", 21): 2100,
    ("cipher", 22): 2200,
    ("cipher", 23): 2300,
    ("cipher", 24): 2400,
    ("cipher", 25): 2500,
    ("cipher", 26): 2600,
    ("cipher", 27): 2700,
    ("cipher", 28): 2800,
    ("cipher", 29): 2900,
    ("cipher", 30): 3000,
    ("cipher", 31): 3100,
    ("pino patula", 1): 100,
    ("pino patula", 2): 200,
    ("pino patula", 3): 300,
    ("pino patula", 4): 400,
    ("pino patula", 5): 500,
    ("pino patula", 6): 600,
    ("pino patula", 7): 700,
    ("pino patula", 8): 800,
    ("pino patula", 9): 900,
    ("pino patula", 10): 1000,
    ("pino patula", 11): 1100,
    ("pino patula", 12): 1200,
    ("pino patula", 13): 1300,
    ("pino patula", 14): 1400,
    ("pino patula", 15): 1500,
    ("pino patula", 16): 1600,
    ("pino patula", 17): 1700,
    ("pino patula", 18): 1800,
    ("pino patula", 19): 1900,
    ("pino patula", 20): 2000,
    ("pino patula", 21): 2100,
    ("pino patula", 22): 2200,
    ("pino patula", 23): 2300,
    ("pino patula", 24): 2400,
    ("pino patula", 25): 2500,
    ("pino patula", 26): 2600,
    ("pino patula", 27): 2700,
    ("pino patula", 28): 2800,
    ("pino patula", 29): 2900,
    ("pino patula", 30): 3000,
    ("pino patula", 31): 900
}

# Get the predicted wood type and color code
predicted_wood_type = "cipher" if wood_class == 0 else "pino patula"
predicted_color_code = color_class + 1

# Check if the combination exists in the dictionary
if (predicted_wood_type, predicted_color_code) in wood_color_values:
    # Return the corresponding value
    value = wood_color_values[(predicted_wood_type, predicted_color_code)]
    print(f"amount of chemical to be added: {value}")
else:
    # Handle the case where the combination is not found
    print("new combination found")

import pickle

with open('plantmodel.pkl', 'wb') as file:
    pickle.dump(model, file)
with open('colormodel.pkl', 'wb') as file:
    pickle.dump(colormodel, file)

