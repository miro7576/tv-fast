from flask import Flask, Response
import requests

app = Flask(__name__)

# تحديث الهوست والبورت الجديد بدقة لحسابك
HOST = "http://live.lynxiptv.xyz:80" 
USER = "777685932038"          
PASS = "VJQBOrw29f"            

@app.route('/')
def home():
    try:
        with open('index.html', 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        return "<h1>خطأ: ملف index.html غير موجود</h1>", 404

# نظام الوسيط الذكي لتخطي حظر متصفحات الهواتف
@app.route('/stream/<stream_id>.m3u8')
def proxy_stream(stream_id):
    target_url = f"{HOST}/live/{USER}/{PASS}/{stream_id}.m3u8"
    
    # جلب البث بالخلفية لفك تشفير بروتوكول HTTP المحظور في الهواتف
    req = requests.get(target_url, stream=True, headers={"User-Agent": "Mozilla/5.0"})
    
    response = Response(req.iter_content(chunk_size=1024), content_type=req.headers.get('Content-Type'))
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
