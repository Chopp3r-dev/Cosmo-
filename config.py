import os
from dotenv import load_dotenv

# 1. Carrega as variáveis do arquivo .env que está na mesma pasta
load_dotenv()

# 2. Define a Chave da API (Pega do .env)
# Se não encontrar, ele define como None para o erro ser tratado depois
API_KEY = os.getenv("GROQ_API_KEY")

# 3. Define o Modelo (Pega do .env ou usa o Llama 3 70B como padrão)
# O Llama 3 70B é o melhor para manter o sarcasmo e a personalidade
MODELO = os.getenv("MODELO_COSMO", "llama3-70b-8192")

# 4. Verificação de Segurança (Aparece no console se algo estiver errado)
if not API_KEY:
    print("\n[!] AVISO: A variável GROQ_API_KEY não foi encontrada no .env")
    print("[!] Certifique-se de que o arquivo .env existe e contém a chave correta.\n")
