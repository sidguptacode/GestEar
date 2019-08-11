import tensorflow as tf
from tensorflow import keras
from constants import SEQUENCE_LENGTH, N_GYRO, N_LIN_ACCEL, N_CLASSES


def create_model(n_fft):
    # Input
    input_fft = keras.layers.Input(shape=[SEQUENCE_LENGTH, n_fft], name="input_fft")

    # Add a "colour" channel and combine batch and sequence length
    reshaped_fft = keras.layers.Reshape(target_shape=(SEQUENCE_LENGTH, n_fft, 1))(input_fft)

    # Convolutions on each part of the sequence
    conv1_fft = keras.layers.TimeDistributed(
        keras.layers.Conv1D(filters=16, kernel_size=(3,), strides=(1,), input_shape=[n_fft, 1], activation=tf.nn.relu))(
        reshaped_fft)

    # Max pooling on each part of the sequence
    max1_fft = keras.layers.TimeDistributed(keras.layers.MaxPool1D(pool_size=2))(conv1_fft)

    # Convolutions on each part of the sequence
    conv2_fft = keras.layers.TimeDistributed(
        keras.layers.Conv1D(filters=16, kernel_size=(3,), strides=(1,), activation=tf.nn.relu))(max1_fft)

    # Max pooling on each part of the sequence
    max2_fft = keras.layers.TimeDistributed(keras.layers.MaxPool1D(pool_size=2))(conv2_fft)

    # Convolutions on each part of the sequence
    conv3_fft = keras.layers.TimeDistributed(
        keras.layers.Conv1D(filters=16, kernel_size=(3,), strides=(1,), activation=tf.nn.relu))(max2_fft)

    # Max pooling on each part of the sequence
    max3_fft = keras.layers.TimeDistributed(keras.layers.MaxPool1D(pool_size=2))(conv3_fft)

    # Flatten on each part of the sequence
    flattened_fft = keras.layers.TimeDistributed(keras.layers.Flatten())(max3_fft)

    # Dense layer for each input
    dense_fft = keras.layers.Dense(10, activation=tf.nn.relu)(flattened_fft)

    time_distributed = keras.layers.Dense(20, activation=tf.nn.relu)(dense_fft)

    # Flatten the sequence into one vector
    flattened_sequence = keras.layers.Flatten()(time_distributed)

    dense1 = keras.layers.Dense(20, activation=tf.nn.relu)(flattened_sequence)

    # Softmax layer to make the decision
    softmax_output_gesture_detection = keras.layers.Dense(2, input_shape=[20],
                                                          activation=tf.nn.softmax,
                                                          name='softmax_gesture_detection')(dense1)

    softmax_output_gesture_type = keras.layers.Dense(N_CLASSES, input_shape=[20], activation=tf.nn.softmax,
                                                     name='softmax_gesture_type')(dense1)

    model = keras.models.Model(inputs=[input_fft],
                               outputs=[softmax_output_gesture_detection, softmax_output_gesture_type])

    return model
