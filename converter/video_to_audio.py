from moviepy.video.io.VideoFileClip import VideoFileClip

def mp4_to_wav(video_path: str, output_audio_path: str) -> None:
	video_clip = VideoFileClip(video_path)
	audio_clip = video_clip.audio
	audio_clip.write_audiofile(output_audio_path, codec="pcm_s16le")
	audio_clip.close()
	video_clip.close()