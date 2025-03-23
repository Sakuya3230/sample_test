# -*- coding: utf-8 -*-

"""
#　選択したルート階層以下のジョイントに円を描画する
sel = cmds.ls(sl=True, dag=True, l=True, typ="joint")
draw_node = cmds.createNode("drawTest")

attr_indices = {}
for i, jnt in enumerate(sel):
    cmds.connectAttr("{}.worldMatrix[0]".format(jnt),"{}.drawCircleList[{}].inputWorldMatrix".format(draw_node, i))
    cmds.setAttr("{}.drawCircleList[{}].radius".format(draw_node, i), 1)
    #cmds.setAttr("{}.drawCircleList[{}].outerColor".format(draw_node, i), 0.3, 0.3, 0.3, type="double3")
    
    parent = cmds.listRelatives(jnt, p=True, f=True, typ="joint")
    if parent:
        attr_index = attr_indices.get(parent[0])
        if attr_index is not None:
            cmds.setAttr("{}.drawCircleList[{}].parentIndex".format(draw_node, i), attr_index)
    attr_indices[jnt] = i
    cmds.connectAttr("{}.radius".format(jnt),"{}.drawCircleList[{}].radius".format(draw_node, i))
"""

import maya.api.OpenMaya as om2
import maya.api.OpenMayaUI as omui2
import maya.api.OpenMayaRender as omr2

import sys
import math
import numpy as np


def maya_useNewAPI():
    pass

class DrawTestNode(omui2.MPxLocatorNode):
    # Plug-in info
    kPluginNodeName     = "drawTest"
    kPluginNodeId       = om2.MTypeId(0x87EFE)
    kPluginNodeClassify = "drawdb/geometry/drawTest"
    drawRegistrantId    = "drawTestPlugin"
    
    # attributes
    aDrawEnable         = None
    aSelectedColor      = None
    aXray               = None

    aDrawCircleList     = None
    aDrawCircle         = None
    aParentIndex        = None
    
    aPosition           = None
    aRadius             = None
    aInnerSize          = None
    aOuterSize          = None
    aSubdivisions       = None
    aInnerColor         = None
    aOuterColor         = None
    aOpacity            = None
    
    aDrawText           = None
    aText               = None
    aTextSize           = None
    aTextPosition       = None
    aTextColor          = None
    aTextOpacity        = None
    
    aInputWorldMatrix   = None
      
    def __init__(self):
        omui2.MPxLocatorNode.__init__(self)
        
    def draw(self, view, path, style, status):
        pass

    def compute(self, plug, dataBlock):
        return None

    def isBounded(self):
        return True

    def boundingBox(self):
        return om2.MBoundingBox(om2.MPoint(1.0, 1.0, 1.0), om2.MPoint(-1.0, -1.0, -1.0))

    @staticmethod
    def creator():
        return DrawTestNode()
    
    @staticmethod
    def initialize():
        """
        アトリビュートの作成
        """
        fnTypedAttr = om2.MFnTypedAttribute()
        fnNumericAttr = om2.MFnNumericAttribute()
        fnMatrixAttr = om2.MFnMatrixAttribute()
        fnCompAttr = om2.MFnCompoundAttribute()

        # ----------------------------------------------------------------------------------
        # COMMON ATTRIBUTES
        # ----------------------------------------------------------------------------------
        # enable attribute
        DrawTestNode.aDrawEnable = fnNumericAttr.create("drawEnable", "dn", om2.MFnNumericData.kBoolean, 1)
        DrawTestNode.addAttribute(DrawTestNode.aDrawEnable)

        # selectedHiLite attribute
        DrawTestNode.aSelectedColor = fnNumericAttr.create("selectedColor", "sc", om2.MFnNumericData.kBoolean, 0)
        DrawTestNode.addAttribute(DrawTestNode.aSelectedColor)

        # Xray attribute
        DrawTestNode.aXray = fnNumericAttr.create("xray", "xr", om2.MFnNumericData.kBoolean, 0)
        DrawTestNode.addAttribute(DrawTestNode.aXray)

        # ----------------------------------------------------------------------------------
        # DRAW CIRCLES ATTRIBUTES
        # ----------------------------------------------------------------------------------
        # 描画有効化
        DrawTestNode.aDrawCircle = fnNumericAttr.create("drawCircle", "dc", om2.MFnNumericData.kBoolean, 1)
        DrawTestNode.addAttribute(DrawTestNode.aDrawCircle)
        
        # 親のインデックス
        DrawTestNode.aParentIndex = fnNumericAttr.create("parentIndex", "pi", om2.MFnNumericData.kInt, -1)
        fnNumericAttr.setMin(-1)
        DrawTestNode.addAttribute(DrawTestNode.aParentIndex)
        
        # 座標
        DrawTestNode.aPosition = fnNumericAttr.create("position", "p", om2.MFnNumericData.k3Float)
        DrawTestNode.addAttribute(DrawTestNode.aPosition)
        
        # 半径
        DrawTestNode.aRadius = fnNumericAttr.create("radius", "r", om2.MFnNumericData.kFloat, 2.0)
        fnNumericAttr.setMin(0.0)
        fnNumericAttr.setMax(10.0)
        DrawTestNode.addAttribute(DrawTestNode.aRadius)

        # インナーの半径割合
        DrawTestNode.aInnerSize = fnNumericAttr.create("innerSize", "is", om2.MFnNumericData.kFloat, 0.5)
        fnNumericAttr.setMin(0.0)
        fnNumericAttr.setSoftMax(1.0)
        DrawTestNode.addAttribute(DrawTestNode.aInnerSize)
        
        # アウターの半径割合
        DrawTestNode.aOuterSize = fnNumericAttr.create("outerSize", "os", om2.MFnNumericData.kFloat, 0.9)
        fnNumericAttr.setMin(0.0)
        fnNumericAttr.setSoftMax(1.0)
        DrawTestNode.addAttribute(DrawTestNode.aOuterSize)

        # サブディビジョン
        DrawTestNode.aSubdivisions = fnNumericAttr.create("subdivisions", "sd", om2.MFnNumericData.kInt, 32)
        fnNumericAttr.setMin(3)
        fnNumericAttr.setMax(256)
        DrawTestNode.addAttribute(DrawTestNode.aSubdivisions)

        # カラー
        DrawTestNode.aInnerColor = fnNumericAttr.create("innerColor", "ico", om2.MFnNumericData.k3Float)
        fnNumericAttr.default = (0.0, 1.0, 1.0)
        fnNumericAttr.usedAsColor = True
        DrawTestNode.addAttribute(DrawTestNode.aInnerColor)
        
        # カラー
        DrawTestNode.aOuterColor = fnNumericAttr.create("outerColor", "oco", om2.MFnNumericData.k3Float)
        fnNumericAttr.default = (0.5, 0.5, 0.5)
        fnNumericAttr.usedAsColor = True
        DrawTestNode.addAttribute(DrawTestNode.aOuterColor)
        
        # 不透明度
        DrawTestNode.aOpacity = fnNumericAttr.create("opacity", "o", om2.MFnNumericData.kFloat, 1.0)
        fnNumericAttr.setMin(0.0)
        fnNumericAttr.setSoftMax(1.0)
        DrawTestNode.addAttribute(DrawTestNode.aOpacity)
        
        # 文字の描画有効化
        DrawTestNode.aDrawText = fnNumericAttr.create("drawText", "dtx", om2.MFnNumericData.kBoolean, 0)
        DrawTestNode.addAttribute(DrawTestNode.aDrawText)
        
        # 文字
        DrawTestNode.aText = fnTypedAttr.create("text", "tx", om2.MFnData.kString)
        DrawTestNode.addAttribute(DrawTestNode.aText)
        
        # 文字の座標
        DrawTestNode.aTextPosition = fnNumericAttr.create("textPosition", "txp", om2.MFnNumericData.k3Float)
        DrawTestNode.addAttribute(DrawTestNode.aTextPosition)

        # 文字のサイズ
        DrawTestNode.aTextSize = fnNumericAttr.create("textSize", "txs", om2.MFnNumericData.kInt, 12)
        fnNumericAttr.setMin(1)
        fnNumericAttr.setSoftMax(50)
        DrawTestNode.addAttribute(DrawTestNode.aTextSize)
        
        # 文字のカラー
        DrawTestNode.aTextColor = fnNumericAttr.create("textColor", "txc", om2.MFnNumericData.k3Float)
        fnNumericAttr.default = (1.0, 0.0, 0.0)
        fnNumericAttr.usedAsColor = True
        DrawTestNode.addAttribute(DrawTestNode.aTextColor)
        
        # 文字の不透明度
        DrawTestNode.aTextOpacity = fnNumericAttr.create("textOpacity", "txo", om2.MFnNumericData.kFloat, 1.0)
        fnNumericAttr.setMin(0.0)
        fnNumericAttr.setSoftMax(1.0)
        DrawTestNode.addAttribute(DrawTestNode.aTextOpacity)

        # 入力行列
        DrawTestNode.aInputWorldMatrix = fnMatrixAttr.create("inputWorldMatrix", "iwm")
        DrawTestNode.addAttribute(DrawTestNode.aInputWorldMatrix)

        DrawTestNode.aDrawCircleList = fnCompAttr.create("drawCircleList", "dcl")
        fnCompAttr.readable = True
        fnCompAttr.array = True
        fnCompAttr.indexMatters = False
        fnCompAttr.addChild(DrawTestNode.aDrawCircle)
        fnCompAttr.addChild(DrawTestNode.aParentIndex)
        fnCompAttr.addChild(DrawTestNode.aPosition)
        fnCompAttr.addChild(DrawTestNode.aRadius)
        fnCompAttr.addChild(DrawTestNode.aInnerSize)
        fnCompAttr.addChild(DrawTestNode.aOuterSize)
        fnCompAttr.addChild(DrawTestNode.aSubdivisions)
        fnCompAttr.addChild(DrawTestNode.aInnerColor)
        fnCompAttr.addChild(DrawTestNode.aOuterColor)
        fnCompAttr.addChild(DrawTestNode.aOpacity)
        fnCompAttr.addChild(DrawTestNode.aDrawText)
        fnCompAttr.addChild(DrawTestNode.aText)
        fnCompAttr.addChild(DrawTestNode.aTextSize)
        fnCompAttr.addChild(DrawTestNode.aTextPosition)
        fnCompAttr.addChild(DrawTestNode.aTextColor)
        fnCompAttr.addChild(DrawTestNode.aTextOpacity)
        fnCompAttr.addChild(DrawTestNode.aInputWorldMatrix)
        DrawTestNode.addAttribute(DrawTestNode.aDrawCircleList)

class DrawTestData(om2.MUserData):
    def __init__(self):
        om2.MUserData.__init__(self, False)
        self.xray                   = False
        
        self.circle_inner_colors    = []
        self.circle_outer_colors    = []
        self.circle_inner_triangles = []
        self.circle_outer_triangles = []
        
        self.parent_triangle_points = []
        self.parent_triangle_colors = []
        
        self.text                   = []
        self.text_size              = []
        self.text_position          = []
        self.text_color             = []
        
class DrawTest(omr2.MPxDrawOverride):
    def __init__(self, obj):
        omr2.MPxDrawOverride.__init__(self, obj, DrawTest.draw)

    @staticmethod
    def draw(context, data):
        pass

    @staticmethod
    def creator(obj):
        return DrawTest(obj)

    def supportedDrawAPIs(self):
        return omr2.MRenderer.kOpenGL | omr2.MRenderer.kDirectX11 | omr2.MRenderer.kOpenGLCoreProfile

    def isBounded(self, objPath, cameraPath):
        return True

    def boundingBox(self, objPath, cameraPath):
        node = objPath.node()
        fn_node = om2.MFnDependencyNode(node)
        draw_circle_list_plug = fn_node.findPlug(DrawTestNode.aDrawCircleList, False)

        # バウンディングボックスを初期化
        bbox = om2.MBoundingBox()
        for i in range(draw_circle_list_plug.numElements()):
            num_plug = draw_circle_list_plug.elementByPhysicalIndex(i)

            # ワールドマトリクスを取得
            world_matrix_obj = num_plug.child(DrawTestNode.aInputWorldMatrix).asMObject()
            world_matrix_data = om2.MFnMatrixData(world_matrix_obj)
            world_matrix = world_matrix_data.matrix()

            # ローカル座標をワールド座標に変換
            pos_obj = num_plug.child(DrawTestNode.aPosition).asMObject()
            local_pos = om2.MPoint(om2.MFnNumericData(pos_obj).getData())
            position = local_pos * world_matrix

            # 半径を取得
            radius = num_plug.child(DrawTestNode.aRadius).asFloat()

            # 円のバウンディングボックスを計算
            min_point = om2.MPoint(position.x - radius, position.y - radius, position.z - radius)
            max_point = om2.MPoint(position.x + radius, position.y + radius, position.z + radius)

            # バウンディングボックスを拡張
            bbox.expand(min_point)
            bbox.expand(max_point)
        return bbox

    def hasUIDrawables(self):
        return True
        
    def prepareForDraw(self, objPath, cameraPath, frameContext, oldData):
        data = oldData
        if not isinstance(data, DrawTestData):
            data = DrawTestData()
        
        node = objPath.node()
        if node.isNull():
            return None
        
        fn_node = om2.MFnDependencyNode(node)
        # 描画の有効化
        draw_enable = fn_node.findPlug(DrawTestNode.aDrawEnable, False).asBool()
        if not draw_enable:
            return None
        
        # 選択の描画
        selected_value = fn_node.findPlug(DrawTestNode.aSelectedColor, False).asBool()
        # 選択されているか判定用
        is_selected = False
        if selected_value:
            status = omui2.M3dView.displayStatus(objPath)
            if (omui2.M3dView.kActive == status or
                    omui2.M3dView.kHilite == status or
                    omui2.M3dView.kLead == status or
                    omui2.M3dView.kActiveTemplate == status or
                    omui2.M3dView.kActiveAffected == status):
                selected_color = omr2.MGeometryUtilities.wireframeColor(objPath)
                is_selected = True
        
        # xRay有効化
        xray_value = fn_node.findPlug(DrawTestNode.aXray, False).asBool()
        data.xray = xray_value
        
        # サークル描画配列
        draw_circle_list_plug = fn_node.findPlug(DrawTestNode.aDrawCircleList, False)
        # 親子関係用の値
        circle_indices          = []
        circle_center_points    = {}
        circle_radius           = {}
        # 配列の値
        color_inner_values      = []
        color_outer_values      = []
        inner_triangles_values  = []
        outer_triangles_values = []
        text_values             = []
        text_size_values        = []
        text_position_values    = []
        text_color_values       = []
        for i in list(range(draw_circle_list_plug.numElements())):
            num_plug = draw_circle_list_plug.elementByPhysicalIndex(i)
            
            # 描画有効化されていなければデータを取得しない
            draw_enable = num_plug.child(DrawTestNode.aDrawCircle).asBool()
            if not draw_enable:
                continue
            
            # ワールドマトリックスを取得
            world_matrix_obj = num_plug.child(DrawTestNode.aInputWorldMatrix).asMObject()
            world_matrix_data = om2.MFnMatrixData(world_matrix_obj)
            world_matrix = world_matrix_data.matrix()
            
            # 円のアトリビュートから値を取得
            pos_obj = num_plug.child(DrawTestNode.aPosition).asMObject()
            local_position = om2.MPoint(om2.MFnNumericData(pos_obj).getData())
            position = local_position * world_matrix
            
            radius = num_plug.child(DrawTestNode.aRadius).asFloat()
            inner_radius =  radius * num_plug.child(DrawTestNode.aInnerSize).asFloat()
            outer_radius =  radius * num_plug.child(DrawTestNode.aOuterSize).asFloat()
            subdivisions = num_plug.child(DrawTestNode.aSubdivisions).asInt()
  
            # 親子関係用の値を格納
            circle_indices.append(i)
            circle_center_points[i] = position
            circle_radius[i] = radius
            
            if is_selected:
                color_inner_values.append(selected_color)
            else:
                color_obj = num_plug.child(DrawTestNode.aInnerColor).asMObject()
                color = om2.MColor(om2.MFnNumericData(color_obj).getData())
                color.a = num_plug.child(DrawTestNode.aOpacity).asFloat()
                color_inner_values.append(color)
                
                color_obj = num_plug.child(DrawTestNode.aOuterColor).asMObject()
                color = om2.MColor(om2.MFnNumericData(color_obj).getData())
                color.a = num_plug.child(DrawTestNode.aOpacity).asFloat()
                color_outer_values.append(color)
            
            # テキストの描画
            draw_text = num_plug.child(DrawTestNode.aDrawText).asBool()
            if draw_text:
                text_values.append(num_plug.child(DrawTestNode.aText).asString())
                text_size_values.append(num_plug.child(DrawTestNode.aTextSize).asInt())
                
                text_pos_obj = num_plug.child(DrawTestNode.aTextPosition).asMObject()
                text_local_pos = om2.MVector(om2.MFnNumericData(text_pos_obj).getData())
                # 文字の座標
                text_position_values.append(om2.MPoint(text_local_pos + om2.MVector(world_matrix[12], world_matrix[13], world_matrix[14])))
                
                if is_selected:
                    text_color_values.append(selected_color)
                else:
                    text_color_obj = num_plug.child(DrawTestNode.aTextColor).asMObject()
                    text_color = om2.MColor(om2.MFnNumericData(text_color_obj).getData())
                    text_color.a = num_plug.child(DrawTestNode.aTextOpacity).asFloat()
                    text_color_values.append(text_color)

            # カメラの位置を取得
            camera_matrix = cameraPath.inclusiveMatrix()
            camera_position = om2.MPoint(camera_matrix[12], camera_matrix[13], camera_matrix[14])

            # カメラへの方向ベクトルを計算
            to_camera = camera_position - position
            to_camera.normalize()

            # カメラ方向に向けるためのベクトル計算
            up_vector = to_camera
            right_vector = om2.MVector(0, 0, 1) ^ up_vector
            right_vector.normalize()
            forward_vector = up_vector ^ right_vector
            forward_vector.normalize()

            # カメラ基準の回転行列作成
            rot_matrix = om2.MMatrix([
                right_vector.x, right_vector.y, right_vector.z, 0,
                up_vector.x, up_vector.y, up_vector.z, 0,
                forward_vector.x, forward_vector.y, forward_vector.z, 0,
                0, 0, 0, 1
            ])

            # カメラの向きで円の頂点座標を取得
            circle_points = []
            circle_points2 = []
            position = om2.MVector(position)
            for x in range(subdivisions):
                theta = (x / subdivisions) * 2.0 * math.pi
                local_outer = om2.MVector(outer_radius * math.cos(theta), 0, outer_radius * math.sin(theta))

                world_center = local_outer * rot_matrix + position

                # 内側の円の範囲制限
                if inner_radius < outer_radius and inner_radius < radius:
                    local_inner = om2.MVector(inner_radius * math.cos(theta), 0, inner_radius * math.sin(theta))
                    world_inner = local_inner * rot_matrix + position
                    circle_points.append((world_center.x, world_center.y, world_center.z, 1.0))
                    circle_points.append((world_inner.x, world_inner.y, world_inner.z, 1.0))
                
                # 外側の円の範囲制限
                if outer_radius < radius:
                    local = om2.MVector(radius * math.cos(theta), 0, radius * math.sin(theta))
                    world_outer = local * rot_matrix + position
                    circle_points2.append((world_outer.x, world_outer.y, world_outer.z, 1.0))
                    circle_points2.append((world_center.x, world_center.y, world_center.z, 1.0))
                    
                
            # 円の三角形の座標で並べる
            triangle_points = []
            triangle_points2 = []
            for x in range(subdivisions):
                idx1 = x * 2
                idx2 = (x * 2 + 1) % (subdivisions * 2)
                idx3 = (x * 2 + 2) % (subdivisions * 2)
                idx4 = (x * 2 + 3) % (subdivisions * 2)

                # 内側の円の範囲制限
                if inner_radius < outer_radius and inner_radius < radius:
                    quad_points = [circle_points[idx] for idx in [idx1, idx2, idx3, idx3, idx2, idx4]]
                    triangle_points.extend(quad_points)
                       
                # 外側の円の範囲制限 
                if outer_radius < radius:         
                    quad_points2 = [circle_points2[idx] for idx in [idx1, idx2, idx3, idx3, idx2, idx4]]
                    triangle_points2.extend(quad_points2)
                    
            # 3角形の座標のアレイ
            inner_triangles_values.append(om2.MPointArray(triangle_points))
            outer_triangles_values.append(om2.MPointArray(triangle_points2))
                
        # 親子を繋げる三角形の描画
        parent_triangle_points = []
        parent_triangle_colors = []
        for i in list(range(draw_circle_list_plug.numElements())):
            num_plug = draw_circle_list_plug.elementByPhysicalIndex(i)
            # 親の円のインデックスを取得
            parent_index = num_plug.child(DrawTestNode.aParentIndex).asInt()
            # 親のインデックスがない場合or自身のインデックスと同じ場合
            if parent_index not in circle_indices or parent_index == i:
                continue
            
            parent_pos = om2.MVector(circle_center_points[parent_index])
            child_pos = om2.MVector(circle_center_points[i])
            parent_radius = circle_radius[parent_index]
            child_radius = circle_radius[i]

            # 円同士の長さ
            vec = np.array(child_pos) - np.array(parent_pos)
            length = np.linalg.norm(vec)

            if length > 0:
                # 親と子の円のベクトル
                vec_center = child_pos - parent_pos
                camera_vec = om2.MVector(camera_position)
                
                # 親の円のカメラ方向の2Dベクトル
                vec_to_camera_parent = camera_vec - parent_pos
                vec_to_camera_parent.normalize()
                projected_vec_parent = vec_center - (vec_center * vec_to_camera_parent) * vec_to_camera_parent
                projected_vec_parent.normalize()
                
                # 子供の円のカメラ方向の2Dベクトル
                vec_to_camera_child = camera_vec - child_pos
                vec_to_camera_child.normalize()
                projected_vec_child = vec_center - (vec_center * vec_to_camera_child) * vec_to_camera_child
                projected_vec_child.normalize()

                # 円周上の接点を取得
                contact_point_parent = parent_pos + projected_vec_parent * parent_radius
                contact_point_child = child_pos - projected_vec_child * child_radius
                
                # 親と子の円の最短の円周上の点のベクトル
                shortest_vec = contact_point_parent - contact_point_child
                vec_length = np.linalg.norm(shortest_vec)
                
                # 接点が同じ位置にある場合スキップ
                if vec_length == 0:
                    continue

                # 単位ベクトル化
                V_unit = shortest_vec / vec_length

                # カメラ方向のベクトル
                to_camera = camera_vec - contact_point_parent
                to_camera /= np.linalg.norm(to_camera)

                # カメラ方向に最も近いベクトルを求める
                base_direction = np.cross(V_unit, to_camera)
                base_direction /= np.linalg.norm(base_direction)

                # 三角形の底辺の中心点から両端の座標計算
                triangle_base_point1 = contact_point_parent + base_direction * (parent_radius)
                triangle_base_point2 = contact_point_parent - base_direction * (parent_radius)
                # 三角形の座標とカラーを格納 
                parent_triangle_points.append(om2.MPointArray([contact_point_child, triangle_base_point1, triangle_base_point2]))
                parent_triangle_colors.append(color_inner_values[circle_indices.index(parent_index)])
            
        # データの格納
        data.circle_inner_colors    = color_inner_values
        data.circle_outer_colors    = color_outer_values
        data.circle_inner_triangles = inner_triangles_values
        data.circle_outer_triangles = outer_triangles_values
        data.text                   = text_values
        data.text_size              = text_size_values
        data.text_position          = text_position_values
        data.text_color             = text_color_values
        data.parent_triangle_points = parent_triangle_points
        data.parent_triangle_colors = parent_triangle_colors

        return data

    def addUIDrawables(self, objPath, drawManager, frameContext, data):
        if data is None:
            return
        
        if data.xray or int(frameContext.getDisplayStyle()) == omr2.MFrameContext.kXray+1:
            drawManager.beginDrawInXray()
        else:
            drawManager.beginDrawable()

        # 内側の円の描画
        for i in list(range(len(data.circle_inner_colors))):
            drawManager.setColor(data.circle_inner_colors[i])
            drawManager.mesh(omr2.MUIDrawManager.kTriangles, data.circle_inner_triangles[i])
        
        # 外側の円の描画
        for i in list(range(len(data.circle_outer_colors))):
            drawManager.setColor(data.circle_outer_colors[i])
            drawManager.mesh(omr2.MUIDrawManager.kTriangles, data.circle_outer_triangles[i])
        
        # 親子関係の三角形の描画
        for i in list(range(len(data.parent_triangle_colors))):
            drawManager.setColor(data.parent_triangle_colors[i])
            drawManager.mesh(omr2.MUIDrawManager.kTriangles, data.parent_triangle_points[i])
                
        # 文字の描画
        for i in list(range(len(data.text))):
            drawManager.setFontSize(data.text_size[i])
            drawManager.setColor(data.text_color[i])
            drawManager.text(data.text_position[i], data.text[i], omr2.MUIDrawManager.kCenter)

        if data.xray or frameContext.getDisplayStyle() == omr2.MFrameContext.kXray+1:
            drawManager.endDrawInXray()
        else:
            drawManager.endDrawable()

# ----------------------------------------------------------------------------------
# Plug-in initialization.
# ----------------------------------------------------------------------------------
def initializePlugin(mObject):
    mPlugin = om2.MFnPlugin(mObject, "user", "1.0", "Any")
    try:
        mPlugin.registerNode(DrawTestNode.kPluginNodeName,
                             DrawTestNode.kPluginNodeId,
                             DrawTestNode.creator,
                             DrawTestNode.initialize,
                             om2.MPxNode.kLocatorNode,
                             DrawTestNode.kPluginNodeClassify)

        omr2.MDrawRegistry.registerDrawOverrideCreator(DrawTestNode.kPluginNodeClassify,
                                                       DrawTestNode.drawRegistrantId,
                                                       DrawTest.creator)

    except:
        sys.stderr.write("Failed to register node: " + DrawTestNode.kPluginNodeName)
        raise

def uninitializePlugin(mObject):
    mPlugin = om2.MFnPlugin(mObject)
    try:
        mPlugin.deregisterNode(DrawTestNode.kPluginNodeId)
        omr2.MDrawRegistry.deregisterDrawOverrideCreator(DrawTestNode.kPluginNodeClassify, DrawTestNode.drawRegistrantId)

    except:
        sys.stderr.write("Failed to deregister node: " + DrawTestNode.kPluginNodeName)
        raise


