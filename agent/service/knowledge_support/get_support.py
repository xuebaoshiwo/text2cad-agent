import json
# FREECAD_PYTHON_KNOWLEDGE = r"D:\Text2Cad\text2cad-agent\agent\service\knowledge_support\freecad_python_knowledge.json"
import os

# 获取当前脚本所在目录（假设是项目根目录）
project_root = os.path.dirname(os.path.abspath(__file__))

# 构造 JSON 文件的相对路径
FREECAD_PYTHON_KNOWLEDGE = os.path.join(
    project_root, "freecad_python_knowledge.json"
)

def get_geometry_support(json_path = FREECAD_PYTHON_KNOWLEDGE):
    with open(json_path, 'r', encoding="utf-8") as f:
        d = json.load(fp=f)
        supports = d.get("supports")
        supports_names = [s.get("name") for s in supports ]
        return supports_names, supports
    
    
if __name__ == "__main__":
    support_names, supports = get_geometry_support()
    print(type(support_names))
    print(type(supports))