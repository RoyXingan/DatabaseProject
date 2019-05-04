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
            form.clean()
            print('Curriculum Name = ' + form['curriculum_name'].value())
            print('Admin Name = ' + form['admin_name'].value())
            print('Admin ID = ' + form['admin_id'].value())
            print('Min Credits = ' + form['min_credits'].value())
            print('Topic Coverage = ' + form['topic_coverage'].value())
            print('Goal Valid Credits = ' + form['goal_valid_credits'].value())
            if form['goal_valid'].value():
                print('Goat Valid = true')
            else:
                print('Goat Valid = true')
            print('FORM PASSED')
            pass
    else:
        form = forms.CurriculumForm()

    return render(request=request,
                  template_name="main/curriculum.html",
                  context={"curriculum_list": curriculum_list,
                           "form": form})
