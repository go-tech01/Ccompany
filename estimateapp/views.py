from django.http import JsonResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse
from django.views.generic import CreateView, DetailView, TemplateView

from estimateapp.forms import ImageCreationForm
from estimateapp.models import EstimateModel, Output
from estimateapp.process import Process

# def CreateEstimateView(request):
#     견적서폼 = ImageCreationForm()
#     if request.method == "POST":
#         out_11 = Output()
#         견적서폼_post = ImageCreationForm(request.POST, request.FILES)
#         if 견적서폼_post.is_valid():
#             input_1 = request.FILES['input_estimateimage']
#             print(request.POST)
#             process_1 = Process(input_1)
#             out_11.list_11 = process_1.df()
#             out_11.list_22 = process_1.construction()
#             out_11.list_33 = process_1.detail()
#             out_11.save()
#             pk = out_11.id
#             return redirect("/estimate/output/"+str(pk))
#     context = {
#         "form": 견적서폼
#     }
#     return render(request, "estimateapp/create.html", context)
from estimateapp.table_cut import TableCut


class CreateEstimateView(CreateView):
    model = EstimateModel
    form_class = ImageCreationForm
    template_name = 'estimateapp/create.html'

    def get_success_url(self):
        obj = EstimateModel.objects.get(pk=self.object.pk)
        outputs = Output()
        input_image = str(obj.input_estimateimage)
        input_area = int(obj.area)
        processing = Process(input_image, input_area)
        # cut_img_save = TableCut(input_image)
        # processing = Process(input_area)
        # print(cut_img_save)
        # processing = Process(input_image, input_area)

        # try:
        outputs.list_11 = processing.df()
        outputs.list_22 = processing.construction()
        outputs.list_33 = processing.detail()
        outputs.save()
        # except:
        #     obj.delete()
        # self.gitrequestfiles(self, request)
        return reverse('estimateapp:detail', kwargs={'pk': self.object.pk})

class OutputImageView(DetailView):
   # model = EstimateModel
   model = Output
   context_object_name = 'target_image'
   template_name = 'estimateapp/detail.html'

def testview(request):
    return render(request, 'estimateapp/test.html')