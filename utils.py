import matplotlib.pyplot as plt
import numpy as np
import yaml
import os

def create_directory_if_not_exists(directory):
    """Create the directory if it does not exist."""
    if not os.path.exists(directory):
        os.makedirs(directory)

def none_or_int(value):
    if value.lower() == 'none':
        return None
    try:
        return int(value)
    except ValueError:
        raise argparse.ArgumentTypeError(f"{value} is not a valid integer or 'None'")

def site_inside_subregion(px, py, x, y, w, h):
    """Check if point (px, py) is inside rectangle (x, y, w, h)."""
    if x <= px <= x + w and y <= py <= y + h:
        return True
    else:
        return False

def read_classi_merc(filepath):
    # read the 'classi merceologiche'
    classes_merc = []
    with open(filepath, 'r') as f:
        lines = f.readlines()

    for line in lines[1:]:
        classes_merc.append(line.strip())
    
    return classes_merc

def read_mezzi_ger(filepath):
    # read the 'mezzi gerarchia'
    mezzi_ger = []
    with open(filepath, 'r') as f:
        lines = f.readlines()

    for line in lines[1:]:
        mezzi_ger.append(line.strip().split('\t'))
    
    return mezzi_ger

def generate_shipping_code(num):
    """Map a number to a unique string of 3 letters followed by a digit."""
    if num < 0 or num >= 26**3 * 10:
        raise ValueError("Number must be in the range 0 to 175759 (inclusive).")
    
    letters = []
    digit = num % 10
    num //= 10
    
    for _ in range(3):
        letters.append(chr((num % 26) + ord('A')))
        num //= 26
    
    return ''.join(reversed(letters)) + str(digit)

def generate_truck_code(num):
    """Map a number to a unique string of two letters followed by a number."""
    if num < 0 or num >= 26**2 * 10:
        raise ValueError("Number must be in the range 0 to 6759 (inclusive).")
    
    first_letter = chr(num // 10 // 26 + ord('A'))
    second_letter = chr(num // 10 % 26 + ord('A'))
    number = num % 10
    
    return f"{first_letter}{second_letter}{number}"

def save_tsv_string(tsv_string, filename):
    """Save a TSV string to a file."""
    with open(filename, 'w') as f:
        f.write(tsv_string)

def dict_list_to_tsv(dict_list):
    """Convert a list of dictionaries to a tab-separated values (TSV) string."""
    if not dict_list:
        return ""
    
    # Extract the headers from the keys of the first dictionary
    headers = dict_list[0].keys()
    tsv_string = "\t".join(headers) + "\n"
    
    # Convert each dictionary to a tab-separated line
    for dictionary in dict_list:
        tsv_string += "\t".join(str(dictionary[key]) for key in headers) + "\n"
    
    return tsv_string

def save_matrix(matrix, ids, filename):
    # Create the header row with "aaa" followed by the list of IDs
    header = "ID_partenzaxID_arrivo\t" + "\t".join(ids)

    # Initialize the lines list with the header
    lines = [header]

    # Add each row of the distance matrix, prefixed with the corresponding ID
    for i, row in enumerate(matrix):
        line = ids[i] + "\t" + "\t".join(map(str, row))
        lines.append(line)

    # Write the lines to the specified file
    with open(filename, 'w') as f:
        f.write("\n".join(lines))
    
    print("Matrix saved to:", filename)


def load_matrix(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()
    
    # Extract the header and the site IDs
    header = lines[0].strip().split('\t')
    site_ids = header[1:]  # Skip the first element ("ID_partenzaxID_arrivo")

    # Initialize an empty list to hold the matrix
    matrix = []

    # Read the rows of the matrix
    for line in lines[1:]:
        parts = line.strip().split('\t')
        row_id = parts[0]  # This is the row ID (can be ignored for the matrix)
        row = list(map(float, parts[1:]))  # Convert the row data to floats
        matrix.append(row)

    # Convert the distance matrix list to a numpy array
    matrix = np.array(matrix)
    
    return matrix, site_ids

def create_6_digit_id_from_pairs(pairs):
    def create_6_digit_id(num1, num2):
        # Ensure num1 and num2 are within the range [0, 999]
        if not (0 <= num1 <= 999) or not (0 <= num2 <= 999):
            raise ValueError("Numbers must be in the range [0, 999]")

        # Format each number as a 3-digit string with leading zeros if necessary
        str1 = f"{num1:03}"
        str2 = f"{num2:03}"

        # Concatenate the two 3-digit strings to form a 6-digit ID
        return str1 + str2

    # Process the list of pairs and generate the list of 6-digit IDs
    ids = [create_6_digit_id(num1, num2) for num1, num2 in pairs]

    return ids

    
def load_parameters(file_path):
    """Load parameters from a YAML file."""
    with open(file_path, 'r') as f:
        parameters = yaml.safe_load(f)
    return parameters


def plot_region(grid, sites, num_sites, region_width, region_height, filepath):
    # Plot the grid, city centers, and sites
    plt.figure(figsize=(10, 10))
    plt.scatter(*zip(*grid), s=5, color='lightgrey', label='Grid Points')  # Plot grid points
    # Plot sites
    plt.scatter(*zip(*sites), s=5, color='red', label='Pick-up/Delivery Sites')

    plt.title(f"{num_sites} Pick-up/Delivery Sites on a {region_width}x{region_height} km2 Region")
    plt.xlabel("X Coordinate (km)")
    plt.ylabel("Y Coordinate (km)")
    plt.legend()
    plt.grid(True)
    plt.savefig(filepath)