#!/usr/bin/env python3
"""
extract_segment.py - Download a specific time segment from a YouTube video.

Uses yt-dlp + ffmpeg to fetch only the requested portion of a video,
instead of downloading the whole thing.

Example:
    python extract_segment.py https://youtu.be/z6ahRMyRumY --start 9:44 --end 14:57

Requirements:
    pip install yt-dlp
    ffmpeg must be installed and available on PATH
"""
import argparse
import shutil
import subprocess
import sys


def parse_timestamp(value):
    """Parse 'SS', 'MM:SS', or 'HH:MM:SS' into total seconds."""
    parts = value.strip().split(":")
    if not 1 <= len(parts) <= 3:
        raise argparse.ArgumentTypeError(f"Invalid timestamp: {value!r}")
    try:
        nums = [float(p) for p in parts]
    except ValueError:
        raise argparse.ArgumentTypeError(f"Invalid timestamp: {value!r}")
    seconds = 0.0
    for n in nums:
        seconds = seconds * 60 + n
    return seconds


def format_timestamp(seconds):
    """Format seconds as HH:MM:SS."""
    total = int(round(seconds))
    h, rem = divmod(total, 3600)
    m, s = divmod(rem, 60)
    return f"{h:02d}:{m:02d}:{s:02d}"


def check_dependencies():
    """Exit with a helpful message if yt-dlp or ffmpeg are missing."""
    missing = []
    if shutil.which("yt-dlp") is None:
        missing.append("yt-dlp  -> install with: pip install yt-dlp")
    if shutil.which("ffmpeg") is None:
        missing.append("ffmpeg  -> install via your OS package manager (e.g. apt install ffmpeg)")
    if missing:
        print("Missing required tools:")
        for m in missing:
            print(f"   - {m}")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description="Download a time segment from a YouTube video."
    )
    parser.add_argument("url", help="YouTube video URL")
    parser.add_argument(
        "--start", required=True, type=parse_timestamp,
        help="Start time as SS, MM:SS, or HH:MM:SS",
    )
    parser.add_argument(
        "--end", required=True, type=parse_timestamp,
        help="End time as SS, MM:SS, or HH:MM:SS",
    )
    parser.add_argument(
        "-o", "--output", default="segment.%(ext)s",
        help="Output filename template (default: segment.%%(ext)s)",
    )
    args = parser.parse_args()

    if args.end <= args.start:
        print("--end must be greater than --start")
        sys.exit(1)

    check_dependencies()

    start = format_timestamp(args.start)
    end = format_timestamp(args.end)
    section = f"*{start}-{end}"

    cmd = [
        "yt-dlp",
        "--download-sections", section,
        "--force-keyframes-at-cuts",
        "-f", "bestvideo+bestaudio/best",
        "--remux-video", "mp4",
        "-o", args.output,
        args.url,
    ]

    print(f"Extracting {start} -> {end} from {args.url}")
    print("Running: " + " ".join(cmd))
    result = subprocess.run(cmd)
    if result.returncode != 0:
        print("yt-dlp failed")
        sys.exit(result.returncode)
    print("Done")


if __name__ == "__main__":
    main()
