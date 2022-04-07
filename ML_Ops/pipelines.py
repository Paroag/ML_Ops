from tfx import v1 as tfx

from ML_Ops import PROJECT_PATH


def create_pipeline() -> tfx.dsl.Pipeline:
    example_gen = tfx.components.CsvExampleGen(f"{PROJECT_PATH}/data/20220404/csv/")
    trainer = tfx.components.Trainer(
        module_file=f"{PROJECT_PATH}/ML_Ops/modeling.py",
        examples=example_gen.outputs['examples'],
        train_args=tfx.proto.TrainArgs(num_steps=100),
        eval_args=tfx.proto.EvalArgs(num_steps=5)
    )
    pusher = tfx.components.Pusher(
        model=trainer.outputs['model'],
        push_destination=tfx.proto.PushDestination(
            filesystem=tfx.proto.PushDestination.Filesystem(
                base_directory=f"{PROJECT_PATH}/tmp"
            )
        )
    )
    components = [
        example_gen,
        trainer,
        pusher,
    ]
    return tfx.dsl.Pipeline(
        pipeline_name="dummy_pipeline",
        pipeline_root=f"{PROJECT_PATH}/tmp",
        components=components,
        metadata_connection_config=tfx.orchestration.metadata.sqlite_metadata_connection_config(
            f"{PROJECT_PATH}/tmp/metadata.db"
        )
    )


if __name__ == "__main__":
    pipeline = create_pipeline()
    tfx.orchestration.LocalDagRunner().run(
        pipeline
    )
