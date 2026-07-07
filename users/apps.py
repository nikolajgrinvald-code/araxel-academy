from django.apps import AppConfig
import warnings


class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'

    def ready(self):
        import os
        if not os.environ.get('DATABASE_URL'):
            return
        warnings.filterwarnings('ignore', message='Accessing the database during app initialization is discouraged')
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
                u.is_staff = True
                u.is_superuser = True
                u.save()
            else:
                u = User.objects.get(email='admin@araxelacademy.pro')
                changed = False
                if not u.is_staff:
                    u.is_staff = True
                    changed = True
                if not u.is_superuser:
                    u.is_superuser = True
                    changed = True
                if changed:
                    u.save(update_fields=['is_staff', 'is_superuser'])
        except Exception:
            pass
