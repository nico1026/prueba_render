"""API de análisis de sentimiento — lista para empaquetar en Docker."""
from fastapi import FastAPI
from pydantic import BaseModel
from transformers import pipeline

app = FastAPI(title="API de Sentimiento en Docker")

# el modelo se carga una vez al arrancar el contenedor
clasificador = pipeline(
    "sentiment-analysis",
    model="distilbert-base-uncased-finetuned-sst-2-english",
)


class Texto(BaseModel):
    texto: str


@app.get("/")
def raiz():
    return {"estado": "viva", "corriendo_en": "Docker"}


@app.post("/analizar")
def analizar(entrada: Texto):
    r = clasificador(entrada.texto)[0]
    return {
        "texto": entrada.texto,
        "sentimiento": r["label"],
        "confianza": round(float(r["score"]), 4),
    }
