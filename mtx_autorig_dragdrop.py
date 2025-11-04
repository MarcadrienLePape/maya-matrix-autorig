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
import maya.mel as mel  # type: ignore
import sys
import os

def main():

    this_file = os.path.realpath(__file__)
    this_dir = os.path.dirname(this_file)

    if this_dir not in sys.path:
        sys.path.append(this_dir)
        print(f"[MatrixAutoRig] Added to sys.path: {this_dir}")

    try:
        from matrixAutorig import UI as ui_mod
        ui = ui_mod.MatrixAutoRigUI()
        ui.create_window()
    except Exception:
        try:
            import importlib.util
            ui_path = os.path.join(this_dir, "matrixAutorig", "UI.py")
            if os.path.exists(ui_path):
                spec = importlib.util.spec_from_file_location("matrixAutorig.UI", ui_path)
                ui_mod = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(ui_mod)
                ui = ui_mod.MatrixAutoRigUI()
                ui.create_window()
                print(f"[MatrixAutoRig] UI launched from {ui_path}")
            else:
                raise ImportError("UI.py not found at " + ui_path)
        except Exception as e:
            cmds.warning(f"MatrixAutoRig error: {e}")

# ------------------------------------------------------------
# DRAG & DROP ENTRY POINT
# ------------------------------------------------------------
if __name__ == "__main__":
    main()
