from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from django.urls import reverse
from django.views.generic import CreateView, DetailView, TemplateView

from estimateapp.forms import ImageCreationForm
from estimateapp.models import EstimateModel, Output
from estimateapp.process import Process


class CreateEstimateView(CreateView):
    model = EstimateModel
    form_class = ImageCreationForm
    template_name = 'estimateapp/create.html'
    # def gitrequestfiles(self, request):
    #     print(request.files)
    #     data = {
    #         "name":request.files
    #     }
    #     return JsonResponse(data)
    def get_success_url(self):
        obj = EstimateModel.objects.get(pk=self.object.pk)
        print(obj)
        out_11 = Output()
        input = str(obj.input_estimateimage)
        process_1 = Process(input)
        out_11.list_11 = process_1.df()
        out_11.list_22 = process_1.construction()
        out_11.list_33 = process_1.detail()
        out_11.save()
        # self.gitrequestfiles(self, request)
        return reverse('estimateapp:detail', kwargs={'pk': self.object.pk})

class OutputImageView(DetailView):
   # model = EstimateModel
   model = Output
   context_object_name = 'target_image'
   template_name = 'estimateapp/detail.html'

def testview(request):
    return render(request, 'estimateapp/test.html')