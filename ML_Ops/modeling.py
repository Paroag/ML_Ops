import tensorflow as tf
from tensorflow import keras
from tensorflow_transform.tf_metadata import schema_utils
from tfx import v1 as tfx
from tfx_bsl.public import tfxio

from ML_Ops import _FEATURES, _TARGET


def create_model() -> keras.models.Model:
    inputs = [keras.layers.Input(shape=(1,), name=feature) for feature in _FEATURES]
    d = keras.layers.concatenate(inputs)
    for _ in range(2):
        d = keras.layers.Dense(8)(d)
    outputs = keras.layers.Dense(1)(d)
    model = keras.Model(inputs=inputs, outputs=outputs)
    model.compile(
        loss='mean_squared_error',
        optimizer='adam',
    )
    return model


def run_fn(fn_args: tfx.components.FnArgs) -> None:
    """This function is named as required by tfx"""
    schema = schema_utils.schema_from_feature_spec(
        {
            **{
                feature: tf.io.FixedLenFeature(shape=[1], dtype=tf.float32)
                for feature
                in _FEATURES
            },
            _TARGET: tf.io.FixedLenFeature(shape=[1], dtype=tf.float32)
        }
    )
    train_dataset = fn_args.data_accessor.tf_dataset_factory(
        fn_args.train_files,
        tfxio.TensorFlowDatasetOptions(batch_size=16, label_key=_TARGET),
        schema=schema,
    ).repeat()
    eval_dataset = fn_args.data_accessor.tf_dataset_factory(
        fn_args.eval_files,
        tfxio.TensorFlowDatasetOptions(batch_size=16, label_key=_TARGET),
        schema=schema,
    ).repeat()

    model = create_model()
    model.fit(
        train_dataset,
        steps_per_epoch=fn_args.train_steps,
    )
    model.save(fn_args.serving_model_dir, save_format="tf")


if __name__ == "__main__":
    pass
