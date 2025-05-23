import FreeCAD as App
import Part
from FreeCAD import Base

def create_handle(doc):
    # 创建C形把手
    # 简化把手创建方法，使用基本几何体组合
    handle_radius = 0.35  # 把手管状结构的半径
    bottom_offset = 1.0  # 把手底部距离杯底的高度
    handle_height = 4.0  # 把手高度
    handle_extension = 1.5  # 把手从杯身延伸出的距离

    # 创建把手的底部连接部分 - 水平圆柱体
    handle_bottom = Part.makeCylinder(
        handle_radius, 
        handle_extension, 
        Base.Vector(2.0, 0, bottom_offset), 
        Base.Vector(1, 0, 0)
    )

    # 创建把手的顶部连接部分 - 水平圆柱体
    handle_top = Part.makeCylinder(
        handle_radius, 
        handle_extension, 
        Base.Vector(2.0, 0, bottom_offset + handle_height), 
        Base.Vector(1, 0, 0)
    )

    # 创建把手的垂直部分 - 垂直圆柱体
    handle_vertical = Part.makeCylinder(
        handle_radius, 
        handle_height, 
        Base.Vector(2.0 + handle_extension, 0, bottom_offset), 
        Base.Vector(0, 0, 1)
    )

    # 创建把手底部圆角连接 - 球体
    handle_bottom_corner = Part.makeSphere(
        handle_radius, 
        Base.Vector(2.0 + handle_extension, 0, bottom_offset)
    )

    # 创建把手顶部圆角连接 - 球体
    handle_top_corner = Part.makeSphere(
        handle_radius, 
        Base.Vector(2.0 + handle_extension, 0, bottom_offset + handle_height)
    )

    # 融合把手的各个部分
    handle_shape = handle_bottom.fuse([
        handle_top,
        handle_vertical,
        handle_bottom_corner,
        handle_top_corner
    ])
    
    # 创建FreeCAD对象
    handle = doc.addObject("Part::Feature", "Handle")
    handle.Shape = handle_shape

    return handle