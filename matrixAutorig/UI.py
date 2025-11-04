#################################################
# Matrix AutoRig UI Module
#################################################
# This file defines the user interface for the Matrix AutoRig tool.
# It includes options for rig generation and naming conventions that are changed in naming.py.
#################################################

import maya.cmds as cmds # type: ignore
import pymel.core as pm # type: ignore
import maya.mel as mel # type: ignore

class MatrixAutoRigUI:
    def __init__(self, window_name="MatrixAutorig"):
        self.window_name = window_name
        self.window = None
        self.options_frame = None
        self.is_quad_field = None
        self.arm_field = None
        self.leg_field = None
        self.spine_field = None
        self.naming_custom_frame = None

    def create_window(self):
        if cmds.window(self.window_name, exists=True):
            cmds.deleteUI(self.window_name)
        self.window = cmds.window(
            self.window_name,
            title="Matrix autorig",
            sizeable=False,
            widthHeight=(500, 500)
        )
        
        # Main scroll layout for the entire window
        main_scroll = cmds.scrollLayout(
            horizontalScrollBarThickness=0,
            verticalScrollBarThickness=16,
            parent=self.window
        )
        
        main_column = cmds.columnLayout(
            adjustableColumn=True, 
            columnAlign='center',
            parent=main_scroll
        )

        # --- Options Frame --- #
        self.options_frame = cmds.frameLayout(
            label="Rig Generation Options",
            collapsable=True,
            collapse=True,  # Start collapsed
            marginWidth=10,
            marginHeight=10,
            parent=main_column,
            labelAlign='center'  # center frame label
        )
        cmds.columnLayout(adjustableColumn=True, parent=self.options_frame, columnAlign='center')

        self.is_quad_field = cmds.optionMenuGrp(
            label="Is quadriped?",
            parent=self.options_frame
        )
        cmds.menuItem(label="No")
        cmds.menuItem(label="Yes")

        self.arm_field = cmds.intFieldGrp(
            label="How many arms? (by side)",
            value1=1,
            numberOfFields=1,
            parent=self.options_frame
        )

        self.leg_field = cmds.intFieldGrp(
            label="How many legs? (by side)",
            value1=1,
            numberOfFields=1,
            parent=self.options_frame
        )

        self.spine_field = cmds.intFieldGrp(
            label="How many spine ctrls?",
            value1=3,
            numberOfFields=1,
            parent=self.options_frame
        )

        cmds.setParent('..')
        cmds.setParent('..')
        # --- Options Frame End --- #

        # --- Separator --- #
        cmds.separator(height=10, style='in', parent=main_column)

        # --- Generate Locators Button ---  #
        cmds.button(
            label="Generate Locator Guides",
            height=30,
            command=self.generate_locators,
            parent=main_column
        )

        # --- Separator --- #
        cmds.separator(height=10, style='in', parent=main_column)

        # --- Naming Options Frame --- #
        self.naming_options_frame = cmds.frameLayout(
            label="Naming Options",
            collapsable=True,
            collapse=True,
            marginWidth=2,
            marginHeight=5,
            parent=main_column,
            labelAlign='center'  # center frame label
        )
        naming_column = cmds.columnLayout(adjustableColumn=True, parent=self.naming_options_frame, columnAlign='center')

        self.option_caps = cmds.radioButtonGrp(
            label="With Caps?",
            labelArray2=["Yes", "No"],
            numberOfRadioButtons=2,
            select=2,
            changeCommand=self.update_naming_example,
            parent=naming_column
        )

        self.option_chrName = cmds.radioButtonGrp(
            label="Character Name Prefix?",
            labelArray2=["Yes", "No"],
            numberOfRadioButtons=2,
            select=2,
            changeCommand=self.update_naming_example,
            parent=naming_column
        )

        self.option_naming = cmds.optionMenuGrp(
            label="Naming Convention",
            changeCommand=self.update_naming_example,
            parent=naming_column
        )
        cmds.menuItem(label="chrName_Side_Group_Part_Number_Component")
        cmds.menuItem(label="chrName_Component_Group_Part_Number_Side")
        cmds.menuItem(label="chrName_Group_Component_Part_Side_Number")

        self.naming_example = cmds.text(
            label="example : l_off_hand_jnt",
            align='center',
            parent=naming_column
        )

        self.custom_naming = cmds.radioButtonGrp(
            label="Custom Naming?",
            labelArray2=["Yes", "No"],
            numberOfRadioButtons=2,
            select=2,
            changeCommand=self.toggle_custom_naming,
            parent=naming_column
        )  

        self.char_name_field = cmds.textFieldGrp(
            label="Character Name:",
            text="",
            parent=naming_column,
            visible=False
        )

        cmds.setParent('..')
        cmds.setParent('..')
        # --- Naming Options Frame End --- #

        # --- Separator --- #
        cmds.separator(height=10, style='in', parent=main_column)

        # --- Generate Locators Button ---  #
        cmds.button(
            label="Generate Rig",
            height=30,
            command=self.generate_rig,
            parent=main_column
        )
        # --- Separator --- #
        cmds.separator(height=10, style='in', parent=main_column)

        cmds.showWindow(self.window)

    def toggle_custom_naming(self, *args):
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

    def create_custom_naming_frame(self):
        self.naming_custom_frame = cmds.frameLayout(
            label="Custom Naming Options",
            collapsable=True,
            collapse=False,
            marginWidth=2,
            marginHeight=5,
            parent=self.naming_options_frame,
            labelAlign='center'
        )
        
        scroll_layout = cmds.scrollLayout(
            horizontalScrollBarThickness=0,
            verticalScrollBarThickness=16,
            height=300,
            parent=self.naming_custom_frame
        )

        custom_column = cmds.columnLayout(
            adjustableColumn=True,
            parent=scroll_layout,
            columnAlign='center'
        )

        self.mtx_field = cmds.textFieldGrp(
            label="Matrix",
            text="Mtx",
            parent=custom_column
        )

        self.mtx_mlt_field = cmds.textFieldGrp(
            label="Multiply Matrix",
            text="MtxMlt",
            parent=custom_column
        )

        self.mtx_inv_field = cmds.textFieldGrp(
            label="Inverse Matrix",
            text="MtxInv",
            parent=custom_column
        )

        self.mtx_dcp_field = cmds.textFieldGrp(
            label="Decompose Matrix",
            text="MtxDcp",
            parent=custom_column
        )

        self.mtx_aim_field = cmds.textFieldGrp(
            label="Aim Matrix",
            text="MtxAim",
            parent=custom_column
        )

        self.wm_field = cmds.textFieldGrp(
            label="World Matrix",
            text="WM",
            parent=custom_column
        )

        self.pom_field = cmds.textFieldGrp(
            label="Parent Offset Matrix",
            text="POM",
            parent=custom_column
        )

        self.lom_field = cmds.textFieldGrp(
            label="Local Offset Matrix",
            text="LOM",
            parent=custom_column
        )

        self.jnt_field = cmds.textFieldGrp(
            label="Joint",
            text="JNT",
            parent=custom_column
        )

        self.gd_field = cmds.textFieldGrp(
            label="Guide",
            text="GD",
            parent=custom_column
        )

        self.ctrl_field = cmds.textFieldGrp(
            label="Controller",
            text="CTRL",
            parent=custom_column
        )

        self.ik_field = cmds.textFieldGrp(
            label="IK",
            text="IK",
            parent=custom_column
        )

        self.fk_field = cmds.textFieldGrp(
            label="FK",
            text="FK",
            parent=custom_column
        )

        self.dist_b_field = cmds.textFieldGrp(
            label="Distance Between",
            text="DistB",
            parent=custom_column
        )

        self.sum_field = cmds.textFieldGrp(
            label="Sum",
            text="Sum",
            parent=custom_column
        )

        self.mult_field = cmds.textFieldGrp(
            label="Multiply",
            text="Mult",
            parent=custom_column
        )

        self.mult_div_field = cmds.textFieldGrp(
            label="Multiply Divide",
            text="MultDiv",
            parent=custom_column
        )  

        self.grp_field = cmds.textFieldGrp(
            label="Group",
            text="Grp",
            parent=custom_column
        )
        
        # Part constants fields
        self.arm_field_custom = cmds.textFieldGrp(
            label="Arm",
            text="Arm",
            parent=custom_column
        )

        self.sh_field = cmds.textFieldGrp(
            label="Shoulder",
            text="Sh",
            parent=custom_column
        )

        self.elb_field = cmds.textFieldGrp(
            label="Elbow",
            text="Elb",
            parent=custom_column
        )

        self.hand_field = cmds.textFieldGrp(
            label="Hand",
            text="Hand",
            parent=custom_column
        )

        self.leg_field_custom = cmds.textFieldGrp(
            label="Leg",
            text="Leg",
            parent=custom_column
        )

        self.knee_field = cmds.textFieldGrp(
            label="Knee",
            text="Knee",
            parent=custom_column
        )

        self.ankle_field = cmds.textFieldGrp(
            label="Ankle",
            text="Ankle",
            parent=custom_column
        )

        self.foot_field = cmds.textFieldGrp(
            label="Foot",
            text="Foot",
            parent=custom_column
        )

        self.ball_field = cmds.textFieldGrp(
            label="Ball",
            text="Ball",
            parent=custom_column
        )

        self.toe_field = cmds.textFieldGrp(
            label="Toe",
            text="Toe",
            parent=custom_column
        )

        self.spine_field_custom = cmds.textFieldGrp(
            label="Spine",
            text="Spine",
            parent=custom_column
        )

        self.root_field = cmds.textFieldGrp(
            label="Root",
            text="Root",
            parent=custom_column
        )

        self.clavicle_field = cmds.textFieldGrp(
            label="Clavicle",
            text="Clavicle",
            parent=custom_column
        )

        self.head_field = cmds.textFieldGrp(
            label="Head",
            text="Head",
            parent=custom_column
        )

        self.neck_field = cmds.textFieldGrp(
            label="Neck",
            text="Neck",
            parent=custom_column
        )

        self.eye_field = cmds.textFieldGrp(
            label="Eye",
            text="Eye",
            parent=custom_column
        )

        self.jaw_field = cmds.textFieldGrp(
            label="Jaw",
            text="Jaw",
            parent=custom_column
        )

        # Side constants fields
        self.l_field = cmds.textFieldGrp(
            label="Left",
            text="L",
            parent=custom_column
        )

        self.r_field = cmds.textFieldGrp(
            label="Right",
            text="R",
            parent=custom_column
        )

        self.c_field = cmds.textFieldGrp(
            label="Center",
            text="C",
            parent=custom_column
        )

    def update_naming_example(self, *args):
        """Update the naming example text based on current settings"""
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

    def generate_locators(self, *args):
        # Placeholder for your locator generation logic
        cmds.confirmDialog(title="Info", message="Generate Locators clicked!", button=["OK"])

    def generate_rig(self, *args):
        # Placeholder for your rig generation logic
        cmds.confirmDialog(title="Info", message="Generate Rig clicked!", button=["OK"])

if __name__ == "__main__":
    ui = MatrixAutoRigUI()
    ui.create_window()

try:
    ui = MatrixAutoRigUI()
    ui.create_window()
except Exception as e:
    # In non-Maya environments importing maya.* will raise; keep silent or log minimal info
    print("MatrixAutoRig UI not launched:", e)
