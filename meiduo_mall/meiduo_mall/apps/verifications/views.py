# Create your views here.
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django_redis import get_redis_connection
from meiduo_mall.apps.verifications import contants
import random
import logging

logger = logging.getLogger('django')


class SMSCodeView(APIView):
    def get(self, request, mobile):
        redis_conn = get_redis_connection('verify')
        send_flag = redis_conn.get('send_flag_%s' % mobile)
        if send_flag:
            return Response({"message": "q请求过于频繁"}, status=status.HTTP_400_BAD_REQUEST)
        sms_code = "%06d" % random.randint(0, 999999)
        pl = redis_conn.pipeline()
        pl.setex('sms_%s' % mobile, contants.SMS_CODES_REDIS_EXPIRES, sms_code)
        pl.setex('send_flag_%s' % mobile, contants.SEND_SMS_INTERVAL, 1)
        pl.execute()
        sms_code_expries = contants.SMS_CODES_REDIS_EXPIRES // 60
        from celery_tasks.sms.tasks import send_sms_code
        send_sms_code.delay(mobile, sms_code, sms_code_expries)
        return Response({"message": "OK"})
