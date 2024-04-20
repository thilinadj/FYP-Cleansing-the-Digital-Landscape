from loader.load_audio import audio_array

def audio_segmenter(audio, segment_length_sec):
  hop_length = int(segment_length_sec/ 2)

  segments = []
  timestamps = []
  start_time = 0
  end_time = segment_length_sec
  
  while (end_time <= len(audio) or start_time <= len(audio)):
    if (end_time > len(audio) or start_time <= len(audio)):
      end_time == len(audio)

    segment = audio[start_time : end_time]

    segments.append(segment)
    timestamps.append((start_time, end_time))

    start_time += hop_length
    end_time += hop_length
  return segments