##############################
# Utility Module
##############################
# This file is part of Mtx_AutoRig
# It is all the small functions used in the rigging process
# Here are the functions like group offsets, attributes creation etc...
##############################

import maya.cmds as cmds # type: ignore
import pymel.core as pm # type: ignore
import maya.mel as mel # type: ignore
from matrixAutorig.naming import MATRIX, MULTIPLY_MATRIX, INVERSE_MATRIX, DECOMPOSE_MATRIX, AIM_MATRIX, WORLD_MATRIX, PARENT_OFFSET_MATRIX, LOCAL_OFFSET_MATRIX, JOINT, GUIDE, CONTROLLER, IK, FK, DISTANCEBETWEEN, SUM, MULTIPLY, MULTIPLYDIVIDE, GROUP, ARM, SHOULDER, ELBOW, HAND, LEG, KNEE, ANKLE, FOOT, BALL, TOE, SPINE, ROOT, CLAVICLE, HEAD, NECK, EYE, JAW, LEFT, RIGHT, CENTER

def hierarchy():
    for part in [ROOT, SPINE, HEAD, LEFT + SHOULDER, RIGHT + SHOULDER, LEFT + ARM, RIGHT + ARM, LEFT + LEG, RIGHT + LEG]:
        grpMod = cmds.createNode('transform', name="{}_mod".format(part))
        grpSetup = cmds.createNode('transform', name="{}_setup".format(part), parent=grpMod)
        grpInputs = cmds.createNode('transform', name="{}_rig".format(part), parent=grpMod)
        grpGuides = cmds.createNode('transform', name="{}_guides".format(part), parent=grpMod)
        grpControls = cmds.createNode('transform', name="{}_controls".format(part), parent=grpMod)
        grpJoints = cmds.createNode('transform', name="{}_joints".format(part), parent=grpMod)
        grpRigNodes = cmds.createNode('transform', name="{}_nodes".format(part), parent=grpMod)
        grpOutputs = cmds.createNode('transform', name="{}_output".format(part), parent=grpMod)




def addOffset(dst, suffix='Offset'):
    grp_offset = cmds.createNode('transform', name="{}_{}".format(dst, suffix))
    dst_mat = cmds.xform(dst, q=True, m=True, ws=True)
    cmds.xform(grp_offset, m=dst_mat, ws=True)

    dst_parent = cmds.listRelatives(dst, parent=True)
    if dst_parent:
        cmds.parent(grp_offset, dst_parent)
    cmds.parent(dst, grp_offset)

    return grp_offset
