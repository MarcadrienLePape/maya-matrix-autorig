import maya.cmds as cmds # type: ignore
from matrixAutorig.naming import MATRIX, MULTIPLY_MATRIX, INVERSE_MATRIX, DECOMPOSE_MATRIX, AIM_MATRIX, WORLD_MATRIX, PARENT_OFFSET_MATRIX, LOCAL_OFFSET_MATRIX, JOINT, GUIDE, CONTROLLER, IK, FK, DISTANCEBETWEEN, SUM, MULTIPLY, MULTIPLYDIVIDE, GROUP, ARM, SHOULDER, ELBOW, HAND, LEG, KNEE, ANKLE, FOOT, BALL, TOE, SPINE, ROOT, CLAVICLE, HEAD, NECK, EYE, JAW, LEFT, RIGHT, CENTER

def create_guides(num_spine=3, num_arms=1):

    # Create root locator
    root = cmds.spaceLocator(name="{}_{}".format(ROOT, GUIDE))[0]
    cmds.setAttr("{}.translateY".format(root), 1)

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
