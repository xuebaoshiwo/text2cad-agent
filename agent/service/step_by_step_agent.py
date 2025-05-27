import sys
import os

# sys.path.append(r"D:/Text2Cad/agent/service")
sys.path.append(os.path.join(os.getcwd(), "agent", "service"))


import asyncio
from qa_chain import QAChainService
from prompt.input_decider_prompt import input_decider_prompt
from prompt.nlp2json_prompt import npl2json_prompt
from prompt.json2py_prompt import json2py_prompt
from prompt.demand_analysis_prompt import demand_analysis_prompt
from prompt.generate_py import generate_py_prompt
from prompt.code_debug_prompt import code_debug_prompt
from prompt.devide_steps_prompt import devide_steps_prompt
from prompt.step_generate_code_prompt import step_generate_code_prompt
from parser import json_parser
from llm_py_parser import parse_llm_py_code
from python_runner import FreeCADPythonRunner
from knowledge_support.get_support import get_geometry_support

import json
import uuid

class NPL2PyStepByStepAgentChain:
    def __init__(self, output_ab_dir=None, freecad_python_path = None, max_retry_times = 3):
         # 获取text2cad-agent根目录
         root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
         if output_ab_dir is None:
             output_ab_dir = os.path.join(root_dir, "output")
         if freecad_python_path is None:
             # 默认使用环境变量或配置文件中的FreeCAD Python路径
             freecad_python_path = os.environ.get("FREECAD_PYTHON_PATH", r"D:/freecad/bin/python.exe")
         self.support_names, self.supports = get_geometry_support()
         self.qa_chain = QAChainService()
         self.code_debug_chain = QAChainService(type="claude")

         # 分析层
         self.demand_analysis_prompt = demand_analysis_prompt
         self.demand_analysis_prompt_key = ["npl_description"]
         # 步骤分解层:
         self.devide_steps_prompt = devide_steps_prompt
         self.devide_steps_prompt_key = ["demand_analysis_npl", "geometry_supports"]
         # 生成代码层
         self.step_generate_code_prompt = step_generate_code_prompt
         self.step_generate_code_prompt_key = ["demand_analysis_npl", "completed_steps", "existing_code", "step_to_generate_code", "support", "output_ab_path"]
         # 执行层
         self.runner = FreeCADPythonRunner(freecad_python_path)
         # debug层
         self.code_debug_prompt = code_debug_prompt
         self.code_debug_prompt_key = ["code_string", "error_info"]
         # 保存路径
         self.output_ab_dir = output_ab_dir
         self.max_retry_times = max_retry_times

    async def run(self, npl: str, output_ab_dir: str = "output"):

        
        id = str(uuid.uuid4())
        
        # 分析层
        demand_analysis_result = await self.code_debug_chain.get_answer(
            self.demand_analysis_prompt, 
            self.demand_analysis_prompt_key, 
            npl_description=npl
            )
        print("分析层: ", demand_analysis_result)
        print("--------------------------------")
        # 步骤分解层
        devide_steps_result = await self.code_debug_chain.get_answer(
            self.devide_steps_prompt, 
            self.devide_steps_prompt_key, 
            demand_analysis_npl=demand_analysis_result,
            geometry_supports = self.support_names
            )
        steps_dict = json_parser(devide_steps_result)
        print("步骤分解层: ", steps_dict)
        print("--------------------------------")
        # 逐步生成代码层
        steps = steps_dict["steps"]
        completed_steps = []
        existing_code = ""
        last_correct_code = ""
        for step in steps:
            file_name = id + "-step" + str(step.get("step_id")) + ".FCStd"
            output_ab_path = os.path.join(output_ab_dir, file_name)
            use_supports = dict()
            support_name = step.get("support")
            if support_name:
                for s in self.supports:
                    if s["name"] == support_name:    
                        use_supports[support_name] = s 
                               
            code_str = await self.code_debug_chain.get_answer(
                self.step_generate_code_prompt, 
                self.step_generate_code_prompt_key, 
                demand_analysis_npl=demand_analysis_result, 
                completed_steps=completed_steps, 
                existing_code=existing_code, 
                step_to_generate_code=step,
                support = use_supports,
                output_ab_path = output_ab_path
            )
            code_str = parse_llm_py_code(code_str)
            
            flag = True
            retry_times = 0
            
            while(flag and retry_times < self.max_retry_times):
                # 执行代码
                try:
                    res = self.runner.run_code_string(code_str)
                    if res['returncode'] == 0:
                        flag = False
                        last_correct_code = code_str
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
            if flag:
                return demand_analysis_result, devide_steps_result, last_correct_code
            
            completed_steps.append(step)
            existing_code = code_str
            print(f"步骤{step['step_id']}完成, 代码正确: {not flag}")
            print(f"当前代码: {existing_code}")
            print("--------------------------------")
        
        # # 保存最终代码到 output_ab_dir
        # output_path = os.path.join(self.output_ab_dir, f"{uuid.uuid4().hex}.py")
        # os.makedirs(self.output_ab_dir, exist_ok=True)
        # with open(output_path, "w", encoding="utf-8") as f:
        #     f.write(existing_code)

        return demand_analysis_result, devide_steps_result, existing_code

if __name__ == "__main__":
    npl2py_step_by_step_agent_chain = NPL2PyStepByStepAgentChain()
    npl = """
   画一只猫的头
"""
    demand_analysis_result, devide_steps_result, existing_code = asyncio.run(npl2py_step_by_step_agent_chain.run(npl))
    print(demand_analysis_result)
    print(devide_steps_result)
    print(existing_code)

