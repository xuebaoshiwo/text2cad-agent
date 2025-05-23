import json
FREECAD_PYTHON_KNOWLEDGE = r"D:\Text2Cad\text2cad-agent\agent\service\knowledge_support\freecad_python_knowledge.json"
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