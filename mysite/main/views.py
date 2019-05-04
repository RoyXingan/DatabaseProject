from django.shortcuts import render
from django.http import HttpResponse
from .models import Curriculum
from . import forms


# Create your views here.
def homepage(request):
    return render(request=request,
                  template_name="main/home.html",
                  context={"models": Curriculum.objects.all})


def curriculum(request):
    curriculum_list = Curriculum.objects.order_by('curriculum_name')
    if request.method == 'POST':
        form = forms.CurriculumForm(request.POST)
        if form.is_valid():
            print('valid form')
    else:
        form = forms.CurriculumForm()

    return render(request=request,
                  template_name="main/curriculum.html",
                  context={"curriculum_list": curriculum_list,
                           "form": form})
