#################################################
# Matrix AutoRig
#
# By Marc-adrien LE PAPE
#
# www.malp-rigs.com
#
#################################################

import maya.cmds as cmds # type: ignore
import pymel.core as pm # type: ignore
import maya.mel as mel # type: ignore

from functools import partial

#-------------------------------------------------------------------------------------------------------------------------
# Create Guides #

num_spine = UI.spine_field
num_arms = UI.arm_field

def create_guides(num_spine, num_arms):

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
    LEG = constants["LEG"]

    # Create root locator
    root = cmds.spaceLocator(name="{}_{}".format(ROOT, GUIDE))[0]
    cmds.setAttr("{}.translateY".format(root), 1)

    cmds.parent(root, )

    # Create spine locators
    spine_guides = []

    for i in range(num_spine):
        loc = cmds.spaceLocator(name="{}_{}_{}".format(SPINE, i+1, GUIDE))[0]
        cmds.setAttr("{}.translateY".format(loc), 2 + i)
        spine_guides.append(loc)
        if i == 0:
            cmds.parent(loc, root)
        else:
            cmds.parent(loc, spine_guides[i-1])

    # Create arm locators (left and right)
    for side in [LEFT, RIGHT]:
        for arm_idx in range(num_arms):
            # Shoulder
            shoulder = cmds.spaceLocator(
                name="{}_{}_{}_{}_{}".format(side, ARM, arm_idx+1, SHOULDER, GUIDE)
            )[0]
            cmds.setAttr("{}.translateY".format(shoulder), 2 + num_spine - 1)
            offset = 1.5 + arm_idx * 1.5
            cmds.setAttr("{}.translateX".format(shoulder), offset if side == LEFT else -offset)
            cmds.parent(shoulder, spine_guides[-1])

            # Elbow
            elbow = cmds.spaceLocator(
                name="{}_{}_{}_{}_{}".format(side, ARM, arm_idx+1, ELBOW, GUIDE)
            )[0]
            cmds.setAttr("{}.translateY".format(elbow), 2 + num_spine - 1)
            cmds.setAttr("{}.translateX".format(elbow), (offset + 1.5) if side == LEFT else -(offset + 1.5))
            cmds.setAttr("{}.translateZ".format(elbow), 1)
            cmds.parent(elbow, shoulder)

            # Hand
            hand = cmds.spaceLocator(
                name="{}_{}_{}_{}_{}".format(side, ARM, arm_idx+1, HAND, GUIDE)
            )[0]
            cmds.setAttr("{}.translateY".format(hand), 2 + num_spine - 1)
            cmds.setAttr("{}.translateX".format(hand), (offset + 3) if side == LEFT else -(offset + 3))
            cmds.setAttr("{}.translateZ".format(hand), 2)
            cmds.parent(hand, elbow)

#-------------------------------------------------------------------------------------------------------------------------
# Create Rig

def generate_rig(*args):

#---------------------------------------------------------------------------------------------------------
# Utils

def hierarchy():

    constants = get_naming_constants()
    ROOT = constants["ROOT"]
    HEAD = constants["HEAD"]
    SPINE = constants["SPINE"]

    LEFT = constants["LEFT"]
    RIGHT = constants["RIGHT"]
    GUIDE = constants["GUIDE"]

    LEG = constants["LEG"]

    ARM = constants["ARM"]
    SHOULDER = constants["SHOULDER"]


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

#-------------------------------------------------------------------------------------------------------------------------
# Naming Constants

def get_naming_constants():
    constants = {}

    if UI.custom_naming == 2:
        if UI.addCapsName:
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
            "MATRIX": UI.mtx_field,
            "MULTIPLY_MATRIX": UI.mtx_mlt_field,
            "INVERSE_MATRIX": UI.mtx_inv_field,
            "DECOMPOSE_MATRIX": UI.mtx_dcp_field,
            "AIM_MATRIX": UI.mtx_aim_field,
            "WORLD_MATRIX": UI.wm_field,
            "PARENT_OFFSET_MATRIX": UI.pom_field,
            "LOCAL_OFFSET_MATRIX": UI.lom_field,
            "JOINT": UI.jnt_field,
            "GUIDE": UI.gd_field,
            "CONTROLLER": UI.ctrl_field,
            "IK": UI.ik_field,
            "FK": UI.fk_field,
            "DISTANCEBETWEEN": UI.dist_b_field,
            "SUM": UI.sum_field,
            "MULTIPLY": UI.mult_field,
            "MULTIPLYDIVIDE": UI.mult_div_field,
            "GROUP": UI.grp_field,
            "ARM": UI.arm_field_custom,
            "SHOULDER": UI.sh_field,
            "ELBOW": UI.elbow_field,
            "HAND": UI.hand_field,
            "LEG": UI.leg_field_custom,
            "KNEE": UI.knee_field,
            "ANKLE": UI.ankle_field,
            "FOOT": UI.foot_field,
            "BALL": UI.ball_field,
            "TOE": UI.toe_field,
            "SPINE": UI.spine_field_custom,
            "ROOT": UI.root_field,
            "CLAVICLE": UI.clavicle_field,
            "HEAD": UI.head_field,
            "NECK": UI.neck_field,
            "EYE": UI.eye_field,
            "JAW": UI.jaw_field,
            "LEFT": UI.l_field,
            "RIGHT": UI.r_field,
            "CENTER": UI.c_field,
        })

    return constants
#-------------------------------------------------------------------------------------------------------------------------
# UI

def UI():

    # Window -------------------------------------------------------------------------------------------
    if cmds.window ("mtxAutoRig", ex=1): cmds.deleteUI ("mtxAutoRig")
    window = cmds.window ("mtxAutoRig", t="Matrix Auto Rig v0.1", w=225, mnb=0, mxb=0, s=1,)
    
    # Layout -------------------------------------------------------------------------------------------
    mainLayout = cmds.formLayout("mtxAutoRigForm", numberOfDivisions=100)
    
    about_Frame = cmds.frameLayout("about", 
        label='News & Updates', 
        cll=1, 
        cl=0, 
        bv=0, 
        cc=partial(cmds.window, "mtxAutoRig", e=1, h=200))
    
    about_Layout = cmds.formLayout("aboutLayout", 
        numberOfDivisions=100, 
        bgc=(0.2, 0.2, 0.2))
    
    mainScroll = cmds.scrollLayout("mtxAutoRigScroll", 
        horizontalScrollBarThickness=0, 
        verticalScrollBarThickness=16, 
        parent=window)
    
    mainColumn = cmds.columnLayout("mtxAutoRigColumn", 
        adjustableColumn=True, 
        columnAlign='center', 
        parent=mainScroll)
    
    options_frame = cmds.frameLayout(
        label="Rig Generation Options",
        collapsable=True,
        collapse=True,
        marginWidth=10,
        marginHeight=10,
        parent=mainColumn,
        labelAlign='center'
    )
    
    option_column = cmds.columnLayout(adjustableColumn=True, 
        parent=options_frame, 
        columnAlign='center')

    naming_options_frame = cmds.frameLayout(
        label="Naming Options",
        collapsable=True,
        collapse=True,
        marginWidth=2,
        marginHeight=5,
        parent=mainColumn,
        labelAlign='center'
        )
    
    naming_column = cmds.columnLayout(adjustableColumn=True,
        parent=naming_options_frame,
        columnAlign='center')
    
    scroll_layout = cmds.scrollLayout(
        horizontalScrollBarThickness=0,
        verticalScrollBarThickness=16,
        height=300,
        parent=naming_custom_frame
        )

    custom_column = cmds.columnLayout(
        adjustableColumn=True,
        parent=scroll_layout,
        columnAlign='center'
        )

    cmds.setParent(mainLayout)

    # Labels -------------------------------------------------------------------------------------------
    linkText = cmds.text(l='<a href="https://github.com/MarcadrienLePape/maya-matrix-autorig">Github Repo.</a>', hl=True)

    # Separators -------------------------------------------------------------------------------------------
    sep01 = cmds.separator(h=10, parent=mainColumn)
    sep02 = cmds.separator(h=5, parent=mainColumn)
    sep03 = cmds.separator(h=15, parent=mainColumn)

    # Option Fields -------------------------------------------------------------------------------------------
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

    option_caps = cmds.radioButtonGrp(
        label="With Caps?",
        labelArray2=["Yes", "No"],
        numberOfRadioButtons=2,
        select=2,
        changeCommand=update_naming_example,
        parent=naming_column
        )

    option_chrName = cmds.radioButtonGrp(
        label="Character Name Prefix?",
        labelArray2=["Yes", "No"],
        numberOfRadioButtons=2,
        select=2,
        changeCommand=update_naming_example,
        parent=naming_column
        )

    option_naming = cmds.optionMenuGrp(
        label="Naming Convention",
        changeCommand=update_naming_example,
        parent=naming_column
        )
    cmds.menuItem(label="chrName_Side_Group_Part_Number_Component")
    cmds.menuItem(label="chrName_Component_Group_Part_Number_Side")
    cmds.menuItem(label="chrName_Group_Component_Part_Side_Number")

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
        changeCommand=toggle_custom_naming,
        parent=naming_column
        )  

    char_name_field = cmds.textFieldGrp(
        label="Character Name:",
        text="",
        parent=naming_column,
        visible=False
        )
    

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

    # Part constants fields
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

    hand_field = cmds.textFieldGrp(
        label="Hand",
        text="Hand",
        parent=custom_column
        )

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

    # Side constants fields
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
    
    # Buttons
    cmds.button(
        label="Generate Locator Guides",
        height=30,
        command=create_guides,
        parent=mainColumn
        )

    cmds.button(
        label="Generate Rig",
        height=30,
        command=generate_rig,
        parent=mainColumn
    )

def toggle_custom_naming(*args):
    naming = cmds.radioButtonGrp(self.custom_naming, query=True, select=True) == 1
        
    if naming and not self.naming_custom_frame:
        self.create_custom_naming_frame()
    elif not naming and self.naming_custom_frame:
        try:
            cmds.deleteUI(self.naming_custom_frame)
            self.naming_custom_frame = None
        except Exception as e:
            print(f"Error deleting custom naming frame: {e}")
        self.update_naming_example()

def create_custom_naming_frame():
        
    

def update_naming_example(self, *args):
    
    sel = cmds.optionMenuGrp(self.option_naming, query=True, value=True)
    addChrName = cmds.radioButtonGrp(self.option_chrName, query=True, select=True) == 1
    addCapsName = cmds.radioButtonGrp(self.option_caps, query=True, select=True) == 1
        
    # Show/hide character name field
    if addChrName:
        cmds.textFieldGrp(self.char_name_field, edit=True, visible=True)
    else:
        cmds.textFieldGrp(self.char_name_field, edit=True, visible=False)
    if addCapsName == False:
        if addChrName == False:
            if sel == "chrName_Side_Group_Part_Number_Component":
                text = "Example: l_grpOff_hand_01_jnt"
            elif sel == "chrName_Component_Group_Part_Number_Side":
                text = "Example: jnt_grpOff_hand_01_l"
            elif sel == "chrName_Group_Component_Part_Side_Number":
                text = "Example: grpOff_jnt_hand_l_01"
            else:
                text = "No Rig Here but Marc-adrien Le Pape is a total badass"
        else:
            if sel == "chrName_Side_Group_Part_Number_Component":
                text = "Example: chrName_l_grpOff_hand_01_jnt"
            elif sel == "chrName_Component_Group_Part_Number_Side":
                text = "Example: chrName_jnt_grpOff_hand_01_l"
            elif sel == "chrName_Group_Component_Part_Side_Number":
                text = "Example: chrName_grpOff_jnt_hand_l_01"
            else:
                text = "No Rig Here but Marc-adrien Le Pape is a not that good in code"
    else:
        if addChrName == False:
            if sel == "chrName_Side_Group_Part_Number_Component":
                text = "Example: L_GRPOff_Hand_01_JNT"
            elif sel == "chrName_Component_Group_Part_Number_Side":
                text = "Example: JNT_GRPOff_Hand_01_L"
            elif sel == "chrName_Group_Component_Part_Side_Number":
                text = "Example: GRPOff_JNT_Hand_L_01"
            else:
                text = "No Rig Here but Marc-adrien Le Pape is a really good guy"
        else:
            if sel == "chrName_Side_Group_Part_Number_Component":
                text = "Example: CHRNAME_L_GRPOff_hand_01_JNT"
            elif sel == "chrName_Component_Group_Part_Number_Side":
                text = "Example: CHRNAME_JNT_GRPOff_hand_01_L"
            elif sel == "chrName_Group_Component_Part_Side_Number":
                text = "Example: CHRNAME_GRPOff_JNT_hand_L_01"
            else:
                text = "No Rig Here but Marc-adrien Le Pape is Cool"
    cmds.text(self.naming_example, edit=True, label=text)


def main():
    showWindow = UI()
    return showWindow
# ============================================================
