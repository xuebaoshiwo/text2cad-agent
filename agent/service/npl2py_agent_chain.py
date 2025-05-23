import sys
sys.path.append(r"E:/Text2Cad/agent/service")

import asyncio
from qa_chain import QAChainService
from prompt.input_decider_prompt import input_decider_prompt
from prompt.nlp2json_prompt import npl2json_prompt
from prompt.json2py_prompt import json2py_prompt
from prompt.demand_analysis_prompt import demand_analysis_prompt
from prompt.generate_py import generate_py_prompt
from prompt.code_debug_prompt import code_debug_prompt
from llm_py_parser import parse_llm_py_code
from python_runner import FreeCADPythonRunner
import uuid
import os

class NPL2PYAgentChain:
    def __init__(self, output_ab_dir = r"D:/Text2Cad/text2cad-agent/output", freecad_python_path = r"D:/freecad/bin/python.exe", max_retry_times = 3):
         self.qa_chain = QAChainService()
         self.code_debug_chain = QAChainService(type="claude")

         # 分析层
         self.demand_analysis_prompt = demand_analysis_prompt
         self.demand_analysis_prompt_key = ["npl_description"]
         # 生成代码层
         self.generate_py_prompt = generate_py_prompt
         self.generate_py_prompt_key = ["npl_description", "output_ab_dir"]
         # 执行层
         self.runner = FreeCADPythonRunner(freecad_python_path)
         # debug层
         self.code_debug_prompt = code_debug_prompt
         self.code_debug_prompt_key = ["code_string", "error_info"]
         # 保存路径
         self.output_ab_dir = output_ab_dir
         self.max_retry_times = max_retry_times

    async def run(self, npl: str):
        # 分析层
        demand_analysis_result = await self.code_debug_chain.get_answer(
            self.demand_analysis_prompt, 
            self.demand_analysis_prompt_key, 
            npl_description=npl
            )
        print("分析层: ", demand_analysis_result)
        # 生成代码层
        uuid_str = str(uuid.uuid4()) + r".FCStd"
        output_ab_path = os.path.join(self.output_ab_dir, uuid_str)
        generate_py_result = await self.code_debug_chain.get_answer(
            self.generate_py_prompt, 
            self.generate_py_prompt_key, 
            npl_description=demand_analysis_result, 
            output_ab_dir=output_ab_path
            )
        print("生成代码层: ", generate_py_result)
        code_str = parse_llm_py_code(generate_py_result)
        # 执行层
        flag = True
        retry_times = 0
        while(flag and retry_times < self.max_retry_times):
            try:
                  res = self.runner.run_code_string(code_str)
                  if res['returncode'] == 0:
                     flag = False
                  else:
                     raise Exception(res['stderr'])
            except Exception as e:
               print(f"执行失败: {e}，开始debug，当前重试次数：{retry_times}")
               code_str = await self.code_debug_chain.get_answer(
                  self.code_debug_prompt, 
                  self.code_debug_prompt_key, 
                  code_string=code_str,
                  error_info=e
               )
               code_str = parse_llm_py_code(code_str)
            retry_times += 1

        return demand_analysis_result, generate_py_result, res

if __name__ == "__main__":
    npl2py_agent_chain = NPL2PYAgentChain()
    npl = """
   画一只高脚杯
"""
    demand_analysis_result, generate_py_result, res = asyncio.run(npl2py_agent_chain.run(npl))
    print(demand_analysis_result)
    print(generate_py_result)
    print(res)

