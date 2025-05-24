import FreeCAD as App
import Part
from FreeCAD import Base

# 创建新文档
doc = App.newDocument("MugModel")

# 步骤1: 绘制杯身外壳
# 创建圆柱体作为杯身外壳
# 参数：半径=1.5 (直径3.0), 高度=3.5
cup_outer = Part.makeCylinder(1.5, 3.5)

# 创建外壳对象并添加到文档
cup_outer_obj = doc.addObject("Part::Feature", "CupOuter")
cup_outer_obj.Shape = cup_outer

# 步骤2: 绘制杯身内腔
# 创建圆柱体作为杯身内腔
# 参数：半径=1.3 (直径2.6), 高度=3.2
# 位置：底面向上偏移0.3单位形成杯底厚度
cup_inner = Part.makeCylinder(1.3, 3.2)
cup_inner.translate(App.Vector(0, 0, 0.3))

# 创建内腔对象并添加到文档
cup_inner_obj = doc.addObject("Part::Feature", "CupInner")
cup_inner_obj.Shape = cup_inner

# 步骤3: 绘制把手主体
# 创建C形把手，使用基本几何体组合
handle_radius = 0.15  # 把手管状结构的半径（管径0.3的一半）
bottom_offset = 0.8   # 把手底部距离杯底的高度
handle_height = 2.0   # 把手高度
handle_extension = 1.2  # 把手从杯身延伸出的距离

# 创建把手的底部连接部分 - 水平圆柱体
handle_bottom = Part.makeCylinder(
    handle_radius, 
    handle_extension, 
    Base.Vector(1.5, 0, bottom_offset), 
    Base.Vector(1, 0, 0)
)

# 创建把手的顶部连接部分 - 水平圆柱体
handle_top = Part.makeCylinder(
    handle_radius, 
    handle_extension, 
    Base.Vector(1.5, 0, bottom_offset + handle_height), 
    Base.Vector(1, 0, 0)
)

# 创建把手的垂直部分 - 垂直圆柱体
handle_vertical = Part.makeCylinder(
    handle_radius, 
    handle_height, 
    Base.Vector(1.5 + handle_extension, 0, bottom_offset), 
    Base.Vector(0, 0, 1)
)

# 创建把手底部圆角连接 - 球体
handle_bottom_corner = Part.makeSphere(
    handle_radius, 
    Base.Vector(1.5 + handle_extension, 0, bottom_offset)
)

# 创建把手顶部圆角连接 - 球体
handle_top_corner = Part.makeSphere(
    handle_radius, 
    Base.Vector(1.5 + handle_extension, 0, bottom_offset + handle_height)
)

# 融合把手的各个部分
handle_shape = handle_bottom.fuse([
    handle_top,
    handle_vertical,
    handle_bottom_corner,
    handle_top_corner
])

# 创建把手对象并添加到文档
handle_obj = doc.addObject("Part::Feature", "Handle")
handle_obj.Shape = handle_shape

# 重新计算文档
doc.recompute()