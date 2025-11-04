import maya.cmds as cmds
from matrixAutorig.naming import LEFT, RIGHT, GUIDE, JAW, ROOT, SPINE, ARM, SHOULDER, ELBOW, HAND  # Add any other needed constants

def create_guides(num_spine=3, num_arms=1):
    """
    Create root, spine, and arm guides.
    :param num_spine: Number of spine controls (locators)
    :param num_arms: Number of arms per side
    """
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