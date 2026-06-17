import os
from pathlib import Path

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
import django

django.setup()
from django.test import Client
from django.contrib.auth import get_user_model
from core.models import DailyMessage

User = get_user_model()
msg = DailyMessage.objects.first()
if not msg:
    raise SystemExit('no DailyMessage records')
user = User.objects.first()
if not user:
    raise SystemExit('no users')

print('msg', msg.pk, msg)
print('user', user.pk, user)
client = Client()
client.force_login(user)

try:
    response = client.get(f'/messages/{msg.pk}/')
    print('status', response.status_code)
    print('content_snippet', response.content[:2000].decode('utf-8', 'ignore'))
except Exception as exc:
    import traceback
    traceback.print_exc()
