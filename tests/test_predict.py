from pathlib import Path

import numpy as np
import pytest
from PIL import Image

import predict


def test_resolve_model_path_with_missing_explicit_path_raises() -> None:
    missing_model = Path("models/does_not_exist.keras")

    with pytest.raises(FileNotFoundError, match="Model file not found"):
        predict.resolve_model_path(str(missing_model))


def test_load_image_missing_path_raises(tmp_path: Path) -> None:
    missing_image = tmp_path / "missing.jpg"

    with pytest.raises(FileNotFoundError, match="Image file not found"):
        predict.load_image(missing_image)


def test_load_image_returns_expected_batch_shape(tmp_path: Path) -> None:
    image_path = tmp_path / "sample.jpg"
    Image.fromarray(np.full((32, 32, 3), 255, dtype=np.uint8)).save(image_path)

    batch = predict.load_image(image_path)

    assert batch.shape == (1, 150, 150, 3)
    assert batch.dtype == np.float32
    assert batch.min() >= 0.0
    assert batch.max() <= 1.0


def test_predict_image_with_mocked_model(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    class DummyModel:
        def predict(self, batch: np.ndarray, verbose: int = 0) -> np.ndarray:
            assert batch.shape == (1, 150, 150, 3)
            assert verbose == 0
            return np.array([[0.2]], dtype=np.float32)

    image_path = tmp_path / "sample.jpg"
    model_path = tmp_path / "dummy.keras"
    Image.fromarray(np.zeros((64, 64, 3), dtype=np.uint8)).save(image_path)
    model_path.write_text("unused", encoding="utf-8")

    monkeypatch.setattr(predict.tf.keras.models, "load_model", lambda _: DummyModel())

    predicted_label, recyclable_probability = predict.predict_image(
        image_path, model_path
    )

    assert predicted_label == "Organic (O)"
    assert recyclable_probability == pytest.approx(0.2)
