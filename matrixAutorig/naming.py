##################################################
# Naming Module
##################################################
# This file defines standard suffixes and prefixes used throughout the rigging process.
# It helps maintain consistency in naming various rig components.
# Change them as you want for your own naming conventions
##################################################

import UI
import maya.cmds as cmds # type: ignore

custom_naming = cmds.radioButtonGrp(UI.custom_naming, q=True, select=True)

if custom_naming == 2:
    if UI.addCapsName == True:

        # Object constants
        MATRIX = 'Mtx'
        MULTIPLY_MATRIX = 'MtxMlt'
        INVERSE_MATRIX = 'MtxInv'
        DECOMPOSE_MATRIX = 'MtxDcp'
        AIM_MATRIX = 'MtxAim'
        WORLD_MATRIX = 'WM'
        PARENT_OFFSET_MATRIX = 'POM'
        LOCAL_OFFSET_MATRIX = 'LOM'
        JOINT = 'JNT'
        GUIDE = 'GD'
        CONTROLLER = 'CTRL'
        IK = 'IK'
        FK = 'FK'
        DISTANCEBETWEEN = 'DistB'
        SUM = 'Sum'
        MULTIPLY = 'Mult'
        GROUP = 'GRP'

        # Part constants
        ARM = 'Arm'
        SHOULDER = 'Sh'
        ELBOW = 'Elb'
        HAND = 'Hand'

        LEG = 'Leg'
        KNEE = 'Knee'
        ANKLE = 'Ankle'
        FOOT = 'Foot'
        BALL = 'Ball'
        TOE = 'Toe'

        SPINE = 'Spine'
        ROOT = 'Root'
        CLAVICLE = 'Clavicle'

        HEAD = 'Head'
        NECK = 'Neck'
        EYE = 'Eye'
        JAW = 'Jaw'


        # Side constants
        LEFT = 'L'
        RIGHT = 'R'
        CENTER = "C"

    else:
        # Object constants
        MATRIX = 'mtx'
        MULTIPLY_MATRIX = 'mtxMlt'
        INVERSE_MATRIX = 'mtxInv'
        DECOMPOSE_MATRIX = 'mtxDcp'
        AIM_MATRIX = 'mtxAim'
        WORLD_MATRIX = 'wm'
        PARENT_OFFSET_MATRIX = 'pom'
        LOCAL_OFFSET_MATRIX = 'lom'
        JOINT = 'jnt'
        GUIDE = 'gd'
        CONTROLLER = 'ctrl'
        IK = 'ik'
        FK = 'fk'
        DISTANCEBETWEEN = 'distB'
        SUM = 'sum'
        MULTIPLY = 'mult'
        MULTIPLYDIVIDE = 'multDiv'
        GROUP = 'grp'

        # Part constants
        ARM = 'arm'
        SHOULDER = 'sh'
        ELBOW = 'elb'
        HAND = 'hand'

        LEG = 'leg'
        KNEE = 'knee'
        ANKLE = 'ankle'
        FOOT = 'foot'
        BALL = 'ball'
        TOE = 'toe'

        SPINE = 'spine'
        ROOT = 'root'
        CLAVICLE = 'clavicle'

        HEAD = 'head'
        NECK = 'neck'
        EYE = 'eye'
        JAW = 'jaw'


        # Side constants
        LEFT = 'l'
        RIGHT = 'r'
        CENTER = "c"
else:
    # Object constants
        MATRIX = UI.mtx_field
        MULTIPLY_MATRIX = UI.mtx_mlt_field
        INVERSE_MATRIX = UI.mtx_inv_field
        DECOMPOSE_MATRIX = UI.mtx_dcp_field
        AIM_MATRIX = UI.mtx_aim_field
        WORLD_MATRIX = UI.wm_field
        PARENT_OFFSET_MATRIX = UI.pom_field
        LOCAL_OFFSET_MATRIX = UI.lom_field
        JOINT = UI.jnt_field
        GUIDE = UI.gd_field
        CONTROLLER = UI.ctrl_field
        IK = UI.ik_field
        FK = UI.fk_field
        DISTANCEBETWEEN = UI.dist_b_field
        SUM = UI.sum_field
        MULTIPLY = UI.mult_field
        MULTIPLYDIVIDE = UI.mult_div_field
        GROUP = UI.grp_field

        # Part constants
        ARM = UI.arm_field_custom
        SHOULDER = UI.sh_field
        ELBOW = UI.elbow_field
        HAND = UI.hand_field

        LEG = UI.leg_field_custom
        KNEE = UI.knee_field
        ANKLE = UI.ankle_field
        FOOT = UI.foot_field
        BALL = UI.ball_field
        TOE = UI.toe_field

        SPINE = UI.spine_field_custom
        ROOT = UI.root_field
        CLAVICLE = UI.clavicle_field

        HEAD = UI.head_field
        NECK = UI.neck_field
        EYE = UI.eye_field
        JAW = UI.jaw_field


        # Side constants
        LEFT = UI.l_field
        RIGHT = UI.r_field
        CENTER = UI.c_field

