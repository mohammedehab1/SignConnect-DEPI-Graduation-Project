import io
import soundfile as sf
import numpy as np
import librosa

class AudioPreprocessor:
    @staticmethod
    def load_and_resample(audio_bytes: bytes, target_sr=16000):
        audio_array, sr = sf.read(io.BytesIO(audio_bytes))
        if len(audio_array.shape) > 1:
            audio_array = np.mean(audio_array, axis=1)

        if sr != target_sr:
            audio_array = librosa.resample(
                audio_array.astype(np.float32),
                orig_sr=sr,
                target_sr=target_sr
            )
            sr = target_sr

        return audio_array, sr
