from flask import Flask, request, Response
import requests

app = Flask(__name__)

@app.route('/')
def index():
    with open('index.html', 'r', encoding='utf-8') as f:
        return f.read()

@app.route('/proxy')
def proxy():
    url = request.args.get('url')
    if not url:
        return "Missing URL", 400
    
    # الترويسات الصحيحة والمعدلة لتقليد متصفح حقيقي وتفادي الحظر
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Referer': 'http://asmrasmr.live:8080/638109080/95827171997/1246118',
        'Origin': 'http://asmrasmr.live:8080',
        'Connection': 'keep-alive'
    }
    
    try:
        req = requests.get(url, headers=headers, stream=True, timeout=10)
        
        # تمرير محتوى البث مباشرة إلى المشغل
        def generate():
            for chunk in req.iter_content(chunk_size=4096):
                yield chunk
                
        return Response(generate(), content_type=req.headers.get('Content-Type'))
    except Exception as e:
        return str(e), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
