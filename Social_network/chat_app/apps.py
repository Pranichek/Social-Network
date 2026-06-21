from django.apps import AppConfig
import threading
import os

class ChatAppConfig(AppConfig):
    name = 'chat_app'

    def ready(self):
        # Запускаємо тільки в основному процесі, не в autoreloader
        if os.environ.get('RUN_MAIN') != 'true':
            return
            
        from .socket_client import start_socket_client
        t = threading.Thread(target=start_socket_client, daemon=True)
        t.start()