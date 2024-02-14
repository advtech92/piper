# Piper_STT.py
from config import PV_ACCESSKEY
import pvporcupine
import pyaudio
import struct
import speech_recognition as sr
from SHM_LIFX import handle_lifx_command
from SHM_Spotify import handle_spotify_command

ACCESS_KEY = PV_ACCESSKEY

def listen_for_wake_word_porcupine(wake_word_path="Hey-Piper_en_windows_v3_0_0/Hey-Piper_en_windows_v3_0_0.ppn", timeout=None):
    """
    Listens for the wake word using Porcupine to activate further commands.

    :param wake_word_path: Path to the Porcupine wake word model file.
    :param timeout: The maximum number of seconds to wait for a wake word. `None` means wait indefinitely.
    :return: True if the wake word was heard, False otherwise.
    """
    porcupine = None
    pa = None
    audio_stream = None

    try:
        porcupine = pvporcupine.create(access_key=ACCESS_KEY,keyword_paths=[wake_word_path])
        pa = pyaudio.PyAudio()
        audio_stream = pa.open(
            rate=porcupine.sample_rate,
            channels=1,
            format=pyaudio.paInt16,
            input=True,
            frames_per_buffer=porcupine.frame_length
        )

        print("I'm listening for 'Hey Piper'. Just say it to wake me up!")
        while True:
            pcm = audio_stream.read(porcupine.frame_length, exception_on_overflow=False)
            pcm_unpacked = struct.unpack_from("h" * porcupine.frame_length, pcm)

            keyword_index = porcupine.process(pcm_unpacked)
            if keyword_index >= 0:
                print("Wake word detected!")
                return True
            # Implement timeout logic if necessary
    except Exception as e:
        print(f"Error detecting wake word: {e}")
        return False
    finally:
        if porcupine is not None:
            porcupine.delete()
        if audio_stream is not None:
            audio_stream.close()
        if pa is not None:
            pa.terminate()

def recognize_speech_from_mic(timeout=5, phrase_time_limit=10):
    """
    Transcribes speech from the microphone.
    """
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    with mic as source:
        print("Go ahead, I'm listening...")
        try:
            audio = recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
        except sr.WaitTimeoutError:
            print("Listening timed out.")
            return {"error": "Listening timed out."}

    try:
        transcription = recognizer.recognize_sphinx(audio)
        print(f"Got it! You said: {transcription}")
        return {"transcription": transcription, "error": None}
    except (sr.UnknownValueError, sr.RequestError) as e:
        print(f"Error understanding audio: {e}")
        return {"error": str(e)}

def handle_command(command):
    """
    Determines the type of command (Spotify or LIFX) and calls the appropriate handler.
    """
    command = command.lower()
    if "spotify" in command:
        handle_spotify_command(command)
    elif "light" in command or "lifx" in command:
        handle_lifx_command(command)
    else:
        print("I'm not sure how to handle that command. Please try again.")

def start_voice_recognition_loop():
    while True:
        if listen_for_wake_word_porcupine():
            speech_result = recognize_speech_from_mic()
            if speech_result and speech_result["error"] is None:
                # Process the recognized speech
                handle_command(speech_result["transcription"])
            else:
                print("There was an error processing your command.")