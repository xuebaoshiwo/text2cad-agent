import asyncio
from service.qa_chain import QAChainService

async def test_qa():
    qa_service = QAChainService()
    question = "请介绍一下你自己，你是谁？"
    try:
        answer = await qa_service.get_answer(question)
        print(f"问题: {question}")
        print(f"回答: {answer}")
    except Exception as e:
        print(f"错误: {str(e)}")

if __name__ == "__main__":
    asyncio.run(test_qa()) 