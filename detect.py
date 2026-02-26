import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from sklearn.preprocessing import StandardScaler

import os

def main():
    # Nome do arquivo informado
    file_path = 'creditcard.csv'
    
    # Caso o arquivo tenha o nome padrão do Kaggle (creditcard.csv), altere a variável acima.
    if not os.path.exists(file_path):
        print(f"Erro: O arquivo '{file_path}' não foi encontrado no diretório atual.")
        return

    print(f"Carregando a base de dados '{file_path}'...")
    df = pd.read_csv(file_path)

    # Assumindo que a coluna alvo se chama 'Class' (padrão de bases como a do Kaggle)
    # Se a sua coluna tiver outro nome, altere 'Class' abaixo.
    target_col = 'Class'
    
    if target_col not in df.columns:
        print(f"Erro: A coluna '{target_col}' não foi encontrada. As colunas disponíveis são: {list(df.columns)}")
        return

    # Separação das variáveis independentes (X) e da variável dependente (y)
    X = df.drop(columns=[target_col])
    y = df[target_col]

    print("\nDistribuição das classes na base:")
    print(y.value_counts())

    # Divisão entre treino (80%) e teste (20%)
    # stratify=y garante que a proporção de fraudes/normais seja mantida no treino e teste
    print("\nDividindo em treino (80%) e teste (20%)...")
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    
    # É uma boa prática escalar os dados em modelos como Regressão Logística
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # Criação e Treinamento do modelo
    # Utilizamos class_weight='balanced' pois a base de fraudes costuma ser extremamente desbalanceada
    print("\nTreinando o modelo de Regressão Logística...")
    model = LogisticRegression(class_weight='balanced', random_state=42, max_iter=1000)
    model.fit(X_train_scaled, y_train)

    # Testando o modelo com a base de teste
    print("\nFazendo previsões na base de teste...")
    y_pred = model.predict(X_test_scaled)

    # Avaliação dos resultados
    print("\n" + "="*40)
    print("RESULTADOS DA AVALIAÇÃO DO MODELO")
    print("="*40)
    
    print("\nMatriz de Confusão:")
    print(confusion_matrix(y_test, y_pred))
    
    print("\nRelatório de Classificação (Precision, Recall, F1-Score):")
    print(classification_report(y_test, y_pred))
    
    print(f"Acurácia Geral: {accuracy_score(y_test, y_pred):.4f}")

if __name__ == "__main__":
    main()
