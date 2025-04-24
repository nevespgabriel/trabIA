import heapq
import random
import pandas as pd

# Carrega as planilhas com as distâncias (aérea e rodoviária)
tb_aereo = pd.read_excel(r"C:\Users\neves\PycharmProjects\trabIA\distancias_aereo.xlsx", index_col=0)
tb_rodov = pd.read_excel(r"C:\Users\neves\PycharmProjects\trabIA\distancias_rodoviario.xlsx", index_col=0)

# Definição do nó que representará a capital ou cidade
class No:
    def __init__(self, nome_cidade, cidade_anterior=None, acao=None, custo_acumulado=0, profundidade=0):
        self.nome_cidade = nome_cidade
        self.cidade_anterior = cidade_anterior
        self.acao = acao
        self.custo_acumulado = custo_acumulado
        self.profundidade = profundidade

    def caminho(self):
        no, caminho = self, []
        while no:
            caminho.append((no.acao, no.nome_cidade))
            no = no.cidade_anterior
        # Retorna o caminho em ordem (excluindo o nó inicial, que não possui ação)
        return list(reversed(caminho))[1:]

def buscarEmA(cidade_origem, cidade_destino):
    no_inicial = No(nome_cidade=cidade_origem, custo_acumulado=0)
    h_inicial = tb_aereo.loc[cidade_origem, cidade_destino]
    f_inicial = h_inicial  # g(n)=0, logo f = h

    # Cria a fila de prioridade (min-heap) e adiciona o nó inicial
    fronteira = []
    heapq.heappush(fronteira, (f_inicial, no_inicial))

    melhor_custo = {cidade_origem: 0}

    while fronteira:
        f_atual, no_atual = heapq.heappop(fronteira)

        if no_atual.nome_cidade == cidade_destino:
            # Quando o destino é alcançado, obtém o caminho (lista de transições)
            caminho_encontrado = no_atual.caminho()
            # A quantidade de cidades percorridas é:
            # tamanho da lista de transições + 1 (para incluir o nó inicial)
            quantidade_cidades = len(caminho_encontrado) + 1
            # A distância percorrida (ou custo) é o custo acumulado no nó final
            distancia_percorrida = no_atual.custo_acumulado
            # Retorna uma tupla com as três informações:
            return caminho_encontrado, quantidade_cidades, distancia_percorrida

        for vizinho in tb_rodov.columns:
            if vizinho == no_atual.nome_cidade:
                continue

            distancia_rodov = tb_rodov.loc[no_atual.nome_cidade, vizinho]
            if pd.isna(distancia_rodov) or distancia_rodov == 0:
                continue

            # Cálculo de fatores (com pesos nos pedágios e tráfego)
            trafego = random.uniform(5, 35)
            custo_pedagio = 2.5 * distancia_rodov / 100
            custo_caminho = distancia_rodov + (custo_pedagio * 0.8) + (trafego * 1.2)

            g_novo = no_atual.custo_acumulado + custo_caminho

            if vizinho not in melhor_custo or g_novo < melhor_custo[vizinho]:
                melhor_custo[vizinho] = g_novo

                # O cálculo da heurística h(n) é feito utilizando a distância aérea
                h_novo = float(tb_aereo.at[vizinho, cidade_destino])
                f_novo = g_novo + h_novo

                novo_no = No(
                    nome_cidade=vizinho,
                    cidade_anterior=no_atual,
                    acao=f"{no_atual.nome_cidade} -> {vizinho}",
                    custo_acumulado=g_novo
                )
                heapq.heappush(fronteira, (f_novo, novo_no))

    return None

# Entrada do usuário
cidade_origem = input("Olá usuário! Digite de qual cidade deseja sair: ").strip()
cidade_destino = input("Agora digite para qual cidade deseja ir: ").strip()

resultadoA = buscarEmA(cidade_origem, cidade_destino)
if resultadoA is None:
    print("Nenhum caminho encontrado!")
else:
    caminho_encontrado, quantidade_cidades, distancia_percorrida = resultadoA
    print("Resultado da busca em A*:")
    print("- Caminho percorrido:")
    for acao, cidade in caminho_encontrado:
        print(acao, "(", cidade, ")")
    print("- Quantidade de cidades percorridas:", quantidade_cidades)
    print("- Distância percorrida:", distancia_percorrida);



#print("Resultado da busca em largura: ", buscarEmLargura());
#print("Resultado da busca em profundidade: ", buscarEmProfundidade());