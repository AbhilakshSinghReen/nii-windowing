from json import dumps
from os import listdir
from os.path import dirname, join

import nibabel as nib
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


def get_mean_and_std_of_volume(volume_path):
    nii_img = nib.load(volume_path)
    volume_data = nii_img.get_fdata()

    slice_means = []
    slice_stds = []
    slice_means_after_windowing = [0]
    slice_stds_after_windowing = [0]

    for z in range(volume_data.shape[2]):
        slice_data = volume_data[:, :, z]

        slice_means.append(np.mean(slice_data))
        slice_stds.append(np.std(slice_data))

        windowed_slice_data = get_windowed_slice(slice_data, 90, 120)
        slice_means_after_windowing.append(np.mean(windowed_slice_data))
        slice_stds_after_windowing.append(np.std(windowed_slice_data))

    return {
        'slices_overall_mean': np.mean(slice_means),
        'slices_overall_std': np.std(slice_stds),
        'slices_overall_mean_after_windowing': np.mean(slice_means_after_windowing),
        'slices_overall_stds_after_windowing': np.std(slice_stds_after_windowing),
    }


if __name__ == "__main__":
    for filename in listdir(dirname(__file__)):
        if not filename.endswith(".nii.gz"):
            continue

        file_path = join(dirname(__file__), filename)

        slice_meta = get_mean_and_std_of_volume(file_path)

        print(filename)
        print(dumps(slice_meta, indent=4))
        print()
        print()
