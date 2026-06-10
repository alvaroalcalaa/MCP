# MCP Sales Demo

Demo simple de un servidor MCP en Python para explicar el patrón de uso con datos de ventas.

## Qué incluye

- `server.py`: servidor MCP con recursos, herramientas y prompt.
- `sales.csv`: datos de ejemplo.
- `requirements.txt`: dependencias mínimas.
- `README.md`: guía de uso y conexión.

## Requisitos

- Python 3.10 o superior.
- `mcp` y `pandas`.

## Instalación

```bash
pip install -r requirements.txt
```

## Cómo ejecutar

```bash
python server.py
```

Este servidor usa `stdio`, que es el modo más común para conectarlo a un host MCP como Claude Desktop.

## Cómo conectarlo a Claude Desktop

Agregá una entrada como esta en la configuración de Claude Desktop:

```json
{
  "mcpServers": {
    "sales-demo": {
      "command": "python",
      "args": ["C:/ruta/al/proyecto/mcp_sales_demo/server.py"]
    }
  }
}
```

En Windows, podés usar la ruta completa a tu `python.exe` si hace falta.

## Cómo probarlo con el Inspector

Podés abrir el Inspector de MCP y conectarlo al servidor local que corre por stdio.

## Qué puede hacer la demo

- Leer el dataset completo como recurso.
- Leer el esquema de la tabla.
- Ejecutar consultas SQL sobre ventas.
- Calcular revenue mensual.
- Obtener top productos.
- Ver métricas generales.
- Generar un prompt base para análisis.

## Idea para explicarlo en una clase

- El host es la app que usa la persona.
- El cliente MCP vive dentro del host.
- El servidor MCP expone datos y acciones.
- El modelo usa ese servidor sin que tengas que hardcodear cada integración por separado.

## Ejemplos de uso

Consulta SQL:

```sql
SELECT category, SUM(revenue) AS total_revenue
FROM sales
GROUP BY category
ORDER BY total_revenue DESC;
```

Top productos:

```text
top_products
```

Revenue mensual:

```text
monthly_revenue
```

## Nota

Si cambiás el CSV, reiniciá el servidor para recargar los datos.
🧠 Pregunta: ¿Cómo viene el revenue mensual?

🤖 El modelo eligió: monthly_revenue

🛠 Resultado tool:
(monthly data...)

📊 Respuesta final:
"El revenue muestra crecimiento en los últimos meses..."
