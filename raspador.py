import requests

def buscar_preco_steam(nome_jogo):
    url = "https://store.steampowered.com/api/storesearch/"
    parametros = {
        'term': nome_jogo,
        'l': 'portuguese',
        'cc': 'BR'
    }
    
    try:
        resposta = requests.get(url, params=parametros)
        resposta.raise_for_status()
        dados = resposta.json()
        
        if dados.get('total', 0) > 0:
            jogo = dados['items'][0]
            nome_oficial = jogo.get('name')
            
            if 'price' in jogo:
                preco_real = jogo['price']['final'] / 100
                preco_formatado = f"R$ {preco_real:.2f}".replace('.', ',')
            else:
                preco_formatado = "Gratuito ou Indisponível"
                
            return nome_oficial, preco_formatado
        else:
            return None, "Jogo não encontrado."
            
    except Exception as e:
        return None, f"Erro na busca: {e}"


print("=== BUSCADOR DE PREÇOS STEAM ===")
print("Digite 'sair' para encerrar o programa.\n")

while True:
    busca_usuario = input("Digite o nome do jogo: ")

    if busca_usuario.lower() in ['sair', 'exit', 'quit', 's']:
        print("Encerrando... Até a próxima!")
        break

    nome, preco = buscar_preco_steam(busca_usuario)

    print("-" * 30)
    if nome:
        print(f"Jogo:  {nome}")
        print(f"Preço: {preco}")
    else:
        print(f"{preco}")
    print("-" * 30 + "\n")