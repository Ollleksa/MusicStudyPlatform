from django.shortcuts import render
from django.views import View


class RequestPage(View):
    template = 'model/request.html'

    def get(self, request, **kwargs):
        req = kwargs['request_id']
        context = {
            'request_id': req,
        }
        return render(request, self.template, context)


class RequestCatalog(View):
    template = 'model/all_requests.html'

    def get(self, request):
        return render(request, self.template)


class CreateRequest(View):
    template = 'model/create_request.html'

    def get(self, request):
        return render(request, self.template)

    def post(self, request):
        return render(request, self.template)
