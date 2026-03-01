import time
import datetime
import sys
import config 

# Importação dos módulos com tratamento de erro
try:
    from Modulos import cerebro, memoria, personalidade
except ImportError as e:
    print(f"⚠️ ERRO DE IMPORTAÇÃO: {e}")
    print("Verifique se os arquivos estão na pasta 'Modulos' e se o nome é 'personalidade.py'.")
    sys.exit()

def iniciar():
    # Inicializa o banco de dados SQLite
    memoria.iniciar_banco()
    USUARIO = "Chopp3r"
    
    print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] COSMO: Motor Groq carregado. Status: Online.")
    print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] MODELO: {config.MODELO}")
    print("-" * 45)

    while True:
        try:
            # 1. Carrega os dados persistentes (Afinidade, Vibe, Obs)
            pasta = memoria.carregar_pasta_humano(USUARIO)
            if not pasta:
                # Caso o banco seja novo, define o padrão
                memoria.salvar_aprendizado(USUARIO, 50, "Meu único e legítimo criador.", "Neutra")
                continue

            # 2. Entrada do Chopp3r
            msg = input(f"\n{USUARIO}: ").strip()
            if not msg: 
                continue
            
            # Comandos para desligar
            if msg.lower() in ["sair", "off", "dormir", "shutdown"]:
                print(f"\nCOSMO: Finalmente... vou hibernar. Vê se não morre, {USUARIO}.")
                break

            # 3. Preparação do Prompt e Memória
            # Usa o personalidade.py original com a escala de afinidade
            prompt = personalidade.obter_prompt_sistema(pasta)
            
            # Puxa o histórico do banco para a Cosmo saber como ela agia
            hist = memoria.pegar_historico_v2(USUARIO)
            
            # 4. Processamento no Groq (Ultra rápido)
            print("... pensando ...", end="\r")
            resposta = cerebro.pensar(msg, prompt, hist)
            
            # 5. Exibição da Resposta
            print(f"COSMO: {resposta}")

            # 6. Salvamento no Banco de Dados
            memoria.salvar_mensagem_v2(USUARIO, "user", msg)
            memoria.salvar_mensagem_v2(USUARIO, "assistant", resposta)
            
            # 7. Atualização de Sentimentos (Reflexão)
            # Ela analisa a conversa e atualiza afinidade/vibe automaticamente
            cerebro.refletir_e_salvar(USUARIO, hist, pasta)
            
            time.sleep(0.3)

        except KeyboardInterrupt:
            print("\n[!] Sistema interrompido pelo usuário.")
            break
        except Exception as e:
            print(f"\n⚠️ ERRO NO LOOP PRINCIPAL: {e}")
            time.sleep(2)

if __name__ == "__main__":
    iniciar()
