from django.apps import AppConfig


class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'

    def ready(self):
        import os
        if not os.environ.get('DATABASE_URL'):
            return
        try:
            from .models import User
            if not User.objects.filter(email='admin@araxelacademy.pro').exists():
                u = User(
                    email='admin@araxelacademy.pro',
                    name='Admin',
                    role='admin',
                    status='active',
                )
                u.set_password('admin123')
                u.save()
        except Exception:
            pass
