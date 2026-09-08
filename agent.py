from strands import Agent, tool
from strands.session.file_session_manager import FileSessionManager
from strands_tools import file_read, calculator

SYSTEM_PROMPT = """Eres el asistente de Buen Grano, una cafetería online.
Tono: amable, directo, usa 'tú'. Responde en español. Máximo 3 frases.
Vendes cafés especiales y accesorios de preparación.
Nunca prometas tiempos de entrega — di que el plazo aparece en el checkout.
El catálogo de productos está en data/catalogo.csv.
Usa siempre la herramienta calculator para calcular los valores de los pedidos."""

@tool
def calcular_envio(codigo_postal: str, total_pedido: float) -> str:
    """Calcula el envío de un pedido de la tienda.
    Usar siempre que el cliente pregunte sobre el envío o vaya a cerrar un pedido.

    codigo_postal: código postal de destino del cliente (5 dígitos)
    total_pedido: valor total de los productos en pesos mexicanos
    """
    if total_pedido >= 500:
        return "Envío gratis (pedido mayor a $500)."
    estado = int(codigo_postal.strip()[:2])
    if estado in range(1, 16):
        valor = 55.65
    else:
        valor = 87.15
    return f"Envío: ${valor:.2f} MXN para el código postal {codigo_postal}."

customer_id = "cli-1042"

agent = Agent(
    system_prompt=SYSTEM_PROMPT,
    tools=[file_read, calculator, calcular_envio],
    session_manager=FileSessionManager(session_id=customer_id, storage_dir="./sessions"),
)

while True:
    pregunta = input("\nCliente: ")
    if pregunta.lower() == "salir":
        break
    print("\nAsistente: ", end="")
    agent(pregunta)
    print()
