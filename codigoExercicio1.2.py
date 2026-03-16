import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from math import comb

print("Executando Parte 2: Simulador Estocástico e Comparação...")

# 1. Função Analítica (Base de comparação)
def disponibilidade_analitica(n, k, p):
    prob_total = 0
    for i in range(k, n + 1):
        prob_total += comb(n, i) * (p**i) * ((1 - p)**(n - i))
    return prob_total

# 2. Simulador Estocástico (Monte Carlo)
def disponibilidade_simulada(n, k, p, num_rodadas):
    # Gera matriz de (rodadas x servidores) com números aleatórios
    rand_vals = np.random.rand(num_rodadas, n)
    # Verifica quais servidores sobreviveram (<= p)
    servidores_online = rand_vals <= p
    # Soma quantos servidores sobreviveram por rodada
    contagem_online = np.sum(servidores_online, axis=1)
    # Verifica quantas rodadas atingiram o quórum k
    rodadas_sucesso = np.sum(contagem_online >= k)
    return rodadas_sucesso / num_rodadas

# Parâmetros de teste
n = 5
ks = [1, max(1, n//2 + n%2), n]
p_vals = np.linspace(0, 1, 21)
rodadas = 10000

resultados = []
plt.figure(figsize=(10, 6))
cores = ['blue', 'green', 'red']
marcadores = ['o', 's', '^']

# Gera os dados e o gráfico comparativo
for idx, k in enumerate(ks):
    analitico_vals = []
    simulado_vals = []
    
    for p in p_vals:
        v_analitico = disponibilidade_analitica(n, k, p)
        v_simulado = disponibilidade_simulada(n, k, p, rodadas)
        
        analitico_vals.append(v_analitico)
        simulado_vals.append(v_simulado)
        
        # Salva dados lado a lado na tabela
        resultados.append({
            'n': n, 'k': k, 'p': round(p, 2), 
            'Analitico': round(v_analitico, 4), 
            'Experimental': round(v_simulado, 4)
        })
        
    # Plota a linha teórica
    plt.plot(p_vals, analitico_vals, label=f'Teórico (k={k})', color=cores[idx], linestyle='-')
    # Plota os pontos experimentais em cima da linha
    plt.scatter(p_vals, simulado_vals, label=f'Prático (k={k})', color=cores[idx], marker=marcadores[idx], alpha=0.7)

# Configuração visual do gráfico
plt.title(f'Comparação: Teórico vs Simulação ({rodadas} rodadas, n={n})')
plt.xlabel('Probabilidade de Disponibilidade do Servidor (p)')
plt.ylabel('Disponibilidade do Serviço')
plt.legend()
plt.grid(True, linestyle='--', alpha=0.6)
plt.tight_layout()

# Exporta os arquivos
plt.savefig('grafico_parte2_comparativo.png', dpi=300)
pd.DataFrame(resultados).to_csv('tabela_parte2_comparativa.csv', index=False)

print("Sucesso! Arquivos 'grafico_parte2_comparativo.png' e 'tabela_parte2_comparativa.csv' gerados.")