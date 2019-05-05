from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import Curriculum, Course


# Create your views here.
def homepage(request):
    return render(request=request,
                  template_name="main/home.html")


def curriculum(request):
    curriculum_list = Curriculum.objects.order_by('curriculum_name')

    if request.method == 'POST':
        if 'create_curriculum' in request.POST:
            post = Curriculum()
            post.curriculum_name = request.POST.get('curriculumName')
            post.admin_name = request.POST.get('adminName')
            post.admin_id = request.POST.get('adminID')
            post.min_credits = request.POST.get('minCredit')
            post.topic_coverage = request.POST.get('topicCoverage')
            post.goal_valid_credits = request.POST.get('goalValidCredit')
            if request.POST.get('goalValid') == 'on':
                post.goal_valid = True
            else:
                post.goal_valid = False
            post.save()

        print('curriculum_name = ' + post.curriculum_name)
        print('admin_name = ' + post.admin_name)
        print('admin_id = ' + post.admin_id)
        print('min_credits = ' + post.min_credits)
        print('topic_coverage = ' + post.topic_coverage)
        print('goal_valid_credits = ' + post.goal_valid_credits)
        if post.goal_valid:
            print('goal_valid')
        else:
            print('not goal_valid')
        return HttpResponseRedirect('/')

    return render(request=request,
                  template_name="main/curriculum.html",
                  context={"curriculum_list": curriculum_list})


def course(request):
    course_list = Course.objects.order_by('course_name')

    if request.method == 'POST':
        if 'create_course' in request.POST:
            post = Course()
            post.course_name = request.POST.get('courseName')
            post.subject_code = request.POST.get('subjectCode')
            post.course_number = request.POST.get('courseNumber')
            post.credits = request.POST.get('credits')
            post.description = request.POST.get('description')
            post.save()

        print('Course Name = ' + post.course_name)
        print('Subject Code = ' + post.subject_code)
        print('Course Number = ' + post.course_number)
        print('Credits = ' + post.credits)
        print('Description = ' + post.description)
        return HttpResponseRedirect('/')

    return render(request=request,
                  template_name="main/course.html",
                  context={"course_list": course_list})
