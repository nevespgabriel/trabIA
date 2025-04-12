import pandas as pd;
import openpyxl as op;
from collections import deque

#Definição do nó que representará a capital
class No:
    def __init__(self, estado, cidade_anterior=None, acao=None, custo=0, profundidade=0):
        self.estado = estado
        self.cidade_anterior = cidade_anterior
        self.acao = acao
        self.custo = custo
        self.profundidade = profundidade

    def caminho(self):
        no, caminho = self, []
        while no:
            caminho.append((no.acao, no.estado))
            no = no.cidade_anterior
        return list(reversed(caminho))[1:]  # remove o nó inicial

def buscarEmLargura():
    return;

def buscarEmProfundidade():
    return;

def buscarEmA():
    return;

#Importando dados do excel
tb_distancias_aereo = pd.read_excel(r"C:\Users\neves\PycharmProjects\trabIA\distancias_aereo.xlsx", index_col=0);
tb_distancias_rodov = pd.read_excel(r"C:\Users\neves\PycharmProjects\trabIA\distancias_rodoviario.xlsx", index_col=0);

cidade_origem = input("Olá usuário! Digite de qual cidade deseja sair: ");
cidade_destino = input("Agora digite para qual cidade deseja ir: ");

print("Resultado da busca em largura: " + buscarEmLargura());
print("Resultado da busca em profundidade: " + buscarEmProfundidade());
print("Resultado da busca em A*: " + buscarEmA());