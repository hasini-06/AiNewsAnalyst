import pyttsx3
import tempfile

def text_to_speech(text, filename=None):
    """
    Convert text to speech using pyttsx3.
    Returns a temporary .wav file path that can be used in Streamlit's st.audio().
    """
    engine = pyttsx3.init()
    engine.setProperty("rate", 140)  # Speed of speech
    engine.setProperty("volume", 1.0)  # Volume (0.0 to 1.0)

    # Use given filename or create a temporary file
    if filename is None:
        tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
        filename = tmp_file.name
        tmp_file.close()

    engine.save_to_file(text, filename)
    engine.runAndWait()

    return filename
