# -*- coding: utf-8 -*-
"""heart condition predictor.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1YbdQOoDZa8XY_XwUjOQiwJ-hzQBxPlFz
"""

import numpy as np
import pandas as pd
from google.colab import files
import io
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn import metrics
import tensorflow as tf
from keras.models import Sequential
from keras.layers import Dense
import coremltools

uploaded = files.upload()

df=pd.read_csv(io.StringIO(uploaded['framingham.csv'].decode('utf-8')),low_memory=False)

df.dropna(inplace=True)

X = df.drop("TenYearCHD", axis = 1)
y = df["TenYearCHD"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=101)

scaler = StandardScaler().fit(X_train)
X_train = scaler.transform(X_train)
X_test = scaler.transform(X_test)

import keras
model = keras.models.Sequential([
    keras.layers.Dense(12, activation='relu', input_shape=(14,)),
    keras.layers.Dense(10, activation='relu'),
    keras.layers.Dense(8, activation='relu'),
    keras.layers.Dense(4, activation='relu'),
    keras.layers.Dense(1, activation='sigmoid'),
  ])

model.compile(loss='binary_crossentropy',
              optimizer='adam',
              metrics=['acc'])

model.fit(X_train, y_train,epochs=50, batch_size=8, verbose=1)

model.save("heart_vit_hack.h5")

class_labels = ["TenYearCHD"]
final_covid_model = coremltools.converters.tensorflow.convert("heart_vit_hack.h5", class_labels = class_labels, output_names = ["TenYearCHD"])
final_covid_model.short_description = "Outputs Chances of Heart Risk"
final_covid_model.save("final_heart_model.mlmodel")

