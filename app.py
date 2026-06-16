from flask import Flask, render_template_string

app = Flask(__name__)

# رابط بث عالمي سريع جدا ونشط ومستقر دائم للتجربة والتأكد من السرعة
STREAM_URL = "https://unified-streaming.com"

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ar">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Live Stream</title>
    <script src="https://jsdelivr.net"></script>
    <style>
        html, body { background-color: #000000; margin: 0; padding: 0; width: 100%; height: 100%; display: flex; justify-content: center; align-items: center; overflow: hidden; }
        .video-container { width: 100%; max-width: 100%; height: 100%; display: flex; justify-content: center; align-items: center; }
        video { width: 100%; height: auto; max-height: 100vh; aspect-ratio: 16 / 9; background: #000000; }
    </style>
</head>
<body>
    <div class="video-container">
        <video id="video" controls autoplay playsinline preload="auto"></video>
    </div>
    <script>
        var video = document.getElementById("video");
        var videoSrc = "{{ stream_url }}";
        if (Hls.isSupported()) {
            var hls = new Hls({
                maxBufferLength: 10,
                maxMaxBufferLength: 20,
                enableWorker: true
            });
            hls.loadSource(videoSrc);
            hls.attachMedia(video);
            hls.on(Hls.Events.MANIFEST_PARSED, function() { video.play(); });
        } else if (video.canPlayType("application/vnd.apple.mpegurl")) {
            video.src = videoSrc;
            video.addEventListener("loadedmetadata", function() { video.play(); });
        }
    </script>
</body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(HTML_TEMPLATE, stream_url=STREAM_URL)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=7860)
