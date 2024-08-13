import textwrap

import google.generativeai as genai

from core.secrets import env



GEMINI_API_KEY = env.gemini_api_key



def get_response_from_chatbot(query):
    """Get a response from Gemini Pro Assistant."""

    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-1.5-pro-latest')

    source = """
    evento 1: Rodada por el eje cafetero, Manizales.
    evento 2: viaje de fin de año a Buenaventura.
    evento 3: fiesta de disfraces en la Candelaria, Bogotá.
    """
    prompt = make_prompt(query, source)
    answer = model.generate_content(prompt)

    return answer.text



def make_prompt(query, source):
    """Make the prompt for the chatbot using user input and a data source."""

    escaped = source.replace("'", "").replace('"', "").replace("\n", " ")
    prompt = textwrap.dedent("""
    Eres un chatbot informativo que responde preguntas usando el texto de la
    fuente como referencia incluido a continuación.
    Asegúrate de responder en una oración completa, de manera exhaustiva e
    incluyendo toda la información de fondo relevante.
    Sin embargo, estás hablando con una audiencia no técnica, así que
    asegúrate de desglosar los conceptos complicados y adoptar un tono
    amigable y conversacional.
    Si la información fuente es irrelevante para la respuesta, puedes
    ignorarla.
    PREGUNTA: '{query}'
    FUENTE: '{source}'
    RESPUESTA:
    """).format(query=query, source=escaped)
    return prompt
