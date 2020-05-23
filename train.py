#!/usr/bin/env python3
import matplotlib.pyplot as plt
import time
import keras_ocr
import glob
import random
import string
import math
import itertools
import os
import numpy as np
import imgaug
import matplotlib.pyplot as plt
import tensorflow as tf
import sklearn.model_selection
import keras_ocr


def get_my_custom_dataset(split="train", cache_dir=None):
    return [
        (x, None, x.split("/")[1].split(".")[0].lower())
        for x in glob.glob("training_data/*.png")
    ]


train_labels = get_my_custom_dataset()

recognizer = keras_ocr.recognition.Recognizer(
    alphabet="abcdefghijklmnpqrstuvwxyz0123456789",
)
recognizer.model.load_weights("recognizer_512.h5")
recognizer.compile()

batch_size = 512
# augmenter = imgaug.augmenters.Sequential([
#    imgaug.augmenters.GaussianBlur(sigma=(0, 3.0)),
# ])
augmenter = None

train_labels, validation_labels = sklearn.model_selection.train_test_split(
    train_labels, test_size=0.2, random_state=42
)
(training_image_gen, training_steps), (validation_image_gen, validation_steps) = [
    (
        keras_ocr.datasets.get_recognizer_image_generator(
            labels=labels,
            height=recognizer.model.input_shape[1],
            width=recognizer.model.input_shape[2],
            alphabet="abcdefghijklmnpqrstuvwxyz0123456789",
            augmenter=augmenter,
        ),
        len(labels) // batch_size,
    )
    for labels, augmenter in [(train_labels, augmenter), (validation_labels, None)]
]
training_gen, validation_gen = [
    recognizer.get_batch_generator(
        image_generator=image_generator, batch_size=batch_size
    )
    for image_generator in [training_image_gen, validation_image_gen]
]

callbacks = [
    tf.keras.callbacks.EarlyStopping(
        monitor="val_loss", min_delta=0, patience=10, restore_best_weights=False
    ),
    tf.keras.callbacks.ModelCheckpoint(
        "recognizer_512.h5", monitor="val_loss", save_best_only=True
    ),
    tf.keras.callbacks.CSVLogger("recognizer_512.csv"),
    tf.keras.callbacks.TensorBoard(log_dir="mylogdir512", histogram_freq=1),
]
recognizer.training_model.fit_generator(
    generator=training_gen,
    steps_per_epoch=training_steps,
    validation_steps=validation_steps,
    validation_data=validation_gen,
    callbacks=callbacks,
    epochs=1000,
)
