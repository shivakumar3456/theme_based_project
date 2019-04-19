import numpy as np
import io
import tensorflow
import keras
from keras import backend as k
from keras.models import load_model
print('loading model')
model=load_model("modelversion1con.h5")
print('loaded')
