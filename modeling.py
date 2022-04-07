import tensorflow as tf


def create_model():

    model = tf.keras.Sequential([
        tf.keras.layers.Input(shape=(2,), name="input"),
        tf.keras.layers.Dense(2),
        tf.keras.layers.Dense(4),
        tf.keras.layers.Dense(1, name="predictions"),
    ])
    model.compile(
        loss='mean_squared_error',
        optimizer='adam',
    )
    return model


if __name__ == "__main__":
    pass
