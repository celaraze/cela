from app.utils import common


def get_brand(device):
    if device.brand is None:
        return None
    return device.brand


def get_category(device):
    if device.category is None:
        return None
    return device.category


def get_users(device):
    return common.filter_secondary_deleted(device.user_has_devices, "user")
