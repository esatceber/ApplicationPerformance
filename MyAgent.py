import time
from flask import request
import logging

metrics = []

class MyAgent:
    def __init__(self, app=None):
        # Logger'ı yapılandır
        logging.basicConfig(filename='metric.log', level=logging.INFO, format='%(asctime)s - %(message)s')
        self.logger = logging.getLogger()
        self.app = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        app.before_request(self.before_request)
        app.after_request(self.after_request)

    def before_request(self):
        # İstek başladığında zaman damgasını kaydet
        request.start_time = time.time()

    def after_request(self, response):
        if not hasattr(request, 'start_time'):
            return response
        # İstek bittiğinde geçen süreyi hesapla ve logla
        duration = time.time() - request.start_time
        self.log_request(request, response, duration)
        return response

    def log_request(self, request, response, duration):
        # Log mesajını dosyaya yaz
        self.logger.info(f"Request: {request.method} {request.url}, Status: {response.status_code}, Duration: {duration:.2f} sec")

    def log_request(self, request, response, duration):
        self.metrics.append({'path': request.path,'method': request.method,'status_code': response.status_code,'duration': duration})
   
        