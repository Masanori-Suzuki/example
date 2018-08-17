import redis

from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView
from fluent import sender
from fluent import event
from .models import Friend

class HelloView(TemplateView):

    def __init__(self):
        self.parames = {}

    def get(self, request):
        # DBから値を取る
        data = Friend.objects.all()
        for item in data:
            if item.id == 1:
                item.name += 'M'
        friend = Friend.objects.get(id=1)
        print(vars(friend))

        # redisから値を取る
        pool = redis.ConnectionPool(host='localhost', port=6379, db=0)
        r = redis.StrictRedis(connection_pool=pool)
        bvalue = r.get('test')
        value = ''
        if bvalue is None:
            value = 'None'
        else:
            value = bvalue.decode()

        # fulentdにログ送信
        sender.setup('debug', host='localhost', port=24224)
        event.Event('follow', {
            'from': 'userA',
            'to': 'userB'
            })

        # templateに渡す値を作る
        params = {
                'title':'Hello/Index',
                'message':'all friend',
                'data':[friend],
                'value':value,
        }
        return render(request, 'hello/index.html', params)

    def post(self, request):
        return self.get(self, request)
