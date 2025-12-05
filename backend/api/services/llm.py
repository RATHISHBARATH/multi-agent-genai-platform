"""LLM HTTP adapter with retries and helpful messages."""
import os, requests, time, logging
logger = logging.getLogger("autoscillab.llm")

class LLMModel:
    def __init__(self):
        self.api_key = os.getenv("LLM_API_KEY", "")
        self.url = os.getenv("LLM_API_URL", "https://api.openai.com/v1/chat/completions")
        self.model = os.getenv("LLM_MODEL", "gpt-4o-mini")

    def chat(self, prompt: str, max_retries: int = 2) -> str:
        if not self.api_key:
            return "[LLM] No API key provided; set LLM_API_KEY environment variable."
        payload = {"model": self.model, "messages": [{"role": "user", "content": prompt}], "temperature": 0.0}
        headers = {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}
        for attempt in range(max_retries + 1):
            try:
                r = requests.post(self.url, json=payload, headers=headers, timeout=30)
                r.raise_for_status()
                data = r.json()
                choices = data.get("choices") or data.get("result") or []
                if choices and isinstance(choices, list):
                    message = choices[0].get("message") or choices[0]
                    content = message.get("content") if isinstance(message, dict) else str(message)
                    return content
                return str(data)
            except Exception as e:
                logger.exception("LLM request failed, attempt %s/%s", attempt, max_retries)
                time.sleep(1 + attempt * 2)
        return "[LLM] Failed after retries."
