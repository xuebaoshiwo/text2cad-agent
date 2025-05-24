import sys
import os
sys.path.append(r"E:/Text2Cad/agent/service")
sys.path.append(os.path.join(os.getcwd(), "agent", "service"))


import asyncio
from qa_chain import QAChainService
from prompt.input_decider_prompt import input_decider_prompt
from prompt.nlp2json_prompt import npl2json_prompt
from prompt.json2py_prompt import json2py_prompt
from prompt.demand_analysis_prompt import demand_analysis_prompt
from prompt.generate_py import generate_py_prompt

if __name__ == "__main__":
    async def main():
        qa_chain = QAChainService()
        question = """
    画一个小轿车
"""
        # answer = await qa_chain.get_answer(question, npl2json_prompt)
        # answer = await qa_chain.get_answer(json2py_prompt, ["json_description"], json_description=question)
        answer = await qa_chain.get_answer(demand_analysis_prompt, ["npl_description"], npl_description=question)
        # answer = await qa_chain.get_answer(generate_py_prompt, ["npl_description"], npl_description=question)
        print(answer)
    
    asyncio.run(main())
