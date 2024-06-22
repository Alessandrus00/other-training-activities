""" This file is used to generate the the spedizioni.txt file """

import argparse
from utils import load_parameters, save_tsv_string, dict_list_to_tsv, generate_shipping_code, site_inside_subregion, read_classi_merc, read_mezzi_ger, load_matrix, none_or_int
import random
import os.path as osp

def get_args_parser():
    parser = argparse.ArgumentParser('Set parameters', add_help=False)
    parser.add_argument('--parameters', default='parameters.yaml', type=str, help="Path to the parameters file")
    parser.add_argument('--seed', default=442, type=none_or_int, help="Seed used for random choices")
    parser.add_argument('--output_dir', default='./instances', type=str, help="Where to store the spedizioni.txt")

    return parser


def restrict_sites(site_ids, params):
  """ Restrict the sites ID to the ones inside the designated area (if specified in the parameters.json file)"""  
  site_ids_restricted = []
  
  if params['all_region']:
    return site_ids
  
  for id in site_ids:
    px = int(id[:3])
    py = int(id[3:])

    x = params['subregion']['x']
    y = params['subregion']['y']
    w = params['subregion']['w']
    h = params['subregion']['h']

    if site_inside_subregion(px,py,x,y,w,h):
      site_ids_restricted.append(id)

  return site_ids_restricted


def build_shipping_table(params, output_dir):
  # get foreign keys
  classes_merc = read_classi_merc(osp.join(output_dir, "classi_merc.txt"))
  mezzi_ger = read_mezzi_ger(osp.join(output_dir, "mezzi_gerarchia.txt"))
  _, site_ids = load_matrix(osp.join(output_dir, "matrix_A_dist.txt"))

  site_ids = restrict_sites(site_ids, params)
  if len(site_ids) == 0:
    print("No sites in the specified subregion, please select a different one.")
    return

  # initialize the table
  shipping_table = []
  n_shippings = params['n_spedizioni']
  for i in range(n_shippings):
    row = {}

    row['CODICE'] = generate_shipping_code(i)

    shipping_type = random.choices(['RT','SL'], [params['ritiri'], 1 - params['ritiri']], k=1)[0]

    row['Tipo Sped (RT=ritiro, altro=consegna)'] = shipping_type

    row['ID_Destinazione_logistica'] = '0' if shipping_type == 'RT' else random.choice(site_ids)

    row['ID_posizione_cliente_ritiro'] = '0' if shipping_type != 'RT' else random.choice(site_ids)

    row['consegna Dalle'] = '06:00' if shipping_type == 'RT' else '08:00'
    row['consegna Alle'] = '20:00' if shipping_type == 'RT' else '13:00'

    row['sosta (minuti)'] = random.randint(1,5)

    row['vincolo 1 (classe merceologica)'] = random.choice(classes_merc)

    row['tempo di carico (minuti)'] = random.randint(1,5)

    row['ORARIO RITIRO dalle'] = '06:00' if shipping_type != 'RT' else '08:00'
    row['Ritiro alle'] = '17:30' if shipping_type != 'RT' else '14:00'

    row['colli'] = random.randint(1,10)
    row['bancali'] = 0
    row['Kg'] = random.randint(1,20)
    row['Volume'] = 0

    row['vincolo 2: tipologia_mezzo_richiesto_minima'] = random.choice(mezzi_ger)[0]

    row['consegna dalle finestra 2'] = '14:00'
    row['consegna alle finestra 2'] = '18:00'

    row['priorità'] = random.choice(['TASSATIVA','NORMALE','BASSA'])

    row['finestra_rigida (0=soft, 1=hard)'] = random.choices([0,1], [params['soft'], 1 - params['soft']], k=1)[0]

    row['nuovo destinatario'] = 'INDIRx'

    header = "CODICE	count(distinct ([Nr SPED]))	data_KPIontime	Data SPE	ID_Posizione_cliente_consegna	consegna Dalle	consegna Alle	sosta (minuti)	Tipo Sped (RT=ritiro, altro=consegna)	vincolo 1 (classe merceologica)	RAGIONE_SOC_CLI	destinatario	ind dest	loc dest	cap dest	pro dest	stato dest	pickup deposit (identifica la matrice delle distanze)	ID_posizione_cliente_ritiro	ind mitt	loc mitt	cap mitt	pro mitt	stato mittente	dropoff deposit	tempo di carico (minuti)	ORARIO RITIRO dalle	Ritiro alle	Colli	bancali	Kg	Volume	vincolo 2: tipologia_mezzo_richiesto_minima	consegna dalle finestra 2	consegna alle  finestra 2	priorità	finestra_rigida (0=soft, 1=hard)	nuovo destinatario"
    header = header.split('\t')

    for key in header:
      if key not in row:
        row[key] = "-"
    
    shipping_table.append(row)
  
  tsv_string = dict_list_to_tsv(shipping_table) # save it in tabular-separated format
  save_tsv_string(tsv_string, osp.join(output_dir, "spedizioni.txt"))
  print("Table saved to:", osp.join(output_dir, "spedizioni.txt"))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Set parameters", parents=[get_args_parser()])
    args = parser.parse_args()
    
    random.seed(args.seed)
    
    # Load the parameters
    params = load_parameters(args.parameters)
    spedizioni_param = params['spedizioni']
    
    # Build the shipping table and store it
    build_shipping_table(spedizioni_param, args.output_dir)