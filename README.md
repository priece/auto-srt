# Video Auto Subtitle Generation System

## Project Overview

This is a Python-based automatic video subtitle generation system that implements subtitle creation through the following steps:
1. Extract audio from video files
2. Call Volcano Engine Large Model Audio Transcription API
3. Automatically generate standard SRT format subtitle files

## Requirements

- **Input**: Video file, path: `./data/sample.mp4`
- **Output**: Subtitle file, save path: `./data/sample.srt`
- **Implementation Language**: Python
- **Core Functions**: Video audio extraction + Volcano Engine API call + SRT subtitle generation
- **API Credentials**: Read Volcano Engine API Key and Access Key from `.env` file

## Technology Stack

- **Python 3.x**
- **FFmpeg**: For video audio extraction
- **Python Dependencies**:
  - `python-dotenv`: Environment variable management
  - `requests`: HTTP request handling
- **Volcano Engine Large Model Audio Transcription API**: For audio-to-text conversion

## Installation Steps

1. **Clone or download the project**
   ```bash
   cd ./auto-srt
   ```

2. **Install Python dependencies**
   ```bash
   pip install python-dotenv requests
   ```

3. **Install FFmpeg**
   - Windows: Download FFmpeg and add it to the system PATH
   - macOS: `brew install ffmpeg`
   - Linux: `sudo apt-get install ffmpeg`

## Configuration

1. **Create and configure .env file**
   ```bash
   cp .env.example .env  # If there is an example file
   ```
   Edit the `.env` file and fill in the Volcano Engine API credentials:
   ```env
   # Volcano Engine API Credentials
   APP_ID=your_app_id_here
   ACCESS_KEY=your_access_key_here
   ```

2. **Prepare video files**
   Name the video file for which you want to generate subtitles as `sample.mp4` and place it in the `./auto-srt/data/` directory

## Usage

### 1. Full Mode (requires FFmpeg and API credentials)

```bash
python auto_srt.py
```

### 2. Mock Mode (no FFmpeg and API calls required, for testing)

```bash
python auto_srt.py --mock
# or
python auto_srt.py -m
```

Mock mode generates sample SRT files for verifying subtitle format and flow

## Project Structure

```
./auto-srt/
├── auto_srt.py          # Main program entry, controls overall flow
├── README.md            # Project documentation (English)
├── README_zh_CN.md      # Project documentation (Chinese)
├── .env                 # Environment variable configuration file
├── data/                # Data directory
│   ├── sample.mp4       # Input video file
│   ├── sample.mp3       # Extracted audio file
│   └── sample.srt       # Generated subtitle file
├── modules/             # Core function modules
│   ├── __init__.py      # Package initialization file
│   ├── audio_extractor.py  # Audio extraction module
│   ├── volcano_api.py     # Volcano Engine API interaction module
│   └── srt_generator.py   # SRT subtitle generation module
```

## Workflow

1. **Audio Extraction**: Use FFmpeg to extract audio from video, save as MP3 format, and automatically convert to mono channel
2. **API Call** (using Volcano Engine Fast API):
   - Directly read local audio files and convert to Base64 encoding
   - Call Volcano Engine API to submit audio transcription task, directly upload Base64 data
   - Poll the API to get transcription results until the task is completed
   - Extract transcribed text and corresponding timestamp information
3. **SRT Generation**: Convert the API response transcription results into standard SRT format subtitle files with correct timestamps and text content
4. **Result Output**: Print Token usage statistics (input tokens, output tokens, total tokens) and display the generated subtitle file path

## Core Module Description

### AudioExtractor Class
- Check if FFmpeg is installed in the system
- Use FFmpeg to extract audio from video

### VolcanoEngineAPI Class
- Handle interaction with Volcano Engine API
- Submit audio transcription tasks
- Poll for transcription results

### SRTGenerator Class
- Convert API response to SRT format
- Generate standard subtitle files

## Notes

1. **API Call Method**
   - Current code uses Volcano Engine Fast API, directly uploading Base64 encoded audio data without cloud storage
   - Fast API responds faster than Standard API but may have functional limitations
   - API calls use HTTPS protocol to ensure data transmission security

2. **Timestamp Processing**
   - The system has fixed the issue of incorrect timestamp for the first subtitle in SRT files
   - The timestamp unit returned by Volcano Engine API is milliseconds, and the code directly uses this timestamp to generate SRT format
   - Timestamp format: `HH:MM:SS,mmm` (e.g., `00:00:00,290` means 0 hours, 0 minutes, 0 seconds, 290 milliseconds)

3. **API Credentials**
   - Ensure that APP_ID and ACCESS_KEY in the `.env` file are valid
   - Credentials can be obtained from the Volcano Engine console
   - Mock mode (`--mock` or `-m` parameter) can be used to test functionality without valid credentials

4. **FFmpeg Dependency**
   - FFmpeg must be installed in full mode
   - Check if it is installed by running `ffmpeg -version`
   - The code has handled the issue of the program getting stuck after FFmpeg execution in Windows environment

5. **Mock Mode**
   - Mock mode is only used to test SRT generation functionality and program flow
   - The generated subtitle content is a fixed example, not real video content
   - Mock mode simulates token usage statistics

6. **Audio Processing**
   - The code defaults to converting extracted audio to **mono channel** to avoid subtitle duplication caused by stereo channels
   - If Volcano Engine API receives stereo audio, there will be two subtitles for two channels
   - You can adjust the channel settings by modifying the `-ac` parameter in `./auto-srt/modules/audio_extractor.py`

7. **Token Usage Statistics**
   - The program prints the token usage of API calls
   - Including: input tokens, output tokens, total tokens
   - Token usage is related to audio duration and content complexity

## Sample Output

Generated SRT file format example:
```srt
1
00:00:00,000 --> 00:00:02,000
This is the first test subtitle.

2
00:00:02,000 --> 00:00:05,000
This is the second test subtitle, used to demonstrate SRT generation functionality.

3
00:00:05,000 --> 00:00:08,000
This is the third test subtitle, containing multiple lines of content.
```

## Reference Documentation

- [Volcano Engine Large Model Audio Transcription API Documentation](https://www.volcengine.com/docs/6561/1354868)
- [FFmpeg Official Documentation](https://ffmpeg.org/documentation.html)
- [Python base64 Module Documentation](https://docs.python.org/3/library/base64.html)
- [requests Library Official Documentation](https://docs.python-requests.org/en/latest/)

## Changelog

### [Latest Version]
- **Fixed**: Incorrect timestamp for the first subtitle in SRT files (original incorrect timestamps like `00:04:50,000 --> 01:28:10,000`)
- **Optimized**: Set audio extraction to mono channel by default to avoid subtitle duplication caused by stereo channels
- **Improved**: Handled the issue of the program getting stuck after FFmpeg execution in Windows environment
- **Added**: Print token usage statistics (input tokens, output tokens, total tokens)
- **Upgraded**: Use Volcano Engine Fast API, directly upload Base64 encoded audio data without cloud storage
- **Refactored**: Adopt modular design, split the code into three core modules: audio extraction, API call, and SRT generation

## License

This project is for learning and reference purposes only.