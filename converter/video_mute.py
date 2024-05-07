from moviepy.editor import VideoFileClip, concatenate_videoclips

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