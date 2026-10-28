"""
LLM Service Module for Multi-Agent Travel Planner.
Provides a unified, modular interface for calling LLM APIs (Google Gemini, OpenAI).
Includes graceful error handling and fallback detection.
"""

import os
import json
import requests
from dotenv import load_dotenv

# Load variables from .env file if available
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "").strip()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "").strip()

def get_llm_status():
    """
    Check if any LLM API key is configured.
    Returns: (is_configured: bool, provider_name: str)
    """
    if GEMINI_API_KEY:
        return True, "Google Gemini"
    elif OPENAI_API_KEY:
        return True, "OpenAI GPT"
    return False, "Intelligent Rule Engine (Offline/Fallback)"


def query_llm(prompt, system_instruction=None, json_format=True, timeout=12):
    """
    Execute a prompt against the configured LLM API.
    Returns the string response or parsed JSON, or None if unavailable/failed.
    """
    # 1. Try Google Gemini API
    if GEMINI_API_KEY:
        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
            contents = []
            if system_instruction:
                contents.append({"role": "user", "parts": [{"text": f"SYSTEM INSTRUCTION: {system_instruction}"}]})
                contents.append({"role": "model", "parts": [{"text": "Understood. I will strictly follow the instructions."}]})
            contents.append({"role": "user", "parts": [{"text": prompt}]})

            payload = {
                "contents": contents,
                "generationConfig": {
                    "temperature": 0.4,
                    "maxOutputTokens": 2048,
                }
            }
            if json_format:
                payload["generationConfig"]["responseMimeType"] = "application/json"

            headers = {"Content-Type": "application/json"}
            response = requests.post(url, headers=headers, json=payload, timeout=timeout)
            
            if response.status_code == 200:
                data = response.json()
                text_content = data["candidates"][0]["content"]["parts"][0]["text"]
                if json_format:
                    clean_text = text_content.strip()
                    if clean_text.startswith("```json"):
                        clean_text = clean_text[7:]
                    if clean_text.startswith("```"):
                        clean_text = clean_text[3:]
                    if clean_text.endswith("```"):
                        clean_text = clean_text[:-3]
                    return json.loads(clean_text.strip())
                return text_content
        except Exception as e:
            print(f"[LLM Service Warning] Gemini API call failed: {e}. Falling back to rule engine.")

    # 2. Try OpenAI API
    if OPENAI_API_KEY:
        try:
            url = "https://api.openai.com/v1/chat/completions"
            messages = []
            if system_instruction:
                messages.append({"role": "system", "content": system_instruction})
            messages.append({"role": "user", "content": prompt})

            payload = {
                "model": "gpt-4o-mini",
                "messages": messages,
                "temperature": 0.4,
            }
            if json_format:
                payload["response_format"] = {"type": "json_object"}

            headers = {
                "Authorization": f"Bearer {OPENAI_API_KEY}",
                "Content-Type": "application/json"
            }
            response = requests.post(url, headers=headers, json=payload, timeout=timeout)
            if response.status_code == 200:
                data = response.json()
                text_content = data["choices"][0]["message"]["content"]
                if json_format:
                    return json.loads(text_content)
                return text_content
        except Exception as e:
            print(f"[LLM Service Warning] OpenAI API call failed: {e}. Falling back to rule engine.")

    # If no API key or failed, return None to trigger domain fallback
    return None
