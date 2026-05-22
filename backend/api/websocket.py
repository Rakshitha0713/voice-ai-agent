import os
import sys
sys.path.insert(0, os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
))

from fastapi import WebSocket, WebSocketDisconnect
import json
import time
import uuid
import tempfile
from dotenv import load_dotenv
load_dotenv()


async def voice_ws_endpoint(websocket: WebSocket):
    await websocket.accept()
    session_id = str(uuid.uuid4())
    patient_id = "patient_001"

    print(f"\n[WS] New session: {session_id}")

    await websocket.send_text(json.dumps({
        "type": "connected",
        "message": "Connected to 2Care.ai"
    }))

    try:
        while True:
            data = await websocket.receive_bytes()
            pipeline_start = time.time()

            print(f"[PIPELINE] Audio received, processing...")

            # Save audio to temp file
            tmp_path = os.path.join(
                tempfile.gettempdir(),
                f"voice_{session_id}.webm"
            )
            with open(tmp_path, "wb") as f:
                f.write(data)

            # STEP 1: Speech to Text
            try:
                from services.speech_to_text import transcribe_audio
                stt_result = transcribe_audio(data)
                user_text = stt_result["text"].strip()
                stt_latency = stt_result["stt_latency_ms"]
                print(f"[STT] '{user_text}' | {stt_latency}ms")

                if not user_text:
                    await websocket.send_text(json.dumps({
                        "type": "error",
                        "message": "No speech detected. Speak clearly and try again."
                    }))
                    continue

            except Exception as e:
                error_msg = str(e)
                print(f"[STT ERROR] {error_msg}")
                await websocket.send_text(json.dumps({
                    "type": "error",
                    "message": f"Speech error: {error_msg}"
                }))
                continue

            # STEP 2: Language Detection
            try:
                from services.language_detection import detect_language
                language = detect_language(user_text)
                print(f"[LANG] {language}")
            except Exception as e:
                print(f"[LANG ERROR] {e}")
                language = "english"

            # STEP 3: AI Agent
            try:
                from agent.reasoning.agent import run_agent
                agent_result = run_agent(
                    session_id, patient_id, user_text, language
                )
                response_text = agent_result["response_text"]
                agent_latency = agent_result["agent_latency_ms"]
                print(f"[AGENT] '{response_text}' | {agent_latency}ms")
            except Exception as e:
                print(f"[AGENT ERROR] {e}")
                response_text = "I had trouble processing that. Please try again."
                agent_latency = 0

            # STEP 4: Text to Speech
            try:
                from services.text_to_speech import synthesize_speech
                tts_result = synthesize_speech(response_text, language)
                audio_bytes = tts_result["audio"]
                tts_latency = tts_result["tts_latency_ms"]
                print(f"[TTS] {tts_latency}ms")
            except Exception as e:
                print(f"[TTS ERROR] {e}")
                audio_bytes = b""
                tts_latency = 0

            # Calculate total latency
            total_latency = (time.time() - pipeline_start) * 1000
            status = "PASS" if total_latency < 450 else "SLOW"
            print(f"[LATENCY] STT:{stt_latency}ms | Agent:{agent_latency}ms | TTS:{tts_latency}ms | Total:{round(total_latency)}ms | {status}")

            # Send text response
            await websocket.send_text(json.dumps({
                "type": "response",
                "transcript": user_text,
                "response": response_text,
                "language": language,
                "latency": {
                    "stt_ms": stt_latency,
                    "agent_ms": agent_latency,
                    "tts_ms": tts_latency,
                    "total_ms": round(total_latency, 2)
                }
            }))

            # Send audio
            if audio_bytes:
                await websocket.send_bytes(audio_bytes)

    except WebSocketDisconnect:
        print(f"[WS] Session {session_id} ended")
    except Exception as e:
        print(f"[WS ERROR] {e}")