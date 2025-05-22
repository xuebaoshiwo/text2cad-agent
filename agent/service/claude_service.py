from langchain.llms.base import LLM
from langchain.callbacks.manager import CallbackManagerForLLMRun
from typing import Any, List, Optional
import requests
from pydantic_settings import BaseSettings

class ClaudeSettings(BaseSettings):
    ANTHROPIC_API_KEY: str = "sk-8Zt52PZNeySmDUEpFe82C9Df039f4c5092625c03FdBbDb3e"
    MODEL_NAME: str = "claude-3-opus-20240229"  # 可根据需要更换
    TEMPERATURE: float = 0.7
    MAX_TOKENS: int = 1500
    TOP_P: float = 0.8
    

class ClaudeLLM(LLM):
    settings: ClaudeSettings = ClaudeSettings()

    @property
    def _llm_type(self) -> str:
        return "Claude"

    def _call(
        self,
        prompt: str,
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> str:
        url = "https://api.anthropic.com/v1/messages"
        headers = {
            "x-api-key": self.settings.ANTHROPIC_API_KEY,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json"
        }
        data = {
            "model": self.settings.MODEL_NAME,
            "max_tokens": self.settings.MAX_TOKENS,
            "temperature": self.settings.TEMPERATURE,
            "top_p": self.settings.TOP_P,
            "messages": [
                {"role": "user", "content": prompt}
            ]
        }
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 200:
            result = response.json()
            # Claude 3返回格式：{"content": [{"text": "..."}], ...}
            if "content" in result and isinstance(result["content"], list):
                return result["content"][0].get("text", "")
            else:
                return str(result)
        else:
            raise Exception(f"Claude API调用失败: {response.status_code} {response.text}") 
        

if __name__ == "__main__":
    url = r"https://api.mjdjourney.cn"
    import http.client
    import json

    conn = http.client.HTTPSConnection("")
    payload = json.dumps({
    "model": "claude-3-7-sonnet-20250219",
    "messages": [
        {
            "role": "user",
            "content": "Hello!"
        }
    ]
    })
    headers = {
    'Accept': 'application/json',
    'Authorization': 'Bearer sk-8Zt52PZNeySmDUEpFe82C9Df039f4c5092625c03FdBbDb3e',
    'Content-Type': 'application/json'
    }
    conn.request("POST", "https://api.mjdjourney.cn/v1/chat/completions", payload, headers)
    res = conn.getresponse()
    data = res.read()
    print(data.decode("utf-8"))