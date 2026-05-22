import time
import os
from dotenv import load_dotenv

load_dotenv()

ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")

def synthesize_speech(text: str, language: str = "english") -> dict:
    """
    Component 5: Text-to-Speech
    Converts agent text response to audio bytes
    Uses ElevenLabs multilingual model
    """
    start = time.time()

    try:
        from elevenlabs.client import ElevenLabs
        client = ElevenLabs(api_key=ELEVENLABS_API_KEY)

        audio_generator = client.generate(
            text=text,
            voice="Rachel",
            model="eleven_multilingual_v2"
        )
        audio_bytes = b"".join(audio_generator)

    except Exception as e:
        print(f"[TTS] ElevenLabs failed: {e}, using fallback")
        # Fallback: use gTTS (free, no API key needed)
        audio_bytes = fallback_tts(text, language)

    elapsed = (time.time() - start) * 1000
    print(f"[TTS] Synthesized in {round(elapsed)}ms")

    return {
        "audio": audio_bytes,
        "tts_latency_ms": round(elapsed, 2)
    }


def fallback_tts(text: str, language: str) -> bytes:
    """
    Fallback TTS using gTTS (free, works offline)
    Install with: pip install gtts
    """
    try:
        from gtts import gTTS
        import tempfile

        lang_map = {
            "english": "en",
            "hindi": "hi",
            "tamil": "ta"
        }
        lang_code = lang_map.get(language, "en")

        tts = gTTS(text=text, lang=lang_code, slow=False)
        tmp_path = os.path.join(
            tempfile.gettempdir(),
            f"tts_{int(time.time())}.mp3"
        )
        tts.save(tmp_path)

        with open(tmp_path, "rb") as f:
            audio_bytes = f.read()

        os.remove(tmp_path)
        return audio_bytes

    except Exception as e:
        print(f"[TTS] Fallback also failed: {e}")
        return b""