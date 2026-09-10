from pydantic import BaseModel, Field

class ItemPedido(BaseModel):
    producto: str = Field(description="Nombre del producto")
    cantidad: int
    precio_unitario: float

class Pedido(BaseModel):
    """Resumen de un pedido"""
    items: list[ItemPedido]
    envio: float = Field(description="Valor del envío")
    total: float = Field(description="Total del pedido con envío")
