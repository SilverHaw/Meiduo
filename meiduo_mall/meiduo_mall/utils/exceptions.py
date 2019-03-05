import logging

from rest_framework.views import exception_handler as drf_exception_handler
from rest_framework.response import Response
from rest_framework import status
from django.db import DatabaseError
from redis.exceptions import RedisError

logger = logging.getLogger('diango')


def exception_handler(exc, context):
    """
    自定义异常处理
    :param exc:异常 
    :param context: 抛出异常的上下文 
    :return: Reaponse响应对象
    """
    response = drf_exception_handler(exc, context)
    if not response:
        view = context['view']
        if isinstance(exc, DatabaseError) or isinstance(exc, RedisError):
            logger.error('[%s] %s' % (view, type(exc)))
            response = Response({'message': '服务器内部错误'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return response
