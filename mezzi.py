""" This file is used to generate the the mezzi.txt file """

import argparse
from utils import load_parameters, save_tsv_string, dict_list_to_tsv, generate_truck_code, read_classi_merc, read_mezzi_ger, none_or_int
from datetime import datetime
import random
import os.path as osp


def get_args_parser():
    parser = argparse.ArgumentParser('Set parameters', add_help=False)
    parser.add_argument('--parameters', default='parameters.yaml', type=str, help="Path to the parameters file")
    parser.add_argument('--seed', default=442, type=none_or_int, help="Seed used for random choices")
    parser.add_argument('--output_dir', default='./instances', type=str, help="Where to store the mezzi.txt")

    return parser


def build_truck_table(n_trucks, output_dir):
  
    # get foreign keys
    classes_merc = read_classi_merc(osp.join(output_dir, "classi_merc.txt"))
    mezzi_ger = read_mezzi_ger(osp.join(output_dir, "mezzi_gerarchia.txt"))

    truck_table = []
    for i in range(n_trucks):
        row = {}

        row['ID_mezzo'] = generate_truck_code(i)
        row['Portata_colli'] = random.randint(80,120)
        row['Portata_pallet'] = random.randint(8,15)
        row['Portata_volume'] = round(random.uniform(900, 1200), 2)
        row['Portata_peso'] = round(random.uniform(900, 1200), 2)
        row['Costo_fisso_euro'] = round(random.uniform(40, 80), 2)
        row['Costo_perKm_euro'] = round(random.uniform(1, 1.7), 2)
        row['Tipologia_mezzo'] = random.choice(mezzi_ger)[0]

        n_classes_to_sample = random.randint(1, len(classes_merc))
        row['Elenco (Classe_1, Classe_2, Classe_3 …)'] = ','.join(random.sample(classes_merc, n_classes_to_sample))

        row['Tipo_distanze'] = 'NORMALE'
        row['ora_minima_inizio_giro'] = random.choice(['05:00', '06:00', '08:00'])
        row['pausa_inizia_a_partire_dalle'] = random.choice(['12:00','12:30','13:00'])
        row['pausa_finisce entro_le'] = '14:00'

        # Parse the time strings into datetime objects
        datetime1 = datetime.strptime(row['pausa_inizia_a_partire_dalle'], '%H:%M')
        datetime2 = datetime.strptime(row['pausa_finisce entro_le'], '%H:%M')

        # Calculate the difference in minutes
        row['durata_pausa'] = int(abs((datetime2 - datetime1).total_seconds() // 60))

        truck_table.append(row)
    
    tsv_string = dict_list_to_tsv(truck_table) # save it in tabular-separated format
    save_tsv_string(tsv_string, osp.join(output_dir, "mezzi.txt"))
    print("Table saved to:", osp.join(output_dir, "mezzi.txt"))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Set parameters", parents=[get_args_parser()])
    args = parser.parse_args()
    
    random.seed(args.seed)
    
    # Load the parameters
    params = load_parameters(args.parameters)
    mezzi_param = params['mezzi']
    
    # Build the trucks table and save it
    build_truck_table(mezzi_param['n_mezzi'], args.output_dir)