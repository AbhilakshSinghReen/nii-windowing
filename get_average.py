from json import dumps
from os import listdir
from os.path import dirname, join

import nibabel as nib
import numpy as np

from windowing import get_windowed_slice


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
    for filename in listdir(join(dirname(__file__), "data")):
        if not filename.endswith(".nii.gz"):
            continue

        file_path = join(dirname(__file__), filename)

        slice_meta = get_mean_and_std_of_volume(file_path)

        print(filename)
        print(dumps(slice_meta, indent=4))
        print()
        print()
