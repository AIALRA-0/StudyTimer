from flask_app import app  # 从 flask_app 文件导入 app
import webbrowser
from threading import Timer
import sys


def open_browser():
    webbrowser.open_new(f'http://127.0.0.1:{port}/')


if __name__ == '__main__':
    sys.stdout = open('stdout.log', 'w')
    sys.stderr = open('stderr.log', 'w')
    port = 5000
    # 使用 threading.Timer 在服务器启动后延迟打开浏览器
    Timer(1, open_browser).start()
    app.run(debug=False, port=port)
