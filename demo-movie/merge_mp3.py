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


def probe_format(path: Path) -> tuple[int, int]:
    """Return (sample_rate, channels) of an audio file's first stream."""
    result = subprocess.run(
        [
            "ffprobe", "-v", "error",
            "-select_streams", "a:0",
            "-show_entries", "stream=sample_rate,channels",
            "-of", "csv=p=0",
            str(path),
        ],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        sys.exit(f"ffprobe failed on {path}:\n{result.stderr}")
    sample_rate, channels = result.stdout.strip().split(",")
    return int(sample_rate), int(channels)


def make_silence(duration: float, sample_rate: int, channels: int) -> Path:
    # Matching the narration's sample rate/channel layout avoids a mid-stream
    # format change: mp3 has no single global header, so splicing in audio
    # with different params breaks decoders that lock onto the first frame's
    # format (many players stop playback there, even though ffmpeg itself
    # tolerates it).
    layout = "mono" if channels == 1 else "stereo"
    fd, path = tempfile.mkstemp(suffix=".mp3")
    os.close(fd)
    Path(path).unlink()
    silence_path = Path(path)
    result = subprocess.run(
        [
            "ffmpeg", "-y",
            "-f", "lavfi", "-i", f"anullsrc=r={sample_rate}:cl={layout}",
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
    sample_rate, channels = probe_format(files[0])
    silence_path = make_silence(PAUSE_SECONDS, sample_rate, channels)

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
        # Always re-encode: the inserted silence clip's format may not match
        # every input's sample rate/channel layout, and ffmpeg's concat
        # demuxer will happily stream-copy (-c copy) mismatched formats
        # together without erroring. The resulting file decodes fine in
        # ffmpeg but many players lock onto the first frame's format and
        # stop playback the moment it changes mid-stream.
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
