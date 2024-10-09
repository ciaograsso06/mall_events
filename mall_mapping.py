import requests
import pymysql
import math
from decouple import config

def buscar_shoppings(api_key, cidades):
    base_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    resultados = []

    for cidade in cidades:
        location = f"{cidade['latitude']},{cidade['longitude']}"
        radius = 50000  # 50 km

        params = {
            'key': api_key,
            'location': location,
            'radius': radius,
            'keyword': 'shopping'
        }

        response = requests.get(base_url, params=params)
        data = response.json()

        if 'results' in data:
            for place in data['results']:
                if 'name' in place and 'geometry' in place and 'location' in place['geometry']:
                    resultados.append({
                        'nome': place['name'],
                        'endereco': place.get('vicinity', ''),
                        'latitude': place['geometry']['location']['lat'],
                        'longitude': place['geometry']['location']['lng'],
                        'cidade': cidade['nome']
                    })

    return resultados

def buscar_sites_proximos(api_key, shopping):
    base_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    radius = 2000  # 2 km
    location = f"{shopping['latitude']},{shopping['longitude']}"
    
    params = {
        'key': api_key,
        'location': location,
        'radius': radius,
        'keyword': 'site'
    }
    
    response = requests.get(base_url, params=params)
    data = response.json()
    
    sites = []
    if 'results' in data:
        for place in data['results']:
            if 'name' in place and 'geometry' in place and 'location' in place['geometry']:
                sites.append({
                    'nome': place['name'],
                    'endereco': place.get('vicinity', ''),
                    'latitude': place['geometry']['location']['lat'],
                    'longitude': place['geometry']['location']['lng']
                })
    
    return sites

def calcular_distancia(lat1, lon1, lat2, lon2):
    R = 6371 
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat/2) ** 2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon/2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distancia = R * c
    return distancia

def conectar_db(host, user, password, db):
    conexao = pymysql.connect(host=host, user=user, password=password, database=db)
    return conexao

def armazenar_dados_proximidade_google(conexao, dados_shoppings):
    cursor = conexao.cursor()
    query = """
    INSERT INTO sites_shoppings (shopping_nome, shopping_endereco, shopping_lat, shopping_lon, site_nome, site_endereco, site_lat, site_lon, distancia)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    
    for shopping in dados_shoppings:
        sites_proximos = buscar_sites_proximos('AIzaSyBRFsDldUYeU9BGoPdP1m3U1t-APwsxgr8', shopping)
        for site in sites_proximos:
            distancia = calcular_distancia(
                shopping['latitude'], shopping['longitude'],
                site['latitude'], site['longitude']
            )
            cursor.execute(query, (
                shopping['nome'],
                shopping['endereco'],
                shopping['latitude'],
                shopping['longitude'],
                site['nome'],
                site['endereco'],
                site['latitude'],
                site['longitude'],
                distancia
            ))
    
    conexao.commit()
    cursor.close()


api_key = config('API_KEY')
cidades = [
{"codigo_ibge": 3550308, "nome": "São Paulo", "latitude": -23.5505, "longitude": -46.6333, "codigo_uf": 11, "regional": "TSP", "uf": "SP"},
{"codigo_ibge": 3304557, "nome": "Rio de Janeiro", "latitude": -22.9068, "longitude": -43.1729, "codigo_uf": 21, "regional": "TRJ", "uf": "RJ"},
{"codigo_ibge": 5300108, "nome": "Brasília", "latitude": -15.7801, "longitude": -47.9292, "codigo_uf": 61, "regional": "TCO", "uf": "DF"},
{"codigo_ibge": 2927408, "nome": "Salvador", "latitude": -12.9714, "longitude": -38.5014, "codigo_uf": 71, "regional": "TNE", "uf": "BA"},
{"codigo_ibge": 2304400, "nome": "Fortaleza", "latitude": -3.71722, "longitude": -38.5434, "codigo_uf": 85, "regional": "TNE", "uf": "CE"},
{"codigo_ibge": 2611606, "nome": "Recife", "latitude": -8.04756, "longitude": -34.877, "codigo_uf": 81, "regional": "TNE", "uf": "PE"},
{"codigo_ibge": 4314902, "nome": "Porto Alegre", "latitude": -30.0346, "longitude": -51.2177, "codigo_uf": 51, "regional": "TSL", "uf": "RS"},
{"codigo_ibge": 3106200, "nome": "Belo Horizonte", "latitude": -19.9167, "longitude": -43.9345, "codigo_uf": 31, "regional": "TLE", "uf": "MG"},
{"codigo_ibge": 4127107, "nome": "Curitiba", "latitude": -25.4195, "longitude": -49.2646, "codigo_uf": 41, "regional": "TSL", "uf": "PR"},
{"codigo_ibge": 1302603, "nome": "Manaus", "latitude": -3.10194, "longitude": -60.025, "codigo_uf": 92, "regional": "TNO", "uf": "AM"},
{"codigo_ibge": 5208707, "nome": "Goiânia", "latitude": -16.6864, "longitude": -49.2643, "codigo_uf": 62, "regional": "TCO", "uf": "GO"},
{"codigo_ibge": 3518800, "nome": "Guarulhos", "latitude": -23.4538, "longitude": -46.5333, "codigo_uf": 11, "regional": "TSP", "uf": "SP"},
{"codigo_ibge": 3509502, "nome": "Campinas", "latitude": -22.9056, "longitude": -47.0608, "codigo_uf": 19, "regional": "TSP", "uf": "SP"},
{"codigo_ibge": 2610707, "nome": "Jaboatão dos Guararapes", "latitude": -8.11298, "longitude": -35.0141, "codigo_uf": 81, "regional": "TNE", "uf": "PE"},
{"codigo_ibge": 1501402, "nome": "Belém", "latitude": -1.45502, "longitude": -48.5024, "codigo_uf": 91, "regional": "TNO", "uf": "PA"},
{"codigo_ibge": 3301702, "nome": "Duque de Caxias", "latitude": -22.7858, "longitude": -43.3048, "codigo_uf": 21, "regional": "TRJ", "uf": "RJ"},
{"codigo_ibge": 3304904, "nome": "São Gonçalo", "latitude": -22.8268, "longitude": -43.3049, "codigo_uf": 21, "regional": "TRJ", "uf": "RJ"},
{"codigo_ibge": 2923201, "nome": "Feira de Santana", "latitude": -12.2664, "longitude": -38.9663, "codigo_uf": 75, "regional": "TNE", "uf": "BA"},
{"codigo_ibge": 5201405, "nome": "Anápolis", "latitude": -16.3281, "longitude": -48.9534, "codigo_uf": 62, "regional": "TCO", "uf": "GO"},
{"codigo_ibge": 3548708, "nome": "São Bernardo do Campo", "latitude": -23.6914, "longitude": -46.5646, "codigo_uf": 11, "regional": "TSP", "uf": "SP"},
{"codigo_ibge": 3502804, "nome": "Santo André", "latitude": -23.6737, "longitude": -46.5436, "codigo_uf": 11, "regional": "TSP", "uf": "SP"},
{"codigo_ibge": 4314902, "nome": "Porto Alegre", "latitude": -30.0346, "longitude": -51.2177, "codigo_uf": 51, "regional": "TSL", "uf": "RS"},
{"codigo_ibge": 4305108, "nome": "Caxias do Sul", "latitude": -29.1678, "longitude": -51.1794, "codigo_uf": 54, "regional": "TSL", "uf": "RS"},
{"codigo_ibge": 4314408, "nome": "Novo Hamburgo", "latitude": -29.6842, "longitude": -51.475, "codigo_uf": 51, "regional": "TSL", "uf": "RS"},
{"codigo_ibge": 4205407, "nome": "Florianópolis", "latitude": -27.5954, "longitude": -48.548, "codigo_uf": 48, "regional": "TSL", "uf": "SC"},
{"codigo_ibge": 4209102, "nome": "Joinville", "latitude": -26.3045, "longitude": -48.8487, "codigo_uf": 47, "regional": "TSL", "uf": "SC"},
{"codigo_ibge": 4318705, "nome": "Santa Maria", "latitude": -29.6842, "longitude": -53.8069, "codigo_uf": 55, "regional": "TSL", "uf": "RS"},
{"codigo_ibge": 4216602, "nome": "Blumenau", "latitude": -26.9194, "longitude": -49.0661, "codigo_uf": 47, "regional": "TSL", "uf": "SC"},
{"codigo_ibge": 4106902, "nome": "Curitiba", "latitude": -25.4195, "longitude": -49.2646, "codigo_uf": 41, "regional": "TSL", "uf": "PR"},
{"codigo_ibge": 4113700, "nome": "Londrina", "latitude": -23.3101, "longitude": -51.1628, "codigo_uf": 43, "regional": "TSL", "uf": "PR"},
{"codigo_ibge": 4115209, "nome": "Maringá", "latitude": -23.4253, "longitude": -51.9389, "codigo_uf": 44, "regional": "TSL", "uf": "PR"},
{"codigo_ibge": 4119904, "nome": "Ponta Grossa", "latitude": -25.0916, "longitude": -50.1668, "codigo_uf": 42, "regional": "TSL", "uf": "PR"},
{"codigo_ibge": 2921008, "nome": "Camaçari", "latitude": -12.6996, "longitude": -38.3263, "codigo_uf": 71, "regional": "TNE", "uf": "BA"},
{"codigo_ibge": 2927408, "nome": "Salvador", "latitude": -12.9714, "longitude": -38.5014, "codigo_uf": 71, "regional": "TNE", "uf": "BA"},
{"codigo_ibge": 1501402, "nome": "Belém", "latitude": -1.45502, "longitude": -48.5024, "codigo_uf": 91, "regional": "TNO", "uf": "PA"},
{"codigo_ibge": 2304400, "nome": "Fortaleza", "latitude": -3.71722, "longitude": -38.5434, "codigo_uf": 85, "regional": "TNE", "uf": "CE"},
{"codigo_ibge": 2207702, "nome": "Teresina", "latitude": -5.09326, "longitude": -42.7675, "codigo_uf": 86, "regional": "TNE", "uf": "PI"},
{"codigo_ibge": 2611606, "nome": "Recife", "latitude": -8.04756, "longitude": -34.877, "codigo_uf": 81, "regional": "TNE", "uf": "PE"},
{"codigo_ibge": 2408102, "nome": "Natal", "latitude": -5.79448, "longitude": -35.211, "codigo_uf": 84, "regional": "TNE", "uf": "RN"},
{"codigo_ibge": 2507507, "nome": "João Pessoa", "latitude": -7.1195, "longitude": -34.845, "codigo_uf": 83, "regional": "TNE", "uf": "PB"},
{"codigo_ibge": 2704302, "nome": "Maceió", "latitude": -9.66599, "longitude": -35.735, "codigo_uf": 82, "regional": "TNE", "uf": "AL"},
{"codigo_ibge": 2800308, "nome": "Aracaju", "latitude": -10.9472, "longitude": -37.0731, "codigo_uf": 79, "regional": "TNE", "uf": "SE"},
{"codigo_ibge": 2903201, "nome": "Vitória da Conquista", "latitude": -14.8615, "longitude": -40.8442, "codigo_uf": 77, "regional": "TNE", "uf": "BA"},
{"codigo_ibge": 1302603, "nome": "Manaus", "latitude": -3.10194, "longitude": -60.025, "codigo_uf": 92, "regional": "TNO", "uf": "AM"},
{"codigo_ibge": 1400100, "nome": "Boa Vista", "latitude": 2.82384, "longitude": -60.6753, "codigo_uf": 95, "regional": "TNO", "uf": "RR"},
{"codigo_ibge": 1100205, "nome": "Porto Velho", "latitude": -8.76116, "longitude": -63.9004, "codigo_uf": 69, "regional": "TNO", "uf": "RO"},
{"codigo_ibge": 1200401, "nome": "Rio Branco", "latitude": -9.97499, "longitude": -67.8243, "codigo_uf": 68, "regional": "TNO", "uf": "AC"},
{"codigo_ibge": 1501402, "nome": "Belém", "latitude": -1.45502, "longitude": -48.5024, "codigo_uf": 91, "regional": "TNO", "uf": "PA"},
{"codigo_ibge": 1600303, "nome": "Macapá", "latitude": 0.034934, "longitude": -51.0694, "codigo_uf": 96, "regional": "TNO", "uf": "AP"}
]


dados_shoppings = buscar_shoppings(api_key, cidades)
conexao = conectar_db('host_db', 'user_db', 'password_db', 'nome_db')
armazenar_dados_proximidade_google(conexao, dados_shoppings)



    
