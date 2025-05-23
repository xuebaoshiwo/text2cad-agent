import json

def json_parser(res_string: str):
    blocks = res_string.split("```json")
    if len(blocks) < 2:
        raise ValueError("未找到 JSON 代码块")
    
    last_block = blocks[-1]
    
    if "```" in last_block:
        json_str = last_block.split("```")[0]
    else:
        json_str = last_block
    
    return json.loads(json_str)

if __name__ == "__main__":
    res_string = """
```json
{
  "object": "高脚杯",
  "steps":[
        {
            "step_id": 1,
            "title": "绘制杯身",
            "goal": "创建倒锥台形的杯身，尺寸为顶部直径3.0，底部直径1.0，高度2.5，壁厚0.1"
        },
        {
            "step_id": 2,
            "title": "绘制杯脚",
            "goal": "创建细长圆柱体的杯脚，尺寸为直径0.5，高度4.0"
        },
        {
            "step_id": 3,
            "title": "绘制底座",
            "goal": "创建圆盘形的底座，尺寸为底部直径2.5，顶部直径1.5，高度0.5"
        }
    ]
}
```
    """
    print(json_parser(res_string))
