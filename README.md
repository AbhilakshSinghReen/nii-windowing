# Steps to run Locally
### Clone this repository
`git clone https://github.com/AbhilakshSinghReen/nii-windowing.git`

### Move into the project directoyr
`cd nii-windowing`

### Install the dependencies
It is recommended to use a virtual environment.
`pip install -r requirements.txt`

### Place your data
Place your .nii.gz files in the `data` folder.

### Test Windowing
Modify the `get_windowed_slice` function in `windowing.py` to use your windowing logic.
Run `windowing_sanity_check.py`

### Get Data Average and Standard Deviation
Run `get_averages.py`
