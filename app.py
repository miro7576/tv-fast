import requests
from flask import Flask, render_template, Response, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

# 💡 هذا هو الحل الجذري: البروكسي الداخلي المباشر لكسر حظر المتصفح
@app.route('/stream-proxy')
def stream_proxy():
    original_url = request.args.get('url')
    if not original_url:
        return "Missing URL", 400
        
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        req = requests.get(original_url, headers=headers, stream=True, timeout=15)
        
        return Response(
            req.iter_content(chunk_size=1024*64),
            content_type=req.headers.get('Content-Type', 'application/x-mpegURL'),
            status=req.status_code
        )
    except Exception as e:
        return str(e), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
