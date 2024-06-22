""" This file is used to generate the classi_merceologiche.txt and mezzi_gerarchia.txt files according to the parameters.json file """

import argparse
from utils import load_parameters
import os.path as osp

def get_args_parser():
    parser = argparse.ArgumentParser('Set parameters', add_help=False)
    parser.add_argument('--parameters', default='parameters.yaml', type=str, help="Path to the parameters file")
    parser.add_argument('--output_dir', default='./instances', type=str, help="Where to store the classi_merceologiche.txt and mezzi_gerarchia.txt files")

    return parser


def create_classi_merceologiche(filepath, param):
    """ Create the classi merceologiche file from the parameters """
    with open(filepath, 'w') as f:
        f.writelines("Classe merceologica o vincolo 1\n")
        for el in param:
            f.writelines(el + '\n')
    
    print("Table saved to:", filepath)
            
def create_mezzi_gerarchia(filepath, param):
    """ Create the mezzi gerarchie file from the parameters """
    with open(filepath, 'w') as f:
        f.writelines("Tipologia Mezzo	gerarchia\n")
        for key, val in param.items():
            f.writelines(key + '\t' + str(val) + '\n')
    
    print("Table saved to:", filepath)

    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Set parameters", parents=[get_args_parser()])
    args = parser.parse_args()
    
    # Load the parameters
    params = load_parameters(args.parameters)
    
    # Create "classi_merceologiche.txt"
    create_classi_merceologiche(osp.join(args.output_dir, "classi_merc.txt"), params['classi_merceologiche'])
    
    # Create "mezzi_gerarchia.txt"
    create_mezzi_gerarchia(osp.join(args.output_dir, "mezzi_gerarchia.txt"), params['mezzi_gerarchia'])