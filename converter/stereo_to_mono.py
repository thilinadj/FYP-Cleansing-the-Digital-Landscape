import librosa
import soundfile as sf

def to_mono(stereo_audio_path: str, mono_audio_path: str) -> None:
  # Load stereo audio and convert to mono
  stereo_audio, sr = librosa.load(stereo_audio_path, sr=None, mono=False)
  mono_audio = librosa.to_mono(stereo_audio)
  # Write the mono audio to a WAV file using soundfile
  sf.write(mono_audio_path, mono_audio, sr)