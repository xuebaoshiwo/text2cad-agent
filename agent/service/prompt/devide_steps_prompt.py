devide_steps_prompt = """
你是一个CAD建模专家和Prompt工程师。你将接收到分析师对用户建模需求的专业分析和思路，你的任务是将分析师的分析描述和思路拆解成标准的建模步骤，适用于FreeCAD Python建模流程。

要求:
1.你的步骤划分必须严格参照分析师的分析描述和思路，不能遗漏任何重要步骤，也不能添加任何无关步骤。
2.你的步骤只能是“绘制某个部分”，不可以是组装或是过于具体的操作。
3.每一个步骤是否需要使用到geometry support list {geometry_supports}中的模型或者元素，如果需要请给这一个步骤加上support属性，值为geometry support的名字；若不在则不用添加。
4.请将输出结构化为 JSON 格式，且你的输出只能是这个JSON，不能输出其他内容，JSON格式如下所示(你可以划分步骤数量不一定为3)：
```json
{{
  "object": "描述的物体名称",
  "steps":[
        {{
            "step_id": 1,
            "title": "绘制杯身",
            "goal": "创建高脚杯的主要容器部分",
            "support": geometry_support_name 1,
        }}
        {{
            "step_id": 2,
            "title": "绘制杯脚",
            "goal": "创建高脚杯的支撑部分",
        }}
        {{
            "step_id": 3,
            "title": "绘制底座",
            "goal": "创建高脚杯的底座部分",
        }}
        ...
    ]
}}

分析师的思路:
{demand_analysis_npl}

"""

if __name__ == "__main__":
    import sys 
    import os
    import asyncio
    # sys.path.append("d:\\Text2Cad\\text2cad-agent\\agent\\service")
    sys.path.append(os.path.join(os.getcwd(), "agent", "service"))

    print(sys.path)
    from qa_chain import QAChainService
    qa_chain = QAChainService()
    demand_analysis_npl = """
思考过程
首先，分析高脚杯的基本组成部分：

杯身/杯碗 - 用于盛放液体的上部，通常呈半球形或倒锥形
杯脚/杯柄 - 连接杯身和底座的细长部分
底座/底盘 - 支撑整个高脚杯的圆形底部
对于尺寸，需要考虑各部分的比例关系：

杯身应该是最大的部分，用于盛放液体
杯脚应该细长，提供足够支撑
底座应该足够宽以提供稳定性
建模分析
简要概述：一只典型的高脚杯，由半球形杯身、细长杯脚和圆盘形底座组成。

组成部分分析：

杯身部分：

形状：倒锥台形（顶部宽、底部窄）
尺寸：顶部直径3.0，底部直径1.0，高度2.5，壁厚0.1
位置：位于杯脚顶部
建模操作：使用Part工作台创建圆锥体，然后挖空内部形成杯壁
杯脚部分：

形状：细长圆柱体
尺寸：直径0.5，高度4.0
位置：连接杯身底部和底座顶部
建模操作：使用Part工作台创建圆柱体
底座部分：

形状：圆盘形
尺寸：底部直径2.5，顶部直径1.5，高度0.5
位置：位于杯脚底部
建模操作：使用Part工作台创建圆盘或圆锥台
位置关系：

底座放置在XY平面上
杯脚竖直向上，底部与底座中心相连
杯身位于杯脚顶部，二者同轴
建模技巧：

使用Part工作台创建基本几何体
使用布尔运算挖空杯身形成容器
对杯身边缘和连接处使用倒角增加美观性
使用Fusion功能将各部分合并为一个整体
    """
    async def main():
        res = await qa_chain.get_answer(devide_steps_prompt, ["demand_analysis_npl"], demand_analysis_npl=demand_analysis_npl)
        print(res)
    
    asyncio.run(main())
