#!/usr/bin/env python3
"""
Merge multiple MP3 files into a single MP3, in the given order.

Usage:
    python merge_mp3.py intro.mp3 middle.mp3 outro.mp3 -o full_demo.mp3
    python merge_mp3.py *.mp3 -o full_demo.mp3

Requires ffmpeg to be installed (e.g. `brew install ffmpeg`).
"""

import argparse
import os
import subprocess
import sys
import tempfile
from pathlib import Path


PAUSE_SECONDS = 1.5


def make_silence(duration: float) -> Path:
    fd, path = tempfile.mkstemp(suffix=".mp3")
    os.close(fd)
    Path(path).unlink()
    silence_path = Path(path)
    result = subprocess.run(
        [
            "ffmpeg", "-y",
            "-f", "lavfi", "-i", "anullsrc=r=44100:cl=stereo",
            "-t", str(duration),
            "-q:a", "2",
            str(silence_path),
        ],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        sys.exit(f"ffmpeg failed to generate silence:\n{result.stderr}")
    return silence_path


def merge(files: list[Path], output_path: Path) -> None:
    silence_path = make_silence(PAUSE_SECONDS)

    # ffmpeg's concat demuxer needs a list file; paths are escaped per
    # its "concat protocol" quoting rules (single quotes doubled).
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".txt", delete=False
    ) as list_file:
        for i, f in enumerate(files):
            if i > 0:
                escaped_silence = str(silence_path.resolve()).replace("'", "'\\''")
                list_file.write(f"file '{escaped_silence}'\n")
            escaped = str(f.resolve()).replace("'", "'\\''")
            list_file.write(f"file '{escaped}'\n")
        list_path = Path(list_file.name)

    try:
        result = subprocess.run(
            [
                "ffmpeg", "-y",
                "-f", "concat", "-safe", "0",
                "-i", str(list_path),
                "-c", "copy",
                str(output_path),
            ],
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            # -c copy can fail if inputs have mismatched formats; fall back
            # to re-encoding, which normalizes everything.
            print("Stream copy failed, re-encoding instead...")
            result = subprocess.run(
                [
                    "ffmpeg", "-y",
                    "-f", "concat", "-safe", "0",
                    "-i", str(list_path),
                    "-c:a", "libmp3lame", "-q:a", "2",
                    str(output_path),
                ],
                capture_output=True,
                text=True,
            )
            if result.returncode != 0:
                sys.exit(f"ffmpeg failed:\n{result.stderr}")
    finally:
        list_path.unlink(missing_ok=True)
        silence_path.unlink(missing_ok=True)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "input_files", nargs="+", type=Path,
        help="MP3 files to merge, in order",
    )
    parser.add_argument(
        "-o", "--output", type=Path, default=Path("merged.mp3"),
        help="Output file (default: merged.mp3)",
    )
    args = parser.parse_args()

    missing = [f for f in args.input_files if not f.exists()]
    if missing:
        sys.exit(f"File(s) not found: {', '.join(str(f) for f in missing)}")

    if len(args.input_files) < 2:
        sys.exit("Provide at least two MP3 files to merge.")

    print(f"Merging {len(args.input_files)} files into {args.output}...")
    merge(args.input_files, args.output)
    print(f"Saved merged audio to {args.output}")


if __name__ == "__main__":
    main()
