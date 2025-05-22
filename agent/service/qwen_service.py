from langchain.llms.base import LLM
from langchain.callbacks.manager import CallbackManagerForLLMRun
from typing import Any, List, Optional
from dashscope import Generation
import sys
sys.path.append(r"E:/Text2Cad/agent/service")
from config import QwenSettings

class QwenLLM(LLM):
    settings: QwenSettings = QwenSettings()
    
    @property
    def _llm_type(self) -> str:
        return "Qwen"

    def _call(
        self,
        prompt: str,
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> str:
        response = Generation.call(
            model=self.settings.MODEL_NAME,
            prompt=prompt,
            api_key=self.settings.DASHSCOPE_API_KEY,
            temperature=self.settings.TEMPERATURE,
            max_tokens=self.settings.MAX_TOKENS,
            top_p=self.settings.TOP_P,
            **kwargs
        )
        
        if response.status_code == 200:
            return response.output.text
        else:
            raise Exception(f"API调用失败: {response.message}") 