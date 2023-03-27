import os
import openai
from tempfile import NamedTemporaryFile
from pydub import AudioSegment
import subprocess


def convert_audio_to_mp3(input_file):
    with NamedTemporaryFile(suffix=".mp3", delete=False) as output_file:
        try:
            subprocess.run(["ffmpeg", "-y", "-i", input_file.name, output_file.name], check=True)
            return output_file.name
        except subprocess.CalledProcessError as e:
            print(f"Error converting audio to mp3: {e}")
            return None
#this sadly never worked and i don't know why. Broke my js 
def speech_to_text(audio_file):
    openai.api_key = os.getenv("OPENAI_API_KEY")

    # Save the audio file to a temporary file
    with NamedTemporaryFile(suffix=".webm", delete=False) as temp_audio_file:
        temp_audio_file.write(audio_file.read())

    # Convert the audio to mp3 format
    mp3_audio_file = convert_audio_to_mp3(temp_audio_file)
    if not mp3_audio_file:
        return None

    # Transcribe the mp3 audio using the OpenAI API
    with open(mp3_audio_file, "rb") as file_to_transcribe:
        transcript = openai.Audio.transcribe("whisper-1", file_to_transcribe)

    # Remove the temporary files
    os.remove(temp_audio_file.name)
    os.remove(mp3_audio_file)

    return transcript.get("text")