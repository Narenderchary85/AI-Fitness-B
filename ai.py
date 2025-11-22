import os
import requests
import json
from dotenv import load_dotenv
from gtts import gTTS
import io


load_dotenv()
PPLX_API_KEY = os.getenv('PPLX_API_KEY')
ELEVENLABS_API_KEY = os.getenv('ELEVENLABS_API_KEY')
REPLICATE_API_KEY = os.getenv('REPLICATE_API_KEY')
BFL_API_KEY = os.getenv('BFL_API_KEY')

def init_ai_clients(pplx_key=None, eleven_key=None, replicate_key=None):
    return

def call_perplexity_api(prompt, model="sonar-pro", max_tokens=800):
    """
    Send prompt to Perplexity-like chat/completions. Returns text.
    """
    url = "https://api.perplexity.ai/chat/completions"
    headers = {
        "Authorization": f"Bearer {PPLX_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": "You are an expert fitness + nutrition assistant. Respond in JSON only when asked."},
            {"role": "user", "content": prompt}
        ]
    }
    r = requests.post(url, headers=headers, json=payload, timeout=30)
    r.raise_for_status()
    res = r.json()
    text = res["choices"][0]["message"]["content"]
    return text

def parse_json_from_text(text):
    """
    Try to extract JSON object from text robustly.
    """
    try:
        cleaned = text.strip()
        cleaned = cleaned.replace('```json', '').replace('```', '').strip()
        return json.loads(cleaned)
    except Exception:
        import re
        m = re.search(r'(\{.*\})', text, flags=re.S)
        if m:
            try:
                return json.loads(m.group(1))
            except:
                return None
        return None

def generate_tts(text: str) -> bytes:
    import time
    import io
    from gtts import gTTS

    chunks = [text[i:i+200] for i in range(0, len(text), 200)]
    
    final_audio = io.BytesIO()

    for chunk in chunks:
        for attempt in range(3):
            try:
                mp3_fp = io.BytesIO()
                tts = gTTS(text=chunk, lang='en')
                tts.write_to_fp(mp3_fp)
                mp3_fp.seek(0)
                final_audio.write(mp3_fp.read())
                break
            except Exception as e:
                if "429" in str(e) and attempt < 2:
                    time.sleep(1.5)
                else:
                    raise e

    final_audio.seek(0)
    return final_audio.read()


def generate_image_bfl(prompt):
    url = "https://api.bfl.ai/v1/workflows/run"
    headers = {
        "Authorization": f"Bearer {BFL_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "workflow_id": "stable-diffusion-xl",  
        "inputs": {
            "prompt": prompt
        }
    }

    r = requests.post(url, json=payload, headers=headers)
    
    r.raise_for_status()
    return r.json()
