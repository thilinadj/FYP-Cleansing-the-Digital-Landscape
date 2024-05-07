from loader.load_audio import audio_array

def audio_segmenter(audio_path: str, segment_length_sec: float) -> tuple[list, list]:
  audio, sr = audio_array(audio_path)
  hop_length = int(segment_length_sec * sr/ 2)
  audio_length = len(audio)

  segments = []
  timestamps = []
  start_time = 0
  end_time = int(segment_length_sec * sr)
  
  while (end_time <= audio_length or start_time < audio_length):
    if (end_time > audio_length and start_time < audio_length):
      end_time = audio_length

    if end_time - start_time > 4000:
      segment = audio[start_time : end_time]

      segments.append((segment, sr))
      timestamps.append((start_time, end_time))

    start_time += hop_length
    end_time += hop_length
  return segments, timestamps