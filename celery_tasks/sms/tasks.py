import logging

from celery_tasks.main import celery_app
from celery_tasks.yuntongxun.sms import CCP

SMS_CODE_TEMP_ID = 1

logger = logging.getLogger('django')


@celery_app.task(name="send_sms_code")
def send_sms_code(mobile, code, expires):
    try:
        cpp = CCP()
        res = cpp.send_template_sms(mobile, [code, expires], SMS_CODE_TEMP_ID)
    except Exception as e:
        logger.error("短信发送异常: %s" % mobile)
    else:
        if res == 0:
            logger.info("短信发送成功: %s" % mobile)
        else:
            logger.error("短信发送失败: %s" % mobile)
