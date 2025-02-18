from query_engine import run_query

if __name__ == "__main__":
    print("🚀 DeepQuery - Assistente SQL com DeepSeek e LangChain 🚀")
    
    while True:
        question = input("\n❓ Faça uma pergunta sobre o banco de dados (ou digite 'sair'): ")
        
        if question.lower() == "sair":
            print("👋 Encerrando o DeepQuery...")
            break
        
        try:
            explanation = run_query(question)
            print(explanation)
        except Exception as e:
            print(f"❌ Erro ao processar a consulta: {e}")
