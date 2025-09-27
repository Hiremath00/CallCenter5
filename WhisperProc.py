import whisper

def transcribe_audio(file_path):

    # Load the Whisper model
    model = whisper.load_model("base")

    # Transcribe the audio file
    result = model.transcribe(file_path, fp16=False)

    # Return the transcribed text
    return result["text"]