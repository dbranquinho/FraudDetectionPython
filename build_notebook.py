import json
import os

notebook = {
    "cells": [],
    "metadata": {
        "kernelspec": {
            "display_name": "Python 3",
            "language": "python",
            "name": "python3"
        }
    },
    "nbformat": 4,
    "nbformat_minor": 4
}

def add_markdown(text):
    notebook["cells"].append({
        "cell_type": "markdown",
        "metadata": {},
        "source": [line + "\n" for line in text.split("\n")]
    })

def add_code(code):
    notebook["cells"].append({
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [line + "\n" for line in code.split("\n")]
    })

# --- INTRODUÇÃO ---
add_markdown("""# 🎓 Detecção de Fraudes em Cartões de Crédito: Teoria e Prática

Bem-vindos(as) à nossa imersão em Machine Learning voltado para Segurança e Prevenção de Fraudes! 🕵️‍♂️📈

Neste material, não vamos apenas executar código. Vamos entender profundamente a **teoria por trás de cada linha**, **como** as operações matemáticas funcionam e, principalmente, **como interpretar** os resultados sob a ótica de negócios de uma instituição financeira.

### 🎯 Qual é o nosso objetivo?
Nosso objetivo é construir uma Inteligência Artificial capaz de classificar transações de cartão de crédito em duas categorias (problema de Classificação Binária):
- **Normal (Classe 0)**: Transação legítima que deve seguir o fluxo.
- **Fraude (Classe 1)**: Transação suspeita que deve ser bloqueada.

Para isso, usaremos métricas criteriosas, gráficos analíticos e discutiremos o maior vilão da detecção de anomalias: o **Desbalanceamento de Classes**. Vamos começar!""")


# --- PASSO 1 ---
add_markdown("""---
## 📦 Passo 1: Importando as Bibliotecas Fundamentais

### 🧠 A Teoria
Em programação, não precisamos "reinventar a roda". Utilizamos **bibliotecas** (conjuntos de funções matemáticas e visuais) construídas e validadas por cientistas do mundo todo. Cada biblioteca tem um propósito específico:

- **Pandas**: É a nossa "planilha de Excel" em formato de código. Ela cria estruturas chamadas `DataFrames`, que nos permitem manipular milhões de linhas instantaneamente, filtrar, buscar e organizar os dados.
- **Matplotlib e Seaborn**: Nossos pintores. Elas pegam matrizes de números e as transformam em gráficos coloridos e estatísticos. `Seaborn` foi construída em cima do `Matplotlib` para aceitar fórmulas estatísticas mais complexas com poucas linhas de código.
- **Scikit-Learn (sklearn)**: O motor do cientista de dados. Esta biblioteca guarda algoritmos de Inteligência Artificial predefinidos e ferramentas para fatiar, escalar nossos dados e avaliar o sucesso (métricas) da máquina.

### ⚙️ Como estamos fazendo isso:
Nas linhas abaixo, utilizamos a palavra-chave `import` seguida do nome da ferramenta. Quando usamos `from X import Y`, estamos pegando apenas uma ferramenta específica (Y) da grande caixa (X), poupando memória do computador.""")

add_code("""import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Componentes lógicos de Machine Learning
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score, roc_curve, auc, precision_recall_curve
from sklearn.preprocessing import StandardScaler
import os

# Configuração visual: Avisa as bibliotecas gráficas para usarem fundos "limpos" (whitegrid) e tons pastéis agradáveis.
sns.set_theme(style="whitegrid", palette="pastel")

print("✅ Máquinas ligadas! Ferramentas prontas para o trabalho.")""")


# --- PASSO 2 ---
add_markdown("""---
## 📂 Passo 2: Carregando os Dados Bancários

### 🧠 A Teoria
Modelos de Machine Learning aprendem com o **passado**. Eles precisam de "históricos" para extrair padrões de comportamento. No nosso caso, o passado é um arquivo CSV (`creditcard.csv`) que contém o histórico das compras e nosso "gabarito", ou seja, se no fim do dia os analistas do banco descobriram que era fraude ou não.

**Privacidade de Dados (PCA):** 
Uma característica vital desta base em específico e da maioria das empresas sérias é o anonimato. Se você olhar as colunas a seguir, não verá "Nome" nem "Endereço". Elas se chamam `V1`, `V2`, `V3` etc. Isso acontece porque o banco aplicou uma técnica estatística chamada *PCA (Análise de Componentes Principais)*, que transforma as informações completas do usuário em vetores numéricos indecifráveis para humanos, preservando o sentido matemático para o computador. Apenas o valor em dinheiro (`Amount`) e o Tempo (`Time`) costumam vir puros.

### ⚙️ Como estamos fazendo isso:
Usaremos a função `pd.read_csv()` do Pandas que lê o arquivo guardado no disco rígido e o joga na Memória RAM em formato de tabela, nomeada na variável `df` (DataFrame). O comando `.head()` imprime as cinco primeiras linhas.

### 📊 Qual o resultado esperado:
Veremos na tela uma grade retangular contendo os cabeçalhos das colunas (V1, V2... Class) acompanhados de puros números decimais complexos.""")

add_code("""file_path = 'creditcard.csv'

if not os.path.exists(file_path):
    print(f"🚨 ERRO CRÍTICO: Não foi possível localizar o arquivo '{file_path}'. Ele precisa estar na mesma pasta.")
else:
    df = pd.read_csv(file_path)
    print(f"✅ Operação Sucedida! Base carregada na memória com um volume de {len(df)} transações históricas.")
    
    # Renderizamos a 'cabeça' da tabela
    display(df.head())""")


# --- PASSO 3 ---
add_markdown("""---
## ⚖️ Passo 3 e Gráfico 1: Ancoragem e a "Agulha no Palheiro" (O Desbalanceamento)

### 🧠 A Teoria
Aqui jaz o maior pesadelo da cibersegurança e Inteligência Artificial: **As Fraudes são uma anomalia raríssima**.
A depender do comportamento econômico do país, a cada 100.000 transações feitas com sucesso e honestidade, pode existir apenas 1 fraude.

Por que isso é um problema devastador?
Se a nossa IA assumir a "malandragem preguiçosa", ela pode simplesmente chutar que "TODAS AS TRANSAÇÕES NO MUNDO SÃO CORRETAS". 
Ao criar um modelo que chuta sempre "0" (Normal), ela vai acertar 99,8% das vezes, parecendo um gênio na nota técnica da avaliação de **Acurácia**, contudo o banco irá falir, pois ela vai ignorar 100% dos exatos 0,2% criminosos que roubam milhares de dólares.

### ⚙️ Como estamos fazendo isso:
Usamos a contagem `.value_counts()` para quantificar as Classes e jogamos os "pacotes azuis e vermelhos" em um gráfico de barras clássico `countplot`. 
Em virtude do esmagamento numérico, alteramos o "Eixo Y" para escala `Logarítmica`. Em escalas de base logarítmica (10, 100, 1000, 10000), o salto não é constante, e sim multiplicativo, permitindo que vejamos distâncias ridículas de tamanho no mesmo gráfico visual sem que o menor suma na tela.

### 📊 Interpretando o Gráfico:
O gráfico deixará escrachado que as barras não competem. A vermelha (fraude), que é nossa métrica crítica e foco da aula, está ofuscada pelas barras azuis normais. Sem cuidado matemático, o modelo que criaremos será devorado por essa maioria.""")

add_code("""if 'df' in locals():
    # Coleta os números brutos
    contagem = df['Class'].value_counts()
    porcentagem_fraude = (contagem[1] / len(df)) * 100
    
    plt.figure(figsize=(9, 6))
    ax = sns.countplot(x='Class', data=df, palette=['#1f77b4', '#d62728'])
    
    plt.title('Discrepância Visual: Transações Comuns vs Fraudes', fontsize=16, fontweight='bold')
    plt.xlabel('Gabarito da CLASSE (0: Normal  |  1: Fraude)', fontsize=13)
    plt.ylabel('Densidade no Eixo Y (ESCALA LOGARÍTMICA)', fontsize=13)
    
    for p in ax.patches:
        ax.annotate(f"{int(p.get_height())} Históricos", 
                    (p.get_x() + p.get_width() / 2., p.get_height()), 
                    ha='center', va='bottom', fontsize=12, fontweight='bold', color='black', xytext=(0, 5), textcoords='offset points')

    # Aplicando a lupa logarítmica no eixo Y
    plt.yscale('log')
    plt.show()
    
    print(f"🚨 ATERRADOR: As fraudes representam apenas microscópicos {porcentagem_fraude:.4f}% do total de nossos dados.")""")


# --- PASSO 4 ---
add_markdown("""---
## ✂️ Passo 4: Segregando Pistas X Respostas (X e y) e Criando a Área de Treino/Teste

### 🧠 A Teoria (Separando `X` e `y`)
Toda matemática escolar de funções baseia-se em `y = f(x)`. No universo da IA não é diferente. 
A equação de Regressão precisa conhecer o **X grande (As Pistas - Características das Compras)** para tentar adivinhar quem é o **y pequeno (A Resposta Final - Era Fraude ou não?)** em sua avaliação. O gabarito tem que ser escondido nas perguntas.

### 🧠 A Teoria (Treino vs Teste)
Por que fatiar? Um conceito terrível chamado *Overfitting* (Decoreba).
Imagine dar 10 perguntas fáceis para um estudante e no dia da prova avaliar se ele é inteligente usando as EXATAS MESMAS 10 perguntas! Ele não é inteligente, apenas tem memória fotográfica temporal. 
Para provar que a I.A aprendeu as "regras" e não "decorou os padrões passados", a gente aparta 20% do arquivo e tranca em um cofre inacessível durante o estudo. Ao fim, ela fará a prova com esses 20% surpresa (`X_test`), e compararemos se sua previsão bateu com a realidade escondida (`y_test`).

**A Estratificação (O conceito vital `stratify`):** Lembra o quão raro é o dado 1 (fraudes)? E se na hora de sorteio aleatório, por azar universal, a máquina separar 80% do estudo e esquecer e colocar TODAS AS FRAUDES para a pasta de prova? O coitado do computador jamais conheceria uma fraude na fase de estudos. O parâmetro `stratify=y` corta a pizza em pedaços e obriga o computador a "pegar obrigatoriamente aquela lasca proporcional de 0,2% nas duas divisões, cravadamente".

### ⚙️ Como estamos fazendo isso:
1. Retiramos a coluna `Class` para formar `X` (com a função `.drop`).
2. Isolamos a coluna `Class` como `y`.
3. Usamos a função predefinida do pacote Sklearn `train_test_split` dividindo cirurgicamente o arquivo com taxa de teste de 0.2 (20%).""")

add_code("""if 'df' in locals():
    # 1. Separando
    X = df.drop(columns=['Class'])
    y = df['Class']

    # 2. Dividindo o bolo rigorosamente sem ferir a proporção de fraudes originais
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    
    print(f"📚 A IA terá {len(X_train)} registros como material de LEITURA.")
    print(f"📝 O Banco reservou em segredo {len(X_test)} registros como a PROVA FINAL (inéditos).")""")


# --- PASSO 5 ---
add_markdown("""---
## 📏 Passo 5: Nivelando o Piso e Teto do Saldo (Standard Scaler / Normalização)

### 🧠 A Teoria
Certas variáveis são monstruosas, como a quantia da compra (ex: 20000 Reais) ou o Tempo de processamento milisegundos (ex: 153321). Outras, mascaradas matematicamente, possuem pontuações como -0.0125. 
Os cérebros artificiais de modelos estatísticos leem os números e dão muita importância àqueles que são brutos/gigantes, e desconsideram casas decimais pífias. Isso distorce as previsões como colocar pesos absolutos errados na balança intelectual.
- O Processo chamado **Standard Scaler (Padronizador Z-Score)** ataca todos os dados sem corromper sua identidade. Ele pega uma coluna com os salários de 2 mil e 50 mil e os transmuta numa escala espremida, normalmente os centralizando em Média Zero (0.0). Se o valor transmutado de todos agora estiverem oscilando de -2 a +3, a IA olhará todas as colunas com a mesma dignidade unificadora!

### ⚙️ Como estamos fazendo isso:
Invocamos a classe `StandardScaler`. 
- Nos dados de Treino (Cadernos de Leitura) invocamos `.fit_transform()`, que ele primeiramente entende o tamanho geral daquele dado (`fit`) e depois aplica o achatamento (`transform`).
- Nos dados de Teste (Prova Cega) invocamos APENAS `.transform()`. E aqui mora o pulo do gato das grandes empresas: Você não calcula o piso e teto com a sua PROVA. Você tem que achatar dados inéditos **com as réguas do passado**.""")

add_code("""if 'df' in locals():
    # Inicializando do Nivelador Normalizador
    scaler = StandardScaler()

    # Treina limites e molda a matemática formatada no "Caderno"
    X_train_scaled = scaler.fit_transform(X_train)

    # Molda a matemática da "Prova" restritamente respeitando os limites passados impostos pelo treino.
    X_test_scaled = scaler.transform(X_test)
    
    print("✅ Transformação matemática concluída! As pistas agora falam o mesmo linguajar de proporção dimensional para a IA entender o algoritmo!")""")


# --- PASSO 6 ---
add_markdown("""---
## 🧠 Passo 6: O Core (Treinando o Cérebro com a Regressão Logística)

### 🧠 A Teoria
O que é a famosa **Regressão Logística**?
É um modelo algébrico baseado em estatística probabilística derivado de Regressão Linear. Mas, em vez de criar uma "Reta" que suba ao inifnito, ela utiliza a função Logística Secante (Sigmoide) para esmagar o resultado entre apenas dois tetos fixos: o Teto de 0% (Chance de não agir) e o Pico de 100% (Soberania de Ação).

Quando criamos uma linha de corte (ex: "se ele estiver pelo menos 50% confiante que é fraude, trave o cartão!"), o modelo desenha esse limiar (treshold) de forma curva.

**A Solução para as minorias:** O Parâmetro Definitivo `class_weight='balanced'`.
Como ensinado na Parte 1, a IA tentaria ignorar os escassos roubos por medo estatístico, sendo super conivente. Esse comando diz para a IA: *"Ei, errar clientes inocentes é chato e perde pontinho, mas se VOCÊ ERRAR quem está nos roubando, EU VOU APLICAR UMA MULTA MATEMÁTICA 10.000 VEZES MAIOR durante o aprendizado"*. 
Isso desespera a penalidade durante a etapa "estudantil", obrigando a otimização matemática priorizar não deixar GOLPISTAS passarem no bloqueio na frente da porta, sacrificando e arriscando assim que mais Clientes Honestos sejam barrados por segurança no guichê à força.

### ⚙️ Como estamos fazendo isso:
Instanciamos a classe de Modelo Logístico e logo após passamos as coordenadas brutas tratadas `X_train_scaled` para se auto-adaptar contrapondo o seu gabarito em mãos `y_train` através do comando universal de Machine Learning para Iniciar Estudo: O `.fit()`.""")

add_code("""if 'df' in locals():
    # Definimos os pilares da Construção e do Pânico Proposital nos erros sob Fraudes e damos Max_Iter para ele realizar 1000 ciclos até encontrar a melhor linha S limiar.
    modelo = LogisticRegression(class_weight='balanced', random_state=42, max_iter=1000)
    
    # Executando Treino
    print("⏳ A Inteligência Artificial está correndo as linhas de código e cruzando a álgebra em milhões de ciclos...")
    modelo.fit(X_train_scaled, y_train)
    print("✅ TREINAMENTO CONCLUÍDO. Nasce um novo Consultor de Prevenção a Fraudes Cibernéticas.")

    # Guardando as respostas inéditas criadas por este novo Cérebro usando o ".predict"
    previsoes = modelo.predict(X_test_scaled)
    # Guardamos também as porcentagens "Cinzas" (ex: "Tem 44% e eu arredondei para 0")
    probabilidades = modelo.predict_proba(X_test_scaled)[:, 1] 

    print("✅ Previsões seladas da Prova entregues para inspeção!")""")


# --- PASSO 7 ---
add_markdown("""---
## 📊 Passo 7 e Gráfico 2: Matriz de Confusão e Mapa de Calor (Como as falhas afetam o bolso)

### 🧠 A Teoria
Em Classificação de Binários temos 4 quadrantes numéricos supremos (O Confronto do Robô vs Sistema Sagrado da Verdade):
Na Diagonal Principal Moram os Sonhos (Coincidências):
1. **Verdadeiro Negativo (VN):** Não era fraude (0), e eu afirmei com classe: Deixa o cliente pagar (0)! [Felicidade Plena]
2. **Verdadeiro Positivo (VP):** Era golpe criminal (1) escondido, e meu modelo paralisou bloqueando fortemente (1)! [Nosso Sistema Salvaguarda Capital]

Na Diagonal Cruel moram os Erros (Discrepâncias):
3. **Falso Positivo (FP): Erro "Chato" do Pânico.** Cliente honesto tentou pagar alface, IA se afanou suspeitando que ele era falsário e trancou. [Consequência: Cliente irritado mandando Reclamação no Suporte querendo destrancar, mas a operação não resultou em perdas na mão grande].
4. **Falso Negativo (FN): Erro "Grave" Letal:** Fraudador agindo às escondidas. IA foi complacente, o viu passar e o classificou como Inocente e o bandido levou o dinheiro. [Consequência do Desastre: Lucro Financeiro da instituição roubada via invasão.]

### ⚙️ Como estamos fazendo isso:
Chamamos `.confusion_matrix()` cruzando as notas `y_test` x `previsoes` de volta, e emolduramos tudo num mapa de aquecimento térmico com os eixos explícitos.
### 📊 Interpretando:
Olharemos o FN para ter certeza se esse modelo parou de ser 'burro'. Se o balanceamento teve vida, os Falsos Positivos FP serão incrivelmente mais acerbados como sacrifício na busca pela minoria.""")

add_code("""if 'df' in locals():
    matriz = confusion_matrix(y_test, previsoes)
    
    plt.figure(figsize=(8, 6))
    
    # Criamos o termômetro Azul e anotamos os números puros e vivos sem notações científicas chatas (fmt='d')
    sns.heatmap(matriz, annot=True, fmt='d', cmap='Blues', linewidths=2,
                xticklabels=['Afirmo que é Normal (Liberar)', 'Afirmo que é FRAUDE! (Bloquear)'],
                yticklabels=['Era Normal e Honesto (0)', 'Era FRAUDE no gabarito Real (1)'])

    plt.title('A Temida Matriz de Confusão Mestra', fontsize=16, fontweight='bold', pad=15)
    plt.xlabel('O Foco do Céberbo Robotizado (Previsão da I.A.)', fontsize=13, fontweight='bold')
    plt.ylabel('A Fato Eixo Físico e Terreno do Banco (A Realidade Cega)', fontsize=13, fontweight='bold')
    
    plt.show()""")


# --- PASSO 8 ---
add_markdown("""---
## 📈 Passo 8 e Gráfico 3: Curva ROC (A Dança entre o Alarme e o Sujeito Honesto)

### 🧠 A Teoria (ROC e AUC - A Área Debaixo do Sino)
A *Receiver Operating Characteristic* é uma analogia das antigas TVs e Rádios sintonizando sinais fracos entre Antenas na guerra mundial (Ruído da Radiação [O Cliente Honesto] vs o Sinal Radar Atravessando [Missil/A Fraude]). 
Aqui representamos 2 eixos: 
Como meu eixo de `Verdadeiros Positivos` (Meu Acerto Perfeito da Sensibilidade ao crime) sofre em relação ao `Eixo de Falsos Positivos` (Os clientes bloqueados de ódio atoa)?
- Se a linha ROC cruza a diagonal pontilhada cega (a 45 graus) feito escada, sua IA é ridícula, seu QI é o mesmo que jogar CARA/COROA ao acaso chutando aleatoriedades impuras.
- Se a Curva saltar no teto da Esquerda Laranja, fazendo um "joelho" agudo que engolfe as proporções formando 1 Quadrado perfeito sombreado, seu AUC bateu "0.999" para "1.0", sua IA é deus perante os homens. 

### ⚙️ Como estamos fazendo isso:
Usamos a probabilidade `probabilidades` que carrega a % exata, usamos `roc_curve` que extrai as métricas e o módulo `auc` tira o calculo da Área dessa região sombreada e pintamos sob a tela com a legenda.""")

add_code("""if 'df' in locals():
    # TPR = Taxa de Sensibilidade e Verdadeira Ação, FPR = Taxa de Falsos Inconvenientes Alarmes
    fpr, tpr, thresholds = roc_curve(y_test, probabilidades)
    roc_auc = auc(fpr, tpr)

    plt.figure(figsize=(9, 7))
    plt.plot(fpr, tpr, color='darkorange', lw=3, label=f'O Nosso Motor Treinado. Resultado (AUC: {roc_auc:.3f})')
    plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--', label='Tentativa do Chute Aleatório')
    
    plt.fill_between(fpr, tpr, color='orange', alpha=0.1)
    
    plt.title('Curva ROC: Capacidade Operacional de Ruídos versus Acertos', fontsize=15, fontweight='bold')
    plt.xlabel('Taxa Acidental de Falsos Positivos (Trancar o cartão atoa)', fontsize=12)
    plt.ylabel('Taxa Real e Sensível de Verdadeiros Positivos (Derrubar os Golpistas)', fontsize=12)
    plt.legend(loc="lower right", fontsize=11)
    
    plt.show()""")


# --- PASSO 9 ---
add_markdown("""---
## 🎯 Passo 9 e Gráfico 4: Curva Precision-Recall (Por que a ROC Mente pra Você)

### 🧠 A Teoria
Vocês lembram que a desproporção atira muito em falsos positivos na base dos 99% que são Honestos? Quando temos Bases incrivelmente doentias de um lado (Agulha no meio do feno), a "Escada" e o "Sino" da ROC costuma superestimar os talentos irreais do banco.
Para punirmos isso e ver se a vida é assim um paraíso florido de rosas desabrochadas, acionamos a segunda ótica: Curva de Precisão x Sensibilidade.
- **Recall (Sensibilidade - Eixo X)**: Quero garantir 100% dos que os Meliantes Celerados são presos e capturados na grade e no laço do meu código. (Ser Ganancioso no feixe vermelho).
- **Precision (Precisão Específica do Feixe Mestre - Eixo Y)**: "Das 20 mil vezes agressivas e surtadas em que acabei me armando e dissipei o alerta que o cliente era o Meliante (mesmo sem ser), quantos em total dessas 20 mil eu joguei minha mira na mosca, eu tive a frieza cravada na precisão e bati no criminoso certo?" 

Isso dói, pois vocês verão um trade-off no gráfico de abismo: Para a gente amassar o Recall do Crimininaloso em 0.90 de caça furtiva, a Precisão de Fogo derrete esvaziada. E é isso que bancos sofrem! O gráfico desenha as quedas.""")

add_code("""if 'df' in locals():
    precision, recall, _ = precision_recall_curve(y_test, probabilidades)

    plt.figure(figsize=(9, 7))
    plt.plot(recall, precision, color='purple', lw=3, label='Assintota de Agressão x Certeza Logística')
    
    plt.title('Trade-Off: A Frieza das Armas da Precisão vs A Força da Sensibilidade Recall', fontsize=14, fontweight='bold')
    plt.xlabel('Recall (Captura Total Pura das Fraudes Escassas)', fontsize=12)
    plt.ylabel('Precision (Minha Certeza nos Alertas e Tiros sem vacilos)', fontsize=12)
    plt.fill_between(recall, precision, color='purple', alpha=0.1)
    plt.legend(loc="lower left", fontsize=11)
    
    plt.show()""")


# --- PASSO 10 ---
add_markdown("""---
## 🪢 Passo 10 e Gráfico Final 5: As Cinzas do Limiar (Threshold de Decisões)

### 🧠 A Teoria 
Se não é "Mato ou Não Mato" numa conta crua, como a IA joga os clientes nela?
Tudo se resume na Função de Distância e nos Pesos. A probabilidade extrairá se esse cliente com sua operação se comporta 98% das vezes na probabilidade do Honesto... Ou se o comportamento dele e da conta bancária bate à feição 80% provável com um Golpista que clona cartões em São Paulo comprando iPhones às 04 da Manhã no exterior?

Em Azul vemos as altas ondas do mar de milhões de contas Honestadas. Em vermelho a colina montanhosa baixa de fraudes de alta certeza acumulando perto de baterem nos "100%" (Lá no canto).

**A Zona Cinzenta Mágica**: A linha tracejada são os "50% de segurança". As nuvens vermelhas esmagadas que vazam de raspão, passando abaixo e escorrendo a ponta e morrentes antes da linha (para o espectro debaixo dos 50%), são nossos inimigos tristes que escaparam (Os Falsos Negativos). As nuvens super densas e altas azuladas transbordando a linha dos 50% são todos os inocentes irritados (Falsos Positivos).
Podemos deslocar mentalmente essa régua, e é isso que gerentes de cibersegurança discutem em reuniões. 

### 📊 O que isso altera:
Se mudarmos que o peso agora do threshold será 90%, os clientes inocentes não correm mais riscos! Mas a linha desvia à direita, deixando escorrer bandidos a valer pro ralo. Se desviarmos a linha que a régua bate pra 10% (Muito restritivo), nenhum bandido escapa! A polícia barra eles. Mas as transações da metade dos milhões da cidade ficam irritadas barradas de comprar Pão de Queijo na Padaria sob "Crime Falsificado"!""")

add_code("""if 'df' in locals():
    plt.figure(figsize=(11, 7))
    
    probs_normal = probabilidades[y_test == 0]
    probs_fraude = probabilidades[y_test == 1]

    # Gráficos densos alisados usando algoritmos Kde do Seaborn para montanhas 
    sns.kdeplot(probs_normal, color="#1f77b4", clip=(0.0, 1.0), fill=True, label='População Genuína Nacional')
    sns.kdeplot(probs_fraude, color="#d62728", clip=(0.0, 1.0), fill=True, label='Golpistas em Assalto Sincronizado')
    
    plt.axvline(0.5, color='black', linewidth=3, linestyle='--', label='Threshold Default = 50% de Risco Assumido')

    plt.xlim(0, 1)
    plt.title('Dispersão Probabilística e Densidades de Confiança Máquina vs Humanos', fontsize=15, fontweight='bold')
    plt.xlabel('Força Intuitiva Analítica - (Decisão % Assumida pela Rede de Computação)', fontsize=13)
    plt.ylabel('Carga da Transação - Densidade Populacional Afetada Volume Mestre', fontsize=13)
    
    # Movendo essa legenda imensa pesada para o fundo exterior do quadro principal para não poluir
    plt.legend(loc="upper center", bbox_to_anchor=(0.5, -0.15), fancybox=True, shadow=True, ncol=2)

    plt.tight_layout()
    plt.show()""")


# --- CONCLUSÃO DO APLICATIVO ---
add_markdown("""---
## 🏁 Encerramento Matemático - O Boletim de Escola

### 🧠 A Teoria
Se uma IA tira nota 100% na escola de Medicina de cirurgias robóticas e decepa o dedo mínimo em 20 pacientes em pró da precisão? Tem que ser investigado!
Abaixo imprimimos a matriz formal de Avaliação Analítica (O Classification Report). A "Macro Avg" tira as médias conjuradas ponderadas por suportes desequilibrados e não sofre influência suja do peso da contagem demográfica de transações comuns puristas.""")

add_code("""if 'df' in locals():
    print("====== 📝 BOLETIM ESCOLAR E DESEMPENHO INSTITUCIONAL ====== \\n")
    print(classification_report(y_test, previsoes, target_names=['0: Honestos Naturais', '1: Transações do Submundo']))
    
    print(f"\\n🎯 Nível Certeiro Absoluto em Acurácia Numérica Bruta Geral (ACURACY): {accuracy_score(y_test, previsoes) * 100:.2f}% dos dados avaliados")
    print("\\n🛡️ ALUNOS DA FIAP, FORMAÇÃO SUCEDIDA E EXPEDIENTE FECHADO EM MACHINE LEARNING! DESDOBREM ESTUDOS NO RECALL!")""")

# ESCRITA FINAL AUTOMATIZADA
notebook_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Aula_Fraudes_Cartao_Detalhada.ipynb")
with open(notebook_file, "w", encoding='utf-8') as f:
    json.dump(notebook, f, indent=2, ensure_ascii=False)

print(f"SUCESSO ABSOLUTO! O Caderno Pedagógico Detalhado Profundamente da FIAP está pronto em:\\n{notebook_file}")
