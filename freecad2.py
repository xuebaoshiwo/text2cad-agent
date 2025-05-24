import FreeCAD as App
import Part

# 创建新文档
doc = App.newDocument("FryingPan")

# 步骤1: 绘制锅身外壳
# 创建锅身外壳 - 圆柱体
pan_body = Part.makeCylinder(130, 60)  # 直径260mm(半径130mm), 高度60mm

# 步骤2: 绘制锅身内腔
# 创建锅身内腔 - 圆柱体（用于挖空）
inner_cavity = Part.makeCylinder(120, 50)  # 直径240mm(半径120mm), 高度50mm

# 设置内腔位置，底面高度为10mm（锅底厚度）
inner_cavity.translate(App.Vector(0, 0, 10))

# 挖空锅身 - 从外壳中减去内腔
pan_body = pan_body.cut(inner_cavity)

# 将挖空后的锅身添加到文档中
pan_body_obj = doc.addObject("Part::Feature", "PanBody")
pan_body_obj.Shape = pan_body



# 步骤3: 绘制锅柄
# 创建锅柄 - 圆柱体
handle = Part.makeCylinder(7.5, 180)  # 直径15mm(半径7.5mm), 长度180mm

# 旋转锅柄使其水平放置（绕Y轴旋转90度）
handle.rotate(App.Vector(0, 0, 0), App.Vector(0, 1, 0), 90)

# 设置锅柄位置，与锅身分离，距离锅身边缘10mm
handle.translate(App.Vector(130, 0, 30))

# 将锅柄添加到文档中
handle_obj = doc.addObject("Part::Feature", "Handle")
handle_obj.Shape = handle

# 重新计算文档
doc.recompute()