""" This file is used to generate the the mezzi.txt file """

import argparse
from utils import *
import random
import os.path as osp


def get_args_parser():
    parser = argparse.ArgumentParser('Set parameters', add_help=False)
    parser.add_argument('--parameters', default='parameters.yaml', type=str, help="Path to the parameters file")
    parser.add_argument('--seed', default=None, type=none_or_int, help="Seed used for random choices")
    parser.add_argument('--output_dir', default='./instances', type=str, help="Where to store the mezzi.txt")

    return parser


def build_truck_table(mezzi_param, output_dir):
  
    # get foreign keys
    classes_merc = read_classi_merc(osp.join(output_dir, "classi_merc.txt"))
    mezzi_ger = read_mezzi_ger(osp.join(output_dir, "mezzi_gerarchia.txt"))

    truck_table = []
    n_trucks = mezzi_param['n_mezzi']
    for i in range(n_trucks):
        row = {}

        row['ID_mezzo'] = generate_truck_code(i)
        row['Portata_colli'] = random.randint(mezzi_param['portata_colli_min'],mezzi_param['portata_colli_max'])
        row['Portata_pallet'] = random.randint(mezzi_param['portata_pallet_min'],mezzi_param['portata_pallet_max'])
        row['Portata_volume'] = round(random.uniform(mezzi_param['portata_volume_min'],mezzi_param['portata_volume_max']), 2)
        row['Portata_peso'] = round(random.uniform(mezzi_param['portata_peso_min'],mezzi_param['portata_peso_max']), 2)
        row['Costo_fisso_euro'] = round(random.uniform(mezzi_param['costo_fisso_euro_min'],mezzi_param['costo_fisso_euro_max']), 2)
        row['Costo_perKm_euro'] = round(random.uniform(mezzi_param['costo_perKm_euro_min'],mezzi_param['costo_perKm_euro_max']), 2)
        row['Tipologia_mezzo'] = random.choice(mezzi_ger)[0]

        n_classes_to_sample = random.randint(1, len(classes_merc))
        row['Elenco (Classe_1, Classe_2, Classe_3 …)'] = ','.join(random.sample(classes_merc, n_classes_to_sample))

        row['Tipo_distanze'] = 'NORMALE'
        row['ora_minima_inizio_giro'] = random.choice(['05:00', '06:00', '08:00'])
        row['pausa_inizia_a_partire_dalle'] = '12:00'
        row['pausa_finisce entro_le'] = '14:00'

        row['durata_pausa'] = random.choice([30,60,90])

        truck_table.append(row)
    
    tsv_string = dict_list_to_tsv(truck_table) # save it in tabular-separated format
    save_tsv_string(tsv_string, osp.join(output_dir, "mezzi.txt"))
    print("Table saved to:", osp.join(output_dir, "mezzi.txt"))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Set parameters", parents=[get_args_parser()])
    args = parser.parse_args()
    
    # Check if output directory exists; otherwise create it
    create_directory_if_not_exists(args.output_dir)
    
    random.seed(args.seed)
    
    # Load the parameters
    params = load_parameters(args.parameters)
    mezzi_param = params['mezzi']
    
    # Build the trucks table and save it
    build_truck_table(mezzi_param, args.output_dir)