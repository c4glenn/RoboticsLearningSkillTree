from django.apps import AppConfig


class SkillsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'skills'
    
    def ready(self):
        import skills.signals
        return super().ready()
