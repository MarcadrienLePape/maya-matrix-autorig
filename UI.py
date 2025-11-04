import maya.cmds as cmds
import pymel.core as pm
import maya.mel as mel

from functools import partial

class MatrixAutoRigUI:
    def __init__(self, window_name="MatrixAutorig"):
        self.window_name = window_name
        self.window = None
        self.options_frame = None
        self.is_quad_field = None
        self.arm_field = None
        self.leg_field = None
        self.spine_field = None

    def create_window(self):
        if cmds.window(self.window_name, exists=True):
            cmds.deleteUI(self.window_name)
        self.window = cmds.window(
            self.window_name,
            title="Matrix autorig",
            sizeable=False,
            widthHeight=(500, 500)
        )
        cmds.columnLayout(adjustableColumn=True, columnAlign='center')  # center top column

        # --- Options Frame --- #
        self.options_frame = cmds.frameLayout(
            label="Rig Generation Options",
            collapsable=True,
            collapse=True,  # Start collapsed
            marginWidth=10,
            marginHeight=10,
            parent=self.window,
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
        cmds.separator(height=10, style='in')

        # --- Generate Locators Button ---  #
        cmds.button(
            label="Generate Locator Guides",
            height=30,
            command=self.generate_locators
        )

        # --- Separator --- #
        cmds.separator(height=10, style='in')

        # --- Naming Options Frame --- #
        self.options_frame = cmds.frameLayout(
            label="Naming Options",
            collapsable=True,
            collapse=True,
            marginWidth=2,
            marginHeight=5,
            parent=self.window,
            labelAlign='center'  # center frame label
        )
        cmds.columnLayout(adjustableColumn=True, parent=self.options_frame, columnAlign='center')

        self.option_caps = cmds.radioButtonGrp(
            label="With Caps?",
            labelArray2=["Yes", "No"],
            numberOfRadioButtons=2,
            select=2,
            changeCommand=self.update_naming_example,
            parent=self.options_frame
        )

        self.option_chrName = cmds.radioButtonGrp(
            label="Character Name Prefix?",
            labelArray2=["Yes", "No"],
            numberOfRadioButtons=2,
            select=2,
            changeCommand=self.update_naming_example,
            parent=self.options_frame
        )

        self.option_naming = cmds.optionMenuGrp(
            label="Naming Convention",
            changeCommand=self.update_naming_example,
            parent=self.options_frame
        )
        cmds.menuItem(label="chrName_Side_Group_Part_Number_Component")
        cmds.menuItem(label="chrName_Component_Group_Part_Number_Side")
        cmds.menuItem(label="chrName_Group_Component_Part_Side_Number")

        self.naming_example = cmds.text(
            label="example : l_off_hand_jnt",  # default for first menu item
            align='center',  # center the example text
            parent=self.options_frame
        )

        cmds.setParent('..')
        cmds.setParent('..')
        # --- Naming Options Frame End --- #

        # --- Separator --- #
        cmds.separator(height=10, style='in')

        # --- Generate Locators Button ---  #
        cmds.button(
            label="Generate Rig",
            height=30,
            command=self.generate_rig
        )

        # --- Separator --- #
        cmds.separator(height=10, style='in')

        cmds.showWindow(self.window)

    def update_naming_example(self, *args):
        sel = cmds.optionMenuGrp(self.option_naming, query=True, value=True)
        addChrName = cmds.radioButtonGrp(self.option_chrName, query=True, select=True) == 1
        addCapsName = cmds.radioButtonGrp(self.option_caps, query=True, select=True) == 1
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
