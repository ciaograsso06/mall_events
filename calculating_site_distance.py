import pymysql
import math

def conectar_db(host, user, password, db):
    conexao = pymysql.connect(host=host, user=user, password=password, database=db)
    return conexao

def buscar_shoppings_db(conexao):
    cursor = conexao.cursor(pymysql.cursors.DictCursor)
    query = "SELECT nome, endereco, latitude, longitude FROM inventario.shoppings"
    cursor.execute(query)
    shoppings = cursor.fetchall()
    cursor.close()
    return shoppings

def buscar_sites_db(conexao):
    cursor = conexao.cursor(pymysql.cursors.DictCursor)
    query = "SELECT nome, endereco, latitude, longitude FROM reports.sites"
    cursor.execute(query)
    sites = cursor.fetchall()
    cursor.close()
    return sites

def calcular_distancia(lat1, lon1, lat2, lon2):
    R = 6371 
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat/2) ** 2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon/2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distancia = R * c
    return distancia

def armazenar_dados_proximidade(conexao, shoppings, sites):
    cursor = conexao.cursor()
    query = """
    INSERT INTO sites_shoppings (shopping_nome, shopping_endereco, shopping_lat, shopping_lon, site_nome, site_endereco, site_lat, site_lon, distancia)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    
    for shopping in shoppings:
        for site in sites:
            distancia = calcular_distancia(
                shopping['latitude'], shopping['longitude'],
                site['latitude'], site['longitude']
            )
            if distancia <= 2:  # Apenas sites dentro de 2 km
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

conexao_inventario = conectar_db('host_inventario', 'user_inventario', 'password_inventario', 'inventario')
conexao_reports = conectar_db('host_reports', 'user_reports', 'password_reports', 'reports')

shoppings = buscar_shoppings_db(conexao_inventario)
sites = buscar_sites_db(conexao_reports)

armazenar_dados_proximidade(conexao_reports, shoppings, sites)
