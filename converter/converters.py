from moviepy.video.io.VideoFileClip import VideoFileClip
from pydub import AudioSegment
from pydub.playback import play
import noisereduce as nr
import numpy as np
from moviepy.editor import VideoFileClip, concatenate_videoclips
import librosa
import soundfile as sf

def mp4_to_wav(video_path: str, output_audio_path: str) -> None:
	video_clip = VideoFileClip(video_path)
	audio_clip = video_clip.audio
	audio_clip.write_audiofile(output_audio_path, codec="pcm_s16le")
	audio_clip.close()
	video_clip.close()

def to_mono(stereo_audio_path: str, mono_audio_path: str) -> None:
  # Load stereo audio and convert to mono
  stereo_audio, sr = librosa.load(stereo_audio_path, sr=None, mono=False)
  mono_audio = librosa.to_mono(stereo_audio)
  # Write the mono audio to a WAV file using soundfile
  sf.write(mono_audio_path, mono_audio, sr)

def noise_reducer(audio_input_path: str, audio_output_path: str) -> None:
  audio = AudioSegment.from_file(audio_input_path)
  audio_array = np.array(audio.get_array_of_samples())
  reduced_noise = nr.reduce_noise(audio_array, 16_000)

  reduced_audio = AudioSegment(
      reduced_noise.tobytes(),
      frame_rate=audio.frame_rate,
      sample_width=audio.sample_width,
      channels=audio.channels
  )

  reduced_audio.export(audio_output_path, format="wav")

def mute_video_part(input_path, output_path, durations):
  clip = VideoFileClip(input_path)
  clips_to_concat = []
  
  for index, (start_time, end_time) in enumerate(durations):
    part_to_mute = clip.subclip(start_time, end_time)
    muted_part = part_to_mute.volumex(0)

    before_part = clip.subclip(0, start_time)
    
    if index + 1 == len(durations):
      after_part = clip.subclip(end_time, clip.duration)
    else:
      after_part = clip.subclip(end_time, durations[index+1][0])

    clips_to_concat.extend([before_part, muted_part, after_part])

  final_clip = concatenate_videoclips(clips_to_concat)
  final_clip.write_videofile(output_path, codec='libx264', audio_codec='aac')