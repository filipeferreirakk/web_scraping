# Buscador de Ofertas Steam

Um script de linha de comando feito em Python para pesquisar e monitorar preços de jogos na Steam. Ele utiliza APIs públicas para buscar o valor atual, o menor preço histórico e listar as melhores promoções do momento, já fazendo a conversão automática de Dólar (USD) para Real (BRL).

## Funcionalidades

O sistema roda direto no terminal e possui um menu interativo com as seguintes opções:

* **Busca de Jogo:** Você digita o nome do jogo e ele retorna o preço atual na loja e o menor preço já registrado na história.
* **Promoções +80% OFF:** Lista os jogos que estão com os maiores descontos aplicados no momento.
* **Jogos até R$ 5,00:** Filtra opções extremamente baratas, mas foca na qualidade ordenando pelas melhores notas no Metacritic.

## Requisitos e Instalação

Para rodar este projeto, você vai precisar do Python instalado no seu sistema e da biblioteca `requests`.

1. Baixe ou clone este repositório para a sua máquina.
2. Instale a dependência necessária rodando o comando abaixo no seu terminal:
   pip install requests
3. Execute o script:
   python nome_do_arquivo.py

*(Lembre-se de substituir `nome_do_arquivo.py` pelo nome real do arquivo salvo)*

## APIs Utilizadas

Este projeto consome dados em tempo real das seguintes APIs:

* **AwesomeAPI:** Para obter a cotação atualizada do dólar.
* **Steam Store API:** Para buscar o nome oficial e o preço atualizado na loja brasileira.
* **CheapShark API:** Para consultar o menor preço histórico e varrer as listas de descontos gerais.