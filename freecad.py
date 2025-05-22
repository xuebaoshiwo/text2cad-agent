import FreeCAD as App
import Part
import Draft

def create_cup_body():
    body = Part.makeCylinder(0.75, 1.25)  # 半径：0.75，高度：1.25
    return body

def create_cup_bottom():
    bottom = Part.makeCylinder(0.9, 0.25)  # 半径：0.9，厚度：0.25
    return bottom

def create_handle():
    # 方法1：使用简单的几何体创建手柄
    # 创建一个环形手柄
    outer_radius = 1.2
    inner_radius = 0.8
    handle_height = 0.6
    
    # 创建外圆环
    outer_torus = Part.makeTorus(outer_radius, 0.1, App.Vector(1.0, 0, 0.8))
    
    # 只保留一半作为手柄
    cutting_box = Part.makeBox(2, 2, 2, App.Vector(-1, -1, -1))
    handle = outer_torus.cut(cutting_box)
    
    return handle

def create_handle_alternative():
    # 方法2：使用更复杂的路径创建手柄
    try:
        # 创建手柄的路径（半圆弧）
        center = App.Vector(1.0, 0, 0.8)
        path_points = []
        import math
        
        # 创建半圆弧的点
        for i in range(11):  # 0到180度，11个点
            angle = math.pi * i / 10
            x = center.x + 0.4 * math.cos(angle)
            y = center.y
            z = center.z + 0.3 * math.sin(angle)
            path_points.append(App.Vector(x, y, z))
        
        # 创建路径
        path_edges = []
        for i in range(len(path_points) - 1):
            edge = Part.makeLine(path_points[i], path_points[i + 1])
            path_edges.append(edge)
        
        path_wire = Part.Wire(path_edges)
        
        # 创建圆形截面
        profile_center = path_points[0]
        profile_normal = (path_points[1] - path_points[0]).normalize()
        profile_circle = Part.makeCircle(0.05, profile_center, profile_normal)
        profile_wire = Part.Wire([profile_circle])
        
        # 创建扫掠
        handle = path_wire.makePipeShell([profile_wire], False, False)
        return handle
        
    except Exception as e:
        print(f"Alternative handle creation failed: {e}")
        # 如果失败，返回简单的圆柱体作为手柄
        handle = Part.makeCylinder(0.05, 0.8)
        handle.Placement.Base = App.Vector(1.0, 0, 0.4)
        handle.Placement.Rotation = App.Rotation(App.Vector(0, 1, 0), 90)
        return handle

def assemble_mug():
    doc = App.newDocument("Mug")

    cup_body = create_cup_body()
    cup_bottom = create_cup_bottom()
    
    # 尝试创建手柄，如果失败则使用备选方案
    try:
        handle = create_handle()
    except Exception as e:
        print(f"Primary handle creation failed: {e}")
        handle = create_handle_alternative()

    # 将杯底移动到适当位置
    cup_bottom.Placement.Base.z = -0.25  # 将杯底放置在杯身下方

    # 组合所有部件
    combined = Part.makeCompound([cup_body, cup_bottom, handle])
    part = doc.addObject("Part::Feature", "Mug")
    part.Shape = combined



if __name__ == "__main__":
    assemble_mug()