from robot import Robot
from basestation import BaseStation
from spot import EmptySpot


def is_robot(obj):
    if isinstance(obj, Robot):
        return True
    return False


def is_base_station(obj):
    if isinstance(obj, BaseStation):
        return True
    return False


def is_empty_spot(obj):
    if isinstance(obj, EmptySpot):
        return True
    return False
