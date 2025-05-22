import sys
sys.path.append(r"E:/Text2Cad/agent")

import asyncio
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from service.claude_service import ClaudeLLM  # 你需要先实现这个类

if __name__ == "__main__":
    async def main():
        llm = ClaudeLLM()
        prompt = PromptTemplate(
            input_variables=["question"],
            template="请用专业、简洁的语言回答：{question}"
        )
        chain = LLMChain(llm=llm, prompt=prompt)
        question = "介绍一下你自己"
        answer = await chain.arun(question=question)
        print(answer)
    asyncio.run(main())
