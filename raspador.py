import requests

def buscar_preco_steam(nome_jogo):
    print(f"Buscando por '{nome_jogo}' na Steam...")
    
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
                preco_centavos = jogo['price']['final']
                
                preco_real = preco_centavos / 100
                preco_formatado = f"R$ {preco_real:.2f}".replace('.', ',')
            else:
                preco_formatado = "Gratuito (Free to Play) ou Indisponível"
                
            return nome_oficial, preco_formatado
            
        else:
            return None, "Nenhum jogo encontrado com esse nome."
            
    except requests.exceptions.RequestException as e:
        return None, f"Erro de conexão: {e}"

if __name__ == "__main__":
    lista_de_busca = ["Cyberpunk 2077", "Elden Ring", "Counter-Strike 2", "Stardew Valley"]
    
    print("-" * 40)
    for jogo_procurado in lista_de_busca:
        nome, preco = buscar_preco_steam(jogo_procurado)
        
        if nome:
            print(f"Jogo Encontrado: {nome}")
            print(f"Preço Atual: {preco}")
        else:
            print(f"Erro ao buscar '{jogo_procurado}': {preco}")
        print("-" * 40)