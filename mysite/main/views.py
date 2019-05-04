from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
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
            tempC = Curriculum()
            tempC.curriculum_name = form['curriculum_name'].value()
            tempC.admin_name = form['admin_name'].value()
            tempC.admin_id = form['admin_id'].value()
            tempC.min_credits  = form['min_credits'].value()
            tempC.topic_coverage = form['topic_coverage'].value()
            tempC.goal_valid_credits = form['goal_valid_credits'].value()
            tempC.goal_valid = form['goal_valid'].value()

            print('Curriculum Name = ' + tempC.curriculum_name)
            print('Admin Name = ' + tempC.admin_name)
            print('Admin ID = ' + tempC.admin_id)
            print('Min Credits = ' + tempC.min_credits)
            print('Topic Coverage = ' + tempC.topic_coverage)
            print('Goal Valid Credits = ' + tempC.goal_valid_credits)

            if tempC.goal_valid:
                print('Goat Valid = true')
            else:
                print('Goat Valid = true')
            print('FORM VALUES READ IN')

            tempC.save()

            return HttpResponseRedirect('/')
    else:
        form = forms.CurriculumForm()

    return render(request=request,
                  template_name="main/curriculum.html",
                  context={"curriculum_list": curriculum_list,
                           "form": form})
