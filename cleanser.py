import os
from shared_data.shared_data import UPLOAD_TEMP_FOLDER, UPLOAD_TEMP_AUDIO, UPLOAD_TEMP_MONO, UPLOAD_TEMP_NO_NOISE, UPLOAD_MAIN_FOLDER, target_length
from converter.converters import *
from segmenter.audio_segmenter import audio_segmenter
from loader.load_audio import extract_mfcc

def cleanser(filename: str, model):
  inputh_path = os.path.join(UPLOAD_TEMP_FOLDER, "".join([filename, ".mp4"]))
  audio_path = os.path.join(UPLOAD_TEMP_AUDIO, "".join([filename, ".wav"]))
  mono_audio_path = os.path.join(UPLOAD_TEMP_MONO, "".join([filename, ".wav"]))
  noise_removed = os.path.join(UPLOAD_TEMP_NO_NOISE, "".join([filename, ".wav"]))
  output_path = os.path.join(UPLOAD_MAIN_FOLDER, "".join([filename, ".mp4"]))
  mp4_to_wav(inputh_path, audio_path)
  to_mono(audio_path, mono_audio_path)
  noise_reducer(mono_audio_path, noise_removed)

  segments, timestamps = audio_segmenter(audio_path= noise_removed, segment_length_sec= 2.0)

  mfcc_features = []
  for segment in segments:
    mfcc_feature = extract_mfcc(audio= segment[0], sr= segment[1], pad_to= target_length)
    mfcc_features.append(mfcc_feature)
  
  timestamps_sec = [(start/16_000, end/16_000) for start, end in timestamps]
  detected = []

  for index, mfcc in enumerate(mfcc_features):
    pred = model.predict(mfcc)
    if int(pred[0]) != 2:
      detected.append((int(timestamps_sec[index][0]), int(timestamps_sec[index][1])))
  
  mute_video_part(inputh_path, output_path, detected)
  print("cleansing done!")