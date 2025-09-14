from gtts import gTTS
import tempfile

def text_to_speech(text: str):
    """Convert text to speech and return the temporary file path."""
    # Create a temporary file
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
    
    # Generate speech
    tts = gTTS(text)
    tts.save(temp_file.name)
    
    return temp_file.name
