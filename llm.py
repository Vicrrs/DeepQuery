from langchain_community.llms import LlamaCpp
from config import MODEL_PATH

def load_model():
    """Carregando o modelo Llama GGUF no langchain"""
    return LlamaCpp(
    model_path=MODEL_PATH,
    n_ctx=2048,
    temperature=0.1,
    max_tokens=100_000_000_000_000_000_000,
    n_gpu_layers=32,
    verbose=False
)

llm = load_model()
