""" This file is used to generate the distance and time matrices from the randomly placed sites """

from utils import create_6_digit_id_from_pairs, save_matrix, load_parameters, none_or_int
import pickle as pk
import argparse
from scipy.spatial import distance_matrix
import numpy as np
import os.path as osp


def get_args_parser():
    parser = argparse.ArgumentParser('Set parameters', add_help=False)
    parser.add_argument('--parameters', default='parameters.yaml', type=str, help="Path to the parameters file")
    parser.add_argument('--seed', default=None, type=none_or_int, help="Seed used for random choices")
    parser.add_argument('--output_dir', default='./instances', type=str, help="Where to store the distance and time matrices")

    return parser


def apply_random_variations(distance_matrix, min_variation, max_variation):
    """ Apply random variation to the distance from (j,i) given the distance from (i,j) """
    # Replace all zeros with the value 3
    distance_matrix[distance_matrix == 0] = 3

    # Introduce variation for each distance (i, j) and (j, i)
    for i in range(distance_matrix.shape[0]):
        for j in range(i + 1, distance_matrix.shape[1]):
            distance = distance_matrix[i, j]
            variation = distance * np.random.uniform(min_variation, max_variation)
            distance_matrix[j, i] = distance + variation

    return distance_matrix

def create_time_matrix(dist_matrix, minutes_per_km_min, minutes_per_km_max):
    """ Create the time matrix from distance matrix chosing the number of minutes per Km at random in the range [minutes_per_km_min, minutes_per_km_max] """
    time_matrix = np.zeros_like(dist_matrix)

    # Introduce variation for each distance (i, j) and (j, i)
    for i in range(dist_matrix.shape[0]):
        for j in range(dist_matrix.shape[1]):
            distance = dist_matrix[i, j]
            time = distance * np.random.uniform(minutes_per_km_min, minutes_per_km_max)
            time_matrix[i, j] = round(time,1)
            
    return time_matrix

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Set parameters", parents=[get_args_parser()])
    args = parser.parse_args()
    
    # Load the parameters
    params = load_parameters(args.parameters)
    matrix_param = params['matrice']
    
    np.random.seed(args.seed)
    
    # Load the object from the file using pickle
    with open(osp.join(args.output_dir,"region_data.pkl"), 'rb') as file:
        region_data = pk.load(file)
    
    # Load the sites
    sites = region_data['sites']
    
    # Generate 6-digit ids for each site
    site_ids = create_6_digit_id_from_pairs(sites)

    # Create the distance matrix
    distances = distance_matrix(sites, sites)

    # Apply random variation to the distances and truncate to the integer value
    distances = apply_random_variations(distances, matrix_param['distanze']['min_variation'], matrix_param['distanze']['max_variation']).astype(int)
    
    # Create time matrix from distance matrix
    times = create_time_matrix(distances, matrix_param['tempi']['minutes_per_km_min'], matrix_param['tempi']['minutes_per_km_max'])
    
    # save distance matrix
    save_matrix(distances, site_ids, osp.join(args.output_dir, "matrix_A_dist.txt"))

    # save time matrix
    save_matrix(times, site_ids, osp.join(args.output_dir, "matrix_A_time.txt"))
