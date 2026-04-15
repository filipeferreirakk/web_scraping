import requests

def buscar_por_nome():
    nome_jogo = input("\nDigite o nome do jogo: ")
    url = "https://store.steampowered.com/api/storesearch/"
    parametros = {'term': nome_jogo, 'l': 'portuguese', 'cc': 'BR'}
    
    try:
        res = requests.get(url, params=parametros).json()
        if res.get('total', 0) > 0:
            jogo = res['items'][0]
            preco = f"R$ {jogo['price']['final']/100:.2f}" if 'price' in jogo else "Gratuito"
            print(f"\n Encontrado: {jogo['name']} | Preço: {preco}")
        else:
            print("\n Jogo não encontrado.")
    except:
        print("\n Erro ao acessar a Steam.")

def listar_grandes_descontos():
    print("\n🔍 Buscando jogos com 80% ou mais de desconto na Steam...")
    url = "https://www.cheapshark.com/api/1.0/deals"
    parametros = {
        'storeID': 1,          
        'upperPrice': 50,    
        'onSale': 1,
        'pageSize': 15       
    }
    
    try:
        res = requests.get(url, params=parametros).json()
        encontrou = False
        
        print(f"{'JOGO':<40} | {'DESC.':<6} | {'PREÇO':<10}")
        print("-" * 62)
        
        for item in res:
            desconto = float(item['savings'])
            if desconto >= 80:
                nome = item['title'][:38]
                preco = f"R$ {float(item['salePrice']):.2f}"
                print(f"{nome:<40} | {desconto:>5.0f}% | {preco:<10}")
                encontrou = True
        
        if not encontrou:
            print("Nenhum jogo com mais de 80% de desconto no momento.")
            
    except Exception as e:
        print(f"\n Erro ao carregar promoções: {e}")

while True:
    print("\n" + "="*30)
    print("      MENU STEAM")
    print("="*30)
    print("1. Buscar jogo por nome")
    print("2. Ver jogos com +80% de desconto")
    print("3. Sair")
    
    opcao = input("\nEscolha uma opção: ")
    
    if opcao == '1':
        buscar_por_nome()
    elif opcao == '2':
        listar_grandes_descontos()
    elif opcao == '3':
        print("Saindo... Até logo!")
        break
    else:
        print("\n Opção inválida! Tente 1, 2 ou 3.")