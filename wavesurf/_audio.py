"""Audio loading and encoding utilities.

Supports four input types:
- ``numpy.ndarray`` + sample rate → base64 WAV data-URL
- ``str`` / ``Path`` file path → load via soundfile → data-URL
- ``str`` starting with ``http`` / ``https`` → URL passthrough (no embedding)
- ``torch.Tensor`` → convert to numpy (optional, runtime-detected)
"""

from __future__ import annotations

import base64
import io
from pathlib import Path
from typing import Any

import numpy as np
import soundfile as sf


def _is_torch_tensor(obj: Any) -> bool:
    """Check if *obj* is a PyTorch tensor without requiring torch at import."""
    try:
        import torch  # noqa: F811
        return isinstance(obj, torch.Tensor)
    except ImportError:
        return False


def _torch_to_numpy(tensor: Any) -> np.ndarray:
    """Convert a PyTorch tensor to a numpy array."""
    return tensor.detach().cpu().float().numpy()


def audio_to_data_url(audio: np.ndarray, sr: int) -> str:
    """Convert a numpy audio array + sample rate to a base64 WAV data-URL."""
    buf = io.BytesIO()
    sf.write(file=buf, data=audio, samplerate=sr, format="WAV", subtype="PCM_16")
    b64 = base64.b64encode(buf.getvalue()).decode("ascii")
    return f"data:audio/wav;base64,{b64}"


def load_audio_file(path: str | Path) -> tuple[np.ndarray, int]:
    """Load an audio file and return ``(numpy_array, sample_rate)``."""
    data, sr = sf.read(file=str(path), dtype="float32")
    return data, int(sr)


def resolve_audio(
    audio: Any,
    sr: int | None = None,
) -> tuple[str, int | None]:
    """Resolve an audio input to a ``(url_or_data_url, sample_rate)`` pair.

    Parameters
    ----------
    audio:
        One of: numpy array, torch tensor, file path string/Path, or URL string.
    sr:
        Sample rate.  Required for numpy arrays and torch tensors.

    Returns
    -------
    tuple:
        ``(data_url_or_url, sample_rate)`` — for URL inputs the sample rate
        may be ``None`` since the audio is not decoded locally.
    """
    # Torch tensor → numpy
    if _is_torch_tensor(audio):
        audio = _torch_to_numpy(tensor=audio)

    # Numpy array
    if isinstance(audio, np.ndarray):
        if sr is None:
            raise ValueError("sr (sample rate) is required when passing a numpy array")
        return audio_to_data_url(audio=audio, sr=sr), sr

    # String or Path
    if isinstance(audio, (str, Path)):
        path_str = str(audio)
        # URL passthrough
        if path_str.startswith(("http://", "https://")):
            return path_str, sr
        # File path
        data, file_sr = load_audio_file(path=path_str)
        return audio_to_data_url(audio=data, sr=file_sr), file_sr

    raise TypeError(
        f"audio must be a numpy array, torch tensor, file path, or URL string — "
        f"got {type(audio).__name__}"
    )
