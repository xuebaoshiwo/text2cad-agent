from langchain.llms.base import LLM
from langchain.callbacks.manager import CallbackManagerForLLMRun
from typing import Any, List, Optional
import requests
from pydantic_settings import BaseSettings
from openai import OpenAI

class ClaudeSettings(BaseSettings):
    ANTHROPIC_API_KEY: str = "sk-8Zt52PZNeySmDUEpFe82C9Df039f4c5092625c03FdBbDb3e"
    # MODEL_NAME: str = "claude-sonnet-4-20250514"  # 可根据需要更换
    MODEL_NAME: str = "claude-sonnet-4-20250514"
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
        client = OpenAI(api_key="sk-8Zt52PZNeySmDUEpFe82C9Df039f4c5092625c03FdBbDb3e", base_url="https://api.mjdjourney.cn/v1")
        try:
            completion = client.chat.completions.create(
                model=self.settings.MODEL_NAME,
                stream=False,
                top_p=self.settings.TOP_P,
                temperature=self.settings.TEMPERATURE,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            response = completion.choices[0].message.content
        except Exception as e:
            raise Exception(f"Claude API调用失败: {e}")
        return str(response)
        

if __name__ == "__main__":
    # from openai import OpenAI

    # client = OpenAI(api_key="sk-8Zt52PZNeySmDUEpFe82C9Df039f4c5092625c03FdBbDb3e", base_url="https://api.mjdjourney.cn/v1")

    # completion = client.chat.completions.create(
    #     model="claude-3-7-sonnet-20250219",
    #     stream=False,
    #     messages=[
    #         {"role": "user", "content": "Hello!"}
    #     ]
    # )

    # print(completion.choices[0].message)
    # print(completion)
    
    llm = ClaudeLLM()
    print(llm.invoke("你好"))
    