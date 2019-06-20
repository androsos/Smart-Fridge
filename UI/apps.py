from django.apps import AppConfig


class UiConfig(AppConfig):
    name = 'UI'

    def ready(self):
    	import UI.signals