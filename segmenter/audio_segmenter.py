from loader.load_audio import audio_array

def audio_segmenter(audio_path: str, segment_length_sec: int) -> tuple[list, list]:
  print("hi")
  audio, sr = audio_array(audio_path)
  hop_length = int(segment_length_sec * sr/ 2)

  segments = []
  timestamps = []
  start_time = 0
  end_time = segment_length_sec * sr
  
  while (end_time <= len(audio) or start_time <= len(audio)):
    print(f"{start_time= }, {end_time= }, {len(audio)= }")
    if (end_time > len(audio) and start_time <= len(audio)):
      end_time == len(audio)

    segment = audio[start_time : end_time]

    segments.append((segment, sr))
    timestamps.append((start_time, end_time))

    start_time += hop_length
    end_time += hop_length
  return segments, timestamps