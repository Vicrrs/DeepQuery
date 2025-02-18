import re
import pandas as pd
from llm import llm
from database import query_db

def generate_sql(question, schema_info):
    """Gera uma query SQL a partir da pergunta do usuário usando LangChain."""
    prompt = f"""
    Você é um assistente SQL especializado em PostgreSQL.
    Gere **apenas** a consulta SQL para responder à pergunta abaixo.
    
    - Não inclua nada de markdown (```sql).
    - Não inclua explicações adicionais (</think>, etc.).
    - Somente a query SQL pura!

    Pergunta: "{question}"

    Esquema do banco de dados:
    {schema_info}

    Responda somente com a consulta SQL válida.
    """

    # Usa invoke() para chamar o modelo
    raw_response = llm.invoke(prompt)

    # 1. Remove tags markdown ```sql ... ```
    #    Se encontrar, captura apenas o que está dentro das crases.
    match_codeblock = re.search(
        r"```sql\s*(.*?)```",   # Padrão: ```sql ... ```
        raw_response,
        flags=re.IGNORECASE | re.DOTALL
    )
    if match_codeblock:
        # Capturamos apenas o conteúdo interno
        sql_query = match_codeblock.group(1).strip()
    else:
        # 2. Caso não encontre code block,
        #    tentamos extrair só o texto que começa em SELECT e termina em ponto-e-vírgula
        match_select = re.search(
            r"(SELECT.*?;)",
            raw_response,
            flags=re.IGNORECASE | re.DOTALL
        )
        if match_select:
            sql_query = match_select.group(1).strip()
        else:
            # 3. Se não achou nada, usamos a resposta "crua"
            sql_query = raw_response.strip()

    # Limpamos outras tags que possam sobrar (</think>, etc.)
    sql_query = re.sub(r"</?\w+>", "", sql_query)
    sql_query = sql_query.strip()

    # Verifica se a query gerada é plausível
    if "SELECT" not in sql_query.upper():
        raise ValueError("A resposta do modelo não parece ser uma consulta SQL válida.")

    return sql_query

def run_query(question):
    """Gera a query SQL, executa no banco e retorna os resultados formatados."""
    schema_info = """
    Tabelas disponíveis:
    - clientes(id, nome, email)
    - pedidos(id, cliente_id, total, data)
    """
    
    sql_query = generate_sql(question, schema_info)
    print(f"\n📌 **Query gerada:**\n{sql_query}")

    try:
        result = query_db(sql_query)

        # usando pandas para formatar
        df = pd.DataFrame(result)

        if len(result) > 0:
            explanation = f"\n📊 **Resultados da consulta:**\n\n{df.head(10)}\n\n"
            explanation += f"A consulta retornou **{len(result)} registros**."
        else:
            explanation = "🔍 A consulta não retornou nenhum resultado."

        return explanation
    except Exception as e:
        return f"❌ Erro ao processar a consulta: {e}"
