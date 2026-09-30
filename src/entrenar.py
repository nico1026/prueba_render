"""Entrena el clasificador de sentimiento y lo guarda en un archivo.

Se corre UNA vez, durante el `docker build`. El contenedor que sale ya trae el
modelo adentro: arranca sin descargar nada y sin necesitar internet.

    python -m src.entrenar
"""
from pathlib import Path

import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import RepeatedStratifiedKFold, cross_val_score
from sklearn.pipeline import FeatureUnion, Pipeline

from src.datos import cargar

MODELO = Path(__file__).parent / "modelo.joblib"


def construir():
    """El modelo: convertir texto en números, y luego trazar una frontera.

    Dos vistas del mismo texto, pegadas una al lado de la otra:
      - palabras: aprende que "horrible" es mala señal y "encantó" es buena.
      - trozos de letras (n-gramas): aprende que "-ísimo" o "malí-" también
        cargan sentimiento, así generaliza a palabras que nunca vio.

    Con un dataset de 100 frases, la segunda vista es la que salva el día.
    """
    texto_a_numeros = FeatureUnion([
        ("palabras", TfidfVectorizer(sublinear_tf=True)),
        ("letras", TfidfVectorizer(analyzer="char_wb", ngram_range=(3, 5),
                                   sublinear_tf=True)),
    ])
    return Pipeline([
        ("vectorizar", texto_a_numeros),
        # C=100 = poca regularización. Con un dataset chico y limpio conviene
        # dejar que el modelo confíe en lo que ve; medido contra C=1 y C=10,
        # este gana por varios puntos.
        ("clasificar", LogisticRegression(C=100, max_iter=2000)),
    ])


def main():
    textos, etiquetas = cargar()
    print(f"Dataset: {len(textos)} frases etiquetadas a mano")

    modelo = construir()

    # Validación cruzada: entrena 5 veces, cada una dejando fuera un 20% para
    # calificarse. Es el número honesto — el accuracy sobre los datos de
    # entrenamiento siempre miente hacia arriba.
    #
    # shuffle=True no es un detalle: el dataset está ordenado (positivos y
    # luego negativos, y por grupos de palabra). Sin mezclar, cada fold recibe
    # un bloque temático entero y el resultado baja varios puntos por un
    # accidente del orden del archivo. n_repeats=6 promedia 6 mezclas
    # distintas, porque con 210 frases una sola partición es muy ruidosa.
    cv = RepeatedStratifiedKFold(n_splits=5, n_repeats=6, random_state=0)
    notas = cross_val_score(modelo, textos, etiquetas, cv=cv)
    print(f"Accuracy (validación cruzada): {notas.mean():.1%} ± {notas.std():.1%}")

    # Ya medido, entrenamos con todo para el modelo final.
    modelo.fit(textos, etiquetas)

    joblib.dump(modelo, MODELO)
    kb = MODELO.stat().st_size / 1024
    print(f"Modelo guardado en {MODELO} ({kb:.0f} KB)")

    for frase in ["Me encantó este curso", "Qué porquería de servicio"]:
        etiqueta = modelo.predict([frase])[0]
        confianza = modelo.predict_proba([frase]).max()
        print(f"  {frase!r} -> {etiqueta} ({confianza:.1%})")


if __name__ == "__main__":
    main()
