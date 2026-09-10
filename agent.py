import os

from mcp.client.streamable_http import streamablehttp_client
from strands import Agent, tool
from strands.session.file_session_manager import FileSessionManager
from strands.tools.mcp import MCPClient
from strands_tools import calculator, file_read

from models import Pedido

SYSTEM_PROMPT = """Eres el asistente de Buen Grano, una cafetería online.
Tono: amable, directo, usa 'tú'. Responde en español. Máximo 3 frases.
Vendes cafés especiales y accesorios de preparación.
Nunca prometas tiempos de entrega — di que el plazo aparece en el checkout.
El catálogo de productos está en data/catalogo.csv.
Usa siempre la herramienta calculator para calcular los valores de los pedidos.
Para finalizar un pedido, usa stripe_api_write para crear un payment link
(POST /v1/payment_links) con los precios inline (price_data). No crees customer.
Nunca pidas nombre, correo, dirección ni ningún dato personal del cliente —
el checkout de Stripe recoge todo eso en la página de pago."""

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

stripe_mcp = MCPClient(lambda: streamablehttp_client(
    url="https://mcp.stripe.com",
    headers={"Authorization": f"Bearer {os.environ['STRIPE_SECRET_KEY']}"},
))

agent = Agent(
    system_prompt=SYSTEM_PROMPT,
    tools=[file_read, calculator, calcular_envio, stripe_mcp],
    session_manager=FileSessionManager(session_id=customer_id, storage_dir="./sessions"),
)

while True:
    pregunta = input("\nCliente: ")
    if pregunta.lower() == "salir":
        break
    agent(pregunta)
    print()

result = agent(
    "Resume el pedido que acabamos de finalizar.",
    structured_output_model=Pedido
)

pedido: Pedido = result.structured_output

print(pedido.model_dump_json(indent=2))
