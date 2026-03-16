import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from math import comb

print("Executando Parte 1: Cálculo Analítico...")

# Função baseada na fórmula deduzida no Exercício 1.1
def disponibilidade_analitica(n, k, p):
    prob_total = 0
    for i in range(k, n + 1):
        prob_total += comb(n, i) * (p**i) * ((1 - p)**(n - i))
    return prob_total

# Parâmetros de teste
n = 5
ks = [1, max(1, n//2 + n%2), n] # Testa k=1, maioria simples e k=n
p_vals = np.linspace(0, 1, 21)  # Varia p de 0 a 1

resultados = []
plt.figure(figsize=(10, 6))
cores = ['blue', 'green', 'red']

# Gera os dados e o gráfico
for idx, k in enumerate(ks):
    analitico_vals = [disponibilidade_analitica(n, k, p) for p in p_vals]
    
    # Salva na lista para exportar para CSV
    for p, a in zip(p_vals, analitico_vals):
        resultados.append({'n': n, 'k': k, 'p': round(p, 2), 'Disponibilidade': round(a, 4)})
        
    # Plota o gráfico 2D (Linhas contínuas)
    plt.plot(p_vals, analitico_vals, label=f'k = {k}', color=cores[idx], linestyle='-')

# Configuração visual do gráfico
plt.title(f'Disponibilidade Analítica do Serviço (n = {n})')
plt.xlabel('Probabilidade de Disponibilidade do Servidor (p)')
plt.ylabel('Disponibilidade do Serviço')
plt.legend()
plt.grid(True, linestyle='--', alpha=0.6)
plt.tight_layout()

# Exporta os arquivos
plt.savefig('grafico_parte1_analitico.png', dpi=300)
pd.DataFrame(resultados).to_csv('tabela_parte1_analitica.csv', index=False)

print("Sucesso! Arquivos 'grafico_parte1_analitico.png' e 'tabela_parte1_analitica.csv' gerados.")