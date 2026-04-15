import requests
from datetime import datetime

def buscar_jogo_completo():
    nome_input = input("\n Digite o nome do jogo: ")
    
    url_steam = "https://store.steampowered.com/api/storesearch/"
    params_steam = {'term': nome_input, 'l': 'portuguese', 'cc': 'BR'}
    
    try:
        res_steam = requests.get(url_steam, params=params_steam).json()
        
        if not res_steam.get('items'):
            print(f" Jogo '{nome_input}' não encontrado na Steam.")
            return

        dados_steam = res_steam['items'][0]
        nome_oficial = dados_steam['name']
        preco_atual = "Gratuito"
        
        if 'price' in dados_steam:
            preco_atual = f"R$ {dados_steam['price']['final']/100:.2f}".replace('.', ',')

        url_cs_busca = "https://www.cheapshark.com/api/1.0/games"
        res_cs_id = requests.get(url_cs_busca, params={'title': nome_oficial, 'limit': 1}).json()

        historico_info = "Histórico não disponível"
        
        if res_cs_id:
            game_id = res_cs_id[0]['gameID']
            url_cs_detalhes = f"https://www.cheapshark.com/api/1.0/games?id={game_id}"
            detalhes = requests.get(url_cs_detalhes).json()
            
            menor_preco = detalhes['cheapestPriceEver']['price']
            data_ts = detalhes['cheapestPriceEver']['date']
            data_pt = datetime.fromtimestamp(data_ts).strftime('%d/%m/%Y')
            historico_info = f"$ {menor_preco} (em {data_pt})"

        print("\n" + "—" * 45)
        print(f" JOGO: {nome_oficial.upper()}")
        print(f" Preço Atual: {preco_atual}")
        print(f" Menor preço histórico: {historico_info}")
        print("—" * 45)
        if "Gratuito" not in preco_atual:
            print(" Dica: O histórico é baseado no valor global (USD).")

    except Exception as e:
        print(f" Erro ao processar busca: {e}")

def listar_promocoes_80():
    print("\n Buscando jogos com 80% ou mais de desconto...")
    url = "https://www.cheapshark.com/api/1.0/deals"
    params = {'storeID': 1, 'onSale': 1, 'pageSize': 15}
    
    try:
        res = requests.get(url, params=params).json()
        print(f"\n{'JOGO':<35} | {'DESC.':<6} | {'PREÇO (USD)':<10}")
        print("-" * 55)
        for item in res:
            desc = float(item['savings'])
            if desc >= 80:
                print(f"{item['title'][:33]:<35} | {desc:>5.0f}% | $ {item['salePrice']:<10}")
    except:
        print(" Erro ao listar promoções.")

# --- MENU PRINCIPAL ---
while True:
    print("\n--- STEAM TRACKER ---")
    print("1. Buscar Jogo (Preço + Histórico)")
    print("2. Ver Ofertas (+80% OFF)")
    print("3. Sair")
    
    escolha = input("\nEscolha uma opção: ")
    
    if escolha == '1':
        buscar_jogo_completo()
    elif escolha == '2':
        listar_promocoes_80()
    elif escolha == '3':
        print("Até a próxima! Boas compras.")
        break
    else:
        print("Opção inválida.")