# 📦 Media Compress v1.2
```
CLI tool for compressing media (Image, Video, Audio, GIF, PDF) with color display.
```
# Developer

```
name : @ExProject
```

# Structure

```
Application/
├── main.py
├── compression_result/
└── module/
└── media-compress_v1.2.py
```

# Installation

```
```bash
pip install Pillow
pip install moviepy
pip install pydub
pip install PyPDF2
```

# Usage

```bash
cd Application
python main.py
```

# Select menu [1-6]:
```
Options Type Format
1 Image JPG, JPEG, PNG, WEBP, BMP
2 Video MP4, AVI, MOV, MKV, FLV
3 Audio MP3, WAV, OGG, M4A, FLAC
4 GIF Animated GIF
5 PDF PDF document
6 All Auto-detect all types
0 Exit Quit application
```
# Compression Level
```
Options Level Description
1 Light High quality, small reduction
2 Balanced Recommended for daily use
3 Strong Good compression, decent quality
4 Extreme Maximum compression, lower quality
0 Back Return to media menu
```
# Status Icons
```
Icon Meaning
? Info / prompt / detected
! Warning / error / not found
* Processing / working
✓ Success / done
+ Extra info / added
# Detail / note
```
# Output
```
All compressed results are saved in compression_result/ with the _compressed suffix.
```
# Notes
```
· moviepy for video/GIF requires FFmpeg to be installed.
· PDF compression works best with Ghostscript, falls back to PyPDF2 if unavailable.
· Image quality: 1-100 (smaller = stronger compression).
```
