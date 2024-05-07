from pydub import AudioSegment
from pydub.playback import play
import noisereduce as nr
import numpy as np

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
