# Important files description

* `parameters.yaml`: parameters that will be used by the python scripts below to generate the synthetic data 
* `region.py`: script that generates the region and the pick-up/delivery sites
* `matrix.py`: script that creates "matrix_A_dist.txt" and "matrix_A_time.txt" according to the region data (saved as "region_data.pkl")
* `classi_merc_mezzi_ger.py`: script that generates "classi_merc.txt" and "mezzi_gerarchia.txt"
* `mezzi.py`: script that generates the "mezzi.txt" table
* `spedizioni.py`: script that generates the "spedizioni.txt" table

# Setup

To start generating the instances you need to setup the environment first. Assuming you have conda, you can hit the following:

```bash
conda create --name delivery python=3.10
conda activate delivery
pip install -r requirements.txt
```

# Start generating

To generate the required files you have to:
1. Change the parameters inside `parameters.yaml` to match the type of instance you want to generate
2. Run the following bash command, replacing <instance_directory> with the name of the directory that will contain your instance files.

**Note**: The directory will be created automatically if it does not exists already.
```bash
bash start.sh <instance_directory>
```