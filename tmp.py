from tensorflow import keras

from ML_Ops.modeling import create_model

if __name__ == "__main__":
    inputs = [keras.layers.Input(shape=(1,)) for _ in range(2)]
    d = keras.layers.concatenate(inputs)
    for _ in range(2):
        d = keras.layers.Dense(8)(d)
    outputs = keras.layers.Dense(3)(d)
    model = keras.Model(inputs=inputs, outputs=outputs)
    print(type(model))
    model.summary()

    print(type(create_model()))
    create_model().summary()
