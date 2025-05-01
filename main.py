import os
import random
import time
from datetime import datetime
from instagrapi import Client
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

# Caminho do arquivo de controle
ARQUIVO_POSTADOS = "postados.txt"

# Autenticação com Google Drive
def auth_google_drive():
    gauth = GoogleAuth()
    gauth.LoadCredentialsFile("mycreds.txt")
    if gauth.credentials is None:
        gauth.LocalWebserverAuth
    elif gauth.access_token_expired:
        gauth.Refresh()
    else:
        gauth.Authorize()
    gauth.SaveCredentialsFile("mycreds.txt")
    return GoogleDrive(gauth)

drive = auth_google_drive()

# Login no Instagram
cl = Client()
cl.login("codigoalpha.m", "Alphacod1575#")

# Carrega IDs de vídeos já postados
def carregar_postados():
    if os.path.exists(ARQUIVO_POSTADOS):
        with open(ARQUIVO_POSTADOS, "r") as f:
            return set(l.strip() for l in f)
    return set()

# Salva ID de vídeo postado
def salvar_postado(file_id):
    with open(ARQUIVO_POSTADOS, "a") as f:
        f.write(file_id + "\n")

# Baixa e posta um vídeo agora
def baixar_e_postar():
    print(f"[{datetime.now().strftime('%d/%m %H:%M:%S')}] 🔍 Procurando vídeo aleatório...")
    file_list = drive.ListFile({
        'q': "'1nZJujcAInfCETttjydIoN8Ar4EUBc6FM' in parents and trashed=false"
    }).GetList()

    postados = carregar_postados()
    videos_nao_postados = [f for f in file_list if f['mimeType'] == 'video/mp4' and f['id'] not in postados]

    if not videos_nao_postados:
        print("⚠️ Nenhum vídeo novo disponível para postagem.")
        return

    video_escolhido = random.choice(videos_nao_postados)
    video_escolhido.GetContentFile("video.mp4")

    try:
        legendas = [
            "Confira esse vídeo! 🔥",
            "Mais um conteúdo pra você 👇",
            "Postagem automática 🤖",
            "Olha isso aqui! 👀"
        ]
        caption = random.choice(legendas)

        cl.clip_upload("video.mp4", caption=caption)
        print(f"[{datetime.now().strftime('%d/%m %H:%M:%S')}] ✅ Postado: {video_escolhido['title']}")
        salvar_postado(video_escolhido['id'])
    except Exception as e:
        print(f"❌ Erro ao postar: {e}")
    finally:
        if os.path.exists("video.mp4"):
            os.remove("video.mp4")
            print("🧨 Vídeo explodido localmente (removido do disco).")

# Executa o bot imediatamente
baixar_e_postar()
