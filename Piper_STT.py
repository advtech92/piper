#Piper_STT.py
import os
from pocketsphinx import LiveSpeech, get_model_path

class STTModule:
    def __init__(self, wake_word="hey piper"):
        model_path = get_model_path()
        self.wake_word = wake_word.lower()
        self.speech = LiveSpeech(
            verbose=False,
            sampling_rate=16000,
            buffer_size=2048,
            no_search=False,
            full_utt=False,
            hmm=os.path.join(model_path, 'en-us'),
            lm=os.path.join(model_path, 'en-us.lm.bin'),
            dic=os.path.join(model_path, 'cmudict-en-us.dict')
        )

    def listen_for_wake_word(self):
        print("Listening for wake word...")
        while True:
            for phrase in self.speech:
                recognized_text = str(phrase).lower()
                print(f"Heard: {recognized_text}")
                if self.wake_word in recognized_text:
                    print("Wake word detected!")
                    return True