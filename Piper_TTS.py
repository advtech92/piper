# type: ignore[import-untyped]
import torch
import torchaudio
import torch.nn as nn
import torch.nn.functional as F

from tortoise.api import TextToSpeech
from tortoise.utils.audio import load_audio, load_voice, load_voices

tts = TextToSpeech(kv_cache=True)

# Choose Preset, Fast is default
preset = "ultra_fast"
voice = 'angie'
voice_samples, conditioning_latents = load_voice(voice)
text = "Hello, My name is Piper"
gen = tts.tts_with_preset(text, voice_samples=voice_samples, conditioning_latents=conditioning_latents, preset=preset)
torchaudio.save("generated.wav", gen.squeeze(0).cpu(), 24000)