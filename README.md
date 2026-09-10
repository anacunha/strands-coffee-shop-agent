# Agente de IA con Strands Agents

[Strands Agents](https://strandsagents.com?trk=54e40584-a59e-4b8d-a5b4-ecfbd722ff7e&sc_channel=el) es el SDK open source de AWS para crear agentes en pocas líneas de Python: defines un prompt, le pasas herramientas, y el modelo decide cuándo usarlas.

Este repo es la demo del video [Cómo Crear un Agente de IA con Strands Agents](https://youtu.be/TCgoZzHHwtU). Es un agente completo, con herramientas propias, MCP, sesiones y salida estructurada.

## Qué hace

Atiende a los clientes de una cafetería online por chat en la terminal. Consulta el catálogo, arma el pedido, cotiza el envío y cierra la venta con un link de pago de Stripe. Al salir, imprime el pedido como JSON.

## Cómo está construido

Todo el agente vive en `agent.py`. Esta es la parte central:

```python
agent = Agent(
    system_prompt=SYSTEM_PROMPT,
    tools=[file_read, calculator, calcular_envio, stripe_mcp],
    session_manager=FileSessionManager(session_id=customer_id, storage_dir="./sessions"),
)
```

De ahí salen los conceptos de Strands que cubre la demo:

| Concepto | En el código | Para qué sirve aquí |
|---|---|---|
| Herramientas de la comunidad | `file_read`, `calculator`, del paquete `strands-agents-tools` | Leer el catálogo y hacer las cuentas del pedido |
| Herramientas personalizadas | `@tool def calcular_envio(...)` | Una función de Python con docstring se vuelve herramienta |
| MCP | `MCPClient` → `https://mcp.stripe.com` | Crear el payment link sin escribir un cliente de la API |
| Sesiones | `FileSessionManager` | El agente recuerda la conversación entre mensajes y entre ejecuciones |
| Salida estructurada | `structured_output_model=Pedido` | Convierte el chat en un modelo Pydantic validado |

## Requisitos

- Python 3.10 o más reciente
- Cuenta de AWS con [acceso habilitado](https://docs.aws.amazon.com/bedrock/latest/userguide/model-access.html?trk=54e40584-a59e-4b8d-a5b4-ecfbd722ff7e&sc_channel=el) al modelo que Strands usa por default en Amazon Bedrock: Claude Sonnet 4.6 (`global.anthropic.claude-sonnet-4-6`)
- Credenciales de AWS locales con permiso `bedrock:InvokeModel`, por ejemplo con [`aws configure`](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html?trk=54e40584-a59e-4b8d-a5b4-ecfbd722ff7e&sc_channel=el)
- Una [llave de test de Stripe](https://docs.stripe.com/keys) (la cuenta es gratis)

## Cómo correrlo

```bash
git clone https://github.com/anacunha/strands-coffee-shop-agent.git
cd strands-coffee-shop-agent

python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate

pip install -r requirements.txt

export STRIPE_SECRET_KEY=sk_test_...

python agent.py
```

Escribe `salir` para terminar el chat y ver el resumen del pedido en JSON.

## Estructura

| Archivo | Qué es |
|---|---|
| `agent.py` | El agente: system prompt, herramientas, sesión, MCP |
| `models.py` | Modelo Pydantic para la salida estructurada del pedido |
| `data/catalogo.csv` | Catálogo de productos |
| `sessions/` | Historial de conversación (generado en runtime, no versionado) |
