import requests
from datetime import datetime

def obter_cotacao_dolar():
    try:
        url = "https://economia.awesomeapi.com.br/last/USD-BRL"
        res = requests.get(url).json()
        return float(res['USDBRL']['bid'])
    except:
        return 5.50 

def buscar_jogo_completo():
    nome_input = input("\n Digite o nome do jogo: ")
    cotacao = obter_cotacao_dolar()
    
    url_steam = "https://store.steampowered.com/api/storesearch/"
    params_steam = {'term': nome_input, 'l': 'portuguese', 'cc': 'BR'}
    
    try:
        res_steam = requests.get(url_steam, params=params_steam).json()
        if not res_steam.get('items'):
            print(f" Jogo '{nome_input}' não encontrado na Steam.")
            return

        dados_steam = res_steam['items'][0]
        nome_oficial = dados_steam['name']
        preco_atual_brl = "Gratuito"
        if 'price' in dados_steam:
            preco_atual_brl = f"R$ {dados_steam['price']['final']/100:.2f}".replace('.', ',')

        url_cs_busca = "https://www.cheapshark.com/api/1.0/games"
        res_cs_id = requests.get(url_cs_busca, params={'title': nome_oficial, 'limit': 1}).json()
        historico_info = "Histórico não disponível"
        
        if res_cs_id:
            game_id = res_cs_id[0]['gameID']
            detalhes = requests.get(f"https://www.cheapshark.com/api/1.0/games?id={game_id}").json()
            menor_usd = float(detalhes['cheapestPriceEver']['price'])
            data_pt = datetime.fromtimestamp(detalhes['cheapestPriceEver']['date']).strftime('%d/%m/%Y')
            historico_info = f"R$ {menor_usd * cotacao:.2f} em {data_pt}"

        print("\n" + "—" * 65)
        print(f" JOGO: {nome_oficial.upper()}")
        print(f" Preço Atual na Loja: {preco_atual_brl}")
        print(f" Menor preço da história: {historico_info}")
        print("—" * 65)
    except Exception as e:
        print(f" Erro na busca: {e}")

def listar_jogos_baratos():
    cotacao = obter_cotacao_dolar()
    limite_brl = 5.00
    limite_usd = limite_brl / cotacao
    
    print(f"\n Buscando os MELHORES jogos abaixo de R$ {limite_brl:.2f}...")
    print(f"   (Filtro: Classificados por nota no Metacritic)")

    url = "https://www.cheapshark.com/api/1.0/deals"
    params = {
        'storeID': 1,
        'upperPrice': limite_usd,
        'sortBy': 'Metacritic',
        'pageSize': 10
    }
    
    try:
        res = requests.get(url, params=params).json()
        print(f"\n{'JOGO':<35} | {'NOTA':<4} | {'PREÇO (R$)':<10}")
        print("-" * 55)
        for item in res:
            nome = item['title'][:33]
            nota = item['metacriticScore']
            nota_exibida = nota if nota != "0" else "--"
            preco_brl = float(item['salePrice']) * cotacao
            
            print(f"{nome:<35} | {nota_exibida:<4} | R$ {preco_brl:>6.2f}")
    except:
        print(" Erro ao listar jogos baratos.")

def listar_promocoes_80():
    cotacao = obter_cotacao_dolar()
    print(f"\n Maiores descontos da Steam (+80% OFF)")
    url = "https://www.cheapshark.com/api/1.0/deals"
    params = {'storeID': 1, 'onSale': 1, 'pageSize': 15, 'sortBy': 'Savings'}
    
    try:
        res = requests.get(url, params=params).json()
        print(f"\n{'JOGO':<35} | {'DESC.':<6} | {'PREÇO (R$)':<10}")
        print("-" * 55)
        for item in res:
            desc = float(item['savings'])
            if desc >= 80:
                preco_brl = float(item['salePrice']) * cotacao
                print(f"{item['title'][:33]:<35} | {desc:>5.0f}% | R$ {preco_brl:>6.2f}")
    except:
        print(" Erro ao listar promoções.")

while True:
    print("\n" + "="*25)
    print("SISTEMA DE RASPAGEM STEAM")
    print("="*25)
    print("1. Buscar Jogo (Preço + Histórico)")
    print("2. Ver Ofertas (+80% OFF)")
    print("3. Jogos Bons até R$ 5,00")
    print("4. Sair")
    
    escolha = input("\nEscolha uma opção: ")
    
    if escolha == '1':
        buscar_jogo_completo()
    elif escolha == '2':
        listar_promocoes_80()
    elif escolha == '3':
        listar_jogos_baratos()
    elif escolha == '4':
        print("Até logo!")
        break
    else:
        print("Opção inválida.")