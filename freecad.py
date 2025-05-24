import FreeCAD as App
import Part

# 创建新文档
doc = App.newDocument("Pan")

# 步骤1: 绘制锅身外壳
# 创建锅身外壳 - 圆柱体
pan_body = Part.makeCylinder(130, 60)  # 直径260mm(半径130mm), 高度60mm
pan_body_obj = doc.addObject("Part::Feature", "PanBody")
pan_body_obj.Shape = pan_body

# 步骤2: 挖出锅身内腔
# 创建内腔圆柱体用于挖空
inner_cavity = Part.makeCylinder(120, 50)  # 直径240mm(半径120mm), 高度50mm
# 将内腔向上移动10mm，留出锅底厚度
inner_cavity.translate(App.Vector(0, 0, 10))
inner_cavity_obj = doc.addObject("Part::Feature", "InnerCavity")
inner_cavity_obj.Shape = inner_cavity

# 使用布尔运算从锅身外壳中减去内腔
pan_hollow = pan_body.cut(inner_cavity)
pan_hollow_obj = doc.addObject("Part::Feature", "PanHollow")
pan_hollow_obj.Shape = pan_hollow

# 步骤3: 绘制锅柄
# 创建锅柄 - 圆柱体
handle = Part.makeCylinder(7.5, 180)  # 直径15mm(半径7.5mm), 长度180mm
# 旋转锅柄使其水平
handle.rotate(App.Vector(0, 0, 0), App.Vector(0, 1, 0), 90)
# 将锅柄移动到锅身侧面，高度为锅身中心高度30mm
handle.translate(App.Vector(130 + 90, 0, 30))  # X方向：锅身半径+锅柄长度一半
handle_obj = doc.addObject("Part::Feature", "Handle")
handle_obj.Shape = handle

# 重新计算文档
doc.recompute()