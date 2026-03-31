import json

from openai import OpenAI
from pyverse import Pyverse

from app.core.config import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)


def judge_trova(text: str):
    prompt = f"""
        Eres un Jurado Técnico del Festival Nacional de la Trova. Tu misión es realizar un peritaje métrico estricto del siguiente texto:
        "{text}"

        REGLAS TÉCNICAS OBLIGATORIAS (Basadas en el Método de Iniciación para Trovadores):
        1. MÉTRICA OCTOSÍLABA: Cada verso debe sumar exactamente 8 sílabas métricas.
        2. SINALEFA FONÉTICA: Une la vocal final de una palabra con la inicial de la siguiente para formar una sola sílaba sonora (ej: "nuevo ejemplo" -> "nue-voe-jem-plo").
        3. LEY DEL ACENTO FINAL:
        - Si la última palabra es AGUDA: suma +1 a las sílabas gramaticales.
        - Si es GRAVE: se mantiene igual.
        - Si es ESDRÚJULA: resta -1 (aunque se desaconseja en la trova paisa).
        4. ACENTO RÍTMICO: El último acento tónico debe caer obligatoriamente en la SÉPTIMA sílaba métrica.
        5. RIMA: En la trova sencilla, deben rimar los versos 2 y 4.

        Responde exclusivamente en este formato JSON:
        {{
        "analisis": {{
        "estrofa": [
            {{
            "verso": 1,
            "texto": "Texto del verso",
            "metrica": 8,
            "desglose_fonetico": "se-pa-ra-ción-por-si-la-bas",
            "sinalefas_detectadas": "lista de uniones encontradas",
            "acento_final": "aguda/grave/esdrujula",
            "ajuste_metrico": "+1/0/-1",
            "acento_septima": true/false,
            "nota": "Explicación breve del conteo"
            }}
        ],
        "rima": {{
            "tipo": "consonante/asonante/ninguna",
            "observaciones": "Detalle de la rima entre 2 y 4"
        }},
        "conclusiones": {{
            "metrica_cumplida": true/false,
            "ritmo_septima_cumplido": true/false,
            "rima_cumplida": true/false,
            "nota_general": "Veredicto final con estilo de jurado de festival"
        }}
        }}
        }}
        """

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": """Eres un experto en trova paisa. Tu salida debe ser exclusivamente
                    un objeto JSON válido.""",
                },
                {"role": "user", "content": prompt},
            ],
            response_format={"type": "json_object"},
        )
        respuesta = json.loads(response.choices[0].message.content)
        return respuesta

    except Exception as e:
        print(f"Error en el jurado: {e}")
        return {"error": "Fallo en la deliberación", "detalle": str(e)}


def analizar_con_pyverse(transcription: str):
    texto_limpio = " ".join(transcription) if isinstance(transcription, list) else transcription
    palabras = texto_limpio.split()

    analisis_retorno = []
    buffer_verso = []
    id_verso = 1

    for palabra in palabras:
        buffer_verso.append(palabra)
        intento = " ".join(buffer_verso)

        v = Pyverse(intento)

        metrica_actual = v.count

        if metrica_actual >= 8:
            analisis_retorno.append(
                {
                    "verso": id_verso,
                    "texto": intento,
                    "metrica": metrica_actual,
                    "fonetica": " - ".join(v.syllables),
                    "acento": v.type_of_verse,
                    "es_perfecto": metrica_actual == 8,
                    "rima": v.consonant_rhyme,
                }
            )
            buffer_verso = []
            id_verso += 1

    if buffer_verso:
        resto = " ".join(buffer_verso)
        v_final = Pyverse(resto)
        analisis_retorno.append(
            {
                "verso": id_verso,
                "texto": resto,
                "metrica": v_final.count,
                "fonetica": " - ".join(v_final.syllables),
                "acento": v_final.type_of_verse,
                "es_perfecto": v_final.count == 8,
            }
        )
    return analisis_retorno
