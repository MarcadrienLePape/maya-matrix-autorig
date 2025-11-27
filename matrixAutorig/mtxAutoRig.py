#################################################
# Matrix AutoRig
#
# By Marc-adrien LE PAPE
#
# www.malp-rigs.com
#
#################################################

import maya.cmds as cmds # type: ignore
from functools import partial

#-------------------------------------------------------------------------------------------------------------------------
# Create Guides #

def create_guides(*args):
    
    global head_gd
    
    try:
        is_quad = cmds.optionMenuGrp(is_quad_field, q=True, value=True) == "Yes"
    except Exception:
        is_quad = False
        
    try:
        num_spine = cmds.intFieldGrp(spine_field, q=True, value1=True)
    except Exception:
        num_spine = 3

    try:
        num_arms = cmds.intFieldGrp(arm_field, q=True, value1=True)
    except Exception:
        num_arms = 1
        
    try:
        num_legs = cmds.intFieldGrp(leg_field, q=True, value1=True)
    except Exception:
        num_legs = 1
    
    try:
        height_num = cmds.intFieldGrp(height_field, q=True, value1=True)
    except Exception:
        height_num = 20
    
    try:
        do_face = cmds.optionMenuGrp(do_face_field, q=True, value=True) == "Yes" == True
        if do_face == True:
            facial_UI()
        else:
            pass
    except Exception:
        do_face = False

    constants = get_naming_constants()
    ROOT = constants["ROOT"]
    SPINE = constants["SPINE"]
    
    LEFT = constants["LEFT"]
    RIGHT = constants["RIGHT"]
    GUIDE = constants["GUIDE"]
    
    ARM = constants["ARM"]
    SHOULDER = constants["SHOULDER"]
    ELBOW = constants["ELBOW"]
    
    HAND = constants["HAND"]
    THUMB = constants["THUMB"]
    INDEX = constants["INDEX"]
    MIDDLE = constants["MIDDLE"]
    RING = constants["RING"]
    PINKY = constants["PINKY"]
    METACARPUS = constants["METACARPUS"]
    
    LEG = constants["LEG"]
    KNEE = constants["KNEE"]
    ANKLE = constants["ANKLE"]
    BALL = constants["BALL"]
    TOE = constants["TOE"]
    
    HEAD = constants["HEAD"]
    NECK = constants["NECK"]
    JAW = constants["JAW"]
    EYE = constants["EYE"]
    
    CHRNAME = constants["CHRNAME"]

    # Base Group
    grp_rig = cmds.createNode('transform', name="{}matrix_rig".format(CHRNAME))
    
    # Create root locator
    root = cmds.spaceLocator(name="{}{}_{}".format(CHRNAME, ROOT, GUIDE))[0]
    cmds.setAttr("{}.translateY".format(root), (height_num/2))
    grpMod_root = cmds.createNode('transform', name="{}{}_mod".format(CHRNAME,ROOT))
    grpSetup_root = cmds.createNode('transform', name="{}{}_setup".format(CHRNAME,ROOT), parent=grpMod_root)
    grpInputs_root = cmds.createNode('transform', name="{}{}_rig".format(CHRNAME,ROOT), parent=grpMod_root)
    grpGuides_root= cmds.createNode('transform', name="{}{}_guides".format(CHRNAME,ROOT), parent=grpMod_root)
    grpControls_root = cmds.createNode('transform', name="{}{}_controls".format(CHRNAME,ROOT), parent=grpMod_root)
    grpJoints_root = cmds.createNode('transform', name="{}{}_joints".format(CHRNAME,ROOT), parent=grpMod_root)
    grpRigNodes_root = cmds.createNode('transform', name="{}{}_nodes".format(CHRNAME,ROOT), parent=grpMod_root)
    grpOutputs_root = cmds.createNode('transform', name="{}{}_output".format(CHRNAME,ROOT), parent=grpMod_root)
    cmds.parent(root, grpGuides_root)
    cmds.parent(grpMod_root, grp_rig)
    for color in [root]:
        cmds.setAttr("{}.overrideEnabled".format(color), 1)
        cmds.setAttr("{}.overrideRGBColors".format(color), 1)
        cmds.setAttr("{}.overrideColorRGB".format(color), 1, 0.165, 0.456) 
        cmds.setAttr("{}.useOutlinerColor".format(color), 1)
        cmds.setAttr("{}.outlinerColor".format(color), 1, 0.165, 0.456)
    
    # Create spine locators
    spine_guides = []
    if is_quad == True:
        print("Quadruped mode not implemented yet.")
        pass
    else:
        for i in range(num_spine):
            loc = cmds.spaceLocator(name="{}{}_{}_{}".format(CHRNAME, SPINE, i+1, GUIDE))[0]
            cmds.setAttr("{}.translateY".format(loc), (height_num/2) + i*(height_num/4))
            spine_guides.append(loc)
            if i == 0:
                cmds.parent(loc, root)
            else:
                cmds.parent(loc, spine_guides[i-1])
            

        # Create arm locators (left and right)
        for side in [LEFT, RIGHT]:
            for arm_idx in range(num_arms):
                grpMod_arm = cmds.createNode('transform', name="{}{}_{}_{}_mod".format(CHRNAME,side, ARM, arm_idx+1))
                grpSetup_arm = cmds.createNode('transform', name="{}{}_{}_{}_setup".format(CHRNAME,side, ARM, arm_idx+1), parent=grpMod_arm)
                grpInputs_arm = cmds.createNode('transform', name="{}{}_{}_{}_rig".format(CHRNAME,side, ARM, arm_idx+1), parent=grpMod_arm)
                grpGuides_arm= cmds.createNode('transform', name="{}{}_{}_{}_guides".format(CHRNAME,side, ARM, arm_idx+1), parent=grpMod_arm)
                grpControls_arm = cmds.createNode('transform', name="{}{}_{}_{}_controls".format(CHRNAME,side, ARM, arm_idx+1), parent=grpMod_arm)
                grpJoints_arm = cmds.createNode('transform', name="{}{}_{}_{}_joints".format(CHRNAME,side, ARM, arm_idx+1), parent=grpMod_arm)
                grpRigNodes_arm = cmds.createNode('transform', name="{}{}_{}_{}_nodes".format(CHRNAME,side, ARM, arm_idx+1), parent=grpMod_arm)
                grpOutputs_arm = cmds.createNode('transform', name="{}{}_{}_{}_output".format(CHRNAME,side, ARM, arm_idx+1), parent=grpMod_arm)
                cmds.parent(grpMod_arm, grp_rig)
                
                # Shoulder
                shoulder = cmds.spaceLocator(
                    name="{}{}_{}_{}_{}_{}".format(CHRNAME, side, ARM, arm_idx+1, SHOULDER, GUIDE)
                )[0]
                cmds.parent(shoulder, spine_guides[-1])
                cmds.setAttr("{}.translateY".format(shoulder), 0 - num_arms)
                cmds.setAttr("{}.translateX".format(shoulder), (height_num/8) if side == LEFT else -(height_num/8))
                cmds.parent(shoulder, grpGuides_arm)

                # Elbow
                elbow = cmds.spaceLocator(
                    name="{}{}_{}_{}_{}_{}".format(CHRNAME, side, ARM, arm_idx+1, ELBOW, GUIDE)
                )[0]
                cmds.parent(elbow, shoulder)
                cmds.setAttr("{}.translateY".format(elbow), 0)
                cmds.setAttr("{}.translateX".format(elbow), (height_num/4) if side == LEFT else -(height_num/4))
                cmds.setAttr("{}.translateZ".format(elbow), -(height_num/8))

                # Hand
                hand = cmds.spaceLocator(
                    name="{}{}_{}_{}_{}_{}".format(CHRNAME, side, ARM, arm_idx+1, HAND, GUIDE)
                )[0]
                cmds.parent(hand, elbow)
                cmds.setAttr("{}.translateY".format(hand), 0)
                cmds.setAttr("{}.translateX".format(hand), (height_num/4) if side == LEFT else -(height_num/4))
                cmds.setAttr("{}.translateZ".format(hand), (height_num/8))
                
                # Fingers
                for fingers in [INDEX, MIDDLE, RING, PINKY]:
                    meta = cmds.spaceLocator(
                        name="{}{}_{}_{}_{}_{}_{}_{}".format(CHRNAME, side, ARM, arm_idx+1, HAND, fingers, METACARPUS, GUIDE))[0]
                    cmds.parent(meta, hand)
                    cmds.setAttr("{}.translateY".format(meta), 0)
                    cmds.setAttr("{}.translateX".format(meta), 0.5 if side == LEFT else -0.5)
                    if fingers == INDEX:
                        cmds.setAttr("{}.translateZ".format(meta), 1)
                    elif fingers == MIDDLE:
                        cmds.setAttr("{}.translateZ".format(meta), 0)
                    elif fingers == RING:
                        cmds.setAttr("{}.translateZ".format(meta), -1)
                    else:
                        cmds.setAttr("{}.translateZ".format(meta), -2)
                    prev = meta
                    
                    for color in [meta]:
                        cmds.setAttr("{}.overrideEnabled".format(color), 1)
                        cmds.setAttr("{}.overrideRGBColors".format(color), 1)
                        cmds.setAttr("{}.overrideColorRGB".format(color), 1, 0.165, 0.456) 
                        cmds.setAttr("{}.useOutlinerColor".format(color), 1)
                        cmds.setAttr("{}.outlinerColor".format(color), 1, 0.165, 0.456)
                    
                    for f in range(4):
                        finger = cmds.spaceLocator(
                            name="{}{}_{}_{}_{}_{}_{}_{}".format(CHRNAME, side, ARM, arm_idx+1, HAND, fingers, f+1, GUIDE))[0]
                        cmds.parent(finger, prev)
                        cmds.setAttr("{}.translateY".format(finger), 0)
                        cmds.setAttr("{}.translateX".format(finger), (0.5+f*0.3) if side == LEFT else -(0.5+f*0.3))
                        cmds.setAttr("{}.translateZ".format(finger), 0)
                        prev = finger
                        
                        for color in [prev]:
                            cmds.setAttr("{}.overrideEnabled".format(color), 1)
                            cmds.setAttr("{}.overrideRGBColors".format(color), 1)
                            cmds.setAttr("{}.overrideColorRGB".format(color), 1, 0.165, 0.456) 
                            cmds.setAttr("{}.useOutlinerColor".format(color), 1)
                            cmds.setAttr("{}.outlinerColor".format(color), 1, 0.165, 0.456)

                # Thumb
                for thumb in range(1):
                    meta = cmds.spaceLocator(
                            name="{}{}_{}_{}_{}_{}_{}_{}".format(CHRNAME, side, ARM, arm_idx+1, HAND, THUMB, METACARPUS, GUIDE))[0]
                    cmds.parent(meta, hand)
                    cmds.setAttr("{}.translateX".format(meta), 0.3 if side == LEFT else -0.3)
                    cmds.setAttr("{}.translateY".format(meta), 0)
                    cmds.setAttr("{}.translateZ".format(meta), 2 if side == LEFT else -2)
                    prev = meta
                    
                    for color in [meta]:
                        cmds.setAttr("{}.overrideEnabled".format(color), 1)
                        cmds.setAttr("{}.overrideRGBColors".format(color), 1)
                        cmds.setAttr("{}.overrideColorRGB".format(color), 1, 0.165, 0.456) 
                        cmds.setAttr("{}.useOutlinerColor".format(color), 1)
                        cmds.setAttr("{}.outlinerColor".format(color), 1, 0.165, 0.456)
                    
                    for t in range(3):
                        thumb_loc = cmds.spaceLocator(
                            name="{}{}_{}_{}_{}_{}_{}".format(CHRNAME, side, ARM, arm_idx+1, THUMB, t+1, GUIDE))[0]
                        cmds.parent(thumb_loc, prev)
                        cmds.setAttr("{}.translateY".format(thumb_loc), 0)
                        cmds.setAttr("{}.translateX".format(thumb_loc), 0.5+t*0.3 if side == LEFT else -(0.5+t*0.3))
                        cmds.setAttr("{}.translateZ".format(thumb_loc), 0)
                        prev = thumb_loc
                        
                        for color in [prev]:
                            cmds.setAttr("{}.overrideEnabled".format(color), 1)
                            cmds.setAttr("{}.overrideRGBColors".format(color), 1)
                            cmds.setAttr("{}.overrideColorRGB".format(color), 1, 0.165, 0.456) 
                            cmds.setAttr("{}.useOutlinerColor".format(color), 1)
                            cmds.setAttr("{}.outlinerColor".format(color), 1, 0.165, 0.456)
                        
                for color in [shoulder, elbow, hand]:
                    cmds.setAttr("{}.overrideEnabled".format(color), 1)
                    cmds.setAttr("{}.overrideRGBColors".format(color), 1)
                    cmds.setAttr("{}.overrideColorRGB".format(color), 1, 0.165, 0.456) 
                    cmds.setAttr("{}.useOutlinerColor".format(color), 1)
                    cmds.setAttr("{}.outlinerColor".format(color), 1, 0.165, 0.456)
            
            # Create leg locators (left and right)
            for leg_idx in range(num_legs):
                grpMod_leg = cmds.createNode('transform', name="{}{}_{}_{}_mod".format(CHRNAME,side, LEG, leg_idx+1))
                grpSetup_leg = cmds.createNode('transform', name="{}{}_{}_{}_setup".format(CHRNAME,side, LEG, leg_idx+1), parent=grpMod_leg)
                grpInputs_leg = cmds.createNode('transform', name="{}{}_{}_{}_rig".format(CHRNAME,side, LEG, leg_idx+1), parent=grpMod_leg)
                grpGuides_leg= cmds.createNode('transform', name="{}{}_{}_{}_guides".format(CHRNAME,side, LEG, leg_idx+1), parent=grpMod_leg)
                grpControls_leg = cmds.createNode('transform', name="{}{}_{}_{}_controls".format(CHRNAME,side, LEG, leg_idx+1), parent=grpMod_leg)
                grpJoints_leg = cmds.createNode('transform', name="{}{}_{}_{}_joints".format(CHRNAME,side, LEG, leg_idx+1), parent=grpMod_leg)
                grpRigNodes_leg = cmds.createNode('transform', name="{}{}_{}_{}_nodes".format(CHRNAME,side, LEG, leg_idx+1), parent=grpMod_leg)
                grpOutputs_leg = cmds.createNode('transform', name="{}{}_{}_{}_output".format(CHRNAME,side, LEG, leg_idx+1), parent=grpMod_leg)
                cmds.parent(grpMod_leg, grp_rig)
                
                # Hip
                hip = cmds.spaceLocator(
                    name="{}{}_{}_{}_{}".format(CHRNAME, side, LEG, leg_idx+1, GUIDE)
                )[0]
                cmds.parent(hip, root)
                cmds.setAttr("{}.translateY".format(hip), 0)
                cmds.setAttr("{}.translateX".format(hip), (height_num/10)+leg_idx if side == LEFT else -(height_num/10)-leg_idx)
                cmds.parent(hip, grpGuides_leg)

                # Knee
                knee = cmds.spaceLocator(
                    name="{}{}_{}_{}_{}_{}".format(CHRNAME, side, LEG, leg_idx+1, KNEE, GUIDE)
                )[0]
                cmds.parent(knee, hip)
                cmds.setAttr("{}.translateY".format(knee), -(height_num/4))
                cmds.setAttr("{}.translateX".format(knee), 0)
                cmds.setAttr("{}.translateZ".format(knee), (height_num/8))

                # Ankle
                ankle = cmds.spaceLocator(
                    name="{}{}_{}_{}_{}_{}".format(CHRNAME, side, LEG, leg_idx+1, ANKLE, GUIDE)
                )[0]
                cmds.parent(ankle, knee)
                cmds.setAttr("{}.translateY".format(ankle), -(height_num/4))
                cmds.setAttr("{}.translateX".format(ankle), 0)
                cmds.setAttr("{}.translateZ".format(ankle), -(height_num/8))
                
                # Ball
                ball = cmds.spaceLocator(
                    name="{}{}_{}_{}_{}_{}".format(CHRNAME, side, LEG, leg_idx+1, BALL, GUIDE)
                )[0]
                cmds.parent(ball, ankle)
                cmds.setAttr("{}.translateY".format(ball), -1)
                cmds.setAttr("{}.translateX".format(ball), 0)
                cmds.setAttr("{}.translateZ".format(ball), 2)
                
                # Toe
                toe = cmds.spaceLocator(
                    name="{}{}_{}_{}_{}_{}".format(CHRNAME, side, LEG, leg_idx+1, TOE, GUIDE)
                )[0]
                cmds.parent(toe, ball)
                cmds.setAttr("{}.translateY".format(toe), 0)
                cmds.setAttr("{}.translateX".format(toe), 0)
                cmds.setAttr("{}.translateZ".format(toe), 1)
                
                for color in [hip, knee, ankle, ball, toe]:
                    cmds.setAttr("{}.overrideEnabled".format(color), 1)
                    cmds.setAttr("{}.overrideRGBColors".format(color), 1)
                    cmds.setAttr("{}.overrideColorRGB".format(color), 1, 0.165, 0.456) 
                    cmds.setAttr("{}.useOutlinerColor".format(color), 1)
                    cmds.setAttr("{}.outlinerColor".format(color), 1, 0.165, 0.456)
        
        for head in range(1):
            grpMod_head = cmds.createNode('transform', name="{}{}_mod".format(CHRNAME, HEAD))
            grpSetup_head = cmds.createNode('transform', name="{}{}_setup".format(CHRNAME, HEAD), parent=grpMod_head)
            grpInputs_head = cmds.createNode('transform', name="{}{}_rig".format(CHRNAME, HEAD), parent=grpMod_head)
            grpGuides_head= cmds.createNode('transform', name="{}{}_guides".format(CHRNAME, HEAD), parent=grpMod_head)
            grpControls_head = cmds.createNode('transform', name="{}{}_controls".format(CHRNAME, HEAD), parent=grpMod_head)
            grpJoints_head = cmds.createNode('transform', name="{}{}_joints".format(CHRNAME, HEAD), parent=grpMod_head)
            grpRigNodes_head = cmds.createNode('transform', name="{}{}_nodes".format(CHRNAME, HEAD), parent=grpMod_head)
            grpOutputs_head = cmds.createNode('transform', name="{}{}_output".format(CHRNAME, HEAD), parent=grpMod_head)
            cmds.parent(grpMod_head, grp_rig)
            
            # Neck
            neck = cmds.spaceLocator(
                name="{}{}_{}_{}".format(CHRNAME, HEAD, NECK, GUIDE))[0]
            cmds.parent(neck, spine_guides[i])
            cmds.setAttr("{}.translateY".format(neck), 2)
            cmds.setAttr("{}.translateZ".format(neck), -1)
            cmds.parent(neck, grpGuides_head)
            
            #Head 
            head_gd = cmds.spaceLocator(
                name="{}{}_{}".format(CHRNAME, HEAD, GUIDE))[0]
            cmds.parent(head_gd, neck)
            cmds.setAttr("{}.translateY".format(head_gd), 1)
            cmds.setAttr("{}.translateZ".format(head_gd), 1)
            
            # Head Top
            head_top = cmds.spaceLocator(
                name="{}{}_{}".format(CHRNAME, HEAD+"_top", GUIDE))[0]
            cmds.parent(head_top, head)
            cmds.setAttr("{}.translateY".format(head_top), 1)
            
        
            for color in [neck, head, head_top]:
                cmds.setAttr("{}.overrideEnabled".format(color), 1)
                cmds.setAttr("{}.overrideRGBColors".format(color), 1)
                cmds.setAttr("{}.overrideColorRGB".format(color), 1, 0.165, 0.456) 
                cmds.setAttr("{}.useOutlinerColor".format(color), 1)
                cmds.setAttr("{}.outlinerColor".format(color), 1, 0.165, 0.456)
                
        
def create_fac_guides(*args):
    
    constants = get_naming_constants()
    
    LEFT = constants["LEFT"]
    RIGHT = constants["RIGHT"]
    GUIDE = constants["GUIDE"]
    
    HEAD = constants["HEAD"]
    NECK = constants["NECK"]
    JAW = constants["JAW"]
    EYE = constants["EYE"]
    
    CHRNAME = constants["CHRNAME"]
    
    # Jaw
    jaw = cmds.spaceLocator(
        name="{}{}_{}_{}".format(CHRNAME, HEAD, JAW, GUIDE))[0]
    cmds.parent(jaw, head)
    cmds.setAttr("{}.translateY".format(jaw), -0.5)
    cmds.setAttr("{}.translateZ".format(jaw), 1)
    
    # Eyes
    for side in [LEFT, RIGHT]:
        eye = cmds.spaceLocator(
            name="{}{}_{}_{}_{}".format(CHRNAME, side, HEAD, EYE, GUIDE))[0]
        cmds.parent(eye, head)
        cmds.setAttr("{}.translateY".format(eye), 0.5)
        cmds.setAttr("{}.translateX".format(eye), 0.5 if side == LEFT else -0.5)
        cmds.setAttr("{}.translateZ".format(eye), 1)
        
        for color in [eye]:
            cmds.setAttr("{}.overrideEnabled".format(color), 1)
            cmds.setAttr("{}.overrideRGBColors".format(color), 1)
            cmds.setAttr("{}.overrideColorRGB".format(color), 1, 0.165, 0.456) 
            cmds.setAttr("{}.useOutlinerColor".format(color), 1)
            cmds.setAttr("{}.outlinerColor".format(color), 1, 0.165, 0.456)
    
#-------------------------------------------------------------------------------------------------------------------------
# Create Rig

def generate_rig(*args):
    pass

#---------------------------------------------------------------------------------------------------------
# Utils

def addOffset(dst, suffix='Offset'):
    grp_offset = cmds.createNode('transform', name="{}_{}".format(dst, suffix))
    dst_mat = cmds.xform(dst, q=True, m=True, ws=True)
    cmds.xform(grp_offset, m=dst_mat, ws=True)

    dst_parent = cmds.listRelatives(dst, parent=True)
    if dst_parent:
        cmds.parent(grp_offset, dst_parent)
    cmds.parent(dst, grp_offset)

    return grp_offset

#-------------------------------------------------------------------------------------------------------------------------
# Naming Constants

def get_naming_constants():
    try:
        customNaming = cmds.radioButtonGrp(custom_naming, q=True, select=True)
    except Exception:
        customNaming = 2

    try:
        addCaps = cmds.radioButtonGrp(option_caps, q=True, select=True)
    except Exception:
        # Default: caps off (2 = No in our UI setup)
        addCaps = 2

    constants = {}

    if customNaming == 2:
        if addCaps == True:
            # Object constants
            constants.update({
                "MATRIX": "Mtx",
                "MULTIPLY_MATRIX": "MtxMlt",
                "INVERSE_MATRIX": "MtxInv",
                "DECOMPOSE_MATRIX": "MtxDcp",
                "AIM_MATRIX": "MtxAim",
                "WORLD_MATRIX": "WM",
                "PARENT_OFFSET_MATRIX": "POM",
                "LOCAL_OFFSET_MATRIX": "LOM",
                "JOINT": "JNT",
                "GUIDE": "GD",
                "CONTROLLER": "CTRL",
                "IK": "IK",
                "FK": "FK",
                "DISTANCEBETWEEN": "DistB",
                "SUM": "Sum",
                "MULTIPLY": "Mult",
                "GROUP": "GRP",
            })

            # Part constants
            constants.update({
                "ARM": "Arm",
                "SHOULDER": "Sh",
                "ELBOW": "Elb",
                "HAND": "Hand",
                "THUMB": "Thumb",
                "INDEX": "Index",
                "MIDDLE": "Middle",
                "RING": "Ring",
                "PINKY": "Pinky",
                "METACARPUS": "Metacarpus",
                "LEG": "Leg",
                "KNEE": "Knee",
                "ANKLE": "Ankle",
                "FOOT": "Foot",
                "BALL": "Ball",
                "TOE": "Toe",
                "SPINE": "Spine",
                "ROOT": "Root",
                "CLAVICLE": "Clavicle",
                
                "HEAD": "Head",
                "NECK": "Neck",
                "EYE": "Eye",
                "JAW": "Jaw",
                
                "CHRNAME": char_prefix,
            })

            # Side constants
            constants.update({
                "LEFT": "L",
                "RIGHT": "R",
                "CENTER": "C",
            })
        else:
            # Lowercase constants
            constants.update({
                "MATRIX": "mtx",
                "MULTIPLY_MATRIX": "mtxMlt",
                "INVERSE_MATRIX": "mtxInv",
                "DECOMPOSE_MATRIX": "mtxDcp",
                "AIM_MATRIX": "mtxAim",
                "WORLD_MATRIX": "wm",
                "PARENT_OFFSET_MATRIX": "pom",
                "LOCAL_OFFSET_MATRIX": "lom",
                "JOINT": "jnt",
                "GUIDE": "gd",
                "CONTROLLER": "ctrl",
                "IK": "ik",
                "FK": "fk",
                "DISTANCEBETWEEN": "distB",
                "SUM": "sum",
                "MULTIPLY": "mult",
                "MULTIPLYDIVIDE": "multDiv",
                "GROUP": "grp",
            })

            # Part constants
            constants.update({
                "ARM": "arm",
                "SHOULDER": "sh",
                "ELBOW": "elb",
                "HAND": "hand",
                "THUMB": "thumb",
                "INDEX": "index",
                "MIDDLE": "middle",
                "RING": "ring",
                "PINKY": "pinky",
                "METACARPUS": "metacarpus",
                "LEG": "leg",
                "KNEE": "knee",
                "ANKLE": "ankle",
                "FOOT": "foot",
                "BALL": "ball",
                "TOE": "toe",
                "SPINE": "spine",
                "ROOT": "root",
                "CLAVICLE": "clavicle",
                
                "HEAD": "head",
                "NECK": "neck",
                "EYE": "eye",
                "JAW": "jaw",
                
                "CHRNAME": char_prefix,
            })

            # Side constants
            constants.update({
                "LEFT": "l",
                "RIGHT": "r",
                "CENTER": "c",
            })
    else:
        # Custom naming constants from UI fields
        constants.update({
            "MATRIX": cmds.textFieldGrp(mtx_field, q=True, text=True),
            "MULTIPLY_MATRIX": cmds.textFieldGrp(mtx_mlt_field, q=True, text=True),
            "INVERSE_MATRIX": cmds.textFieldGrp(mtx_inv_field, q=True, text=True),
            "DECOMPOSE_MATRIX": cmds.textFieldGrp(mtx_dcp_field, q=True, text=True),
            "AIM_MATRIX": cmds.textFieldGrp(mtx_aim_field, q=True, text=True),
            "WORLD_MATRIX": cmds.textFieldGrp(wm_field, q=True, text=True),
            "PARENT_OFFSET_MATRIX": cmds.textFieldGrp(pom_field, q=True, text=True),
            "LOCAL_OFFSET_MATRIX": cmds.textFieldGrp(lom_field, q=True, text=True),
            "JOINT": cmds.textFieldGrp(jnt_field, q=True, text=True),
            "GUIDE": cmds.textFieldGrp(gd_field, q=True, text=True),
            "CONTROLLER": cmds.textFieldGrp(ctrl_field, q=True, text=True),
            "IK": cmds.textFieldGrp(ik_field, q=True, text=True),
            "FK": cmds.textFieldGrp(fk_field, q=True, text=True),
            "DISTANCEBETWEEN": cmds.textFieldGrp(dist_b_field, q=True, text=True),
            "SUM": cmds.textFieldGrp(sum_field, q=True, text=True),
            "MULTIPLY": cmds.textFieldGrp(mult_field, q=True, text=True),
            "MULTIPLYDIVIDE": cmds.textFieldGrp(mult_div_field, q=True, text=True),
            "GROUP": cmds.textFieldGrp(grp_field, q=True, text=True),
            
            "ARM": cmds.textFieldGrp(arm_field_custom, q=True, text=True),
            "SHOULDER": cmds.textFieldGrp(sh_field, q=True, text=True),
            "ELBOW": cmds.textFieldGrp(elb_field, q=True, text=True),
            "HAND": cmds.textFieldGrp(hand_field, q=True, text=True),
            "THUMB": "thumb",
            "INDEX": "index",
            "MIDDLE": "middle",
            "RING": "ring",
            "PINKY": "pinky",
            "METACARPUS": "metacarpus",
            
            "LEG": cmds.textFieldGrp(leg_field_custom, q=True, text=True),
            "KNEE": cmds.textFieldGrp(knee_field, q=True, text=True),
            "ANKLE": cmds.textFieldGrp(ankle_field, q=True, text=True),
            "FOOT": cmds.textFieldGrp(foot_field, q=True, text=True),
            "BALL": cmds.textFieldGrp(ball_field, q=True, text=True),
            "TOE": cmds.textFieldGrp(toe_field, q=True, text=True),
            "SPINE": cmds.textFieldGrp(spine_field_custom, q=True, text=True),
            "ROOT": cmds.textFieldGrp(root_field, q=True, text=True),
            "CLAVICLE": cmds.textFieldGrp(clavicle_field, q=True, text=True),
            
            "HEAD": cmds.textFieldGrp(head_field, q=True, text=True),
            "NECK": cmds.textFieldGrp(neck_field, q=True, text=True),
            "EYE": cmds.textFieldGrp(eye_field, q=True, text=True),
            "JAW": cmds.textFieldGrp(jaw_field, q=True, text=True),
            
            "LEFT": cmds.textFieldGrp(l_field, q=True, text=True),
            "RIGHT": cmds.textFieldGrp(r_field, q=True, text=True),
            "CENTER": cmds.textFieldGrp(c_field, q=True, text=True),
            
            "CHRNAME": char_prefix,
        })

    return constants
#-------------------------------------------------------------------------------------------------------------------------
# UI

def UI():
    # Expose frequently-used widget names to module scope so callbacks can access them
    global custom_naming, naming_custom_frame, option_caps, option_chrName, char_name_field, naming_example, is_quad_field, arm_field, leg_field, spine_field, height_field,do_face_field, mtx_field, mtx_mlt_field, mtx_inv_field, mtx_dcp_field, mtx_aim_field, wm_field, pom_field, lom_field, jnt_field, gd_field, ctrl_field, ik_field, fk_field, dist_b_field, sum_field, mult_field, mult_div_field, grp_field, arm_field_custom, sh_field, elb_field, hand_field, leg_field_custom, knee_field, ankle_field, foot_field, ball_field, toe_field, spine_field_custom, root_field, clavicle_field, head_field, neck_field, eye_field, jaw_field, l_field, r_field, c_field, metacarpus_field
    # Window -------------------------------------------------------------------------------------------
    if cmds.window ("mtxAutoRig", ex=1): cmds.deleteUI ("mtxAutoRig")
    window = cmds.window ("mtxAutoRig", t="Matrix Auto Rig v0.1", w=225, s=1)
    
    # Layout -------------------------------------------------------------------------------------------
    mainForm = cmds.formLayout(parent=window)

    # Main Scroll and Column (placed inside the form)
    mainScroll = cmds.scrollLayout(horizontalScrollBarThickness=0,
                                   verticalScrollBarThickness=16,
                                   parent=mainForm)

    mainColumn = cmds.columnLayout(adjustableColumn=True,
                                   columnAlign='center',
                                   parent=mainScroll)

    # ========================================================================================================
    # 1) About layout -> about frame
    # ========================================================================================================
    about_layout = cmds.columnLayout(adjustableColumn=True, parent=mainColumn)
    about_Frame = cmds.frameLayout("about",
        label='News & Updates',
        cll=1,
        cl=0,
        bv=0,
        cc=partial(cmds.window, "mtxAutoRig", e=1, h=200),
        parent=about_layout
        )
    aboutText1 = cmds.text(l='Welcome to Matrix Auto Rig v0.1!\n', parent=about_Frame)
    aboutText2 = cmds.text(l='- This is the initial release with basic guide creation and rig structure setup.\n- More features coming soon!\n', parent=about_Frame)
    aboutText3 = cmds.text(l='\n- Stay tuned for updates on the <a href="https://github.com/MarcadrienLePape/maya-matrix-autorig">Github Repo.</a>', parent=about_Frame)
    
    howto_frame = cmds.frameLayout(
        label="How to use Matrix Auto Rig",
        collapsable=True,
        collapse=True,
        marginWidth=10,
        marginHeight=10,
        parent=about_Frame,
    )
    howtoText1 = cmds.text(l='1 - Set if quadriped (Not implemented yet)', parent=howto_frame)
    howtoText2 = cmds.text(l='2 - Set Number of arms/legs/spine controllers', parent=howto_frame)
    howtoText3 = cmds.text(l='3 - Generate Locators and place of character', parent=howto_frame)
    howtoText4 = cmds.text(l='4 - Set Naming options if wanted', parent=howto_frame)
    howtoText5 = cmds.text(l='5 - Generate the rig and get the joints from the joints group', parent=howto_frame)
    howtoText3 = cmds.text(l='6 - Skin and Enjoy !', parent=howto_frame)
    
    # separator
    sep_about = cmds.separator(h=8, style='in', parent=mainColumn)
    
    # ========================================================================================================
    # 2) Options Frame -> options layout
    # ========================================================================================================
    options_frame = cmds.frameLayout(
        label="Rig Generation Options",
        collapsable=True,
        collapse=True,
        marginWidth=10,
        marginHeight=10,
        parent=mainColumn,
        labelAlign='center'
    )
    option_column = cmds.columnLayout(adjustableColumn=True, parent=options_frame, columnAlign='center')
    
    is_quad_field = cmds.optionMenuGrp(
         l="Is quadriped?", 
         p=options_frame)
    cmds.menuItem(label="No")
    cmds.menuItem(label="Yes")

    arm_field = cmds.intFieldGrp(
        label="How many arms? (by side)",
        value1=1,
        numberOfFields=1,
        parent=options_frame
    )

    leg_field = cmds.intFieldGrp(
        label="How many legs? (by side)",
        value1=1,
        numberOfFields=1,
        parent=options_frame
    )

    spine_field = cmds.intFieldGrp(
        label="How many spine ctrls?",
        value1=3,
        numberOfFields=1,
        parent=options_frame
    )
    
    height_field = cmds.intFieldGrp(
        label="Character Height?",
        value1=20,
        numberOfFields=1,
        parent=options_frame
    )
    
    do_face_field = cmds.button(label="Face Auto Rig", height=30, command=facial_UI, parent=options_frame)
    
    # ========================================================================================================
    # separator
    # ========================================================================================================
    sep_options = cmds.separator(h=8, style='in', parent=mainColumn)

    # ========================================================================================================
    # 3) Create guides button
    # ========================================================================================================
    cmds.button(label="Generate Locator Guides", height=30, command=create_guides, parent=mainColumn)

    # ========================================================================================================
    # separator
    # ========================================================================================================
    sep_guides = cmds.separator(h=8, style='in', parent=mainColumn)
    
    # ========================================================================================================
    # 4) Naming Options Frame
    # ========================================================================================================
    naming_options_frame = cmds.frameLayout(
        label="Naming Options",
        collapsable=True,
        collapse=True,
        marginWidth=2,
        marginHeight=5,
        parent=options_frame,
        labelAlign='center'
        )
    naming_column = cmds.columnLayout(adjustableColumn=True, parent=naming_options_frame, columnAlign='center')

    naming_custom_frame = cmds.frameLayout(
            label="Custom Naming Options",
            collapsable=True,
            collapse=True,
            marginWidth=2,
            marginHeight=5,
            parent=naming_options_frame,
            labelAlign='center'
        )
    scroll_layout = cmds.scrollLayout(horizontalScrollBarThickness=0, verticalScrollBarThickness=16, height=300, parent=naming_custom_frame)
    custom_column = cmds.columnLayout(adjustableColumn=True, parent=scroll_layout, columnAlign='center')

    # ========================================================================================================
    # 5) Generate rig button
    # ========================================================================================================
    cmds.button(label="Generate Rig", height=30, command=generate_rig, parent=mainColumn)
    
    # ========================================================================================================
    # Footer
    # ========================================================================================================
    footer_frame = cmds.frameLayout(labelVisible=False, parent=mainForm, height=24, bgc=(0., 0.1, 0.1))
    sep_footer = cmds.separator(h=3, style='in', parent=footer_frame)
    linkText = cmds.text(l='Script by Marc-adrien LE PAPE', hl=True, parent=footer_frame)
    try:
        cmds.formLayout(mainForm, edit=True,
                        attachForm=[(mainScroll, 'top', 0), (mainScroll, 'left', 0), (mainScroll, 'right', 0),
                                    (footer_frame, 'left', 0), (footer_frame, 'right', 0), (footer_frame, 'bottom', 0)],
                        attachControl=[(mainScroll, 'bottom', 0, footer_frame)])
    except Exception:
        pass
    
    # ========================================================================================================
    # Naming Options Fields
    option_caps = cmds.radioButtonGrp(
        label="With Caps?",
        labelArray2=["Yes", "No"],
        numberOfRadioButtons=2,
        select=2,
        changeCommand=partial(update_naming_example),
        parent=naming_column
        )

    option_chrName = cmds.radioButtonGrp(
        label="Character Name Prefix?",
        labelArray2=["Yes", "No"],
        numberOfRadioButtons=2,
        select=2,
        changeCommand=partial(update_naming_example),
        parent=naming_column
        )
    
    char_name_field = cmds.textFieldGrp(
        label="Character Name:",
        text="",
        changeCommand=partial(update_naming_example),
        parent=naming_column,
        )
    
    naming_example = cmds.text(
        label="example : l_off_hand_jnt",
        align='center',
        parent=naming_column
        )
    
    custom_naming = cmds.radioButtonGrp(
        label="Custom Naming?",
        labelArray2=["Yes", "No"],
        numberOfRadioButtons=2,
        select=2,
        changeCommand=partial(toggle_custom_naming),
        parent=naming_column
        )  

    # ========================================================================================================
    # Custom Naming Constants Fields
    # ========================================================================================================
    text01 = cmds.text(l="Nodes", align='center', parent=custom_column)
    mtx_field = cmds.textFieldGrp(
        label="Matrix",
        text="Mtx",
        parent=custom_column
        )

    mtx_mlt_field = cmds.textFieldGrp(
        label="Multiply Matrix",
        text="MtxMlt",
        parent=custom_column
        )

    mtx_inv_field = cmds.textFieldGrp(
        label="Inverse Matrix",
        text="MtxInv",
        parent=custom_column
        )

    mtx_dcp_field = cmds.textFieldGrp(
        label="Decompose Matrix",
        text="MtxDcp",
        parent=custom_column
        )

    mtx_aim_field = cmds.textFieldGrp(
        label="Aim Matrix",
        text="MtxAim",
        parent=custom_column
        )

    wm_field = cmds.textFieldGrp(
        label="World Matrix",
        text="WM",
        parent=custom_column
        )

    pom_field = cmds.textFieldGrp(
        label="Parent Offset Matrix",
        text="POM",
        parent=custom_column
        )

    lom_field = cmds.textFieldGrp(
        label="Local Offset Matrix",
        text="LOM",
        parent=custom_column
        )

    jnt_field = cmds.textFieldGrp(
        label="Joint",
        text="JNT",
        parent=custom_column
        )

    gd_field = cmds.textFieldGrp(
        label="Guide",
        text="GD",
        parent=custom_column
        )

    ctrl_field = cmds.textFieldGrp(
        label="Controller",
        text="CTRL",
        parent=custom_column
        )

    ik_field = cmds.textFieldGrp(
        label="IK",
        text="IK",
        parent=custom_column
        )

    fk_field = cmds.textFieldGrp(
        label="FK",
        text="FK",
        parent=custom_column
        )

    dist_b_field = cmds.textFieldGrp(
        label="Distance Between",
        text="DistB",
        parent=custom_column
        )

    sum_field = cmds.textFieldGrp(
        label="Sum",
        text="Sum",
        parent=custom_column
        )

    mult_field = cmds.textFieldGrp(
        label="Multiply",
        text="Mult",
        parent=custom_column
        )

    mult_div_field = cmds.textFieldGrp(
        label="Multiply Divide",
        text="MultDiv",
        parent=custom_column
        )  

    grp_field = cmds.textFieldGrp(
        label="Group",
        text="Grp",
        parent=custom_column
        )
    
    text03 = cmds.text(l="Arm", align='center', parent=custom_column)
    sep01 = cmds.separator(h=8, style='in', parent=custom_column)
    
    arm_field_custom = cmds.textFieldGrp(
        label="Arm",
        text="Arm",
        parent=custom_column
        )

    sh_field = cmds.textFieldGrp(
        label="Shoulder",
        text="Sh",
        parent=custom_column
        )

    elb_field = cmds.textFieldGrp(
        label="Elbow",
        text="Elb",
        parent=custom_column
        )
    
    text04 = cmds.text(l="Hand", align='center', parent=custom_column)
    sep02 = cmds.separator(h=8, style='in', parent=custom_column)
    hand_field = cmds.textFieldGrp(
        label="Hand",
        text="Hand",
        parent=custom_column
        )
    
    thumb_field = cmds.textFieldGrp(
        label="Thumb",
        text="Tmb",
        parent=custom_column
        )
    
    index_field = cmds.textFieldGrp(
        label="Index",
        text="Idx",
        parent=custom_column
        )
    
    middle_field = cmds.textFieldGrp(
        label="Middle",
        text="Mid",
        parent=custom_column
        )
    
    ring_field = cmds.textFieldGrp(
        label="Ring",
        text="Rng",
        parent=custom_column
        )
    
    pinky_field = cmds.textFieldGrp(
        label="Pinky",
        text="Pnk",
        parent=custom_column
        )
    
    metacarpus_field = cmds.textFieldGrp(
        label="Metacarpus",
        text="Met",
        parent=custom_column
        )

    text05 = cmds.text(l="Legs", align='center', parent=custom_column)
    sep03 = cmds.separator(h=8, style='in', parent=custom_column)
    leg_field_custom = cmds.textFieldGrp(
        label="Leg",
        text="Leg",
        parent=custom_column
        )

    knee_field = cmds.textFieldGrp(
        label="Knee",
        text="Knee",
        parent=custom_column
        )

    ankle_field = cmds.textFieldGrp(
        label="Ankle",
        text="Ankle",
        parent=custom_column
        )

    foot_field = cmds.textFieldGrp(
        label="Foot",
        text="Foot",
        parent=custom_column
        )

    ball_field = cmds.textFieldGrp(
        label="Ball",
        text="Ball",
        parent=custom_column
        )

    toe_field = cmds.textFieldGrp(
        label="Toe",
        text="Toe",
            parent=custom_column
        )

    text06 = cmds.text(l="Spine", align='center', parent=custom_column)
    sep04 = cmds.separator(h=8, style='in', parent=custom_column)
    
    spine_field_custom = cmds.textFieldGrp(
        label="Spine",
        text="Spine",
        parent=custom_column
    )

    root_field = cmds.textFieldGrp(
        label="Root",
        text="Root",
        parent=custom_column
        )

    clavicle_field = cmds.textFieldGrp(
        label="Clavicle",
        text="Clavicle",
        parent=custom_column
        )
    
    text07 = cmds.text(l="Head", align='center', parent=custom_column)
    sep05 = cmds.separator(h=8, style='in', parent=custom_column)
    
    head_field = cmds.textFieldGrp(
        label="Head",
        text="Head",
        parent=custom_column
        )

    neck_field = cmds.textFieldGrp(
        label="Neck",
        text="Neck",
        parent=custom_column
        )

    eye_field = cmds.textFieldGrp(
        label="Eye",
        text="Eye",
        parent=custom_column
        )

    jaw_field = cmds.textFieldGrp(
        label="Jaw",
        text="Jaw",
        parent=custom_column
        )
    
    text08 = cmds.text(l="Sides", align='center', parent=custom_column)
    sep06 = cmds.separator(h=8, style='in', parent=custom_column)

    l_field = cmds.textFieldGrp(
        label="Left",
        text="L",
        parent=custom_column
        )

    r_field = cmds.textFieldGrp(
        label="Right",
        text="R",
        parent=custom_column
        )

    c_field = cmds.textFieldGrp(
        label="Center",
        text="C",
        parent=custom_column
        )

    # Initialize naming UI state (gray out custom naming if radio is set to No)
    try:
        # Ensure example text reflects defaults
        update_naming_example()
        toggle_custom_naming()
    except Exception:
        pass

    # Show the window
    try:
        cmds.showWindow(window)
    except Exception:
        pass

def facial_UI(*args):
    fac_window = cmds.window ("mtxAutoRig_facial", t="Matrix Auto Facial Rig", w=225, s=1)
    
    mainForm = cmds.formLayout(parent=fac_window)
    
    mainScroll = cmds.scrollLayout(horizontalScrollBarThickness=0,
                                verticalScrollBarThickness=16,
                                parent=mainForm)

    mainColumn = cmds.columnLayout(adjustableColumn=True,
                                columnAlign='center',
                                parent=mainScroll)
    
    howto_frame = cmds.frameLayout(
        label="How to use Matrix Auto Face Rig",
        collapsable=True,
        collapse=True,
        marginWidth=10,
        marginHeight=10,
        parent=mainColumn,
    )
    howtoText1 = cmds.text(l='1 - Set if quadriped (Not implemented yet)', parent=howto_frame)
    howtoText2 = cmds.text(l='2 - Set Number of arms/legs/spine controllers', parent=howto_frame)
    howtoText3 = cmds.text(l='3 - Generate Locators and place of character', parent=howto_frame)
    howtoText4 = cmds.text(l='4 - Set Naming options if wanted', parent=howto_frame)
    howtoText5 = cmds.text(l='5 - Generate the rig and get the joints from the joints group', parent=howto_frame)
    howtoText3 = cmds.text(l='6 - Skin and Enjoy !', parent=howto_frame)
        
    try:
        cmds.showWindow(fac_window)
    except Exception:
        pass



def toggle_custom_naming(*args):
    try:
        state = cmds.radioButtonGrp(custom_naming, q=True, select=True) == 1
    except:
        state = False
        
    try:
        cmds.frameLayout(naming_custom_frame, e=True, enable=state)
    except:
        pass

    update_naming_example()

def update_naming_example(*args):
    global addCaps, char_prefix
    try:
        addChrName = cmds.radioButtonGrp(option_chrName, q=True, select=True) == 1
    except:
        addChrName = False

    try:
        addCaps = cmds.radioButtonGrp(option_caps, q=True, select=True) == 1
    except:
        addCaps = False

    try:
        cmds.textFieldGrp(char_name_field, e=True, enable=addChrName)
    except:
        pass
    
    char_prefix = ""
    if addChrName:
        prefix = cmds.textFieldGrp(char_name_field, q=True, text=True)
        prefix = prefix.strip() if prefix else "chr"
        char_prefix = prefix + "_"
    
    if addChrName:    
        if addCaps:
            example = f"CHR_L_GRPOFF_Hand_01_JNT"
        else:
            example = f"chr_l_grpOff_hand_01_jnt"
    else:
        if addCaps:
            example = f"L_GRPOFF_Hand_01_JNT"
        else:
            example = f"l_grpOff_hand_01_jnt"

    try:
        cmds.text(naming_example, e=True, label=f"Example: {example}")
    except:
        pass

# ============================================================
# Initialization
# ============================================================
def main():
    showWindow = UI()
    return showWindow
# ============================================================
