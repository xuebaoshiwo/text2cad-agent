import subprocess
import sys
import os
import tempfile
from pathlib import Path

class FreeCADPythonRunner:
    def __init__(self, freecad_python_path=r"D:\freecad\bin\python.exe"):
        """
        初始化FreeCAD Python执行器
        
        Args:
            freecad_python_path (str): FreeCAD Python解释器的路径
        """
        self.freecad_python_path = freecad_python_path
    
    def _check_freecad_python(self):
        """检查FreeCAD Python解释器是否存在"""
        if not os.path.exists(self.freecad_python_path):
            raise FileNotFoundError(f"FreeCAD Python解释器未找到: {self.freecad_python_path}")
    
    def run_code_string(self, code_string, capture_output=True, timeout=30):
        """
        执行Python代码字符串
        
        Args:
            code_string (str): 要执行的Python代码
            capture_output (bool): 是否捕获输出
            timeout (int): 超时时间（秒）
            
        Returns:
            dict: 包含返回码、输出和错误信息的字典
        """
        try:
            # 使用-c参数直接执行代码字符串
            cmd = [self.freecad_python_path, "-c", code_string]
            
            result = subprocess.run(
                cmd,
                capture_output=capture_output,
                text=True,
                timeout=timeout,
                encoding='utf-8',
                errors='replace'
            )
            
            return {
                'returncode': result.returncode,
                'stdout': result.stdout,
                'stderr': result.stderr,
                'success': result.returncode == 0
            }
            
        except subprocess.TimeoutExpired:
            return {
                'returncode': -1,
                'stdout': '',
                'stderr': f'执行超时 ({timeout}秒)',
                'success': False
            }
        except Exception as e:
            return {
                'returncode': -2,
                'stdout': '',
                'stderr': f'执行失败: {str(e)}',
                'success': False
            }
        
if __name__ == "__main__":
    runner = FreeCADPythonRunner()
    code_string = """
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
    print(f"model save to {file_path}")

# 运行主函数
main()
    """
    res = runner.run_code_string(code_string)
    print(res)
    
