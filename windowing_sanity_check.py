from os.path import dirname, join

import cv2
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


class VolumeDisplayer:
    def __init__(self, volume_path):
        self.nii_img = nib.load(volume_path)
        self.volume_affine = self.nii_img.affine
        self.volume_data = self.nii_img.get_fdata()
        self.num_axial_slices = self.volume_data.shape[2]

        self.current_axial_slice_index = 0
        self.current_level = np.mean(self.volume_data[:, :, 0])
        self.current_width = np.max(self.volume_data[:, :, 0]) - np.min(self.volume_data[:, :, 0])

        cv2.namedWindow("Volume")
        cv2.createTrackbar("Axial Slice", "Volume", 0, self.num_axial_slices - 1, self.on_axial_slice_trackbar)
        cv2.createTrackbar("Window Level", "Volume", -500, 500, self.on_window_level_trackbar)
        cv2.createTrackbar("Window Width", "Volume", 0, 1000, self.on_window_width_trackbar)

        self.on_axial_slice_trackbar(0)

        while True:
            if (cv2.waitKey(1) & 0xFF) == 27:
                break
        
        cv2.destroyAllWindows()

    def process_and_display_slice(self):
        slice_data = self.volume_data[:, :, self.current_axial_slice_index]
        slice_data = get_windowed_slice(slice_data, self.current_level, self.current_width)
        slice_data = slice_data.astype(np.uint8)

        cv2.imshow("Volume", slice_data)
    
    def on_axial_slice_trackbar(self, position):
        self.current_axial_slice_index = max(0, min(self.num_axial_slices - 1, position))
        self.process_and_display_slice()

    def on_window_level_trackbar(self, position):
        self.current_level = position
        self.process_and_display_slice()

    def on_window_width_trackbar(self, position):
        self.current_width = position
        self.process_and_display_slice()


if __name__ == "__main__":
    filename = "106272387_chest_cropped.nii.gz"
    file_path = join(dirname(__file__), filename)

    volume_displayer = VolumeDisplayer(file_path)
