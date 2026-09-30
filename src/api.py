"""API de análisis de sentimiento — lista para empaquetar en Docker."""
from pathlib import Path

import joblib
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="API de Sentimiento en Docker")

# El modelo se carga una vez al arrancar el contenedor, no en cada petición.
# Ya viene entrenado dentro de la imagen (ver el Dockerfile), así que esto es
# leer un archivo de unos pocos cientos de KB: milisegundos, y sin red.
MODELO = Path(__file__).parent / "modelo.joblib"
clasificador = joblib.load(MODELO)


class Texto(BaseModel):
    texto: str


@app.get("/")
def raiz():
    return {"estado": "viva", "corriendo_en": "Docker"}


@app.get("/modelo")
def info_modelo():
    """Qué hay dentro de la caja — útil para explicar el modelo en clase."""
    vectorizador = clasificador.named_steps["vectorizar"]
    rasgos = sum(
        len(v.vocabulary_) for _, v in vectorizador.transformer_list
    )
    return {
        "tipo": "TF-IDF + Regresión Logística (scikit-learn)",
        "clases": list(clasificador.classes_),
        "rasgos_aprendidos": rasgos,
        "tamano_kb": round(MODELO.stat().st_size / 1024),
    }


@app.post("/analizar")
def analizar(entrada: Texto):
    etiqueta = clasificador.predict([entrada.texto])[0]
    confianza = clasificador.predict_proba([entrada.texto]).max()
    return {
        "texto": entrada.texto,
        "sentimiento": etiqueta,
        "confianza": round(float(confianza), 4),
    }
