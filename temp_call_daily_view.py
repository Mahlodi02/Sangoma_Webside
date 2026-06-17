import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','config.settings')
import django
django.setup()
from django.test import RequestFactory
from django.contrib.auth import get_user_model
from core.views import daily_message_detail
from core.models import DailyMessage

User = get_user_model()
msg = DailyMessage.objects.first()
user = User.objects.first()
if not (msg and user):
    raise SystemExit('missing msg or user for test')

rf = RequestFactory()
request = rf.get(f'/messages/{msg.pk}/')
request.user = user
try:
    response = daily_message_detail(request, pk=msg.pk)
    print('view returned', type(response), getattr(response,'status_code', None))
except Exception:
    import traceback
    traceback.print_exc()
