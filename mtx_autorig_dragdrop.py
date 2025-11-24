# ============================================================
# Matrix AutoRig - Drag & Drop Installer / Launcher
# ============================================================
# Author: Marc-adrien LE PAPE
# License: MIT
# ============================================================

import maya.cmds as cmds
import sys
import os

def main():
    this_dir = os.path.dirname(os.path.realpath(__file__))

    # Make sure the parent directory is in sys.path
    if this_dir not in sys.path:
        sys.path.append(this_dir)

    try:
        import matrixAutorig.mtxAutoRig as mtxAutoRig
        mtxAutoRig.main()
        print("[MatrixAutoRig] Launched successfully.")

    except Exception as e:
        cmds.warning(f"[MatrixAutoRig] Error: {e}")


def onMayaDroppedPythonFile(*args):
    main()
