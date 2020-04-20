from tensorflow.keras.layers import Activation, Add, BatchNormalization, Conv2D, Dense, GlobalAveragePooling2D, Input
from tensorflow.keras.models import Model
from tensorflow.keras.regularizers import l2
from tensorflow.keras import backend as K
import os

import tensorflow as tf
config = tf.compat.v1.ConfigProto()
config.gpu_options.allow_growth = True
session = tf.compat.v1.InteractiveSession(config=config)

DN_FILTER = 256 #AlphaZero is 256
DN_RESIDUAL_NUM = 19 #Residual (19)
SCALE = 8
DN_INPUT_SHAPE = (SCALE, SCALE, 2) #盤面サイズを自分相手分
DN_OUTPUT_SIZE = SCALE**2 + 1

def conv(filters):
    return Conv2D(filters, 3, padding='same', use_bias=False, kernel_initializer='he_normal', kernel_regularizer=l2(0.0005))

def residual_block():
    def f(x):
        sc = x
        x = conv(DN_FILTER)(x)
        x = BatchNormalization()(x)
        x = Activation('relu')(x)
        x = conv(DN_FILTER)(x)
        x = BatchNormalization()(x)
        x = Add()([x, sc])
        x = Activation('relu')(x)
        return x
    return f

def dual_network():
    if os.path.exists('./model/best.h5'):
        return
    
    input = Input(shape=DN_INPUT_SHAPE)

    x = conv(DN_FILTER)(input)
    x = BatchNormalization()(x)
    x = Activation('relu')(x)

    for i in range(DN_RESIDUAL_NUM):
        x = residual_block()(x)
    
    x = GlobalAveragePooling2D()(x)

    #方策
    p = Dense(DN_OUTPUT_SIZE, kernel_regularizer=l2(0.0005), activation='softmax', name='pi')(x)

    #価値
    v = Dense(1, kernel_regularizer=l2(0.0005))(x)
    v = Activation('tanh', name='v')(v)

    model = Model(inputs=input, outputs=[p, v])

    os.makedirs('./model/', exist_ok=True)
    model.save('./model/best.h5')
    K.clear_session()
    del model

if __name__ == '__main__':
    dual_network()
