import os
import time
import tempfile
import subprocess
from dotenv import load_dotenv
load_dotenv()


def convert_webm_to_wav(webm_path: str) -> str:
    wav_path = webm_path.replace(".webm", ".wav")
    try:
        from pydub import AudioSegment
        audio = AudioSegment.from_file(webm_path)
        audio = audio.set_frame_rate(16000).set_channels(1)
        audio.export(wav_path, format="wav")
        print(f"[STT] Converted to WAV: {wav_path}")
        return wav_path
    except Exception as e:
        print(f"[STT] Conversion error: {e}")
        return None


def transcribe_audio(audio_data, language: str = None) -> dict:
    start = time.time()

    if isinstance(audio_data, bytes):
        audio_bytes = audio_data
    else:
        audio_bytes = audio_data.read()

    if len(audio_bytes) < 500:
        return {"text": "", "stt_latency_ms": 0}

    print(f"[STT] Received {len(audio_bytes)} bytes")

    tmp_webm = os.path.join(
        tempfile.gettempdir(),
        f"stt_{int(time.time())}.webm"
    )

    with open(tmp_webm, "wb") as f:
        f.write(audio_bytes)

    text = ""

    try:
        # METHOD 1: Try OpenAI Whisper
        api_key = os.getenv("OPENAI_API_KEY")
        if api_key and api_key != "your_openai_api_key_here":
            try:
                import openai
                client = openai.OpenAI(api_key=api_key)
                with open(tmp_webm, "rb") as af:
                    result = client.audio.transcriptions.create(
                        model="whisper-1",
                        file=af,
                        response_format="text"
                    )
                text = result if isinstance(result, str) else result.text
                print(f"[STT-Whisper] '{text}'")
            except Exception as e:
                print(f"[STT-Whisper] Failed ({e}), trying Google...")

        # METHOD 2: Free Google Speech Recognition
        if not text:
            import speech_recognition as sr

            wav_path = convert_webm_to_wav(tmp_webm)

            if wav_path and os.path.exists(wav_path):
                recognizer = sr.Recognizer()
                lang_map = {
                    "hindi": "hi-IN",
                    "tamil": "ta-IN",
                    "english": "en-US",
                    None: "en-US"
                }
                lang_code = lang_map.get(language, "en-US")

                try:
                    with sr.AudioFile(wav_path) as source:
                        recognizer.adjust_for_ambient_noise(source)
                        audio = recognizer.record(source)

                    text = recognizer.recognize_google(
                        audio,
                        language=lang_code
                    )
                    print(f"[STT-Google] '{text}'")

                except sr.UnknownValueError:
                    print("[STT-Google] Could not understand audio")
                    text = ""
                except sr.RequestError as e:
                    print(f"[STT-Google] Request error: {e}")
                    text = ""

    finally:
        for path in [tmp_webm,
                     tmp_webm.replace(".webm", ".wav")]:
            if path and os.path.exists(path):
                try:
                    os.remove(path)
                except:
                    pass

    elapsed = (time.time() - start) * 1000
    print(f"[STT] Final: '{text}' | {round(elapsed)}ms")

    return {
        "text": text,
        "stt_latency_ms": round(elapsed, 2)
    }