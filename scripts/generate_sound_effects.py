import wave
import struct
import math
import os

SOUNDS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'sounds')

def generate_wav(filename, tones, sample_rate=44100):
    """
    tones: list of (frequency, duration, volume)
    """
    total_samples = 0
    raw_audio = bytearray()
    
    for freq, duration, volume in tones:
        n_samples = int(sample_rate * duration)
        for i in range(n_samples):
            # Smooth fade in / fade out envelope
            env = 1.0
            attack = int(0.01 * sample_rate)
            decay = int(0.05 * sample_rate)
            if i < attack:
                env = i / attack
            elif i > (n_samples - decay):
                env = (n_samples - i) / decay
                
            val = int(32767.0 * volume * env * math.sin(2.0 * math.pi * freq * (i / sample_rate)))
            val = max(-32768, min(32767, val))
            raw_audio.extend(struct.pack('<h', val))
        total_samples += n_samples
        
    filepath = os.path.join(SOUNDS_DIR, filename)
    with wave.open(filepath, 'w') as wav:
        wav.setparams((1, 2, sample_rate, total_samples, 'NONE', 'not compressed'))
        wav.writeframesraw(raw_audio)
    print(f"Generated {filepath} ({total_samples} samples)")

# 1. Correct sound: bright ascending 2-tone chime (523Hz -> 659Hz, C5 to E5)
generate_wav("correct.wav", [(523.25, 0.12, 0.35), (659.25, 0.22, 0.4)])

# 2. Wrong sound: soft lower double-tone
generate_wav("wrong.wav", [(261.63, 0.15, 0.3), (220.00, 0.25, 0.35)])

# 3. Complete sound: celebratory fanfare (C5 -> E5 -> G5 -> C6)
generate_wav("complete.wav", [
    (523.25, 0.10, 0.3),
    (659.25, 0.10, 0.35),
    (783.99, 0.12, 0.4),
    (1046.50, 0.35, 0.45)
])

# Also overwrite the dummy placeholder .mp3 files with valid audio data so existing references don't crash
for name in ["correct", "wrong", "complete"]:
    src = os.path.join(SOUNDS_DIR, f"{name}.wav")
    dst = os.path.join(SOUNDS_DIR, f"{name}.mp3")
    with open(src, 'rb') as f_in, open(dst, 'wb') as f_out:
        f_out.write(f_in.read())
    print(f"Updated {dst}")
