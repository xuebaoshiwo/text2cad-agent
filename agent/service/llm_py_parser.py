def parse_llm_py_code(code_string: str) -> str:
    """
    从 LLM 返回的文本中提取 Python 代码块。
    
    Args:
        code_string (str): 包含 Python 代码块的文本
        
    Returns:
        str: 提取出的 Python 代码
        
    Raises:
        ValueError: 当没有找到有效的 Python 代码块时
    """
    if not code_string:
        raise ValueError("输入字符串为空")
        
    # 分割代码
    code_blocks = code_string.split("```python")
    
    if len(code_blocks) < 2:
        raise ValueError("未找到 Python 代码块")
    
    # 获取最后一个代码块
    last_block = code_blocks[-1]
    
    # 提取代码块结束标记之前的内容
    if "```" in last_block:
        code = last_block.split("```")[0]
    else:
        code = last_block
        
    # 清理代码（去除首尾空白字符）
    code = code.strip()
    
    if not code:
        raise ValueError("提取的代码块为空")
        
    return code

if __name__ == "__main__":
    code_string = """
```python
import FreeCAD, Part, Draft

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
        new_leg.Placement.Base.x = radius * cos(angle * pi / 180)
        new_leg.Placement.Base.y = radius * sin(angle * pi / 180)
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
    Part.show(final_table)

# 运行主函数
if __name__ == "__main__":
    main()
```
    """
    print(parse_llm_py_code(code_string))


