import numpy as np


def get_windowed_slice(slice_data, level=None, width=None):
    if level is None or width is None:
        window_lower_bound = np.min(slice_data)
        window_upper_bound = np.max(slice_data)
    else:
        window_lower_bound = level - width // 2
        window_upper_bound = level + width // 2

    slice_data = np.clip(slice_data, window_lower_bound, window_upper_bound)
    slice_data = ((slice_data - window_lower_bound) / (window_upper_bound - window_lower_bound)) * 255
    slice_data = slice_data.astype(np.uint8)

    return slice_data
