import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score
import joblib

def load_and_preprocess_data():
    print("Wczytywanie danych...")
    # Wczytywanie plikow
    try:
        df1 = pd.read_csv('sqli.csv', encoding='utf-16')
        df2 = pd.read_csv('sqliv2.csv', encoding='utf-16')
        df3 = pd.read_csv('SQLiV3.csv')
    except Exception as e:
        print(f"Blad wczytywania zbiorow danych: {e}")
        return None

    # Zachowanie tylko istotnych kolumn 'Sentence' oraz 'Label'
    if 'Sentence' in df3.columns and 'Label' in df3.columns:
        df3 = df3[['Sentence', 'Label']]
    
    # Laczenie zbiorow danych
    df_combined = pd.concat([df1, df2, df3], ignore_index=True)
    
    # Czyszczenie danych
    print(f"Poczatkowa liczba wierszy: {len(df_combined)}")
    df_combined.dropna(subset=['Sentence', 'Label'], inplace=True)
    print(f"Liczba wierszy po usunieciu pustych wartosci: {len(df_combined)}")
    
    # Upewnienie sie, ze zdania sa tekstem, a etykiety liczbami calkowitymi
    df_combined['Sentence'] = df_combined['Sentence'].astype(str)
    df_combined['Label'] = pd.to_numeric(df_combined['Label'], errors='coerce')
    
    # Usuniecie wierszy, ktorych etykiet nie udalo sie przekonwertowac na liczby
    df_combined.dropna(subset=['Label'], inplace=True)
    df_combined['Label'] = df_combined['Label'].astype(int)
    
    print(f"Koncowa liczba wierszy przed trenowaniem: {len(df_combined)}")
    return df_combined

def train_model():
    df = load_and_preprocess_data()
    if df is None:
        return

    X = df['Sentence']
    y = df['Label']

    print("Ekstrakcja cech za pomoca TF-IDF...")
    vectorizer = TfidfVectorizer(max_features=5000, analyzer='char', ngram_range=(1, 3))
    X_vectorized = vectorizer.fit_transform(X)

    print("Dzielenie danych na zbior treningowy i testowy...")
    X_train, X_test, y_train, y_test = train_test_split(X_vectorized, y, test_size=0.2, random_state=42)

    print("Trenowanie RandomForestClassifier...")
    model = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
    model.fit(X_train, y_train)

    print("Ocena modelu...")
    y_pred = model.predict(X_test)
    
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred, average='binary')
    recall = recall_score(y_test, y_pred, average='binary')

    print("\n--- Metryki Modelu ---")
    print(f"Dokladnosc (Accuracy): {accuracy:.4f}")
    print(f"Precyzja (Precision):  {precision:.4f}")
    print(f"Czulosc (Recall):      {recall:.4f}")
    print("----------------------\n")

    print("Zapisywanie modelu i wektoryzatora...")
    joblib.dump(model, 'sqli_rf_model.joblib')
    joblib.dump(vectorizer, 'tfidf_vectorizer.joblib')
    print("Zapisano jako 'sqli_rf_model.joblib' oraz 'tfidf_vectorizer.joblib'")

if __name__ == "__main__":
    train_model()
