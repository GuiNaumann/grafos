import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from collections import Counter
import plotly.graph_objects as go


# TODO: Função para carregar um grafo a partir de um arquivo CSV contendo arestas.
def carregar_grafo_de_arestas(caminho_arquivo, coluna_origem, coluna_destino, dirigido):
    """Carrega um grafo a partir de um arquivo CSV contendo arestas."""
    arestas = pd.read_csv(caminho_arquivo)

    if dirigido:
        grafo = nx.from_pandas_edgelist(arestas, source=coluna_origem, target=coluna_destino, create_using=nx.DiGraph())
    else:
        grafo = nx.from_pandas_edgelist(arestas, source=coluna_origem, target=coluna_destino, create_using=nx.Graph())

    return grafo

# TODO: Função para plotar um grafo, com a opção de amostrar nós para grafos grandes.
def plotar_grafo(grafo, titulo, amostra=None):
    if amostra and len(grafo.nodes) > amostra:
        print(f"Grafo grande detectado! Amostrando {amostra} nós para visualização...")
        nos_amostrados = list(grafo.nodes)[:amostra]
        grafo = grafo.subgraph(nos_amostrados)
    plt.figure(figsize=(10, 10))
    pos = nx.spring_layout(grafo, seed=42)
    nx.draw(
        grafo,
        pos,
        node_size=10,
        edge_color="gray",
        node_color="purple",
        with_labels=False,
        alpha=0.7
    )
    plt.title(titulo, fontsize=15)
    plt.show()


# TODO: Função para plotar a distribuição de graus dos vértices de um grafo.
def plotar_distribuicao_grau(grafo, titulo):
    graus = [grau for _, grau in grafo.degree()]
    plt.figure(figsize=(8, 6))
    plt.hist(graus, bins=30, color="blue", edgecolor="black", alpha=0.7)
    plt.title(f"Distribuição de Graus - {titulo}", fontsize=15)
    plt.xlabel("Grau")
    plt.ylabel("Frequência")
    plt.show()


def plotar_distribuicao_grau_plotly(grafo, titulo):
    graus = [grau for _, grau in grafo.degree()]
    quantidade = Counter(graus)
    graus_unicos = list(quantidade.keys())
    valores_quantidade = list(quantidade.values())

    fig = go.Figure(data=[
        go.Bar(
            x=graus_unicos,
            y=valores_quantidade,
            text=valores_quantidade,
            textposition='outside',
            marker=dict(
                color=valores_quantidade,
                colorscale=[
                    [0, 'indigo'],
                    [1, 'violet']
                ]
            )
        )
    ])

    fig.update_layout(
        title=dict(
            text=f"Distribuição de Graus - {titulo}",
            font=dict(size=20, color="black", family="Arial"),
            x=0.5  # Centraliza o título
        ),
        xaxis=dict(
            title="Grau",
            titlefont=dict(size=16, color="black", family="Arial"),
            rangeslider=dict(visible=True)
        ),
        yaxis=dict(
            title="Quantidade",
            titlefont=dict(size=16, color="black", family="Arial")
        ),
        bargap=0.15
    )
    fig.show()


# Função para calcular e exibir o grau médio
def calcular_grau_medio(grafo):
    """Calcula o grau médio do grafo."""
    if grafo.is_directed():
        # Grafo direcionado
        grau_medio_entrada = sum(dict(grafo.in_degree()).values()) / grafo.number_of_nodes()
        grau_medio_saida = sum(dict(grafo.out_degree()).values()) / grafo.number_of_nodes()
        print(f"Grau médio de entrada: {grau_medio_entrada:.2f}")
        print(f"Grau médio de saída: {grau_medio_saida:.2f}")
        return grau_medio_entrada, grau_medio_saida
    else:
        # Grafo não direcionado
        grau_medio = sum(dict(grafo.degree()).values()) / grafo.number_of_nodes()
        print(f"Grau médio: {grau_medio:.2f}")
        return grau_medio

# Função para plotar a distribuição de graus (geral, entrada e saída)
def plotar_distribuicao_graus(grafo, titulo):
    """Plota a distribuição de graus para grafos direcionados e não direcionados."""
    if grafo.is_directed():
        # Distribuição de graus de entrada
        graus_entrada = [grau for _, grau in grafo.in_degree()]
        plotar_histograma(graus_entrada, f"Distribuição de Graus de Entrada - {titulo}", "Grau de Entrada")

        # Distribuição de graus de saída
        graus_saida = [grau for _, grau in grafo.out_degree()]
        plotar_histograma(graus_saida, f"Distribuição de Graus de Saída - {titulo}", "Grau de Saída")
    else:
        # Distribuição de graus para grafos não direcionados
        graus = [grau for _, grau in grafo.degree()]
        plotar_histograma(graus, f"Distribuição de Graus - {titulo}", "Grau")

# Função auxiliar para plotar um histograma
def plotar_histograma(dados, titulo, xlabel):
    """Plota um histograma para os dados fornecidos."""
    plt.figure(figsize=(8, 6))
    plt.hist(dados, bins=30, color="purple", edgecolor="black", alpha=0.7)
    plt.title(titulo, fontsize=15)
    plt.xlabel(xlabel)
    plt.ylabel("Frequência")
    plt.show()


# Função para calcular e exibir o grau médio e plotar a distribuição
def calcular_e_plotar_graus(grafo, titulo):
    """
    Calcula o grau médio e gera gráficos de distribuição de graus de entrada e saída (para grafos direcionados).
    Para grafos não direcionados, calcula o grau geral.
    """
    if grafo.is_directed():
        # Para grafos direcionados: calcular graus de entrada e saída
        distribuicao_grau_entrada = [grau for _, grau in grafo.in_degree()]
        distribuicao_grau_saida = [grau for _, grau in grafo.out_degree()]

        # Grau médio
        grau_medio_entrada = sum(distribuicao_grau_entrada) / len(distribuicao_grau_entrada)
        grau_medio_saida = sum(distribuicao_grau_saida) / len(distribuicao_grau_saida)

        print(f"Grau médio de entrada: {grau_medio_entrada:.2f}")
        print(f"Grau médio de saída: {grau_medio_saida:.2f}")

        # Plotar distribuição de graus
        plotar_grafico_graus(distribuicao_grau_entrada, f"Distribuição de Graus de Entrada - {titulo}", "Grau de Entrada")
        plotar_grafico_graus(distribuicao_grau_saida, f"Distribuição de Graus de Saída - {titulo}", "Grau de Saída")
    else:
        # Para grafos não direcionados: calcular o grau geral
        distribuicao_grau = [grau for _, grau in grafo.degree()]
        grau_medio = sum(distribuicao_grau) / len(distribuicao_grau)
        print(f"Grau médio: {grau_medio:.2f}")

        # Plotar distribuição de graus
        plotar_grafico_graus(distribuicao_grau, f"Distribuição de Graus - {titulo}", "Grau")

# Função para plotar gráficos de distribuição de graus
def plotar_grafico_graus(dados, titulo, xlabel):
    """
    Plota a distribuição de graus com barra de rolagem.
    """
    # Contar a frequência de cada grau
    quantidade = Counter(dados)
    graus_unicos = list(quantidade.keys())
    valores_quantidade = list(quantidade.values())

    # Criar o gráfico
    fig = go.Figure(data=[
        go.Bar(
            x=graus_unicos,
            y=valores_quantidade,
            text=valores_quantidade,  # Adiciona os valores das frequências
            textposition='outside',   # Posiciona os textos fora das barras
            marker=dict(
                color=valores_quantidade,  # Baseia a cor na frequência
                colorscale=[
                    [0, 'indigo'],
                    [1, 'violet']
                ]
            )
        )
    ])

    fig.update_layout(
        title=dict(
            text=titulo,
            font=dict(size=20, color="black", family="Arial"),
            x=0.5  # Centraliza o título
        ),
        xaxis=dict(
            title=xlabel,
            titlefont=dict(size=16, color="black", family="Arial"),
            rangeslider=dict(visible=True)
        ),
        yaxis=dict(
            title="Quantidade",
            titlefont=dict(size=16, color="black", family="Arial")
        ),
        bargap=0.15  # Espaçamento entre as barras
    )

    fig.show()

def grafico_tamanho_componentes_agrupados(grafo, titulo="Distribuição dos Componentes"):
    if grafo.is_directed():
        # Componentes Fortemente Conectados
        componentes_fortes = list(nx.strongly_connected_components(grafo))
        tamanhos_fortes = [len(componente) for componente in componentes_fortes]
        frequencias_fortes = Counter(tamanhos_fortes)
        plotar_grafico_componentes(
            tamanhos=list(frequencias_fortes.keys()),
            frequencias=list(frequencias_fortes.values()),
            titulo=f"Distribuição de Componentes Fortemente Conectados - {titulo}",
            eixo_x="Tamanho do Componente",
            eixo_y="Quantidade de Componentes"
        )

        # Componentes Fracamente Conectados
        componentes_fracos = list(nx.weakly_connected_components(grafo))
        tamanhos_fracos = [len(componente) for componente in componentes_fracos]
        frequencias_fracos = Counter(tamanhos_fracos)
        plotar_grafico_componentes(
            tamanhos=list(frequencias_fracos.keys()),
            frequencias=list(frequencias_fracos.values()),
            titulo=f"Distribuição de Componentes Fracamente Conectados - {titulo}",
            eixo_x="Tamanho do Componente",
            eixo_y="Quantidade de Componentes"
        )
    else:
        # Componentes Conectados (para grafos não direcionados)
        componentes = list(nx.connected_components(grafo))
        tamanhos = [len(componente) for componente in componentes]
        frequencias = Counter(tamanhos)
        plotar_grafico_componentes(
            tamanhos=list(frequencias.keys()),
            frequencias=list(frequencias.values()),
            titulo=f"Distribuição de Componentes Conectados - {titulo}",
            eixo_x="Tamanho do Componente",
            eixo_y="Quantidade de Componentes"
        )


# Função para plotar gráficos interativos de componentes
def plotar_grafico_componentes(tamanhos, frequencias, titulo, eixo_x, eixo_y):
    """
    Plota gráficos de barra para distribuição de componentes.
    """
    fig = go.Figure(data=[
        go.Bar(
            x=tamanhos,
            y=frequencias,
            text=frequencias,
            textposition='outside',
            marker=dict(
                color=frequencias,
                colorscale=[
                    [0, 'indigo'],
                    [1, 'violet']
                ]
            )
        )
    ])

    fig.update_layout(
        title=dict(
            text=titulo,
            font=dict(size=20, color="black", family="Arial"),
            x=0.5
        ),
        xaxis=dict(
            title=eixo_x,
            titlefont=dict(size=16, color="black", family="Arial"),
            rangeslider=dict(visible=True)
        ),
        yaxis=dict(
            title=eixo_y,
            titlefont=dict(size=16, color="black", family="Arial")
        ),
        bargap=0.15
    )

    fig.show()

    # Função para calcular e plotar a distribuição das distâncias
def grafico_distancia_pares(grafo, titulo="Distância Média e Distribuição"):
    """
    Calcula a distância média e a distribuição das distâncias entre todos os pares de vértices.
    Plota a distribuição das distâncias.
    """
    if grafo.is_directed():
        # Calcula as distâncias para grafos dirigidos
        distancias = dict(nx.all_pairs_shortest_path_length(grafo))
    else:
        # Calcula as distâncias para grafos não dirigidos
        distancias = dict(nx.all_pairs_shortest_path_length(grafo.to_undirected()))

    # Extrair todas as distâncias calculadas
    todas_distancias = []
    for origem, destinos in distancias.items():
        todas_distancias.extend(destinos.values())

    # Filtrar apenas distâncias finitas (desconsidera vértices desconectados)
    todas_distancias = [d for d in todas_distancias if d < float('inf')]

    # Calcular a distância média
    distancia_media = np.mean(todas_distancias)

    # Contar a frequência de cada distância
    distribuicao = Counter(todas_distancias)
    distancias_unicas = list(distribuicao.keys())
    frequencias = list(distribuicao.values())

    # Criar o gráfico de distribuição das distâncias
    fig = go.Figure(data=[
        go.Bar(
            x=distancias_unicas,
            y=frequencias,
            text=frequencias,
            textposition='outside',
            marker=dict(
                color=frequencias,
                colorscale="Viridis"
            )
        )
    ])
    fig.update_layout(
        title=dict(
            text=f"Distribuição das Distâncias - {titulo}",
            font=dict(size=20, color="black", family="Arial"),
            x=0.5  # Centraliza o título
        ),
        xaxis=dict(
            title="Distância",
            titlefont=dict(size=16, color="black", family="Arial"),
            rangeslider=dict(visible=True)  # Habilita barra de rolagem
        ),
        yaxis=dict(
            title="Quantidade",
            titlefont=dict(size=16, color="black", family="Arial")
        ),
        bargap=0.15  # Espaçamento entre as barras
    )
    fig.show()

    return distancia_media
def encontrar_pontes(grafo):
    """
    Identifica arestas que são pontes em um grafo.
    Utiliza uma abordagem baseada em DFS e valores low-link.
    Funciona para grafos não direcionados.
    """
    # Inicializações
    discovery = {}  # Tempo de descoberta (disc)
    low = {}        # Valor low-link
    parent = {}     # Pai no DFS
    pontes = []     # Lista para armazenar pontes
    tempo = [0]     # Tempo de descoberta global (imutável no escopo)

    def dfs(u):
        discovery[u] = low[u] = tempo[0]
        tempo[0] += 1

        for v in grafo.neighbors(u):
            if v not in discovery:  # v não foi visitado
                parent[v] = u
                dfs(v)

                # Atualizar low-link de u com base no retorno de v
                low[u] = min(low[u], low[v])

                # Verificar se a aresta (u, v) é uma ponte
                if low[v] > discovery[u]:
                    pontes.append((u, v))
            elif parent.get(u) != v:  # Atualizar low-link de u com base no ciclo
                low[u] = min(low[u], discovery[v])

    # Executar DFS para todos os vértices
    for u in grafo.nodes:
        if u not in discovery:
            dfs(u)

    return pontes

# TODO: Dicionário que configura os caminhos dos arquivos de entrada e suas colunas.
# Configurar os caminhos dos arquivos
arquivos_dados = {
    "deezer": {
        "caminho": "social_networks/deezer_europe/deezer_europe_edges.csv",
        "coluna_origem": "node_1",
        "coluna_destino": "node_2",
        "bool": True
    },
    # "facebook": {
    #     "caminho": "social_networks/facebook_large/musae_facebook_edges.csv",
    #     "coluna_origem": "id_1",
    #     "coluna_destino": "id_2",
    #     "bool": False
    # },
    "lastfm": {
        "caminho": "social_networks/lastfm_asia/lastfm_asia_edges.csv",
        "coluna_origem": "node_1",
        "coluna_destino": "node_2",
        "bool": True
    },
    "scientometrics": {
        "caminho": "scientometrics/scientometrics/scientometrics.net"
    }
}

# TODO: Bloco principal para processar os grafos das redes sociais e exibir análises.
# Processar grafos das redes sociais
resultados = {}
for rede in ["deezer", "lastfm"]:
    print(f"\n{'=' * 60}")
    print(f"Processando a Rede: {rede.capitalize()}")
    print(f"{'=' * 60}\n")

    # TODO: Carregar o grafo da rede social atual.
    grafo = carregar_grafo_de_arestas(
        arquivos_dados[rede]["caminho"],
        arquivos_dados[rede]["coluna_origem"],
        arquivos_dados[rede]["coluna_destino"],
        arquivos_dados[rede]["bool"]
    )
    print(f"Grafo carregado com sucesso: {len(grafo.nodes):,} nós, {len(grafo.edges):,} arestas.\n")


# todo: ################################################################################################################
# todo: ################################################################################################################
# todo: ################################################################################################################
# todo: ################################################################################################################

    # TODO: Plotar o grafo (Questão 1A).
    # Questão 1A: Plotar o grafo
    print(f"{'-' * 40}")
    print(f"Questão 1A: Plotando o Grafo")
    print(f"{'-' * 40}")
    plotar_grafo(grafo, f"Grafo da Rede {rede.capitalize()}", amostra=500)


# todo: ################################################################################################################
# todo: ################################################################################################################
# todo: ################################################################################################################
# todo: ################################################################################################################



    # Questão 1B: Calcular o grau médio e gerar gráficos
    print(f"\n{'-' * 40}")
    print(f"Questão 1B: Grau Médio e Distribuição de Graus")
    print(f"{'-' * 40}")
    calcular_e_plotar_graus(grafo, f"Rede {rede.capitalize()}")




# todo: ################################################################################################################
# todo: ################################################################################################################
# todo: ################################################################################################################
# todo: ################################################################################################################


    # # TODO: Plotar a distribuição de graus (Questão 1C).
    # # Questão 1C: Plotar a distribuição de graus
    print(f"\n{'-' * 40}")
    print(f"Questão 1C: Distribuição de Graus")
    print(f"{'-' * 40}")
    # plotar_distribuicao_grau(grafo, f"Rede {rede.capitalize()}")
    # plotar_distribuicao_grau(grafo, f"Rede {rede.capitalize()}")
    # Plotar a distribuição com plotly
    plotar_distribuicao_grau_plotly(grafo, f"Rede {rede.capitalize()}")

# todo: ################################################################################################################
# todo: ################################################################################################################
# todo: ################################################################################################################
# todo: ################################################################################################################


    # TODO: Calcular o número de componentes conexos e o tamanho do maior componente (Questão 1D).
    # Atualizando a Questão 1D no fluxo principal
    print(f"\n{'-' * 40}")
    print(f"Questão 1D: Componentes Conexos")
    print(f"{'-' * 40}")

    # Calcular e exibir componentes conectados
    if grafo.is_directed():
        # Componentes Fortemente Conectados
        componentes_fortes = list(nx.strongly_connected_components(grafo))
        tamanhos_fortes = [len(componente) for componente in componentes_fortes]
        maior_componente_forte = max(tamanhos_fortes)
        num_componentes_fortes = len(componentes_fortes)

        # Componentes Fracamente Conectados
        componentes_fracos = list(nx.weakly_connected_components(grafo))
        tamanhos_fracos = [len(componente) for componente in componentes_fracos]
        maior_componente_fraco = max(tamanhos_fracos)
        num_componentes_fracos = len(componentes_fracos)

        print(f"Número de componentes fortemente conectados: {num_componentes_fortes}")
        print(f"Tamanho do maior componente fortemente conectado: {maior_componente_forte:,} nós.")
        print(f"Número de componentes fracamente conectados: {num_componentes_fracos}")
        print(f"Tamanho do maior componente fracamente conectado: {maior_componente_fraco:,} nós.")
    else:
        # Componentes Conectados (para grafos não direcionados)
        componentes = list(nx.connected_components(grafo))
        tamanhos = [len(componente) for componente in componentes]
        maior_componente = max(tamanhos)
        num_componentes = len(componentes)

        print(f"Número de componentes conexos: {num_componentes}")
        print(f"Tamanho do maior componente: {maior_componente:,} nós.")

    # Gerar os gráficos da distribuição de tamanhos dos componentes
    grafico_tamanho_componentes_agrupados(grafo, titulo=f"Rede {rede.capitalize()}")



# todo: ################################################################################################################
# todo: ################################################################################################################
# todo: ################################################################################################################
# todo: ################################################################################################################

    # Atualizando a Questão 1E no fluxo principal
    print(f"\n{'-' * 40}")
    print(f"Questão 1E: Distância Média e Distribuição")
    print(f"{'-' * 40}")

    # Calcular e plotar a distribuição das distâncias
    distancia_media = grafico_distancia_pares(grafo, titulo=f"Rede {rede.capitalize()}")
    print(f"Distância média na rede: {distancia_media:.2f}")



# todo: ################################################################################################################
# todo: ################################################################################################################
# todo: ################################################################################################################
# todo: ################################################################################################################


    # Atualizando a Questão 1F no fluxo principal
    print(f"\n{'-' * 40}")
    print(f"Questão 1F: Arestas Pontes")
    print(f"{'-' * 40}")

    pontes = encontrar_pontes(grafo)
    print(f"Quantidade de arestas que podem ser pontes: {len(pontes)}")
    print(f"Arestas com grandes chances de serem pontes: {pontes}")


# todo: ################################################################################################################
# todo: ################################################################################################################
# todo: ################################################################################################################
# todo: ################################################################################################################
# todo:#################################################################################################################
# todo:#################################################################################################################
# todo:
# todo:     QUESTÃO 2 A BAIXO:
# todo:     QUESTÃO 2 A BAIXO:
# todo:     QUESTÃO 2 A BAIXO:
# todo:
# todo:#################################################################################################################
# todo:#################################################################################################################


# TODO: Bloco dedicado à análise da rede Scientometrics (Questão 2).
# Questão 2: Ciência Cientométrica
print(f"\n{'=' * 60}")
print("Processando o Grafo de Citações: Scientometrics")
print(f"{'=' * 60}\n")

# TODO: Carregar o grafo de citações como orientado.
# Carregar o grafo como orientado
grafo_citacoes = nx.read_edgelist(
    arquivos_dados["scientometrics"]["caminho"],
    create_using=nx.DiGraph()
)
print(f"Grafo carregado com sucesso: {len(grafo_citacoes.nodes):,} nós, {len(grafo_citacoes.edges):,} arestas.\n")

# TODO: Calcular a densidade do grafo (Questão 2A).
# Questão 2A: Densidade do Grafo
print(f"{'-' * 40}")
print("Questão 2A: Densidade do Grafo")
print(f"{'-' * 40}")
densidade = nx.density(grafo_citacoes)
print(f"Densidade do Grafo: {densidade:.4f}\n")

# TODO: Calcular o grau médio de entrada e saída (Questão 2B).
# Questão 2B: Grau dos Vértices
print(f"{'-' * 40}")
print("Questão 2B: Grau dos Vértices")
print(f"{'-' * 40}")
grau_entrada = sum(dict(grafo_citacoes.in_degree()).values()) / len(grafo_citacoes.nodes)
grau_saida = sum(dict(grafo_citacoes.out_degree()).values()) / len(grafo_citacoes.nodes)
print(f"Grau médio de entrada: {grau_entrada:.2f}")
print(f"Grau médio de saída: {grau_saida:.2f}\n")

# TODO: Identificar componentes fortemente e fracamente conectados (Questão 2C).
# Questão 2C: Componentes Conexos
print(f"{'-' * 40}")
print("Questão 2C: Componentes Conexos")
print(f"{'-' * 40}")
componentes_fortes = nx.number_strongly_connected_components(grafo_citacoes)
componentes_fracos = nx.number_weakly_connected_components(grafo_citacoes)
print(f"Número de componentes fortemente conectados: {componentes_fortes}")
print(f"Número de componentes fracamente conectados: {componentes_fracos}\n")

# TODO: Verificar ciclos e calcular caminhos mais curtos na maior componente (Questão 2D).
# Questão 2D: Caminhos e Ciclos
print(f"{'-' * 40}")
print("Questão 2D: Caminhos e Ciclos")
print(f"{'-' * 40}")
print("Verificando a presença de ciclos...")
ciclos = list(nx.simple_cycles(grafo_citacoes))
print(f"Número de ciclos encontrados: {len(ciclos)}")

print("\nCalculando a média dos caminhos mais curtos...")
try:
    distancia_media = nx.average_shortest_path_length(grafo_citacoes)
    print(f"Média dos caminhos mais curtos: {distancia_media:.2f}")
except nx.NetworkXError:
    print("O grafo não é fortemente conectado; não é possível calcular a distância média.\n")

# TODO: Exibir centralidade de grau normalizada e grau absoluto (Questão 2E).
# Questão 2E: Centralidade de Grau
print(f"{'-' * 40}")
print("Questão 2E: Centralidade de Grau")
print(f"{'-' * 40}")

# TODO: Calcular e exibir centralidade de grau normalizada.
# Centralidade de Grau Normalizada
centralidade_grau_entrada = nx.in_degree_centrality(grafo_citacoes)
centralidade_grau_saida = nx.out_degree_centrality(grafo_citacoes)

print("\nTop 5 nós por centralidade de grau (entrada - normalizada):")
for no, valor in sorted(centralidade_grau_entrada.items(), key=lambda x: x[1], reverse=True)[:5]:
    print(f"Nó {no}: {valor:.4f}")

print("\nTop 5 nós por centralidade de grau (saída - normalizada):")
for no, valor in sorted(centralidade_grau_saida.items(), key=lambda x: x[1], reverse=True)[:5]:
    print(f"Nó {no}: {valor:.4f}")

# TODO: Calcular e exibir grau absoluto.
# Grau Absoluto
graus_entrada = dict(grafo_citacoes.in_degree())
graus_saida = dict(grafo_citacoes.out_degree())

print("\nTop 5 nós por grau de entrada (absoluto):")
for no, grau in sorted(graus_entrada.items(), key=lambda x: x[1], reverse=True)[:5]:
    print(f"Nó {no}: {grau}")

print("\nTop 5 nós por grau de saída (absoluto):")
for no, grau in sorted(graus_saida.items(), key=lambda x: x[1], reverse=True)[:5]:
    print(f"Nó {no}: {grau}")

# TODO:
# TODO:
# TODO: HTML
# TODO:
# TODO:
# TODO: Dicionário global para resultados
resultados = {}

# Processar redes sociais (Deezer e Lastfm, por exemplo)
for rede in ["deezer", "lastfm"]:
    # Carregar o grafo
    grafo = carregar_grafo_de_arestas(
        arquivos_dados[rede]["caminho"],
        arquivos_dados[rede]["coluna_origem"],
        arquivos_dados[rede]["coluna_destino"],
        arquivos_dados[rede]["bool"]
    )

    # Atualizar os resultados no dicionário
    resultados[rede] = {
        "numero_nos": grafo.number_of_nodes(),
        "numero_arestas": grafo.number_of_edges(),
        "grau_medio_entrada": sum(dict(grafo.in_degree()).values()) / grafo.number_of_nodes(),
        "grau_medio_saida": sum(dict(grafo.out_degree()).values()) / grafo.number_of_nodes(),
        "numero_componentes_fortes": nx.number_strongly_connected_components(grafo),
        "tamanho_maior_componente_forte": max(len(c) for c in nx.strongly_connected_components(grafo)),
        "numero_componentes_fracos": nx.number_weakly_connected_components(grafo),
        "tamanho_maior_componente_fraco": max(len(c) for c in nx.weakly_connected_components(grafo)),
        "distancia_media": grafico_distancia_pares(grafo, titulo=f"Rede {rede.capitalize()}"),
        "numero_arestas_pontes": len(encontrar_pontes(grafo)),
        "pontes_amostra": encontrar_pontes(grafo)[:10],  # Exibir apenas as primeiras 10 pontes
    }

# Processar o grafo de citações para a Questão 2
grafo_citacoes = nx.read_edgelist(
    arquivos_dados["scientometrics"]["caminho"],
    create_using=nx.DiGraph()
)

resultados["scientometrics"] = {
    "densidade": nx.density(grafo_citacoes),
    "grau_medio_entrada": sum(dict(grafo_citacoes.in_degree()).values()) / grafo_citacoes.number_of_nodes(),
    "grau_medio_saida": sum(dict(grafo_citacoes.out_degree()).values()) / grafo_citacoes.number_of_nodes(),
    "componentes_fortes": nx.number_strongly_connected_components(grafo_citacoes),
    "componentes_fracos": nx.number_weakly_connected_components(grafo_citacoes),
    "ciclos": len(list(nx.simple_cycles(grafo_citacoes))),
    "distancia_media": grafico_distancia_pares(grafo, titulo=f"Rede {rede.capitalize()}"),
}

# Geração do HTML
html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">z
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Resultados da Análise de Grafos</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
            background-color: #f9f9f9;
            color: #333;
        }
        header {
            background-color: #5c2d91;
            color: white;
            padding: 20px;
            text-align: center;
        }
        .container {
            margin: 20px auto;
            max-width: 900px;
            padding: 20px;
            background: white;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            border-radius: 8px;
        }
        h1, h2 {
            font-family: 'Arial Black', sans-serif;
            margin-top: 0;
        }
        h3 {
            color: #5c2d91;
        }
        .section {
            margin-bottom: 30px;
        }
        .results-table {
            border-collapse: collapse;
            width: 100%;
            margin-top: 10px;
        }
        .results-table th, .results-table td {
            border: 1px solid #ddd;
            padding: 10px;
            text-align: left;
        }
        .results-table th {
            background-color: #e6e6e6;
        }
        ul {
            padding-left: 20px;
        }
        li {
            margin-bottom: 5px;
        }
        p {
            font-size: 1.1em;
            margin: 5px 0;
        }
        footer {
            text-align: center;
            padding: 10px 0;
            background-color: #5c2d91;
            color: white;
            margin-top: 20px;
        }
    </style>
</head>
<body>
<header>
    <h1>Resultados da Análise de Grafos</h1>
</header>
<div class="container">
"""

# Adicionar seções para cada rede
for rede, analise in resultados.items():
    html_content += f"""
    <div class="section">
        <h3>Rede: {rede.capitalize()}</h3>
        <table class="results-table">
            <tr><th>Métrica</th><th>Valor</th></tr>
    """
    for metrica, valor in analise.items():
        html_content += f"<tr><td>{metrica.replace('_', ' ').capitalize()}</td><td>{valor}</td></tr>"
    html_content += "</table></div>"

html_content += """
</div>
<footer>
    <p>&copy; 2024 Análise de Grafos</p>
</footer>
</body>
</html>
"""

# Salvar o HTML
with open("resultados.html", "w", encoding="utf-8") as f:
    f.write(html_content)

print("Arquivo HTML gerado: resultados.html")
