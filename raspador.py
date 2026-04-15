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
            url_cs_detalhes = f"https://www.cheapshark.com/api/1.0/games?id={game_id}"
            detalhes = requests.get(url_cs_detalhes).json()
            
            menor_preco_usd = float(detalhes['cheapestPriceEver']['price'])
            data_ts = detalhes['cheapestPriceEver']['date']
            data_pt = datetime.fromtimestamp(data_ts).strftime('%d/%m/%Y')
            
            menor_preco_convertido = menor_preco_usd * cotacao
            
            historico_info = (f"$ {menor_preco_convertido:.2f} "
                              f"em {data_pt}")

        print("\n" + "—" * 60)
        print(f" JOGO: {nome_oficial.upper()}")
        print(f" Preço Atual na Loja: {preco_atual_brl}")
        print(f" Menor preço da história: {historico_info}")
        print("-" * 60)

    except Exception as e:
        print(f" Erro ao processar busca: {e}")


def listar_promocoes_80():
    cotacao = obter_cotacao_dolar()
    print(f"\n Buscando jogos com +80% OFF (Dólar hoje: R$ {cotacao:.2f})")
    url = "https://www.cheapshark.com/api/1.0/deals"
    params = {'storeID': 1, 'onSale': 1, 'pageSize': 15}
    
    try:
        res = requests.get(url, params=params).json()
        print(f"\n{'JOGO':<35} | {'DESC.':<6} | {'PREÇO (R$ ESTIMADO)':<15}")
        print("-" * 70)
        for item in res:
            desc = float(item['savings'])
            if desc >= 80:
                preco_brl = float(item['salePrice']) * cotacao
                print(f"{item['title'][:33]:<35} | {desc:>5.0f}% | R$ {preco_brl:>6.2f}")
    except:
        print(" Erro ao listar promoções.")

while True:
    print("\n--- RASPADOR STEAM ---")
    print("1. Buscar Jogo (Preço + Histórico)")
    print("2. Ver Jogos com +80% OFF")
    print("3. Sair")
    
    escolha = input("\nEscolha uma opção: ")
    
    if escolha == '1':
        buscar_jogo_completo()
    elif escolha == '2':
        listar_promocoes_80()
    elif escolha == '3':
        print("Saindo... Economize muito!")
        break
    else:
        print("Opção inválida.")