from robot import Robot
from basestation import BaseStation


def is_robot(obj):
    if isinstance(obj, Robot):
        return True
    return False


def is_base_station(obj):
    if isinstance(obj, BaseStation):
        return True
    return False
