# -*- coding: utf-8 -*-
"""Tensorflow.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/github/applepieiris/cs213n_assignments/blob/main/assignment2_colab/assignment2/Tensorflow.ipynb
"""



import tensorflow as tf
import tensorflow_datasets as tfds
import matplotlib.pyplot as plt
import numpy as np
import PIL
import tensorflow as tf

from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.models import Sequential

from tensorflow.keras.applications.vgg16 import VGG16
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.vgg16 import preprocess_input
import numpy as np

(ds_train,ds_test),ds_info = tfds.load('cifar10',split=['train','test'],with_info=True,as_supervised=True) # as_supervised=True：返回元组 (img, label) 而非字典 {'image': img, 'label': label}

model = VGG16(include_top=False,input_shape = (224,224,3))

def normalize_img(image, label):
  """Normalizes images: `uint8` -> `float32`."""
  image = tf.image.resize(image,(224,224))
  image = preprocess_input(image)
  return image, label

ds_train = ds_train.map(normalize_img)
ds_train = ds_train.batch(4)
ds_train = ds_train.prefetch(2)

ds_test = ds_test.map(normalize_img)
ds_test = ds_test.batch(4)
ds_test = ds_test.prefetch(2)

Input = tf.keras.layers.Input(shape=(224,224,3))
x = model(Input)
x = tf.keras.layers.Flatten()(x)
x = tf.keras.layers.Dense(256,activation='relu')(x)
x = tf.keras.layers.Dense(10,activation='softmax')(x)

new_model = tf.keras.Model(inputs = Input,outputs = x)

new_model.summary()

new_model.compile(loss=tf.keras.losses.sparse_categorical_crossentropy,
              optimizer = tf.keras.optimizers.RMSprop(learning_rate=0.0001),
              metrics=['acc'])

history = new_model.fit(
    ds_train ,
    epochs=10,
    validation_data=ds_test,
)



