from app.utils import common


def get_users(role):
    return common.filter_secondary_deleted(role.user_has_roles, "user")
