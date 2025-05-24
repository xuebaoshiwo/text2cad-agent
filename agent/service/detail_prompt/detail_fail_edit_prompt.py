detail_fail_edit_prompt = """
你是一个FreeCad Python专家，专门负责接收用户写的python代码，这些代码一般可以正常运行，但是可能一些建模细节不符合预期，用户会告诉你他们想要修改的细节效果，而你只需要修改用户提供python代码，实现用户的需求。
要求：
1. 你的输出只能是完整正确的python代码，不要输出任何解释，不要输出任何其他内容。
2. 你不能修改用户要求细节以外部分的代码。
3. 严格按照用户要求修改


以下是用户对细节的细节修改要求：
{edit_detail_info}

以下是用户的代码：
{code_str}
"""

if __name__ == "__main__":
    import sys 
    import os
    import asyncio
    # sys.path.append(r"D:\Text2Cad\text2cad-agent\agent\service")
    sys.path.append(os.path.join(os.getcwd(), "agent", "service"))
    from qa_chain import QAChainService
    qa_chain = QAChainService(type="claude")
    edit_detail_info = "火箭的三角板平衡翼方向有误，不应该三角面与地面平行，而应该是三角面与地面垂直才对"
    code_str = """
import Part

# 创建新文档
doc = App.newDocument("Rocket")

# 步骤1: 绘制头锥部分
# 创建圆锥形头锥（载荷舱）
nose_cone = doc.addObject("Part::Cone", "NoseCone")
nose_cone.Radius1 = 0.5  # 底面半径（直径1.0）
nose_cone.Radius2 = 0.0  # 顶面半径（尖锥）
nose_cone.Height = 1.5   # 高度
nose_cone.Placement = App.Placement(App.Vector(0, 0, 8.0), App.Rotation(0, 0, 0))  # 位置在主体顶部

# 步骤2: 绘制主体部分
# 创建圆柱形主体（燃料舱）
main_body = doc.addObject("Part::Cylinder", "MainBody")
main_body.Radius = 0.5   # 半径（直径1.0）
main_body.Height = 8.0   # 高度
main_body.Placement = App.Placement(App.Vector(0, 0, 0), App.Rotation(0, 0, 0))  # 位置在原点

# 步骤3: 绘制尾部喷嘴
# 创建圆锥形尾部喷嘴（推进器喷嘴）
tail_nozzle = doc.addObject("Part::Cone", "TailNozzle")
tail_nozzle.Radius1 = 0.5   # 顶部半径（与主体直径匹配）
tail_nozzle.Radius2 = 0.3   # 底部半径（直径0.6）
tail_nozzle.Height = 1.0    # 高度
tail_nozzle.Placement = App.Placement(App.Vector(0, 0, -1.0), App.Rotation(0, 0, 0))  # 位置在主体底部

# 步骤4: 添加三个三角形平衡翼
import math

# 定义三角形翼的参数
wing_thickness = 0.05
wing_height = 1.0
wing_base = 0.8

# 创建三个平衡翼，每个相隔120度
for i in range(3):
    angle = i * 120  # 每个翼相隔120度

    # 定义三角形的三个点
    p1 = App.Vector(0, 0, 0)
    p2 = App.Vector(wing_base, 0, 0)
    p3 = App.Vector(0, wing_height, 0)

    # 创建三角形面
    triangle_wire = Part.makePolygon([p1, p2, p3, p1])
    triangle_face = Part.Face(triangle_wire)

    # 拉伸成实体
    triangle_solid = triangle_face.extrude(App.Vector(0, 0, wing_thickness))

    # 添加到文档
    wing = doc.addObject("Part::Feature", f"Wing{i+1}")
    wing.Shape = triangle_solid

    # 计算位置和旋转
    x_pos = 0.5 * math.cos(math.radians(angle))
    y_pos = 0.5 * math.sin(math.radians(angle))

    # 设置翼的位置和旋转
    wing.Placement = App.Placement(
        App.Vector(x_pos, y_pos, 1.0),  # 位置在火箭主体侧面
        App.Rotation(App.Vector(0, 0, 1), angle)  # 绕Z轴旋转
    )

# 重新计算文档
doc.recompute()
    """
    async def main():
        res = await qa_chain.get_answer(detail_fail_edit_prompt
                                , ["edit_detail_info", "code_str"]
                                , edit_detail_info=edit_detail_info,
                                code_str=code_str
                                )
        print(res)

    asyncio.run(main())
