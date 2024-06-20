from app.utils import common


def get_devices(user):
    return common.filter_secondary_deleted(user.user_has_devices, "device")


def get_roles(user):
    return common.filter_secondary_deleted(user.user_has_roles, "role")
