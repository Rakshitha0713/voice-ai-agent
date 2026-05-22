from langdetect import detect, DetectorFactory
DetectorFactory.seed = 0  # Makes detection consistent

LANGUAGE_MAP = {
    "en": "english",
    "hi": "hindi",
    "ta": "tamil"
}

def detect_language(text: str) -> str:
    """
    Component 2: Language Detection
    Automatically detects English, Hindi, or Tamil
    """
    if not text or len(text.strip()) < 3:
        return "english"

    try:
        code = detect(text)
        detected = LANGUAGE_MAP.get(code, "english")
        print(f"[LANG] Detected '{code}' → {detected}")
        return detected
    except Exception as e:
        print(f"[LANG] Detection failed: {e}, defaulting to english")
        return "english"