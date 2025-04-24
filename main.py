import heapq
import random
import pandas as pd

# Um certo alguém deixou um caminho absoluto ao invés de relativo kk
tabela_aerea = pd.read_excel("distancias_aereo.xlsx", index_col=0)
tabela_rodoviaria = pd.read_excel("distancias_rodoviario.xlsx", index_col=0)

class Ponto:
    def __init__(self, nome_cidade : str = None, cidade_anterior = None, custo_acumulado : float = 0.0, profundidade : int = 0, rota_realizada : str = None):
        self.nome_cidade        = nome_cidade
        self.cidade_anterior    = cidade_anterior
        self.custo_acumulado    = custo_acumulado
        self.profundidade       = profundidade
        self.rota_realizada     = rota_realizada

    def caminho(self):
        ponto_atual : Ponto = self
        caminho : list = []

        while ponto_atual:
            caminho.append((ponto_atual.rota_realizada, ponto_atual.nome_cidade))
            ponto_atual = ponto_atual.cidade_anterior
        return list(reversed(caminho))[1:]

def calcularCusto(distancia_base: float) -> float:
    trafego = 10 # Deixei 10 para ser deterministíco  #random.uniform(5, 35)
    distancia_base_float = float(distancia_base)
    custo_pedagio = (2.5 * distancia_base_float / 100) * 0.8
    custo_final_trecho = distancia_base_float + custo_pedagio + (trafego * 1.2)
    return custo_final_trecho

def buscarEmA(cidade_origem, cidade_destino) -> Ponto:
    no_inicial = Ponto(nome_cidade=cidade_origem, custo_acumulado=0.0, profundidade=0)
    h_inicial = tabela_aerea.loc[cidade_origem, cidade_destino]
    f_inicial = h_inicial  # g(n)=0, logo f = h

    # Cria a fila de prioridade (min-heap) e adiciona o nó inicial
    fronteira = []
    # Adiciona o objeto Ponto inicial
    heapq.heappush(fronteira, (f_inicial, no_inicial))

    melhor_custo = {cidade_origem: 0.0} # Usa 0.0 para float

    while fronteira:
        f_atual, no_atual = heapq.heappop(fronteira)

        if no_atual.nome_cidade == cidade_destino:
            # Retorna o objeto Ponto encontrado
            return no_atual


        for vizinho in tabela_rodoviaria.columns:
            if vizinho == no_atual.nome_cidade:
                continue

            distancia_rodov = tabela_rodoviaria.loc[no_atual.nome_cidade, vizinho]
            # Usa <= 0 para checagem mais robusta
            if pd.isna(distancia_rodov) or distancia_rodov <= 0:
                continue

            custo_caminho = calcularCusto(distancia_rodov)
            g_novo = float(no_atual.custo_acumulado) + custo_caminho

            if vizinho not in melhor_custo or g_novo < melhor_custo[vizinho]:
                melhor_custo[vizinho] = g_novo

                # O cálculo da heurística h(n) é feito utilizando a distância aérea
                h_novo = float(tabela_aerea.at[vizinho, cidade_destino])
                f_novo = g_novo + h_novo

                # Usa rota_realizada e adiciona profundidade
                novo_ponto = Ponto(
                    nome_cidade=vizinho,
                    cidade_anterior= no_atual, # no_atual é o Ponto anterior
                    rota_realizada=f"{no_atual.nome_cidade} -> {vizinho}",
                    custo_acumulado=g_novo,
                    profundidade=no_atual.profundidade + 1
                )
                heapq.heappush(fronteira, (f_novo, novo_ponto))

    return None

def buscarEmLargura(cidade_origem, cidade_destino) -> Ponto:
    ponto_inicial = Ponto(nome_cidade=cidade_origem, custo_acumulado=0.0, profundidade=0)
    
    if cidade_origem == cidade_destino:
        return ponto_inicial

    fronteira = [ponto_inicial]
    explorados = {cidade_origem}

    while fronteira:
        ponto_atual = fronteira.pop(0)

        for vizinho in tabela_rodoviaria.columns:

            if vizinho == ponto_atual.nome_cidade or ponto_atual.nome_cidade not in tabela_rodoviaria.index:
                continue
            
            if vizinho not in tabela_rodoviaria.index:
                continue

            distancia_rodov = tabela_rodoviaria.loc[ponto_atual.nome_cidade, vizinho]
            
            if pd.isna(distancia_rodov) or distancia_rodov <= 0:
                continue

            if vizinho not in explorados:
                explorados.add(vizinho)

                custo_caminho = calcularCusto(distancia_rodov)
                g_novo = float(ponto_atual.custo_acumulado) + custo_caminho

                novo_ponto = Ponto(
                    nome_cidade=vizinho,
                    cidade_anterior=ponto_atual,
                    rota_realizada=f"{ponto_atual.nome_cidade} -> {vizinho}",
                    custo_acumulado=g_novo,
                    profundidade=ponto_atual.profundidade + 1
                )

                if vizinho == cidade_destino:
                    return novo_ponto

                fronteira.append(novo_ponto)

    return None

def buscarEmProfundidade(cidade_origem, cidade_destino) -> Ponto:
    ponto_inicial = Ponto(nome_cidade=cidade_origem, custo_acumulado = 0.0, profundidade = 0)

    if cidade_origem == cidade_destino:
        return ponto_inicial

    fronteira = [ponto_inicial]
    explorados = set()

    while fronteira:
        ponto_atual = fronteira.pop()

        if ponto_atual.nome_cidade == cidade_destino:
            return ponto_atual

        if ponto_atual.nome_cidade in explorados:
            continue
        
        explorados.add(ponto_atual.nome_cidade)

        if ponto_atual.nome_cidade not in tabela_rodoviaria.index:
            continue

        for vizinho in reversed(tabela_rodoviaria.columns): 
            if vizinho == ponto_atual.nome_cidade:
                continue
            
            if vizinho not in tabela_rodoviaria.index:
                continue

            distancia_rodov = tabela_rodoviaria.loc[ponto_atual.nome_cidade, vizinho]

            if pd.isna(distancia_rodov) or distancia_rodov <= 0:
                continue

            if vizinho not in explorados:
                custo_caminho = calcularCusto(distancia_rodov)
                g_novo = float(ponto_atual.custo_acumulado) + custo_caminho

                novo_ponto = Ponto(
                    nome_cidade=vizinho,
                    cidade_anterior=ponto_atual,
                    rota_realizada=f"{ponto_atual.nome_cidade} -> {vizinho}",
                    custo_acumulado=g_novo,
                    profundidade=ponto_atual.profundidade + 1
                )
                fronteira.append(novo_ponto)

    return None

def mostrarResultado(ponto_final: Ponto, cidade_origem: str):
    print("--- Resultado da Busca ---")
    if ponto_final:
        print(f"Rota encontrada de '{cidade_origem}' para '{ponto_final.nome_cidade}':")

        rota_detalhada = ponto_final.caminho()

        if not rota_detalhada:
             if cidade_origem == ponto_final.nome_cidade:
                 print("  (Origem é igual ao destino)")
        else:
            print("  Trajeto:")
            for trecho, cidade_chegada in rota_detalhada:
                print(f"    - {trecho}")

        print(f"\n  Custo total acumulado: {ponto_final.custo_acumulado:.2f}")
        print(f"  Número de trechos percorridos: {ponto_final.profundidade}")
        # profundidade + 1
        print(f"  Número de cidades no caminho (incluindo origem): {ponto_final.profundidade + 1}")

    else:
        # Se buscarEmAlgumaCoisa retornou None
        print(f"Não foi possível encontrar uma rota de '{cidade_origem}' para o destino solicitado.")
    print("--------------------------")

# --- Exemplo de Uso ---
# Escolha das cidades
print("O nosso sitema suporta:\nAracajú        | Belém          | Belo Horizonte\nBoa Vista      | Brasília       | Campo Grande  \nCuiabá         | Curitiba       | Florianópolis \nFortaleza      | Goiânia        | João Pessoa   \nMacapá         | Maceió         | Manaus        \nNatal          | Palmas         | Porto Alegre  \nPorto Velho    | Recife         | Rio Branco    \nR. Janeiro     | Salvador       | São Luis      \nSão Paulo      | Teresina       | Vitória       ")
cidade_origem = input("\nDigite de qual cidade deseja sair: ").strip()
cidade_destino = input("Agora digite para qual cidade deseja ir: ").strip()

resultadoA = buscarEmA(cidade_origem, cidade_destino)
resultadoLargura = buscarEmLargura(cidade_origem, cidade_destino)
resultadoProfundidade = buscarEmProfundidade(cidade_origem, cidade_destino)

print("===========================================\nResultado de A*:\n===========================================")
mostrarResultado(resultadoA, cidade_origem)
print("Resultado de Largura:")
mostrarResultado(resultadoLargura, cidade_origem)
print("Resultado de Profundidade:")
mostrarResultado(resultadoProfundidade, cidade_origem)