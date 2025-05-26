#########################################################
# DATA EXTRACTION
# FROM INEGI'S API
# Author: Álvaro León
# Date: 26/05/2025
#########################################################

# Import libraries
import pandas as pd
import requests
import dotenv
import numpy as np
import os

# Load TOKEN
dotenv.load_dotenv()
TOKEN = os.getenv("INEGI_TOKEN")

# Setup for API call
COORDS = {
    'CDMX': {'LAT': 19.4326, 'LONG': -99.1970},  # Coord.: CDMX Polanco.
    'GDL': {'LAT': 20.672556, 'LONG': -103.363290},  # Coord.: GDL Americana.
    'MTY': {'LAT': 25.6573, 'LONG': -100.3703}  # Coord.: MTY San Pedro.
}
KEYWORD = 'restaurantes'  # Type of establishment to lookup in DNUE
RADIUS = 3500  # Radius (in meters) from coordinates

# URL's
URLS = []  # Store them here
CALL_STRUCTURE = 'https://www.inegi.org.mx/app/api/denue/v1/consulta/Buscar'

for i in COORDS.keys():

    LAT = COORDS[i]['LAT']
    LONG = COORDS[i]['LONG']

    URLS.append(f"{CALL_STRUCTURE}/{KEYWORD}/{LAT},{LONG}/{RADIUS}/{TOKEN}")

# Store responses
API_RESPONSE = []

# Retrieve data
for i in URLS:

    API_RESPONSE.append(requests.get(i).json())

# Concat into single dataframe
df = (
    pd
    .concat(
        [
            pd.DataFrame(API_RESPONSE[0]),
            pd.DataFrame(API_RESPONSE[1]),
            pd.DataFrame(API_RESPONSE[2])
        ],
        axis='index'
    )
)

# City column
df['city'] = np.where(df['Ubicacion'].str.contains('CIUDAD DE MÉXICO'), 'CDMX', df['Ubicacion'])
df['city'] = np.where(df['Ubicacion'].str.contains('MÉXICO'), 'CDMX', df['city'])
df['city'] = np.where(df['Ubicacion'].str.contains('JALISCO'), 'GDL', df['city'])
df['city'] = np.where(df['Ubicacion'].str.contains('NUEVO LEÓN'), 'MTY', df['city'])

# Column selection and naming
COL_NAMES = {
    'CLEE': 'inegi_id',
    'id': 'restaurant_id',
    'Nombre': 'restaurant_name',
    'Estrato': 'restaurant_capacity',
    'Calle': 'street_name',
    'Num_Exterior': 'ext_number',
    'Num_Interior': 'int_number',
    'Longitud': 'coord_long',
    'Latitud': 'coord_lat'
}
df = df[[x for x in df.columns if x in COL_NAMES.keys() or 'city' in x]]
df.rename(columns=COL_NAMES, inplace=True)

# Codify capacity column
REST_CAPACITY = {
    '0 a 5 personas': '0-5',
    '6 a 10 personas': '6-10',
    '11 a 30 personas': '11-30',
    '31 a 50 personas': '31-50',
    '51 a 100 personas': '51-100'
}
df['restaurant_capacity'] = df['restaurant_capacity'].map(REST_CAPACITY)

# Write into data folder
PATH = os.path.join('..', 'data', 'inegi_rest_data.csv')
df.to_csv(path_or_buf=PATH, index=False)
