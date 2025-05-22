import FreeCAD, Part, Draft
import math

def create_table_top(diameter=4, thickness=0.2):
    # 创建桌面
    table_top = Part.makeCylinder(diameter/2, thickness)
    table_top.Placement.Base.z = -thickness/2  # 调整位置使底面与原点对齐
    return table_top

def create_table_leg(diameter=0.3, height=1.5):
    # 创建单个桌腿
    leg = Part.makeCylinder(diameter/2, height)
    leg.Placement.Base.z = -height  # 调整位置使底部接触地面
    return leg

def arrange_legs(leg, num_legs=4, radius=2-0.3/2):
    # 安排桌腿的位置
    legs = []
    for i in range(num_legs):
        angle = i * (360 / num_legs)
        new_leg = leg.copy()
        new_leg.Placement.Base.x = radius * math.cos(angle * math.pi / 180)
        new_leg.Placement.Base.y = radius * math.sin(angle * math.pi / 180)
        legs.append(new_leg)
    return legs

def assemble_table(table_top, legs):
    # 组装桌子
    table_parts = [table_top] + legs
    table = Part.makeCompound(table_parts)
    return table

# 主函数
def main():
    # 创建桌面和桌腿
    top = create_table_top()
    leg = create_table_leg()
    arranged_legs = arrange_legs(leg)

    # 组装桌子
    final_table = assemble_table(top, arranged_legs)

    # 将最终模型添加到FreeCAD文档中
    doc = FreeCAD.ActiveDocument
    if doc is None:
        doc = FreeCAD.newDocument("Table")
    obj = doc.addObject("Part::Feature", "Table")
    obj.Shape = final_table
    doc.recompute()

    # 保存
    # 保存文档
    file_path = "output/table_model.FCStd"  # 指定保存路径和文件名
    doc.saveAs(file_path)
    print(f"模型已保存为 {file_path}")

main()