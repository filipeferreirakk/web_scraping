import requests
from datetime import datetime

def buscar_por_nome():
    nome_jogo = input("\nDigite o nome do jogo: ")
    url = "https://store.steampowered.com/api/storesearch/"
    parametros = {'term': nome_jogo, 'l': 'portuguese', 'cc': 'BR'}
    
    try:
        res = requests.get(url, params=parametros).json()
        if res.get('total', 0) > 0:
            jogo = res['items'][0]
            preco = f"R$ {jogo['price']['final']/100:.2f}" if 'price' in jogo else "Gratuito"
            print(f"\n Encontrado: {jogo['name']} | Preço Atual: {preco}")
        else:
            print("\n Jogo não encontrado.")
    except:
        print("\n Erro ao acessar a Steam.")

def ver_historico_preco():
    nome_jogo = input("\nDigite o nome do jogo para ver o histórico: ")
    
    url_busca = "https://www.cheapshark.com/api/1.0/games"
    params_busca = {'title': nome_jogo, 'limit': 1}
    
    try:
        res_busca = requests.get(url_busca, params=params_busca).json()
        
        if not res_busca:
            print(" Jogo não encontrado para histórico.")
            return

        game_id = res_busca[0]['gameID']
        nome_correto = res_busca[0]['external']

        url_detalhes = f"https://www.cheapshark.com/api/1.0/games?id={game_id}"
        res_detalhes = requests.get(url_detalhes).json()

        melhor_preco = res_detalhes['cheapestPriceEver']['price']
        data_timestamp = res_detalhes['cheapestPriceEver']['date']
        
        data_formatada = datetime.fromtimestamp(data_timestamp).strftime('%d/%m/%Y')

        print("-" * 40)
        print(f" HISTÓRICO DE: {nome_correto.upper()}")
        print(f" Menor preço já registrado: $ {melhor_preco}")
        print(f" Data do recorde: {data_formatada}")
        print(f" Dica: Se o preço atual for próximo de ${melhor_preco}, compre!")
        print("-" * 40)

    except Exception as e:
        print(f" Erro ao buscar histórico: {e}")

def listar_grandes_descontos():
    print("\n Buscando jogos com +80% de desconto...")
    url = "https://www.cheapshark.com/api/1.0/deals"
    parametros = {'storeID': 1, 'onSale': 1, 'pageSize': 15}
    
    try:
        res = requests.get(url, params=parametros).json()
        print(f"{'JOGO':<40} | {'DESC.':<6} | {'PREÇO':<10}")
        print("-" * 62)
        for item in res:
            desconto = float(item['savings'])
            if desconto >= 80:
                print(f"{item['title'][:38]:<40} | {desconto:>5.0f}% | $ {item['salePrice']:<10}")
    except:
        print("\n Erro ao carregar promoções.")

# --- Menu Principal ---
while True:
    print("\n" + "="*30)
    print("      STEAM HELPER")
    print("="*30)
    print("1. Buscar jogo por nome")
    print("2. Ver jogos com +80% de desconto")
    print("3. Ver Menor Preço Histórico (All-time Low)")
    print("4. Sair")
    
    opcao = input("\nEscolha uma opção: ")
    
    if opcao == '1':
        buscar_por_nome()
    elif opcao == '2':
        listar_grandes_descontos()
    elif opcao == '3':
        ver_historico_preco()
    elif opcao == '4':
        print("Saindo... Economize bastante!")
        break
    else:
        print("\n Opção inválida!")