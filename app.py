from flask import Flask, request, jsonify
import yt_dlp

app = Flask(__name__)

@app.route('/')
def home():
    return "API de descarga activa."

@app.route('/api', methods=['GET'])
def download():
    url = request.args.get('url')
    formato = request.args.get('format', 'video')
    if not url:
        return jsonify({'error': 'Falta la URL'}), 400

    ydl_opts = {
        'format': 'bestaudio' if formato == 'audio' else 'bestvideo+bestaudio/best',
        'quiet': True
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            return jsonify({'download_url': info['url'], 'title': info['title']})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
