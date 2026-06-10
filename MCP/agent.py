import os
from openai import OpenAI

# =========================
# CONFIG LLM (usa tu .env)
# =========================
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("OPENAI_API_BASE"),
)

MODEL = os.getenv("LMSTUDIO_MODEL")

# =========================
# IMPORTAMOS LAS TOOLS
# =========================
# ⚠️ Esto simula MCP (llamamos directo a las funciones del server)
from server import monthly_revenue, summary_stats, query_sales


# =========================
# AGENTE SIMPLE
# =========================
def agent(question: str):
    print(f"\n🧠 Pregunta: {question}\n")

    # 1. Le preguntamos al modelo qué hacer
    decision_prompt = f"""
Sos un analista de ventas.

Tenés estas tools disponibles:
- monthly_revenue
- summary_stats
- query_sales

Decidí SOLO el nombre de la tool a usar para responder:

Pregunta: {question}

Respondé SOLO con el nombre de la tool.
"""

    resp = client.responses.create(
        model=MODEL,
        input=decision_prompt
    )

    tool_name = resp.output_text.strip().lower()

    print(f"🤖 El modelo eligió: {tool_name}\n")

    # =========================
    # 2. Ejecutamos la tool
    # =========================
    if "monthly" in tool_name:
        result = monthly_revenue()

    elif "summary" in tool_name:
        result = summary_stats()

    elif "query" in tool_name:
        result = query_sales("SELECT * FROM sales LIMIT 5")

    else:
        result = "No se pudo decidir una tool"

    print("🛠 Resultado tool:\n")
    print(result)

    # =========================
    # 3. Respuesta final del modelo
    # =========================
    final_prompt = f"""
Pregunta: {question}

Resultado de herramientas:
{result}

Generá una respuesta clara para el usuario.
"""

    final_resp = client.responses.create(
        model=MODEL,
        input=final_prompt
    )

    print("\n Respuesta final:\n")
    print(final_resp.output_text)


# =========================
# MAIN
# =========================
if __name__ == "__main__":
    agent("¿Cómo viene el revenue mensual?")