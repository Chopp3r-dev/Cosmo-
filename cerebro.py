from groq import Groq
import config
import json

# Inicializa o cliente do Groq
client = Groq(api_key=config.API_KEY)

def pensar(pergunta, prompt_sistema, historico):
    """
    Faz a Cosmo pensar usando a velocidade absurda do Groq.
    """
    try:
        # 1. Montagem do contexto (System + Histórico + User)
        mensagens = [{"role": "system", "content": prompt_sistema}]
        
        for msg in historico:
            role = "assistant" if msg['role'] == "assistant" else "user"
            mensagens.append({"role": role, "content": msg['content']})
        
        mensagens.append({"role": "user", "content": pergunta})

        # 2. Chamada para o Groq
        completion = client.chat.completions.create(
            model=config.MODELO,
            messages=mensagens,
            temperature=0.9, # Mantendo a temperatura alta para ela ser sarcástica
            max_tokens=1024,
            top_p=1,
            stream=False,
        )
        
        return completion.choices[0].message.content

    except Exception as e:
        return f"Erro no motor Groq: {e}"

def refletir_e_salvar(nome_usuario, historico, pasta_atual):
    """Lógica para atualizar afinidade e vibe usando o Groq"""
    if not historico: return
    
    prompt_analise = (
        "Analise a conversa e retorne APENAS um JSON: "
        "{\"nova_afinidade\": int, \"nova_vibe\": \"string\", \"resumo_pasta\": \"string\"}"
    )

    try:
        response = client.chat.completions.create(
            model=config.MODELO,
            messages=[{"role": "user", "content": prompt_analise}],
            response_format={"type": "json_object"}
        )
        dados = json.loads(response.choices[0].message.content)
        from Modulos import memoria
        memoria.salvar_aprendizado(
            nome_usuario, 
            dados.get('nova_afinidade', pasta_atual['afinidade']), 
            dados.get('resumo_pasta', ''), 
            dados.get('nova_vibe', 'Neutra')
        )
    except:
        pass
