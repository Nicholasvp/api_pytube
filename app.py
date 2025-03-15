from flask import Flask, request, jsonify
import yt_dlp
import os

app = Flask(__name__)

def baixar_audio(url):
    cookies_data = os.getenv("COOKIES_DATA")
    
    if not cookies_data:
        raise ValueError("Erro: Variável de ambiente 'COOKIES_DATA' não encontrada.")
    
    with open("cookies.txt", "w", encoding="utf-8") as f:
        f.write(cookies_data)

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': '%(title)s.%(ext)s',
        'cookiefile': 'cookies.txt'  
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    os.remove("cookies.txt")

@app.route('/download_audio', methods=['POST'])
def download_audio():
    data = request.get_json()
    url = data.get('url')
    if not url:
        return jsonify({'error': 'URL is required'}), 400

    try:
        baixar_audio(url)
        return jsonify({'message': 'Download concluído.'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
