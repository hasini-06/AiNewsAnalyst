import pyttsx3
import tempfile

def text_to_speech(text, filename=None):
    """
    Convert text to speech using pyttsx3.
    Returns a temporary .wav file path that can be used in Streamlit's st.audio().
    """
    engine = pyttsx3.init()
    engine.setProperty("rate", 140)
    engine.setProperty("volume", 1.0)  

    if filename is None:
        tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
        filename = tmp_file.name
        tmp_file.close()

    engine.save_to_file(text, filename)
    engine.runAndWait()

    return filename
