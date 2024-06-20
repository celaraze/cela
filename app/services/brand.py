def get_devices(brand):
    return [device for device in brand.devices if device.deleted_at is None]
