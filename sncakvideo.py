import os
import requests
import subprocess
import speech_recognition as sr
from moviepy.editor import VideoFileClip

def download_snack_video(url, output_path="."):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"}
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            content_type = response.headers.get("Content-Type")
            if "video" in content_type:
                video_filename = os.path.join(output_path, "snack_video.mp4")
                with open(video_filename, "wb") as file:
                    file.write(response.content)
                print("Downloaded Snack Video.")
                return video_filename
            else:
                print("The URL does not point to a video (wrong content type).")
        else:
            print("Failed to download Snack Video. Status Code:", response.status_code)
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def convert_video_to_audio(video_file, audio_output_file):
    try:
        video = VideoFileClip(video_file)
        audio = video.audio
        audio.write_audiofile(audio_output_file)
        print("Video converted to audio.")
    except Exception as e:
        print(f"An error occurred: {e}")

def clean_filename(filename):
    forbidden_chars = r'<>:"/\|?*'  # Karakter yang tidak diizinkan dalam nama file
    cleaned_filename = "".join([char for char in filename if char not in forbidden_chars])
    return cleaned_filename

def convert_audio_to_text(audio_file, lang):
    r = sr.Recognizer()
    all_text = []

    with sr.AudioFile(audio_file) as source:
        print("Fetching audio...")
        audio_text = r.listen(source)
        try:
            print("Converting audio to text...")
            text = r.recognize_google(audio_text, language=lang)
            all_text.append(text)
        except sr.UnknownValueError:
            print("Speech Recognition could not understand audio")
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")

    return all_text

if __name__ == "__main__":
    snack_video_url = "https://cloudflare-sgp-cdn.snackvideo.in/upic/2023/06/16/21/BMjAyMzA2MTYyMTUwMjRfMTUwMDAxMTgwNzQ0NjY3XzE1MDEwMzIxMzI5OTUzMl8yXzM=_b_B0598a28e0389abd536b311c4042e1744.mp4?tag=1-1694067990-s-0-retqnnx0de-6b52ba39ce2bba83"
    output_path = "downloaded_snack_video"
    lang = "id"

    if not os.path.exists(output_path):
        os.makedirs(output_path)

    video_filename = download_snack_video(snack_video_url, output_path)
    if video_filename:
        cleaned_video_title = clean_filename(os.path.basename(video_filename))
        audio_file = os.path.join(output_path, f"{cleaned_video_title}.wav")

        print("Video downloaded, now converting to audio...")
        convert_video_to_audio(video_filename, audio_file)

        text_output_path = "snack_video_text"  # Direktori untuk menyimpan teks
        if not os.path.exists(text_output_path):
            os.makedirs(text_output_path)  # Buat direktori jika belum ada

        print("Audio conversion completed, now converting to text...")
        text_result = convert_audio_to_text(audio_file, lang)

        if text_result:
            output_text_file = os.path.join(text_output_path, f"{cleaned_video_title}.txt")
            with open(output_text_file, "w") as txt_file:
                txt_file.write("\n".join(text_result))

            print(f"Converted text saved to {output_text_file}")
        else:
            print("No text to save.")