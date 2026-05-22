import openai
import json
import re
import time
import os
from dotenv import load_dotenv
from agent.prompt.system_prompt import SYSTEM_PROMPT
from agent.tools.appointment_tools import execute_tool
from memory.session_memory import get_session, update_session

load_dotenv()
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def run_agent(
    session_id: str,
    patient_id: str,
    user_text: str,
    language: str
) -> dict:
    """
    Component 3 + 4: LLM Agent + Tool Orchestration
    - Understands patient intent
    - Calls appointment tools
    - Returns response in correct language
    """
    start = time.time()

    # Load conversation history from Redis session memory
    session = get_session(session_id)
    history = session.get("history", [])

    # Add user message to history
    history.append({
        "role": "user",
        "content": user_text
    })

    # Build messages for LLM
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT}
    ] + history

    print(f"[AGENT] Processing: '{user_text}' in {language}")

    try:
        # First LLM call — understand intent
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            temperature=0.3,
            max_tokens=500
        )

        reply = response.choices[0].message.content
        agent_latency = (time.time() - start) * 1000
        tool_result = None

        # Check if agent wants to call a tool
        tool_match = re.search(
            r"<tool_call>(.*?)</tool_call>",
            reply,
            re.DOTALL
        )

        if tool_match:
            print(f"[AGENT] Tool call detected")
            try:
                tool_data = json.loads(tool_match.group(1).strip())
                tool_data["args"]["patient_id"] = patient_id

                # Execute the tool
                tool_result = execute_tool(
                    tool_data["tool"],
                    tool_data["args"]
                )
                print(f"[TOOL] Result: {tool_result}")

                # Feed tool result back to LLM
                history.append({
                    "role": "assistant",
                    "content": reply
                })
                history.append({
                    "role": "user",
                    "content": f"Tool result: {tool_result}. Now respond to the patient in {language}."
                })

                messages = [
                    {"role": "system", "content": SYSTEM_PROMPT}
                ] + history

                # Second LLM call — generate final response
                response2 = client.chat.completions.create(
                    model="gpt-4o",
                    messages=messages,
                    temperature=0.3,
                    max_tokens=300
                )
                reply = response2.choices[0].message.content

            except Exception as e:
                print(f"[AGENT] Tool execution error: {e}")
                reply = "I had trouble processing that request. Could you please repeat?"

    except Exception as e:
        print(f"[AGENT] LLM error: {e}")
        reply = "I'm having trouble connecting. Please try again."
        agent_latency = (time.time() - start) * 1000

    # Save updated history to Redis (keep last 10 turns)
    history.append({"role": "assistant", "content": reply})
    update_session(session_id, {
        "history": history[-10:],
        "language": language
    })

    print(f"[AGENT] Response: '{reply}' in {round(agent_latency)}ms")

    return {
        "response_text": reply,
        "tool_result": tool_result,
        "agent_latency_ms": round(agent_latency, 2)
    }