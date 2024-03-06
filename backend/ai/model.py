from __future__ import annotations

import io
import numpy as np
from pydantic import BaseModel
from tensorflow.keras import layers, models
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from PIL import Image


class EmojiClassifierConfig(BaseModel):
    image_shape: tuple[int, int] = (256, 256)
    num_classes: int = 12
    batch_size: int = 32
    epochs: int = 10

    train_path: str = "../dataset/train"
    validation_path: str = "../dataset/validation"
    test_path: str = "../dataset/test"


class EmojiClassifier:
    def __init__(self, config: EmojiClassifierConfig):
        self.config = config
        self.model = self.build_model()

        data_gen_args = dict(
            rotation_range=15,
            width_shift_range=0.1,
            height_shift_range=0.1,
            zoom_range=0.1,
        )

        self.train_generator = ImageDataGenerator(**data_gen_args).flow_from_directory(
            self.config.train_path,
            target_size=(64, 64),
            batch_size=self.config.batch_size,
            class_mode="categorical",
            color_mode="grayscale",
        )
        self.validation_generator = ImageDataGenerator().flow_from_directory(
            self.config.validation_path,
            target_size=(64, 64),
            batch_size=self.config.batch_size,
            class_mode="categorical",
            color_mode="grayscale",
        )
        self.test_generator = ImageDataGenerator().flow_from_directory(
            self.config.test_path,
            target_size=(64, 64),
            batch_size=self.config.batch_size,
            class_mode="categorical",
            color_mode="grayscale",
        )

    def build_model(self):
        model = models.Sequential(
            [
                layers.Conv2D(32, (3, 3), activation="relu", input_shape=(64, 64, 1)),
                layers.MaxPooling2D((2, 2)),
                layers.Conv2D(64, (3, 3), activation="relu"),
                layers.MaxPooling2D((2, 2)),
                layers.Conv2D(128, (3, 3), activation="relu"),
                layers.MaxPooling2D((2, 2)),
                layers.Conv2D(128, (3, 3), activation="relu"),
                layers.MaxPooling2D((2, 2)),
                layers.Flatten(),
                layers.Dense(512, activation="relu"),
                layers.Dense(self.config.num_classes, activation="softmax"),
            ]
        )

        model.compile(
            optimizer="adam",
            loss="categorical_crossentropy",
            metrics=["accuracy"],
        )

        return model

    def train(self, epochs: int | None = None, batch_size: int | None = None):
        if not epochs:
            epochs = self.config.epochs
        if not batch_size:
            batch_size = self.config.batch_size

        history = self.model.fit(
            self.train_generator,
            epochs=epochs,
            batch_size=batch_size,
            validation_data=self.validation_generator,
        )
        return history

    def evaluate(self):
        return self.model.evaluate(self.test_generator)

    def save(self, path: str):
        self.model.save(path)

    def load(self, path: str):
        self.model = models.load_model(path)

    def predict(self, image):
        return self.model.predict(image)

    def evaluate_another(self):
        incorrects = []
        for i in range(len(self.test_generator)):
            x_test, y_test = self.test_generator[i]
            y_pred = self.model.predict(x_test)
            y_pred_classes = np.argmax(y_pred, axis=1)
            y_true_classes = np.argmax(y_test, axis=1)
            incorrects.extend(
                [
                    (x, p, t)
                    for x, p, t in zip(x_test, y_pred_classes, y_true_classes)
                    if p != t
                ]
            )
        return incorrects


def _main():
    import sys
    import datetime

    action = sys.argv[1] if len(sys.argv) > 1 else "train"
    model_name = (
        sys.argv[2]
        if len(sys.argv) > 2
        else f"../model-{datetime.datetime.now().isoformat()}.keras"
    )

    if action == "train" or action == "load+train":
        classifier = EmojiClassifier(EmojiClassifierConfig())

        if action == "load+train":
            classifier.load(model_name)

        classifier.train(epochs=20)
        test_loss, test_accuracy = classifier.evaluate()
        print(f"Test accuracy: {test_accuracy * 100:.2f}%")
        print(f"Test loss: {test_loss}")

        classifier.save(model_name)
    elif action == "load":
        classifier = EmojiClassifier(EmojiClassifierConfig())
        classifier.load(model_name)
        incorrects = classifier.evaluate_another()
        print(f"Corrects: {len(incorrects) - len(classifier.test_generator)}")
        print(f"Incorrects: {len(incorrects)}")
        print(f"Total: {len(classifier.test_generator)}")
        print(f"Accuracy: {1 - len(incorrects) / len(classifier.test_generator):.2f}")
    elif action == "test":
        classifier = EmojiClassifier(EmojiClassifierConfig())
        classifier.load(model_name)

        with open("./var/test.png", "rb") as f:
            # This image has 3 channels, but the model expects 1 channel
            image = f.read()

            # Converting to grayscale 1 channel
            image = np.array(Image.open(io.BytesIO(image)).convert("L"))

            # Reshape to 64x64 image
            image = image.reshape(1, 64, 64, 1)

        print(classifier.predict(image))

    else:
        print(f"Unknown action: {action}")


if __name__ == "__main__":
    _main()
