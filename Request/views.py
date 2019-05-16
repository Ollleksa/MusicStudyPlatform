from django.shortcuts import render
from django.views import View
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator

from .models import Request
from .forms import NewRequest


class RequestPage(View):
    template = 'model/request.html'

    def get(self, request, **kwargs):
        req = Request.objects.get(pk = kwargs['request_id'])
        context = {
            'request': req,
        }
        return render(request, self.template, context)


class RequestCatalog(View):
    template = 'model/all_requests.html'

    def get(self, request):
        all_requests = Request.objects.all().order_by('id')
        paginator = Paginator(all_requests, 20)
        page = request.GET.get('page')
        current_page = paginator.get_page(page)

        context = {
            'requests': current_page,
        }
        return render(request, self.template, context)


class CreateRequest(View):
    template = 'model/create_request.html'

    def get(self, request):
        form = NewRequest()
        context = {
            'form': form,
        }
        return render(request, self.template, context)

    def post(self, request):
        form = NewRequest(request.POST)
        if form.is_valid():
            new_request = Request(requester=request.user, agent=form.cleaned_data['agent'],
                                  title=form.cleaned_data['title'], content=form.cleaned_data['content'])
            new_request.save()
            return HttpResponseRedirect('{}'.format(new_request.pk))
        else:
            form = NewRequest()

        context = {
            'form': form,
        }
        return render(request, self.template, context)
