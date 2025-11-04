##############################
# Description: Utility functions

# This file is part of Mtx_AutoRig

# It is all the small functions used in the rigging process
# Here are the functions like group offsets, attributes creation etc...
##############################

import maya.cmds as cmds # type: ignore
import pymel.core as pm # type: ignore
import maya.mel as mel # type: ignore

def addOffset(dst, suffix='Offset'):
    """
    
    :return:
    """

    grp_offset = mc.createNode('transform', name="{}_{}".format(dst, suffix))
    dst_mat = mc.xform(dst, q=True, m=True, ws=True)
    mc.xform(grp_offset, m=dst_mat, ws=True)

    dst_parent = mc.listRelatives(dst, parent=True)
    if dst_parent:
        mc.parent(grp_offset, dst_parent)
    mc.parent(dst, grp_offset)

    return grp_offset