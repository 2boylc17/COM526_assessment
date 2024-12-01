from robot import Robot


def is_robot(object):
    if isinstance(object, Robot):
        return True
    return False
