# PLY to TXT Converter with Class Mapping
------------------------------------------------
This script converts `.ply` point cloud files to `.txt` format and maps the original class labels to a custom set of classes. This is often necessary when preparing data for deep learning tasks where you need to consolidate or re-organize your classes.

## How it Works

1. **Reads .ply file:** Uses the `plyfile` library to read the point cloud data from the input `.ply` file.
2. **Shifts coordinates:**  Shifts all point coordinates so that the minimum x and y values are 0. This can be helpful for certain deep learning models.
3. **Extracts data:** Extracts the x, y, z coordinates, RGB colors, intensity, and class labels from the `.ply` data.
4. **Maps classes:**  Maps the original class labels to new labels based on the provided `class_mapping` dictionary.
5. **Saves to .txt:**  Saves the processed point cloud data to a `.txt` file where each line represents a point with the following format:  `x y z r g b intensity new_label`.

## Usage

1. **Install dependencies:** Make sure you have the required libraries installed. You can install them using `pip`:

   ```bash
   pip install numpy plyfile
