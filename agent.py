from strands import Agent
from strands_tools import file_read, calculator

SYSTEM_PROMPT = """Eres el asistente de Buen Grano, una cafetería online.
Tono: amable, directo, usa 'tú'. Responde en español. Máximo 3 frases.
Vendes cafés especiales y accesorios de preparación.
Nunca prometas tiempos de entrega — di que el plazo aparece en el checkout.
El catálogo de productos está en data/catalogo.csv.
Usa siempre la herramienta calculator para calcular los valores de los pedidos."""

agent = Agent(system_prompt=SYSTEM_PROMPT, tools=[file_read, calculator])

while True:
    pregunta = input("\nCliente: ")
    if pregunta.lower() == "salir":
        break
    print("\nAsistente: ", end="")
    agent(pregunta)
    print()
