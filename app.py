from flask import Flask, request, jsonify, send_file
import yt_dlp
import io
import os
import tempfile

app = Flask(__name__)

def baixar_audio(url):
    # Lê a variável de ambiente COOKIES_DATA
    cookies_data = os.getenv('COOKIES_DATA')
    
    if cookies_data:
        # Cria um arquivo temporário para os cookies
        cookies_path = tempfile.mktemp()
        with open(cookies_path, 'w') as f:
            f.write(cookies_data)
    else:
        cookies_path = None  # Não usará cookies se a variável não for encontrada
    
    ydl_opts = {
        'format': 'bestaudio/best',
        'cookies': cookies_path,  # Usando cookies a partir do arquivo temporário
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': os.path.join(tempfile.gettempdir(), '%(title)s.%(ext)s'),
        'quiet': True,
        'no_warnings': True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=True)
        file_path = ydl.prepare_filename(info_dict).replace('.webm', '.mp3').replace('.m4a', '.mp3')

    return file_path

@app.route('/download_audio', methods=['POST'])
def download_audio():
    data = request.get_json()
    url = data.get('url')
    if not url:
        return jsonify({'error': 'URL is required'}), 400

    try:
        file_path = baixar_audio(url)
        return send_file(file_path, as_attachment=True, download_name='audio.mp3', mimetype='audio/mpeg')
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
