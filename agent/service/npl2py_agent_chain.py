import sys
sys.path.append(r"E:/Text2Cad/agent/service")

import asyncio
from qa_chain import QAChainService
from prompt.input_decider_prompt import input_decider_prompt
from prompt.nlp2json_prompt import npl2json_prompt
from prompt.json2py_prompt import json2py_prompt

class NPL2PYAgentChain:
    def __init__(self):
        self.qa_chain = QAChainService()
        # 是否需要处理成JSON
        self.decider_prompt = input_decider_prompt
        self.decider_prompt_key = ["question"]

        # 将自然语言转换为JSON
        self.npl2json_prompt = npl2json_prompt
        self.npl2json_prompt_key = ["question"]
        
        # 将JSON转换为Python代码
        self.json2py_prompt = json2py_prompt
        self.json2py_prompt_key = ["json_description"]

    async def run(self, npl: str):
        decide_result = await self.qa_chain.get_answer(self.decider_prompt, self.decider_prompt_key, question=npl)
        json_description = await self.qa_chain.get_answer(self.npl2json_prompt, self.npl2json_prompt_key, question=npl)
        py_code = await self.qa_chain.get_answer(self.json2py_prompt, self.json2py_prompt_key, json_description=json_description)

        return decide_result, json_description, py_code


if __name__ == "__main__":
    npl2py_agent_chain = NPL2PYAgentChain()
    npl = """
### 用户输入描述：
"画一个漏斗"

---

### 对象理解：
用户想要建模一个典型的漏斗，由一个上大下小的锥形主体和一个较小的出口组成。

---

### 基本几何分解：
1. 锥形主体：圆台（顶部大，底部小）
2. 出口部分：小圆柱体（连接锥形主体的底部）

---

### 建模步骤分析：
1. **创建锥形主体**：
   - 绘制一个大圆（代表漏斗的顶部开口），并标注其半径 \( R_{\text{top}} \)。
   - 在下方绘制一个小圆（代表漏斗的底部开口），并标注其半径 \( R_{\text{bottom}} \)。
   - 连接两个圆的中心点，确定锥形的高度 \( H \)。
   - 使用“旋转”或“拉伸”工具，基于两个圆生成一个锥形主体。

2. **创建出口部分**：
   - 在锥形主体的底部，绘制一个比底部开口稍小的小圆（出口直径 \( D_{\text{outlet}} \)）。
   - 使用“拉伸”工具，将小圆向上拉伸一段高度 \( H_{\text{outlet}} \)，形成一个小圆柱体作为出口。

3. **组合主体和出口**：
   - 将出口部分放置在锥形主体的底部中央，确保两者无缝对齐。
   - 如果需要更高的精度，可以使用布尔运算（合并）将两者融合成一个整体。

4. **添加细节（可选）**：
   - 根据需求，可以在漏斗表面添加一些纹理或细节（如防滑纹路）。
   - 如果需要更真实的外观，可以为漏斗添加材质贴图或颜色。

---

### 关键尺寸参数：
1. 漏斗顶部开口半径 \( R_{\text{top}} \)
2. 漏斗底部开口半径 \( R_{\text{bottom}} \)
3. 漏斗高度 \( H \)
4. 出口直径 \( D_{\text{outlet}} \)
5. 出口高度 \( H_{\text{outlet}} \)

---

### 潜在挑战：
1. **比例协调**：
   - 确保漏斗的锥度（即 \( R_{\text{top}} / R_{\text{bottom}} \) 和 \( H \) 的关系）符合实际需求，避免比例失调。

2. **出口对齐**：
   - 在将出口与锥形主体对齐时，需注意出口的中心点必须精确位于锥形主体底部的中心线上。

3. **细节处理**：
   - 如果需要添加纹理或细节，需注意这些细节不会影响整体结构的稳定性。

4. **布尔运算问题**：
   - 在合并主体和出口时，可能会遇到布尔运算失败的问题（如重叠区域不一致）。建议先检查几何体是否完全对齐。

---

### 指导原则：
- 使用参数化建模，方便后续调整尺寸。
- 优先选择简单直观的操作（如旋转、拉伸），避免复杂的布尔运算。
- 在建模过程中，随时验证几何体的比例和位置关系，确保最终模型的准确性。
- 如果需要进一步优化，可以尝试使用CAD软件中的细分工具或网格编辑功能来提升模型的光滑度。
"""
    decide_result, json_description, py_code = asyncio.run(npl2py_agent_chain.run(npl))
    print(decide_result)
    print(json_description)
    print(py_code)

