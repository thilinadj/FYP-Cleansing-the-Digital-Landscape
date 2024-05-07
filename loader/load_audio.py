import librosa
import numpy as np
import pandas as pd
from pandas.core.frame import DataFrame

def audio_array(path: str):
	audio, sr = librosa.load(path, sr=16_000)
	return audio, sr

def extract_mfcc(audio, sr, pad_to=None, num_mfcc=13, n_fft=2048, hop_length=512) -> DataFrame:
  mfcc = librosa.feature.mfcc(y=audio, sr=sr, n_mfcc=num_mfcc, n_fft=n_fft, hop_length=hop_length)
  if pad_to:
    pad_width = pad_to - mfcc.shape[1]
    mfcc = np.pad(mfcc, pad_width=((0, 0), (0, pad_width)), mode='constant')
  return pd.DataFrame([mfcc.flatten()])