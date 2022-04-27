import os
from keras.models import Model
from keras.layers import (
    Input,
    Dense,
    Dropout,
    Flatten,
    Conv2D,
    MaxPooling2D,
)

PATH = os.path.dirname(os.path.abspath(__file__))

def load_model():
    tensor_in = Input((60, 200, 3))
    tensor_out = tensor_in
    tensor_out = Conv2D(
        filters=32, kernel_size=(3, 3), padding="same", activation="relu"
    )(tensor_out)
    tensor_out = Conv2D(filters=32, kernel_size=(3, 3), activation="relu")(
        tensor_out
    )
    tensor_out = MaxPooling2D(pool_size=(2, 2))(tensor_out)
    tensor_out = Dropout(0.25)(tensor_out)
    tensor_out = Conv2D(
        filters=64, kernel_size=(3, 3), padding="same", activation="relu"
    )(tensor_out)
    tensor_out = Conv2D(filters=64, kernel_size=(3, 3), activation="relu")(
        tensor_out
    )
    tensor_out = MaxPooling2D(pool_size=(2, 2))(tensor_out)
    tensor_out = Dropout(0.25)(tensor_out)
    tensor_out = Conv2D(
        filters=128, kernel_size=(3, 3), padding="same", activation="relu"
    )(tensor_out)
    tensor_out = Conv2D(filters=128, kernel_size=(3, 3), activation="relu")(
        tensor_out
    )
    tensor_out = MaxPooling2D(pool_size=(2, 2))(tensor_out)
    tensor_out = Dropout(0.25)(tensor_out)
    tensor_out = Conv2D(
        filters=256, kernel_size=(3, 3), padding="same", activation="relu"
    )(tensor_out)
    tensor_out = Conv2D(filters=256, kernel_size=(3, 3), activation="relu")(
        tensor_out
    )
    tensor_out = MaxPooling2D(pool_size=(2, 2))(tensor_out)
    tensor_out = Dropout(0.25)(tensor_out)
    # tensor_out = Conv2D(filters=512, kernel_size=(3, 3), activation='relu')(tensor_out)
    # tensor_out = MaxPooling2D(pool_size=(2, 2))(tensor_out)
    Dense(1024, activation="relu")
    tensor_out = Flatten()(tensor_out)
    tensor_out = Dropout(0.5)(tensor_out)
    tensor_out = [
        Dense(37, name="digit1", activation="softmax")(tensor_out),
        Dense(37, name="digit2", activation="softmax")(tensor_out),
        Dense(37, name="digit3", activation="softmax")(tensor_out),
        Dense(37, name="digit4", activation="softmax")(tensor_out),
        Dense(37, name="digit5", activation="softmax")(tensor_out),
    ]
    model = Model(inputs=tensor_in, outputs=tensor_out)
    # Define the optimizer
    model.compile(
        loss="categorical_crossentropy",
        optimizer="Adamax",
        metrics=["accuracy"],
    )
    model.load_weights(f"{PATH}/weight/verificatioin_code_788.h5")
    return model
