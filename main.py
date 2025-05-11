from google.cloud import speech
import pyaudio
import difflib
import os
from commands import COMMAND_MAP
from robot_state_machine import RobotStateMachine

# Set Google credentials (in case not done via terminal)
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "key.json"

# Audio configuration
RATE = 16000
CHUNK = int(RATE / 10)

def record_audio(seconds=4):
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16,
                    channels=1,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    print("🎧 Listening...")
    frames = []

    for _ in range(0, int(RATE / CHUNK * seconds)):
        data = stream.read(CHUNK)
        frames.append(data)

    stream.stop_stream()
    stream.close()
    p.terminate()

    return b''.join(frames)

def recognize_speech(audio_data):
    client = speech.SpeechClient()
    audio = speech.RecognitionAudio(content=audio_data)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=RATE,
        language_code="en-US"
    )

    response = client.recognize(config=config, audio=audio)
    for result in response.results:
        return result.alternatives[0].transcript.lower()
    return ""

def interpret_command(command):
    for key, variants in COMMAND_MAP.items():
        if command in variants or difflib.get_close_matches(command, variants, n=1, cutoff=0.8):
            return key
    return None

def main():
    robot = RobotStateMachine()
    print("🗣️ Say a command (e.g., 'move up', 'grip', 'release') or 'exit' to stop.")

    while True:
        audio_data = record_audio()
        text = recognize_speech(audio_data)
        print(f"✅ You said: {text}")

        if text == "exit":
            print("👋 Exiting program.")
            break

        cmd = interpret_command(text)
        if cmd:
            robot.transition(cmd)
        else:
            print("⚠️ Could not understand that command.")

if __name__ == "__main__":
    main()
