# -*- coding: utf-8 -*-
"""CT_Kidney24.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1tD2QuxILL6IBT3GCuC8rkp0FKOeAz0Hy
"""

!kaggle datasets download nazmul0087/ct-kidney-dataset-normal-cyst-tumor-and-stone

!mkdir -p ./CTKidney

!unzip -qq ct-kidney-dataset-normal-cyst-tumor-and-stone.zip -d ./CTKidney

# Commented out IPython magic to ensure Python compatibility.
# %%capture
# 
# # This Python 3 environment comes with many helpful analytics libraries installed
# # It is defined by the kaggle/python Docker image: https://github.com/kaggle/docker-python
# # For example, here's several helpful packages to load
# 
# import numpy as np # linear algebra
# import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
# 
# # Input data files are available in the read-only "../input/" directory
# # For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory
# 
# import os
# for dirname, _, filenames in os.walk('/kaggle/input'):
#     for filename in filenames:
#         print(os.path.join(dirname, filename))
# 
# # You can write up to 20GB to the current directory (/kaggle/working/) that gets preserved as output when you create a version using "Save & Run All"
# # You can also write temporary files to /kaggle/temp/, but they won't be saved outside of the current session

import keras
from keras.models import Sequential
from keras.layers import Conv2D, Flatten, Dense, MaxPooling2D, Dropout
from sklearn.metrics import accuracy_score

import ipywidgets as widgets
import io
from PIL import Image
import tqdm
from sklearn.model_selection import train_test_split
import cv2
from sklearn.utils import shuffle
import tensorflow as tf

X = []
Y = []
image_size = 128
labels = ['Cyst','Normal','Stone','Tumor']

for i in labels:
    folderPath = os.path.join('/content/CTKidney/CT-KIDNEY-DATASET-Normal-Cyst-Tumor-Stone/CT-KIDNEY-DATASET-Normal-Cyst-Tumor-Stone',i)
    for j in os.listdir(folderPath):
        img = cv2.imread(os.path.join(folderPath,j))
        img = cv2.resize(img,(image_size,image_size))
        X.append(img)
        Y.append(i)

X = np.array(X)
Y = np.array(Y)

from sklearn.preprocessing import LabelEncoder
le = LabelEncoder()
Y = le.fit_transform(Y)

import matplotlib.pyplot as plt

# Assuming X_train is a NumPy array of images
# and the images are in the format (num_samples, height, width, channels)

# Set the number of images to display
num_images = 5

# Create a figure to display the images
plt.figure(figsize=(15, 5))

# Loop through the images and plot them
for i in range(num_images):
    plt.subplot(1, num_images, i + 1)
    plt.imshow(X[i])  # Adjust indexing if needed (e.g., grayscale images)
    plt.axis('off')  # Hide the axis
    plt.title(f'Image {i + 1}')  # Optional title for each image

plt.tight_layout()
plt.show()

X_train,X_test,y_train,y_test = train_test_split(X,Y,test_size=0.2,random_state=100)

X_train,X_val,y_train,y_val = train_test_split(X_train,y_train,test_size=0.2,random_state=100)

model = Sequential()
model.add(Conv2D(32,(3,3),activation ='relu',input_shape=(128,128,3)))
model.add(Conv2D(64,(3,3),activation='relu'))
model.add(MaxPooling2D(2,2))
model.add(Dropout(0.3))
model.add(Conv2D(64,(3,3),activation='relu'))
model.add(Conv2D(64,(3,3),activation='relu'))
model.add(Dropout(0.3))
model.add(MaxPooling2D(2,2))
model.add(Dropout(0.3))
model.add(Conv2D(128,(3,3),activation='relu'))
model.add(Conv2D(128,(3,3),activation='relu'))
model.add(Conv2D(128,(3,3),activation='relu'))
model.add(Dropout(0.3))
model.add(Conv2D(128,(3,3),activation='relu'))
model.add(Conv2D(256,(3,3),activation='relu'))
model.add(MaxPooling2D(2,2))
model.add(Dropout(0.3))
model.add(Flatten())
model.add(Dense(512,activation='relu'))
model.add(Dense(512,activation='relu'))
model.add(Dropout(0.3))
model.add(Dense(4,activation='softmax'))

model.summary()

model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
              loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=False),
              metrics=["accuracy"])

# Compile the model
model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

# Fit the model
history = model.fit(
    x=X_train,
    y=y_train,
    batch_size=32,
    validation_data=(X_val, y_val),
    epochs=50
)

scores = model.evaluate(X_test, y_test)

import matplotlib.pyplot as plt
import seaborn as sns

#Model_save
#Accuracy
acc = history.history['accuracy']
val_acc = history.history['val_accuracy']
epochs = range(len(acc))
fig = plt.figure(figsize=(14,7))
plt.plot(epochs, acc, 'r', label="Training Accuracy")
plt.plot(epochs, val_acc, 'b', label="Validation Accuracy")
plt.legend(loc='upper left')
plt.show()

#Loss
loss = history.history['loss']
val_loss = history.history['val_loss']
epochs = range(len(loss))
fig = plt.figure(figsize=(14,7))
plt.plot(epochs, loss, 'r', label="Training loss")
plt.plot(epochs, val_loss, 'b', label="Validation loss")
plt.legend(loc='upper left')
plt.show()

