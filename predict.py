from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import tensorflow as tf

IMAGE_SIZE = (150, 150)
CLASS_NAMES = {
    0: "Organic (O)",
    1: "Recyclable (R)",
}
DEFAULT_MODELS = [
    Path("models/vgg16_waste_classifier.keras"),
]


def resolve_model_path(model_arg: str | None) -> Path:
    if model_arg:
        model_path = Path(model_arg)
        if not model_path.exists():
            raise FileNotFoundError(
                "Model file not found: "
                f"{model_path}. Add a valid local checkpoint or rerun the notebook "
                "to generate one."
            )
        return model_path

    for candidate in DEFAULT_MODELS:
        if candidate.exists():
            return candidate

    searched = ", ".join(str(path) for path in DEFAULT_MODELS)
    raise FileNotFoundError(
        "No default model checkpoint was found. "
        f"Searched: {searched}. "
        "The project is configured to use models/vgg16_waste_classifier.keras "
        "as the default bundled checkpoint, so verify that the file exists or "
        "pass --model with a valid local checkpoint."
    )


def load_image(image_path: Path) -> np.ndarray:
    if not image_path.exists():
        raise FileNotFoundError(f"Image file not found: {image_path}")

    image = tf.keras.utils.load_img(image_path, target_size=IMAGE_SIZE)
    array = tf.keras.utils.img_to_array(image).astype("float32") / 255.0
    return np.expand_dims(array, axis=0)


def predict_image(image_path: Path, model_path: Path) -> tuple[str, float]:
    model = tf.keras.models.load_model(model_path)
    batch = load_image(image_path)
    recyclable_probability = float(model.predict(batch, verbose=0)[0][0])
    predicted_index = 0 if recyclable_probability < 0.5 else 1
    return CLASS_NAMES[predicted_index], recyclable_probability


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Predict waste class for a single image using the saved VGG16 model."
    )
    parser.add_argument("image", help="Path to the image file.")
    parser.add_argument(
        "--model",
        help="Optional path to a specific .keras model file.",
    )
    args = parser.parse_args()
    try:
        image_path = Path(args.image)
        model_path = resolve_model_path(args.model)
        predicted_label, recyclable_probability = predict_image(image_path, model_path)
    except FileNotFoundError as error:
        raise SystemExit(str(error)) from error

    print(f"Model: {model_path}")
    print(f"Predicted class: {predicted_label}")
    print(f"Recyclable probability: {recyclable_probability:.4f}")
    print(f"Organic probability: {1.0 - recyclable_probability:.4f}")


if __name__ == "__main__":
    main()
