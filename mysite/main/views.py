from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import Curriculum, Course, Topic, TopicSet, CurriculumCourse, Section, GradeDistribution


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
            if not request.POST.get('editTopic') == 'addTopic':
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
        try:
            if 'create_topic_set' in request.POST:
                post = TopicSet()
                if not request.POST.get('editTopicSet') == 'addTopicSet':
                    print("Editing...")
                    topic_sets = request.POST.get('editTopicSet').split(",")
                    post.topic_set_id = topic_sets[0]
                    print('Topic set ID = ' + post.topic_set_id)
                else:
                    print("Creating new topic set...")

                post.topic_set_id = request.POST.get('topicSetID')
                print('Topic Set ID = ' + post.topic_set_id)

                course_name = request.POST.get('topicSetCourse').split(",\xa0")
                for courses in course_list:
                    if courses.course_name == course_name[1]:
                        post.assign_course_name = courses
                print('Topic Course = ' + post.assign_course_name.course_name)

                aTopic = request.POST.get('topicSetTopic').split(",")
                for topics in topic_list:
                    if topics.topic_id == int(aTopic[0]):
                        post.topic_id = topics
                print('Topic ID = ' + str(post.topic_id.topic_id))
                post.save()
        except Exception as error:
            return render(request=request,
                          template_name="main/topic_set.html",
                          context={"topic_list": topic_list,
                                   "course_list": course_list,
                                   "topic_set_list": topic_set_list,
                                   "error": error})

    return render(request=request,
                  template_name="main/topic_set.html",
                  context={"topic_list": topic_list,
                           "course_list": course_list,
                           "topic_set_list": topic_set_list})


def curriculum_course(request):
    curriculum_list = Curriculum.objects.order_by('curriculum_name')
    course_list = Course.objects.order_by('course_name')
    curriculum_course_list = CurriculumCourse.objects.order_by('id')

    if request.method == 'POST':
        try:
            if 'create_curriculum_course' in request.POST:
                post = CurriculumCourse()
                if not request.POST.get('editCurriculumCourse') == 'addCurriculumCourse':
                    print("Editing...")
                    tCourse = request.POST.get('editCurriculumCourse').split(",")
                    post.id = tCourse[0]
                    print('Curriculum Course ID = ' + post.id)
                else:
                    print("Creating new curriculum course...")
                hasCurr = False
                for aCurriculum in curriculum_list:
                    if aCurriculum.curriculum_name == request.POST.get('curriculum_name'):
                        post.curriculum_name = aCurriculum
                        hasCurr = True
                        break
                if not hasCurr:
                    print("Error: No matching curriculum found!")
                    return HttpResponseRedirect('/curriculum')
                print('Curriculum Name = ' + post.curriculum_name.curriculum_name)

                hasCour = False
                course_name = request.POST.get('course_name').split(",\xa0")
                for aCourse in course_list:
                    if aCourse.course_name == course_name[1]:
                        post.course_name = aCourse
                        hasCour = True
                        break
                if not hasCour:
                    print("Error: No course name matching '" + request.POST.get('course_name') + "' found!")
                    return HttpResponseRedirect('/course')
                print('Course Name = ' + post.course_name.course_name)

                if request.POST.get('required') == 'on':
                    post.required = True
                    print('This curriculum course is required!')
                else:
                    post.required = False
                    print('This curriculum course is NOT required!')
                post.topic_set_id = request.POST.get('topic_set_id')
                print('Topic set ID = ' + post.topic_set_id)
                post.units_of_topic = request.POST.get('units_of_topic')
                print('Units of Topic = ' + post.units_of_topic)
                post.save()
            # return HttpResponseRedirect('/')
        except Exception as error:
            return render(request=request,
                          template_name="main/curriculum_course.html",
                          context={"course_list": course_list,
                                   "curriculum_list": curriculum_list,
                                   "curriculum_course_list": curriculum_course_list,
                                   "error": error})

    return render(request=request,
                  template_name="main/curriculum_course.html",
                  context={"course_list": course_list,
                           "curriculum_list": curriculum_list,
                           "curriculum_course_list": curriculum_course_list})


def section(request):
    course_list = Course.objects.order_by('course_name')
    section_list = Section.objects.order_by('section_id')
    grade_distribution_list = GradeDistribution.objects.order_by('grade_distribution_id')

    if request.method == 'POST':
        # try:
        if 'create_section' in request.POST:
            post = Section()
            sameIDFound = False
            for sect in section_list:
                if sect.section_id == request.POST.get('section_id'):
                    sameIDFound = True
                    break
            if not sameIDFound:
                post.section_id = request.POST.get('section_id')
                print('Section ID = ' + str(post.section_id))
            else:
                print('Error: Section ID already being used!')

            hasCour = False
            for aCourse in course_list:
                tCourse = request.POST.get('course_name').split(",")
                if aCourse.course_name == tCourse[0]:
                    post.course_name = aCourse
                    hasCour = True
                    break
            if not hasCour:
                print("Error: No course name matching '" + request.POST.get('course_name') + "' found!")
                return HttpResponseRedirect('/course')
            print('Course Name = ' + post.course_name.course_name)

            post.semester = request.POST.get('semester')
            print('Semester = ' + post.semester)
            post.student_count = request.POST.get('student_count')
            print('Student Count = ' + str(post.student_count))
            post.comment1 = request.POST.get('comment1')
            print('Comment 1 = ' + post.comment1)
            post.comment2 = request.POST.get('comment2')
            print('Comment 2 = ' + post.comment2)
            # post.grade_distribution_id = request.POST.get('grade_distribution_id')
            # aGD = GradeDistribution()
            # aGD.grade_distribution_id = request.POST.get('grade_distribution_id')
            # aGD.A_plus = 97
            # aGD.A = 95
            # aGD.A_minus = 90
            # aGD.B_plus = 87
            # aGD.B = 85
            # aGD.B_minus = 80
            # aGD.C_plus = 77
            # aGD.C = 75
            # aGD.C_minus = 70
            # aGD.D_plus = 67
            # aGD.D = 65
            # aGD.D_minus = 60
            # aGD.Fail = 59
            # aGD.Withdraw = 50
            # aGD.Incomplete = 0
            # post.grade_distribution_id = aGD
            sameIDFound = False
            for aGD in grade_distribution_list:
                if str(aGD.grade_distribution_id) == str(request.POST.get('grade_distribution_id')):
                    post.grade_distribution_id = aGD
                    sameIDFound = True
                    break
            if not sameIDFound:
                print('Error: No Grade Distribution ID match found!')

            print('Grade Distribution ID = ' + str(post.grade_distribution_id.grade_distribution_id))
            post.save()
            print('FINISHED SAVING SECTION')
        # except Exception as error:
        #     return render(request=request,
        #                   template_name="main/section.html",
        #                   context={"course_list": course_list,
        #                            "section_list": section_list,
        #                            "error": error})

        # return HttpResponseRedirect('/')

    return render(request=request,
                  template_name="main/section.html",
                  context={"course_list": course_list,
                           "section_list": section_list,
                           "grade_distribution_list": grade_distribution_list})