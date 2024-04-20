from moviepy.editor import VideoFileClip, concatenate_videoclips

def mute_video_part(input_path, output_path, start_time, end_time):

  clip = VideoFileClip(input_path)
  part_to_mute = clip.subclip(start_time, end_time)
  muted_part = part_to_mute.set_audio(part_to_mute.audio.set_mute(True))

  before_part = clip.subclip(0, start_time)
  after_part = clip.subclip(end_time, clip.duration)
  

  final_clip = concatenate_videoclips([before_part, muted_part, after_part])
  final_clip.write_videofile(output_path, codec='libx264', audio_codec='aac')