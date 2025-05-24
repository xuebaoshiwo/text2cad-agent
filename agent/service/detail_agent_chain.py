import sys
sys.path.append(r"D:\Text2Cad\text2cad-agent\agent\service")
from qa_chain import QAChainService
from detail_prompt.detail_suggest_promt import detail_suggest_prompt
from detail_prompt.detail_fail_edit_prompt import detail_fail_edit_prompt

class DetailAgentChain:
    def __init__(self) -> None:
        self.qa_chain = QAChainService(type="claude")
        self.detail_suggest_prompt = detail_suggest_prompt
        self.detail_suggest_prompt_key = ["code_str"]
        
        self.detail_fail_edit_prompt = detail_fail_edit_prompt
        self.detail_fail_edit_prompt_key = ["code_str", "edit_detail_info"]
    
    async def detail_suggest(self, code_str: str):
        detail_suggest_result = await self.qa_chain.get_answer(
            self.detail_suggest_prompt,
            self.detail_suggest_prompt_key,
            code_str=code_str
        )
        return detail_suggest_result
    
    async def detail_fail_edit(self, code_str: str, edit_detail_info: str):
        detail_fail_edit_result = await self.qa_chain.get_answer(
            self.detail_fail_edit_prompt,
            self.detail_fail_edit_prompt_key,
            code_str=code_str, edit_detail_info=edit_detail_info
        )
        return detail_fail_edit_result


if __name__ == "__main__":
    import asyncio
    detail_agent_chain = DetailAgentChain()
    code_str = """
import FreeCAD as App
import Part

# 创建新文档
doc = App.newDocument("FryingPan")

# 步骤1: 绘制锅身外壳
# 创建锅身外壳 - 圆柱体
pan_body = Part.makeCylinder(130, 60)  # 直径260mm(半径130mm), 高度60mm

# 步骤2: 绘制锅身内腔
# 创建锅身内腔 - 圆柱体（用于挖空）
inner_cavity = Part.makeCylinder(120, 50)  # 直径240mm(半径120mm), 高度50mm

# 设置内腔位置，底面高度为10mm（锅底厚度）
inner_cavity.translate(App.Vector(0, 0, 10))

# 挖空锅身 - 从外壳中减去内腔
pan_body = pan_body.cut(inner_cavity)

# 将挖空后的锅身添加到文档中
pan_body_obj = doc.addObject("Part::Feature", "PanBody")
pan_body_obj.Shape = pan_body



# 步骤3: 绘制锅柄
# 创建锅柄 - 圆柱体
handle = Part.makeCylinder(7.5, 180)  # 直径15mm(半径7.5mm), 长度180mm

# 旋转锅柄使其水平放置（绕Y轴旋转90度）
handle.rotate(App.Vector(0, 0, 0), App.Vector(0, 1, 0), 90)

# 设置锅柄位置，一端连接到锅身侧壁，高度为锅身中心高度（30mm）
handle.translate(App.Vector(130, 0, 30))

# 将锅柄添加到文档中
handle_obj = doc.addObject("Part::Feature", "Handle")
handle_obj.Shape = handle

# 重新计算文档
doc.recompute()
    """
    edit_info = "平底锅的把手，没有连在锅身上"
    # detail_suggest_result = asyncio.run(detail_agent_chain.detail_suggest(code_str))
    detail_edit_result = asyncio.run(detail_agent_chain.detail_fail_edit(code_str=code_str, edit_detail_info=edit_info))
    # print(detail_suggest_result)
    print(detail_edit_result)
