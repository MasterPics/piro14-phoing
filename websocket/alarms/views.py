from django.views.generic import TemplateView
from . import models
import json
from django.shortcuts import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404


class Alarm(TemplateView):
    template_name = "templates/alarms/alarm.html"

    def get_context_data(self, **kwargs):
        context = super(TemplateView, self).get_context_data()
        context['username'] = self.request.user.username

        return context

class ShareMe(TemplateView):
    template_name = "templates/alarms/ShareMe.html"

    def get_context_data(self, **kwargs):
        context=super(TemplateView, self).get_context_data()
        context['username']=self.request.user.username

        return context

    def post(self, request, **kwargs):
        ins=models.Alarm()
        data_unicode=request.body.decode('utf-8')
        data=json.loads(data_unicode)
        ins.message=data['message']
        ins.save()

        return HttpResponse('')

def massage_list(request):
    alarms=Alarm.objects.all().order_by('created_at') #[:5]
    request_user=request.user

    ctx={'alarms':alarms,
    'request_user':request_user}

    return render(request, 'alarms/alarm.html', context=ctx)

