from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
import sys
sys.path.append(r"E:/Text2Cad/agent/service")
from qwen_service import QwenLLM

class QAChainService:
    def __init__(self):
        self.llm = QwenLLM()
        self.prompt = PromptTemplate(
            input_variables=["question"],
            template="""请回答下面的问题。请保持专业、准确和简洁。

问题: {question}

回答:"""
        )
        self.chain = LLMChain(llm=self.llm, prompt=self.prompt)
    
    async def get_answer(self, prompt: str = None, insert_key: list[str] = ["question"], **kwargs) -> str:
        """
        获取问题的答案
        
        Args:
            question: 用户提问
            prompt: 可选的提示词，用于自定义回答

        Returns:
            str: 通义千问的回答
        """

        final_prompt = self.prompt
        if prompt:
            final_prompt = PromptTemplate(
                input_variables=insert_key,
                template=prompt
            )
        
        self.chain.prompt = final_prompt
        try:
            response = await self.chain.arun(**kwargs)
            return response.strip()
        except Exception as e:
            raise Exception(f"获取答案失败: {str(e)}")
        finally:
            self.chain.prompt = None

if __name__ == "__main__":
    import asyncio
    
    async def main():
        qa_chain = QAChainService()
        question = "介绍以下你自己"
        answer = await qa_chain.get_answer(question)
        print(answer)
    
    asyncio.run(main())
