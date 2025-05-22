import FreeCAD as App
import Part

def create_cone(r_top, r_bottom, height):
    """
    创建一个锥形主体。

    参数:
    r_top (float): 顶部开口半径
    r_bottom (float): 底部开口半径
    height (float): 锥形的高度

    返回:
    Part::Feature: 锥形主体
    """
    # 创建两个圆
    top_circle = Part.makeCircle(r_top, App.Vector(0, 0, 0))
    bottom_circle = Part.makeCircle(r_bottom, App.Vector(0, 0, -height))

    # 创建线段连接两个圆的中心点
    line = Part.makeLine(App.Vector(0, 0, 0), App.Vector(0, 0, -height))

    # 创建锥形主体
    cone = Part.makeLoft([top_circle, bottom_circle], True)
    return cone

def create_outlet(diameter, height, position):
    """
    创建一个小圆柱体作为出口。

    参数:
    diameter (float): 出口直径
    height (float): 出口高度
    position (App.Vector): 出口的位置

    返回:
    Part::Feature: 出口部分
    """
    radius = diameter / 2
    outlet = Part.makeCylinder(radius, height, position)
    return outlet

def create_funnel(r_top, r_bottom, height, d_outlet, h_outlet):
    """
    创建一个完整的漏斗模型。

    参数:
    r_top (float): 漏斗顶部开口半径
    r_bottom (float): 漏斗底部开口半径
    height (float): 漏斗高度
    d_outlet (float): 出口直径
    h_outlet (float): 出口高度

    返回:
    Part::Compound: 完整的漏斗模型
    """
    # # 创建锥形主体
    # cone = create_cone(r_top, r_bottom, height)

    # 创建出口部分
    outlet_position = App.Vector(0, 0, -height + h_outlet/2)
    outlet = create_outlet(d_outlet, h_outlet, outlet_position)

    # 将锥形主体和出口部分组合在一起
    # funnel = Part.makeCompound([cone, outlet])

    return outlet

# 设置参数
r_top = 50  # 顶部开口半径
r_bottom = 20  # 底部开口半径
height = 100  # 漏斗高度
d_outlet = 10  # 出口直径
h_outlet = 20  # 出口高度

# 创建漏斗
funnel = create_funnel(r_top, r_bottom, height, d_outlet, h_outlet)

# 显示漏斗
Part.show(funnel)