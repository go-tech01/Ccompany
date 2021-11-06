from django.shortcuts import render

# Create your views here.
from django.urls import reverse
from django.views.generic import CreateView, DetailView, TemplateView

from estimateapp.forms import ImageCreationForm
from estimateapp.models import EstimateModel, Output


class CreateEstimateView(CreateView):
    model = EstimateModel
    form_class = ImageCreationForm
    template_name = 'estimateapp/create.html'
    def get_success_url(self):
        # print(self.object.id)
        obj = EstimateModel.objects.get(pk=self.object.pk)
        out_11 = Output()
        out_11.list_11 = obj.df()
        out_11.list_22 = obj.construction()
        out_11.list_33 = obj.detail()
        out_11.save()
        return reverse('estimateapp:detail', kwargs={'pk': self.object.pk})

class OutputImageView(DetailView):
   # model = EstimateModel
   model = Output
   context_object_name = 'target_image'
   template_name = 'estimateapp/detail.html'

def testview(request):
    return render(request, 'estimateapp/test.html')