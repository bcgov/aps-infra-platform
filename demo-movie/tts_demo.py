#!/usr/bin/env python3
"""
Convert a text file to speech using the OpenAI TTS API and save it as an
MP3 file that can be dropped straight into iMovie.

Usage:
    python tts_demo.py script.txt
    python tts_demo.py script.txt -o narration.mp3 --voice nova

Requires:
    pip install openai
    export OPENAI_API_KEY=sk-...
"""

import argparse
import sys
from pathlib import Path

from openai import OpenAI

# Voices well suited to a confident, friendly product-demo tone.
# (Full list from OpenAI: alloy, ash, ballad, coral, echo, fable,
#  nova, onyx, sage, shimmer, verse)
DEMO_FRIENDLY_VOICES = ["nova", "shimmer", "onyx", "alloy", "ash", "coral", "echo", "fable", "verse"]

# The API rejects input over this many characters, so long scripts are
# split on sentence/paragraph boundaries and the resulting MP3 chunks
# are concatenated.
MAX_CHARS = 4000


def chunk_text(text: str, max_chars: int = MAX_CHARS) -> list[str]:
    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
    chunks: list[str] = []
    current = ""

    for para in paragraphs:
        candidate = f"{current}\n\n{para}" if current else para
        if len(candidate) <= max_chars:
            current = candidate
            continue

        if current:
            chunks.append(current)
            current = ""

        if len(para) <= max_chars:
            current = para
            continue

        # A single paragraph is itself too long; split on sentences.
        sentence = ""
        for word in para.split(" "):
            candidate = f"{sentence} {word}".strip()
            if len(candidate) <= max_chars:
                sentence = candidate
            else:
                chunks.append(sentence)
                sentence = word
        if sentence:
            current = sentence

    if current:
        chunks.append(current)

    return chunks


def synthesize(
    client: OpenAI,
    text: str,
    voice: str,
    model: str,
    output_path: Path,
) -> None:
    chunks = chunk_text(text)

    if len(chunks) == 1:
        with client.audio.speech.with_streaming_response.create(
            model=model,
            voice=voice,
            input=chunks[0],
            response_format="mp3",
        ) as response:
            response.stream_to_file(output_path)
        return

    print(f"Text is long; splitting into {len(chunks)} chunks...")
    with open(output_path, "wb") as out_file:
        for i, chunk in enumerate(chunks, start=1):
            print(f"  synthesizing chunk {i}/{len(chunks)}...")
            with client.audio.speech.with_streaming_response.create(
                model=model,
                voice=voice,
                input=chunk,
                response_format="mp3",
            ) as response:
                out_file.write(response.read())


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input_file", type=Path, help="Path to a .txt file with the script")
    parser.add_argument(
        "-o", "--output", type=Path, default=None,
        help="Output audio file (default: <input_file>.mp3). Use .mp3 or .wav for iMovie.",
    )
    parser.add_argument(
        "--voice", default="nova", choices=DEMO_FRIENDLY_VOICES,
        help="TTS voice (default: nova - clear and upbeat, good for demos)",
    )
    parser.add_argument(
        "--model", default="gpt-4o-mini-tts",
        help="OpenAI TTS model (default: gpt-4o-mini-tts)",
    )
    args = parser.parse_args()

    if not args.input_file.exists():
        sys.exit(f"Input file not found: {args.input_file}")

    text = args.input_file.read_text(encoding="utf-8").strip()
    if not text:
        sys.exit("Input file is empty.")

    output_path = args.output or args.input_file.with_suffix(".mp3")

    client = OpenAI()  # reads OPENAI_API_KEY from the environment

    print(f"Generating speech with voice '{args.voice}'...")
    synthesize(client, text, args.voice, args.model, output_path)
    print(f"Saved audio to {output_path} (ready to import into iMovie)")


if __name__ == "__main__":
    main()
