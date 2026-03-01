import sqlite3
import os

DB_PATH = "/storage/emulated/0/Projeto_Cosmo/Dados/memoria_cosmo.db"

def iniciar_banco():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # LONGO PRAZO: Informações sobre o Chopp3r
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS humanos (
            nome TEXT PRIMARY KEY,
            afinidade INTEGER,
            observacoes TEXT,
            vibe_atual TEXT
        )
    ''')

    # Correção para garantir a coluna 'id' no histórico
    try:
        cursor.execute("SELECT id FROM historico_v2 LIMIT 1")
    except sqlite3.OperationalError:
        cursor.execute("DROP TABLE IF EXISTS historico_v2")

    # MÉDIO PRAZO: Histórico persistente
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS historico_v2 (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT,
            role TEXT,
            content TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def carregar_pasta_humano(nome):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM humanos WHERE nome = ?", (nome,))
    res = cursor.fetchone()
    conn.close()
    if res:
        return {"nome": res[0], "afinidade": res[1], "observacoes": res[2], "vibe": res[3]}
    return None

def salvar_aprendizado(nome, afinidade, observacoes, vibe):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO humanos (nome, afinidade, observacoes, vibe_atual)
        VALUES (?, ?, ?, ?)
        ON CONFLICT(nome) DO UPDATE SET 
            afinidade = excluded.afinidade,
            observacoes = excluded.observacoes,
            vibe_atual = excluded.vibe_atual
    ''', (nome, afinidade, observacoes, vibe))
    conn.commit()
    conn.close()

def salvar_mensagem_v2(usuario, role, conteudo):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO historico_v2 (usuario, role, content) VALUES (?, ?, ?)", 
                   (usuario, role, conteudo))
    conn.commit()
    conn.close()

def pegar_historico_v2(usuario, limite=12):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT role, content FROM (
            SELECT id, role, content FROM historico_v2 
            WHERE usuario = ? 
            ORDER BY id DESC LIMIT ?
        ) ORDER BY id ASC
    ''', (usuario, limite))
    res = cursor.fetchall()
    conn.close()
    return [{"role": r, "content": c} for r, c in res]

def busca_profunda(usuario, termo):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    # Busca mensagens que contenham a palavra-chave (ex: 'prova')
    # Limitamos a 5 para não inundar o contexto de tokens
    cursor.execute('''
        SELECT role, content FROM historico_v2 
        WHERE usuario = ? AND content LIKE ? 
        ORDER BY id DESC LIMIT 5
    ''', (usuario, f'%{termo}%'))
    res = cursor.fetchall()
    conn.close()
    
    if not res:
        return "Nenhuma lembrança específica sobre isso no meu banco de dados."
    
    # Formata as lembranças para a IA ler
    lembrancas = "\n".join([f"{r}: {c}" for r, c in reversed(res)])
    return lembrancas
