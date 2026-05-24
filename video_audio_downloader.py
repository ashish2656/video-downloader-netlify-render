#!/usr/bin/env python3
"""
Instagram & YouTube Video/Audio Downloader
Downloads videos from Instagram and YouTube in highest quality possible
Allows user to choose: video only, audio only, or both
"""

import yt_dlp
import os
import sys


def get_user_choice():
    """Ask user what they want to download"""
    print("\n" + "="*50)
    print("What would you like to download?")
    print("="*50)
    print("1. Video only (highest quality)")
    print("2. Audio only (MP3)")
    print("3. Both video and audio")
    print("="*50)
    
    while True:
        choice = input("Enter your choice (1, 2, or 3): ").strip()
        if choice in ['1', '2', '3']:
            return choice
        print("Invalid choice. Please enter 1, 2, or 3.")


def get_output_format(choice):
    """Return yt-dlp format string based on user choice"""
    if choice == '1':
        # Video only - best quality
        return {
            'format': 'bestvideo[ext=mp4]/best[ext=mp4]/best',
            'postprocessors': []
        }
    elif choice == '2':
        # Audio only - MP3
        return {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }]
        }
    else:  # choice == '3'
        # Both video and audio
        return {
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/bestvideo+bestaudio/best',
            'postprocessors': []
        }


def download_media(url, choice):
    """Download media from the provided URL"""
    
    print("\n" + "="*50)
    print("Starting download...")
    print("="*50 + "\n")
    
    format_config = get_output_format(choice)
    
    # Create output directory if it doesn't exist
    output_dir = os.path.expanduser("~/Downloads/Videos")
    os.makedirs(output_dir, exist_ok=True)
    
    # Configure yt-dlp options
    ydl_opts = {
        'format': format_config['format'],
        'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),
        'quiet': False,
        'no_warnings': False,
        'socket_timeout': 30,
        'postprocessors': format_config['postprocessors'],
        'merge_output_format': 'mp4',
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            print(f"URL: {url}")
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            print("\n" + "="*50)
            print(f"✓ Download completed successfully!")
            print(f"File saved to: {filename}")
            print("="*50 + "\n")
            return True
    
    except yt_dlp.utils.DownloadError as e:
        print(f"\n✗ Download Error: {e}")
        print("Make sure the URL is correct and the video is publicly available.")
        return False
    except Exception as e:
        print(f"\n✗ Error occurred: {e}")
        return False


def main():
    """Main function"""
    print("\n")
    print("╔════════════════════════════════════════════════════╗")
    print("║   Instagram & YouTube Video/Audio Downloader      ║")
    print("╚════════════════════════════════════════════════════╝")
    
    try:
        while True:
            # Get URL from user
            url = input("\n📎 Paste the Instagram/YouTube link (or 'q' to quit): ").strip()
            
            if url.lower() == 'q':
                print("\nGoodbye! 👋\n")
                break
            
            if not url:
                print("Please provide a valid URL.")
                continue
            
            # Validate URL
            if 'instagram.com' not in url and 'youtube.com' not in url and 'youtu.be' not in url:
                print("⚠️  Please provide an Instagram or YouTube link.")
                continue
            
            # Get user choice
            choice = get_user_choice()
            
            # Download
            success = download_media(url, choice)
            
            if not success:
                print("Would you like to try again? (y/n): ", end="")
                if input().lower() != 'y':
                    break
    
    except KeyboardInterrupt:
        print("\n\nDownload cancelled by user. Goodbye! 👋\n")
        sys.exit(0)


if __name__ == "__main__":
    main()
