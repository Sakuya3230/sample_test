# -*- coding: utf-8 -*-

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
    aSubdivisions       = None
    aColor              = None
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

        # サブディビジョン
        DrawTestNode.aSubdivisions = fnNumericAttr.create("subdivisions", "sd", om2.MFnNumericData.kInt, 32)
        fnNumericAttr.setMin(3)
        fnNumericAttr.setMax(256)
        DrawTestNode.addAttribute(DrawTestNode.aSubdivisions)

        # カラー
        DrawTestNode.aColor = fnNumericAttr.create("color", "col", om2.MFnNumericData.k3Float)
        fnNumericAttr.default = (1.0, 0.0, 0.0)
        fnNumericAttr.usedAsColor = True
        DrawTestNode.addAttribute(DrawTestNode.aColor)
        
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
        fnCompAttr.addChild(DrawTestNode.aSubdivisions)
        fnCompAttr.addChild(DrawTestNode.aColor)
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
        self.circle_colors          = []
        self.circle_triangle_points = []
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
            position = local_pos * world_matrix  # ワールド座標

            # 半径を取得
            radius = num_plug.child(DrawTestNode.aRadius).asFloat()

            # 円のバウンディングボックスを計算
            min_point = om2.MPoint(position.x - radius, position.y - radius, position.z - radius)
            max_point = om2.MPoint(position.x + radius, position.y + radius, position.z + radius)

            # バウンディングボックスを拡張
            bbox.expand(min_point)
            bbox.expand(max_point)
            
        return bbox
        # return om2.MBoundingBox(om2.MPoint(1000.0, 1000.0, 1000.0), om2.MPoint(-1000.0, -1000.0, -1000.0))

    def hasUIDrawables(self):
        return True
        
    def prepareForDraw(self, objPath, cameraPath, frameContext, oldData):
        data = oldData
        if not isinstance(data, DrawTestData):
            data = DrawTestData()
        
        node = objPath.node()
        if node.isNull():
            return None
        
        fnNode = om2.MFnDependencyNode(node)
        # 描画の有効化
        draw_enable = fnNode.findPlug(DrawTestNode.aDrawEnable, False).asBool()
        if not draw_enable:
            return None
        
        # 選択の描画
        selected_value = fnNode.findPlug(DrawTestNode.aSelectedColor, False).asBool()
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
        xray_value = fnNode.findPlug(DrawTestNode.aXray, False).asBool()
        data.xray = xray_value
        
        # サークル描画配列
        draw_circle_list_plug = fnNode.findPlug(DrawTestNode.aDrawCircleList, False)
        # 親子関係用の値
        draw_indices            = []
        world_positions         = {}
        outer_radiuses          = {}
        # 配列の値
        color_values            = []
        triangle_points_values  = []
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
            local_pos = om2.MPoint(om2.MFnNumericData(pos_obj).getData())
            position = local_pos * world_matrix
            
            outer_radius = num_plug.child(DrawTestNode.aRadius).asFloat()
            inner_radius =  outer_radius * num_plug.child(DrawTestNode.aInnerSize).asFloat()
            subdivisions = num_plug.child(DrawTestNode.aSubdivisions).asInt()
            
            # 親子関係用の値を格納
            draw_indices.append(i)
            world_positions[i] = position
            outer_radiuses[i] = outer_radius
            
            if is_selected:
                color_values.append(selected_color)
            else:
                color_obj = num_plug.child(DrawTestNode.aColor).asMObject()
                color_values.append(om2.MColor(om2.MFnNumericData(color_obj).getData()))
            
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
                    text_color_values.append(om2.MColor(om2.MFnNumericData(text_color_obj).getData()))

            # 円の描画するための三角形の座標を取得
            # カメラの位置を取得
            cam_matrix = cameraPath.inclusiveMatrix()
            cam_position = om2.MPoint(cam_matrix[12], cam_matrix[13], cam_matrix[14])  # カメラのワールド座標

            # カメラへの方向ベクトルを計算
            to_camera = cam_position - position
            to_camera.normalize()

            # Y軸をカメラ方向に向けるためのベクトル計算
            up_vector = to_camera  # Y軸をカメラの方向に合わせる
            right_vector = om2.MVector(0, 0, 1) ^ up_vector  # ワールドZ軸とY軸の外積 → 右方向
            right_vector.normalize()

            forward_vector = up_vector ^ right_vector  # 右方向とY軸の外積 → 前方向
            forward_vector.normalize()

            # カメラ基準の回転行列作成
            rot_matrix = om2.MMatrix([
                right_vector.x, right_vector.y, right_vector.z, 0,
                up_vector.x, up_vector.y, up_vector.z, 0,
                forward_vector.x, forward_vector.y, forward_vector.z, 0,
                0, 0, 0, 1
            ])

            # 頂点データ（カメラ方向に回転）
            vertices = []
            indices = []
            outer_points = []
            position = om2.MVector(position)
            for x in range(subdivisions):
                theta = (x / subdivisions) * 2.0 * math.pi
                local_outer = om2.MVector(outer_radius * math.cos(theta), 0, outer_radius * math.sin(theta))
                local_inner = om2.MVector(inner_radius * math.cos(theta), 0, inner_radius * math.sin(theta))

                # 回転行列を適用
                world_outer = local_outer * rot_matrix + position
                world_inner = local_inner * rot_matrix + position

                outer_points.append((world_outer.x, world_outer.y, world_outer.z))
                vertices.append((world_outer.x, world_outer.y, world_outer.z, 1.0))
                vertices.append((world_inner.x, world_inner.y, world_inner.z, 1.0))

            # インデックスデータ（トライアングルストリップ用）
            for x in range(subdivisions):
                idx1 = x * 2
                idx2 = (x * 2 + 1) % (subdivisions * 2)
                idx3 = (x * 2 + 2) % (subdivisions * 2)
                idx4 = (x * 2 + 3) % (subdivisions * 2)
                indices.extend([idx1, idx2, idx3, idx3, idx2, idx4])

            # 3角形の座標のアレイ
            triangle_points = om2.MPointArray()
            for x in indices:
                triangle_points.append(vertices[x])
            triangle_points_values.append(triangle_points)
                
        # 子供の円まで三角形を描画
        child_triangle_vertices = []
        connect_color = []
        temp_points = []
        for i in list(range(draw_circle_list_plug.numElements())):
            num_plug = draw_circle_list_plug.elementByPhysicalIndex(i)
            # 子供のインデックスを取得
            parent_index = num_plug.child(DrawTestNode.aParentIndex).asInt()
            
            # 親のインデックスがない場合
            if parent_index not in draw_indices:
                continue
            # 自身のインデックスと同じ場合
            if parent_index == i:
                continue
            
            parent_pos = om2.MVector(world_positions[parent_index])
            child_pos = om2.MVector(world_positions[i])
            parent_radius = outer_radiuses[parent_index]
            child_radius = outer_radiuses[i]

            # カメラの位置を取得
            cam_matrix = cameraPath.inclusiveMatrix()
            cam_position = om2.MVector(cam_matrix[12], cam_matrix[13], cam_matrix[14])  # カメラのワールド座標

            # **修正: 法線をカメラ方向に向ける**
            normal = cam_position - parent_pos
            normal.normalize()

            # **修正: Y 軸を基準に底辺の向きを求める**
            up_vector = om2.MVector(0, 1, 0)  # **Y軸を維持**
            right_vector = up_vector ^ normal  # **外積で底辺の向きを求める**
            right_vector.normalize()

            vec = np.array(child_pos) - np.array(parent_pos)
            length = np.linalg.norm(vec)  # ベクトルの長さ

            if length > 0:
                # 単位ベクトル化
                unit_vec = vec / length
                right_vec = np.cross(unit_vec, right_vector)
                right_vec /= np.linalg.norm(right_vec)  # 正規化

                point_1, point_2 = self._get_shortest_circle_contact_points(parent_pos, child_pos, parent_radius, child_radius, cam_position)
                triangle_points = self.calculate_triangle_points(point_1, point_2, parent_radius, cam_position)
                if triangle_points:
                    base_left = om2.MPoint(triangle_points[0])
                    base_right = om2.MPoint(triangle_points[1])
                                        
                    # **三角形の頂点座標**
                    child_triangle_vertices.append(om2.MPointArray([point_2, base_left, base_right]))  # 上の頂点（2個目の円）
                    connect_color.append(color_values[draw_indices.index(parent_index)])
                    
                    temp_points.append([om2.MPoint(point_1), om2.MPoint(point_2)])
            
        # データの格納
        data.circle_colors          = color_values
        data.circle_triangle_points = triangle_points_values
        data.text                   = text_values
        data.text_size              = text_size_values
        data.text_position          = text_position_values
        data.text_color             = text_color_values
        data.parent_triangle_points = child_triangle_vertices     
        data.parent_triangle_colors = connect_color

        
        return data

    def _get_shortest_circle_contact_points(self, position_source, position_target, radius_1, radius_2, camera_position):
        """
        カメラの奥行きを考慮せず、2つの円の最短の接点を取得する
        """
        # 円の中心を結ぶベクトル
        vec_center = position_target - position_source

        # カメラ方向のベクトル(ソース)
        vec_to_camera_source = camera_position - position_source
        vec_to_camera_source.normalize()

        # カメラ方向のベクトル(ターゲット)
        vec_to_camera_target = camera_position - position_target
        vec_to_camera_target.normalize()

        # カメラ方向を考慮して奥行きを排除した最短ベクトルを作成(ソース)
        projected_vec_source = vec_center - (vec_center * vec_to_camera_source) * vec_to_camera_source
        projected_vec_source.normalize()

        # カメラ方向を考慮して奥行きを排除した最短ベクトルを作成(ターゲット)
        projected_vec_target = vec_center - (vec_center * vec_to_camera_target) * vec_to_camera_target
        projected_vec_target.normalize()

        # 円周上の接点を取得
        contact_point_1 = position_source + projected_vec_source * radius_1
        contact_point_2 = position_target - projected_vec_target * radius_2

        return contact_point_1, contact_point_2

    def calculate_triangle_points(self, point_A, point_B, radius_A, camera_position):
        """
        円Aと円Bを結ぶ最短円周点から、カメラの方向に向けた三角形の底辺を計算する。

        Parameters:
            point_A (numpy.ndarray): 円Aの円周上の最短点 (x, y, z)
            point_B (numpy.ndarray): 円Bの円周上の最短点 (x, y, z)
            radius_A (float): 円Aの半径
            camera_position (numpy.ndarray): カメラのワールド座標 (x, y, z)

        Returns:
            tuple: (底辺の左端, 底辺の右端)
        """
        # ベクトルV = B_s - A_s（Point A から Point B へのベクトル）
        V = point_B - point_A
        V_length = np.linalg.norm(V)
        if V_length == 0:
            return None  # 円が同じ位置にある場合は処理を終了

        # 単位ベクトル化
        V_unit = V / V_length

        # カメラ方向のベクトル
        to_camera = camera_position - point_A
        to_camera /= np.linalg.norm(to_camera)  # 正規化

        # `V_unit` に直交し、カメラ方向に最も近いベクトルを求める
        base_direction = np.cross(V_unit, to_camera)
        base_direction /= np.linalg.norm(base_direction)  # 単位ベクトル化

        # 底辺の両端を求める（左右に円Aの半径分移動）
        P1 = point_A + base_direction * radius_A  # 底辺の左端
        P2 = point_A - base_direction * radius_A  # 底辺の右端

        return P1, P2

    def addUIDrawables(self, objPath, drawManager, frameContext, data):
        """
        描画の実行。prepareForDrawで設定したデータをもとに描画を行う。
        """
        if data is None:
            return
        
        if data.xray or int(frameContext.getDisplayStyle()) == omr2.MFrameContext.kXray+1:
                drawManager.beginDrawInXray()
        else:
            drawManager.beginDrawable()

        # 円の描画
        for i in list(range(len(data.circle_colors))):
            drawManager.setColor(data.circle_colors[i])
            drawManager.mesh(omr2.MUIDrawManager.kTriangles, data.circle_triangle_points[i])
        
        # 親との描画
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
    mPlugin = om2.MFnPlugin(mObject, "user_test", "1.0", "Any")
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


