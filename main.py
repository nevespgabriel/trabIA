import heapq
import random
import pandas as pd;

tb_aereo = pd.read_excel(r"C:\Users\neves\PycharmProjects\trabIA\distancias_aereo.xlsx", index_col=0);
tb_rodov = pd.read_excel(r"C:\Users\neves\PycharmProjects\trabIA\distancias_rodoviario.xlsx", index_col=0);

#Definição do nó que representará a capital
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
        return list(reversed(caminho))[1:] # remove o nó inicial

def buscarEmLargura():
    return;

def buscarEmProfundidade():
    return;


#Para calcular g(n) (o custo até o momento), são levados em conta a distância rodoviária, o volume de veículos na via (o qual,
#com o intuito de ser usado apenas como exemplo, é aleatorizado) e o valor total em pedágios para chegar ao destino (que no
#exemplo também possui um fator de aleatoriedade, mas além disso, é influenciado pela distância rodoviária).

#No cálculo de h(n) (custo estimado do momento até o destino final), a heurística aplicada é a distância em linha reta até o
#destino final
def buscarEmA(cidade_origem, cidade_destino):

    no_inicial = No(nome_cidade=cidade_origem, custo_acumulado=0)
    h_inicial = tb_aereo.loc[cidade_origem, cidade_destino]
    f_inicial = h_inicial  # g(n)=0, logo f = h

    #Cria a fila de prioridade e adiciona a cidade de origem a ela
    #Essa fila ordena os itens de acordo com o f(x) deles (soma de g(x) + h(x))
    #Quanto menor a soma, maior a prioridade do nó, e antes ele estará na fila para ser escolhido como próximo caminho
    fronteira = []
    heapq.heappush(fronteira, (f_inicial, no_inicial))

    melhor_custo = {cidade_origem: 0}

    while fronteira:
        f_atual, no_atual = heapq.heappop(fronteira)

        print(no_atual.nome_cidade.strip(), " = ", cidade_destino);
        if no_atual.nome_cidade == cidade_destino:
            return no_atual.caminho()

        for vizinho in tb_rodov.columns:
            if vizinho == no_atual.nome_cidade:
                continue

            distancia_rodov = tb_rodov.loc[no_atual.nome_cidade, vizinho]

            if pd.isna(distancia_rodov) or distancia_rodov == 0:
                continue

           #trafego = random.uniform(5, 35)
           # custo_pedagio = 2.5 * distancia_rodov / 100
            custo_caminho = distancia_rodov #* custo_pedagio + trafego

            g_novo = no_atual.custo_acumulado + custo_caminho

            if vizinho not in melhor_custo or g_novo < melhor_custo[vizinho]:
                melhor_custo[vizinho] = g_novo

                # Cálculo da heurística
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

cidade_origem = input("Olá usuário! Digite de qual cidade deseja sair: ").strip()
cidade_destino = input("Agora digite para qual cidade deseja ir: ").strip()

print("Resultado da busca em A*: ", buscarEmA(cidade_origem, cidade_destino));
print("Resultado da busca em largura: ", buscarEmLargura());
print("Resultado da busca em profundidade: ", buscarEmProfundidade());