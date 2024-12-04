import os
import numpy as np
from plyfile import PlyData

def convert_ply_to_txt(ply_path, output_dir, class_mapping):
    # Read .ply file
    plydata = PlyData.read(ply_path)
    data = plydata.elements[0].data
    coords = np.vstack((data['x'], data['y'], data['z'])).T
    min_vals = np.min(coords, axis=0)
    # Shift the coordinates in the original data dictionary
    data['x'] = (data['x'] - min_vals[0]).astype(np.float32)
    data['y'] = (data['y'] - min_vals[1]).astype(np.float32)
    data['z'] = (data['z']).astype(np.float32)
    coords = np.vstack((data['x'], data['y'], data['z'])).T

    ########## Convert to float32 after shifting (Important!)
    coords = coords.astype(np.float32)
    colors = np.vstack((data['red'], data['green'], data['blue'])).T
    intensity = np.array(data['scalar_intensity'])
    labels = np.array(data['scalar_label'])

    # Debug: Print unique labels in the file
    unique_labels = np.unique(labels)
    print(f"Unique labels in {ply_path}: {unique_labels}")

    # Create output directory
    os.makedirs(output_dir, exist_ok=True)

    # Collect all points in one file
    all_points = []

    # Process each class
    for class_id, new_label in class_mapping.items():
        mask = labels == class_id
        if np.any(mask):
            points = np.hstack((
                coords[mask],
                colors[mask],
                intensity[mask, None],  # Add as a column
                np.full((mask.sum(), 1), new_label)  # Use the mapped label
            ))
            all_points.append(points)
        else:
            print(f"No points found for class {class_id} in {ply_path}")

    # Concatenate all points into a single array
    if all_points:
        all_points = np.vstack(all_points)
        # Save to a single file
        output_file = os.path.join(output_dir, f"{os.path.basename(ply_path).replace('.ply', '.txt')}")
        np.savetxt(output_file, all_points, fmt="%.6f %.6f %.6f %d %d %d %.6f %d")
        print(f"Saved all points to {output_file}")
    else:
        print(f"No points found in {ply_path}, skipping.")

# Path to your dataset
dataset_root = "/home/mehrdad/datasets/Victoriaville/2iem-exame/Mehrdad-Victoriaville"
output_root = "/home/mehrdad/Codes/PTV3-2/output_root"

# List of .ply files
ply_files = ["ND-Train-1.ply", "ND-Train-2.ply", "ND-Train-3.ply", "validation.ply"]

# Class mapping
class_mapping = {
    1: 0,   # other -> other
    2: 1,   # sidewalk -> sidewalk
    3: 2,   # road -> road and asphalt
    4: 9,   # building -> other
    5: 4,   # vegetation -> Vegetation
    6: 10,  # steps
    7: 11,  # Door
    8: 9,   # Fans
    9: 3,   # curb cut -> curb cut
    10: 0,  # Curb of jardin
    11: 8,  # Road-sign
    12: 0,  # trash can (unfixed) -> other
    13: 5,  # Tree
    14: 6,  # post -> post
    15: 0,  # Ad-Board
    16: 0,  # Wires
    17: 12,  # car
    18: 6,  # Traffic pole
    19: 7,  # Ramp
    20: 0,  # Barrier
    21: 0,  # Bench
    22: 0,  # Bicycle parking
    23: 0,  # pedestrian
    24: 9,  # stair Rod- Rambarde
    25: 8,  # Snow stick
    26: 0,  # Box -> Electricity-Box, Post-Box
    27: 0,  # Fire-Hydrant
    28: 0,  # Pot
    29: 8,  # Bollard
    30: 1,  # Beside of sid-walk
    31: 2   # Cross-Walk
}

# Convert each .ply file
for ply_file in ply_files:
    ply_path = os.path.join(dataset_root, ply_file)
    output_dir = output_root  # Single directory for all output files
    convert_ply_to_txt(ply_path, output_dir, class_mapping)
