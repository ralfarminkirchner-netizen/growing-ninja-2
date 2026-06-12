#!/usr/bin/env python3
"""Erzeugt sanfte Platzhalter-Sounds (WAV) fuer "Growing Ninja - First Steps".

Aufruf:  python3 make_audio.py
Schreibt nach: ../assets/audio/

Alles synthetisch (Sinus + Huellkurven), bewusst leise und freundlich.
Spaeter durch richtige Sounds ersetzen (freesound.org, Kenney Audio Pack).
"""
import math
import os
import struct
import wave

SR = 22050
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.normpath(os.path.join(HERE, "..", "assets", "audio"))
os.makedirs(OUT, exist_ok=True)


def write_wav(name, samples):
    peak = max(1e-9, max(abs(s) for s in samples))
    norm = min(1.0, 0.85 / peak)
    with wave.open(os.path.join(OUT, name), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(b"".join(struct.pack("<h", int(s * norm * 32767)) for s in samples))
    print("ok", name, round(len(samples) / SR, 2), "s")


def buf(dur):
    return [0.0] * int(SR * dur)


def add(base, samples, at, gain=1.0):
    i0 = int(at * SR)
    for i, v in enumerate(samples):
        j = i0 + i
        if 0 <= j < len(base):
            base[j] += v * gain


def pluck(freq, dur=0.5, vol=0.5):
    """Weicher Glockenton mit exponentiellem Ausklang."""
    n = int(SR * dur)
    out = []
    for i in range(n):
        t = i / SR
        env = math.exp(-6.0 * t) * min(1.0, i / 40.0)
        s = math.sin(2 * math.pi * freq * t) + 0.35 * math.sin(2 * math.pi * freq * 2 * t)
        out.append(vol * env * s)
    return out


def sweep(f0, f1, dur=0.14, vol=0.5):
    """Froehlicher aufsteigender Huepf-Ton."""
    n = int(SR * dur)
    out = []
    ph = 0.0
    for i in range(n):
        t = i / n
        f = f0 + (f1 - f0) * t
        ph += 2 * math.pi * f / SR
        out.append(vol * math.sin(math.pi * t) * math.sin(ph))
    return out


# Jump: kleiner froehlicher "Boing"
write_wav("jump.wav", sweep(300, 620, 0.14, 0.6))

# Collect: zwei helle Glockentoene
c = buf(0.5)
add(c, pluck(880, 0.3, 0.6), 0.0)
add(c, pluck(1320, 0.35, 0.5), 0.07)
write_wav("collect.wav", c)

# Win: kleines Aufwaerts-Arpeggio
wn = buf(1.7)
for i, f in enumerate([523.25, 659.25, 783.99, 1046.5]):
    add(wn, pluck(f, 0.6, 0.55), i * 0.16)
add(wn, pluck(1318.5, 0.9, 0.4), 0.72)
write_wav("win.wav", wn)

# Ruhige Hintergrundmusik (12.8 s Loop): Pad-Akkorde + Pentatonik-Gloeckchen
DUR = 12.8
m = buf(DUR)
chords = [
    (0.0, [130.81, 196.00, 329.63]),  # C
    (3.2, [110.00, 164.81, 261.63]),  # Am
    (6.4, [87.31, 174.61, 261.63]),   # F
    (9.6, [98.00, 196.00, 293.66]),   # G
]
for start, freqs in chords:
    n = int(3.2 * SR)
    for f in freqs:
        tone = []
        for i in range(n):
            t = i / SR
            env = max(0.0, min(t / 0.8, 1.0, (3.2 - t) / 0.8))
            tone.append(0.10 * env * math.sin(2 * math.pi * f * t))
        add(m, tone, start)
penta = [523.25, 587.33, 659.25, 783.99, 880.0]
pattern = [
    (0.0, 0), (0.8, 2), (1.6, 4), (2.4, 3), (3.2, 1), (4.0, 2), (4.8, 0),
    (6.4, 4), (7.2, 3), (8.0, 2), (8.8, 4), (9.6, 1), (10.4, 2), (11.2, 3), (12.0, 4),
]
for t0, idx in pattern:
    add(m, pluck(penta[idx], 0.7, 0.30), t0)
# Weiche Loop-Kanten gegen Knackser
fade = int(0.05 * SR)
for i in range(fade):
    g = i / fade
    m[i] *= g
    m[-1 - i] *= g
write_wav("music_loop.wav", m)

print("Alle Sounds erzeugt ->", OUT)
