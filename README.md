# Trabalho de Computação Distribuída: Disponibilidade de Serviços Replicados

## 1. Grupo:
* **André Luiz Cavalcante da Silva** - 2310287
* **Ian Sampaio Lira Waki** - 2310398
* **José Arthur Leite Brito** - 2315760
* **João Arthur Veras Barros Dias** - 2315431

---

## 2. Exercício 1.1: Dedução do Modelo Matemático

O objetivo deste exercício é calcular a disponibilidade de um serviço replicado em múltiplos servidores. A disponibilidade total depende de eventos probabilísticos independentes, assumindo que a falha de um servidor não interfere no estado dos demais.

Os parâmetros definidos para o modelo são:
* $n$: número total de servidores ($n > 0$).
* $k$: número mínimo de servidores disponíveis para o serviço operar de forma consistente ($0 < k \le n$).
* $p$: probabilidade de cada servidor estar disponível em um dado instante ($0 \le p \le 1$).

### Casos Extremos

1. **Operação de Atualização ($k = n$):**
Neste cenário, todos os servidores precisam estar operacionais simultaneamente. Como os eventos são independentes, a probabilidade conjunta é o produto das probabilidades individuais:
$$A(n, n, p) = p^n$$

2. **Operação de Consulta ($k = 1$):**
Aqui, basta que pelo menos um servidor esteja disponível. O cálculo mais eficiente é encontrar a probabilidade de **nenhum** servidor estar disponível e subtrair esse valor de $1$. A probabilidade de um servidor falhar é $(1 - p)$.
$$A(n, 1, p) = 1 - (1 - p)^n$$

### Caso Geral

Para o caso geral, onde precisamos que pelo menos $k$ servidores estejam disponíveis (ou seja, $k$, $k+1$, ..., até $n$ servidores operacionais), utilizamos a **Distribuição Binomial**. A disponibilidade do serviço é a soma das probabilidades de se obter exatamente $i$ servidores disponíveis, variando de $i = k$ até $n$:

$$A(n, k, p) = \sum_{i=k}^{n} \binom{n}{i} p^i (1 - p)^{n-i}$$

Onde $\binom{n}{i} = \frac{n!}{i!(n-i)!}$ representa as combinações possíveis de $i$ servidores online dentre os $n$ totais.

---

## 3. Exercício 1.2: Cálculo Analítico e Simulador Estocástico

A implementação das soluções foi desenvolvida em linguagem Python, dividida em dois scripts distintos para separar a modelagem matemática pura da simulação baseada em força bruta (Monte Carlo). Utilizamos as bibliotecas NumPy para a geração de números aleatórios em larga escala e Pandas para a organização tabular dos resultados.

### 3.1. Parte 1: Cálculo Analítico (`codigoExercicio1.py`)
A fórmula binomial deduzida no Exercício 1.1 foi traduzida para uma função computacional. Para uma bateria de testes, fixamos $n = 5$ servidores e variamos a probabilidade individual $p$ de $0$ a $1$ em incrementos de $0.05$. Testamos três cenários de exigência ($k$):
* $k = 1$ (Mínimo rigor - Consulta)
* $k = 3$ (Maioria simples para $n=5$)
* $k = 5$ (Máximo rigor - Atualização)

**Resultados da Parte 1:**
*Gráfico no arquivo `grafico_parte1_analitico.png`*
Os dados completos encontram-se no arquivo `tabela_parte1_analitica.csv`.

### 3.2. Parte 2: Simulador Estocástico e Comparação (`codigoExercicio1.2.py`)
Para validar o modelo teórico, construímos um simulador que executa $10.000$ rodadas para cada combinação de $n$, $k$ e $p$. 
1. Em cada rodada, geramos $n$ números aleatórios entre $0$ e $1$.
2. Se o número sorteado for $\le p$, consideramos o servidor "Disponível".
3. Se a quantidade de servidores sobreviventes na rodada for $\ge k$, a rodada contabiliza um sucesso.
4. A disponibilidade experimental final é a razão entre as rodadas de sucesso e as $10.000$ rodadas totais.

**Resultados da Parte 2 (Comparativo):**
O gráfico abaixo sobrepõe os resultados teóricos (linhas) com os resultados obtidos pela simulação prática (marcadores).
*Gráfico no arquivo `grafico_parte2_analitico.png`*

Abaixo, um extrato da tabela comparativa evidenciando a proximidade dos valores (dados completos no arquivo `tabela_parte2_comparativa.csv`):

| $n$ | $k$ | $p$ | Analítico | Experimental |
|---|---|---|---|---|
| 5 | 3 | 0.50 | 0.5000 | 0.4985 |
| 5 | 3 | 0.80 | 0.9421 | 0.9412 |
| 5 | 5 | 0.90 | 0.5905 | 0.5891 |

---

## 4. Conclusão

A análise dos gráficos e da tabela evidencia a convergência quase perfeita entre o modelo analítico e o simulador estocástico. Isso atesta a validade da fórmula baseada na distribuição binomial para prever a confiabilidade de sistemas distribuídos. 

Observa-se o trade-off clássico de tolerância a falhas: 
* Para operações de atualização que exigem consenso em todos os nós ($k=n$), a disponibilidade geral do serviço cai drasticamente a menos que a confiabilidade individual $p$ de cada máquina seja extremamente alta (próxima de $1$). 
* Por outro lado, arquiteturas focadas em leitura ou que exigem apenas uma minoria de nós vivos ($k=1$) conseguem entregar altíssima disponibilidade geral, mitigando a instabilidade individual dos servidores.
