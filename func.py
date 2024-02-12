import threading
import time


def get_attr(obj, key, default=None):
    if isinstance(obj, dict):
        return obj.get(key, default)
    else:
        return getattr(obj, key, default)

