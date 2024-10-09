# mall_events

# Shoppings do Brasil - Google Maps API

Este repositório contém um script Python que utiliza a API do Google Maps para buscar informações sobre shoppings localizados em diversas cidades do Brasil. O script faz requisições à API para retornar dados como nome, endereço, coordenadas (latitude e longitude) e os organiza em um arquivo CSV.

## Funcionalidades

- Busca shoppings em todas as capitais do Brasil e outras 100 cidades principais.
- Utiliza a API do Google Places (Google Maps) para obter detalhes dos shoppings.
- Armazena as informações dos shoppings em um arquivo CSV contendo:
  - Nome do Shopping
  - Endereço
  - Latitude e Longitude
  - Unidade Federativa (UF)
  - Regional (TSP, TRJ, TCO, TSL, TLE, TNE, TNO)

## Pré-requisitos

Antes de rodar o script, certifique-se de que você tem:

1. **Python 3.x** instalado. Se não tiver, baixe e instale a versão mais recente do [site oficial do Python](https://www.python.org/).
2. **API Key** do Google Maps. Para obter a sua chave de API:
   - Acesse o [Google Cloud Console](https://console.cloud.google.com/).
   - Crie um novo projeto ou selecione um existente.
   - Habilite a API "Places API".
   - Gere uma chave de API no menu "APIs e Serviços" > "Credenciais".
3. Instale as dependências necessárias:

   ```bash
   pip install -r requirements.txt
   ```

  ```bash
   git clone https://github.com/youruserhere/mall_events.git
   cd mall_events
  ```

4. Execute seu script com o comando:
   ```bash
   python mall_mapping.py
   ```
   
