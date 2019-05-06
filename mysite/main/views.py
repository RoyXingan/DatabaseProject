from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import Curriculum, Course, Topic, TopicSet


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
            print('curriculum_name = ' + post.curriculum_name)
            post.admin_name = request.POST.get('adminName')
            print('admin_name = ' + post.admin_name)
            post.admin_id = request.POST.get('adminID')
            print('admin_id = ' + post.admin_id)
            post.min_credits = request.POST.get('minCredit')
            print('min_credits = ' + post.min_credits)
            post.topic_coverage = request.POST.get('topicCoverage')
            print('topic_coverage = ' + post.topic_coverage)
            post.goal_valid_credits = request.POST.get('goalValidCredit')
            print('goal_valid_credits = ' + post.goal_valid_credits)
            if request.POST.get('goalValid') == 'on':
                post.goal_valid = True
                print('This curriculum is goal valid')
            else:
                post.goal_valid = False
                print('This curriculum is NOT goal valid')
            post.save()
        # return HttpResponseRedirect('/')

    return render(request=request,
                  template_name="main/curriculum.html",
                  context={"curriculum_list": curriculum_list})


def course(request):
    course_list = Course.objects.order_by('course_name')

    if request.method == 'POST':
        try:
            if 'create_course' in request.POST:
                post = Course()
                post.course_name = request.POST.get('courseName')
                print('Course Name = ' + post.course_name)
                post.subject_code = request.POST.get('subjectCode')
                print('Subject Code = ' + post.subject_code)
                post.course_number = request.POST.get('courseNumber')
                print('Course Number = ' + post.course_number)
                post.credits = request.POST.get('credits')
                print('Credits = ' + post.credits)
                post.description = request.POST.get('description')
                print('Description = ' + post.description)
                post.save()
        except Exception as error:
            return render(request=request,
                          template_name="main/course.html",
                          context={"course_list": course_list,
                                   "error": error})

        # return HttpResponseRedirect('/')

    return render(request=request,
                  template_name="main/course.html",
                  context={"course_list": course_list})


def topic(request):
    curriculum_list = Curriculum.objects.order_by('curriculum_name')
    topic_list = Topic.objects.order_by('topic_id')

    if request.method == 'POST':
        if 'create_topic' in request.POST:
            post = Topic()
            if not request.POST.get('editTopic') == -1:
                topics = request.POST.get('editTopic').split(",")
                post.topic_id = topics[0]
                print('Topic ID = ' + post.topic_id)
            hasCurr = False
            for aCurriculum in curriculum_list:
                if aCurriculum.curriculum_name == request.POST.get('curriculumName'):
                    post.curriculum_name = aCurriculum
                    hasCurr = True
                    break
            if not hasCurr:
                return HttpResponseRedirect('/curriculum')
            print('Curriculum Name = ' + post.curriculum_name.curriculum_name)
            post.topic_name = request.POST.get('topicName')
            print('Topic Name = ' + post.topic_name)
            post.level = request.POST.get('level')
            print('Level = ' + post.level)
            post.subject_area = request.POST.get('subjectArea')
            print('Subject Area = ' + post.subject_area)
            post.units = request.POST.get('units')
            print('Units = ' + post.units)
            post.save()

    return render(request=request,
                  template_name="main/topic.html",
                  context={"topic_list": topic_list,
                           "curriculum_list": curriculum_list})


def topic_set(request):
    course_list = Course.objects.order_by('course_name')
    topic_list = Topic.objects.order_by('topic_id')
    topic_set_list = TopicSet.objects.order_by('topic_set_id')

    if request.method == 'POST':
        if 'create_topic_set' in request.POST:
            post = TopicSet()
            if not request.POST.get('editTopicSet') == -1:
                topic_sets = request.POST.get('editTopicSet').split(",")
                post.topic_set_id = topic_sets[0]
                print('Topic set ID = ' + post.topic_set_id)

            course_name = request.POST.get('topicSetCourse').split(",")
            post.assign_course_name = course_name[1]
            print('Topic Course = ' + post.assign_course_name)
            topic = request.POST.get('topicSetTopic').split(",")
            post.topic_id = topic[0]
            print('Topic ID = ' + post.topic_id)
            post.curriculum_name = topic[1]
            print('Curriculum Name = ' + post.curriculum_name)

    return render(request=request,
                  template_name="main/topic_set.html",
                  context={"topic_list": topic_list,
                           "course_list": course_list,
                           "topic_set_list": topic_set_list})
