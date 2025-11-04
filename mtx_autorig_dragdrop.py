# ============================================================
# Matrix AutoRig - Drag & Drop Installer / Launcher
# ============================================================
# Description:
#   Drag this file into Maya's viewport to automatically
#   launch or install the Matrix AutoRig tool.
# ------------------------------------------------------------
# Author: Marc-adrien LE PAPE
# License: MIT
# ============================================================

import maya.cmds as cmds # type: ignore
import sys
import os


def main():
    """Main logic to launch Matrix AutoRig UI."""
    this_file = os.path.realpath(__file__)
    this_dir = os.path.dirname(this_file)

    if this_dir not in sys.path:
        sys.path.append(this_dir)
        print(f"[MatrixAutoRig] Added to sys.path: {this_dir}")

    try:
        # Import the UI module
        from matrixAutorig.UI import MatrixAutoRigUI

        # Create and show the window
        ui = MatrixAutoRigUI()
        ui.create_window()

        print("[MatrixAutoRig] Successfully launched UI!")
    except ImportError as e:
        cmds.warning(f"[MatrixAutoRig] ImportError: {e}")
    except Exception as e:
        cmds.warning(f"[MatrixAutoRig] Error: {e}")


# ------------------------------------------------------------
# REQUIRED ENTRY POINT FOR MAYA DRAG & DROP
# ------------------------------------------------------------
def onMayaDroppedPythonFile(*args):
    """Called automatically when this .py file is dropped into Maya."""
    main()

