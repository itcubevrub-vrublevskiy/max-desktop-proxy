from flask import Flask, Response, request
import requests

app = Flask(__name__)

@app.route('/<path:path>', methods=['GET'])
@app.route('/', defaults={'path': ''}, methods=['GET'])
def proxy(path):
    base_url = "https://web.max.ru"
    url = f"{base_url.rstrip('/')}/{path}" if path else base_url

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
    }

    try:
        # Отключаем автоматические редиректы!
        resp = requests.get(
            url,
            headers=headers,
            params=request.args,
            stream=True,
            timeout=10,
            allow_redirects=False
        )

        # Если сервер всё же пытается перенаправить — игнорируем Location
        if 300 <= resp.status_code < 400:
            # Повторяем запрос с тем же URL, но разрешаем редиректы
            resp = requests.get(
                url,
                headers=headers,
                params=request.args,
                stream=True,
                timeout=10,
                allow_redirects=True
            )

        return Response(
            resp.iter_content(chunk_size=1024),
            status=resp.status_code,
            content_type=resp.headers.get('content-type'),
            headers={
                'X-Proxy-Mode': 'desktop',
                'Cache-Control': 'no-cache'
            }
        )
    except Exception as e:
        return f"Proxy error: {str(e)}", 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
