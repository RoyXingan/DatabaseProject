from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import Curriculum, Course, Topic, TopicSet, CurriculumCourse, Section, GradeDistribution, Goal
from django.db.models import Count


# Create your views here.
def homepage(request):
    return render(request=request,
                  template_name="main/home.html")


def curriculum(request):
    curriculum_list = Curriculum.objects.order_by('curriculum_name')

    if request.method == 'POST':
        try:
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
        except Exception as error:
            return render(request=request,
                          template_name="main/curriculum.html",
                          context={"curriculum_list": curriculum_list,
                                   "error": error})

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
        try:
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
        except Exception as error:
            return render(request=request,
                          template_name="main/topic.html",
                          context={"topic_list": topic_list,
                                   "curriculum_list": curriculum_list,
                                   "error": error})

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
        try:
            if 'create_section' in request.POST:
                post = Section()
                if not request.POST.get('editSection') == 'addSection':
                    print("Editing...")
                    aSection = request.POST.get('editSection').split(",")
                    post.id = aSection[0]
                    print('Section ID = ' + post.id)
                else:
                    print("Creating new section...")

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

                post.section_id = request.POST.get('section_id')
                print('Section ID = ' + str(post.section_id))
                post.year = request.POST.get('year')
                print('Year = ' + str(post.year))
                post.semester = request.POST.get('semester')
                print('Semester = ' + post.semester)
                post.student_count = request.POST.get('student_count')
                print('Student Count = ' + str(post.student_count))
                post.comment1 = request.POST.get('comment1')
                print('Comment 1 = ' + post.comment1)
                post.comment2 = request.POST.get('comment2')
                print('Comment 2 = ' + post.comment2)

                if request.POST.get('grade_distribution_id') == 'null':
                    post.grade_distribution_id = None
                else:
                    grade_dist_found = False
                    for grade_dist in grade_distribution_list:
                        if grade_dist.grade_distribution_id == int(request.POST.get('grade_distribution_id')):
                            post.grade_distribution_id = grade_dist
                            grade_dist_found = True
                            if grade_dist.total_student != int(post.student_count):
                                raise ValueError
                            break
                    if not grade_dist_found:
                        return HttpResponseRedirect('/grade_distribution')
                    print('Grade Distribution ID = ' + str(post.grade_distribution_id.grade_distribution_id))
                post.save()
                print('FINISHED SAVING SECTION')
        except Exception as error:
            return render(request=request,
                          template_name="main/section.html",
                          context={"course_list": course_list,
                                   "section_list": section_list,
                                   "grade_distribution_list": grade_distribution_list,
                                   "error": error})
        # return HttpResponseRedirect('/')

    return render(request=request,
                  template_name="main/section.html",
                  context={"course_list": course_list,
                           "section_list": section_list,
                           "grade_distribution_list": grade_distribution_list})


def goal(request):
    curriculum_list = Curriculum.objects.order_by('curriculum_name')
    course_list = Course.objects.order_by('course_name')
    grade_distribution_list = GradeDistribution.objects.order_by('grade_distribution_id')
    goal_list = Goal.objects.order_by('goal_id')

    if request.method == 'POST':
        try:
            if 'create_goal' in request.POST:
                post = Goal()
                if not request.POST.get('editGoal') == 'addGoal':
                    print("Editing...")
                    aGoal = request.POST.get('editGoal').split(",")
                    post.goal_id = aGoal[0]
                    print('Curriculum Course ID = ' + post.goal_id)
                else:
                    print("Creating new goal...")

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

                post.description = request.POST.get('description')
                print('Description = ' + post.description)

                if request.POST.get('grade_distribution_id') == 'null':
                    post.grade_distribution_id = None
                else:
                    grade_dist_found = False
                    for grade_dist in grade_distribution_list:
                        if grade_dist.grade_distribution_id == int(request.POST.get('grade_distribution_id')):
                            post.grade_distribution_id = grade_dist
                            grade_dist_found = True
                            break
                    if not grade_dist_found:
                        return HttpResponseRedirect('/grade_distribution')
                    print('Grade Distribution ID = ' + str(post.grade_distribution_id.grade_distribution_id))
                post.save()
            # return HttpResponseRedirect('/')
        except Exception as error:
            return render(request=request,
                          template_name="main/goal.html",
                          context={"course_list": course_list,
                                   "curriculum_list": curriculum_list,
                                   "goal_list": goal_list,
                                   "grade_distribution_list": grade_distribution_list,
                                   "error": error})

    return render(request=request,
                  template_name="main/goal.html",
                  context={"course_list": course_list,
                           "curriculum_list": curriculum_list,
                           "grade_distribution_list": grade_distribution_list,
                           "goal_list": goal_list})


def grade_distribution(request):
    grade_distribution_list = GradeDistribution.objects.order_by('grade_distribution_id')

    if request.method == 'POST':
        try:
            if 'create_grade_distribution' in request.POST:
                post = GradeDistribution()
                if not request.POST.get('editGradeDistribution') == 'addGradeDistribution':
                    print("Editing...")
                    gd = request.POST.get('editGradeDistribution').split(":")
                    post.grade_distribution_id = int(gd[0])
                    print('Grade Distribution ID = ' + str(post.grade_distribution_id))
                else:
                    print("Creating new grade distribution...")

                total_student_temp = 0;
                post.A_plus = request.POST.get('A_plus')
                total_student_temp += int(post.A_plus)
                print('A+ = ' + str(post.A_plus))
                post.A = request.POST.get('A')
                total_student_temp += int(post.A)
                print('A = ' + str(post.A))
                post.A_minus = request.POST.get('A_minus')
                total_student_temp += int(post.A_minus)
                print('A- = ' + str(post.A_minus))

                post.B_plus = request.POST.get('B_plus')
                total_student_temp += int(post.B_plus)
                print('B+ = ' + str(post.B_plus))
                post.B = request.POST.get('B')
                total_student_temp += int(post.B)
                print('B = ' + str(post.B))
                post.B_minus = request.POST.get('B_minus')
                total_student_temp += int(post.B_minus)
                print('B- = ' + str(post.B_minus))

                post.C_plus = request.POST.get('C_plus')
                total_student_temp += int(post.C_plus)
                print('C+ = ' + str(post.C_plus))
                post.C = request.POST.get('C')
                total_student_temp += int(post.C)
                print('C = ' + str(post.C))
                post.C_minus = request.POST.get('C_minus')
                total_student_temp += int(post.C_minus)
                print('C- = ' + str(post.C_minus))

                post.D_plus = request.POST.get('D_plus')
                total_student_temp += int(post.D_plus)
                print('D+ = ' + str(post.D_plus))
                post.D = request.POST.get('D')
                total_student_temp += int(post.D)
                print('D = ' + str(post.D))
                post.D_minus = request.POST.get('D_minus')
                total_student_temp += int(post.D_minus)
                print('D- = ' + str(post.D_minus))

                post.Fail = request.POST.get('Fail')
                total_student_temp += int(post.Fail)
                print('F = ' + str(post.Fail))
                post.Withdraw = request.POST.get('Withdraw')
                total_student_temp += int(post.Withdraw)
                print('W = ' + str(post.Withdraw))
                post.Incomplete = request.POST.get('Incomplete')
                total_student_temp += int(post.Incomplete)
                print('I- = ' + str(post.Incomplete))

                post.total_student = total_student_temp
                print('Total Student = ' + str(post.total_student))
                post.save()
                print('FINISHED SAVING GRADE DISTRIBUTION')
        except Exception as error:
            return render(request=request,
                          template_name="main/grade_distribution.html",
                          context={"grade_distribution_list": grade_distribution_list,
                                   "error": error})
            # return HttpResponseRedirect('/')

    return render(request=request,
                  template_name="main/grade_distribution.html",
                  context={"grade_distribution_list": grade_distribution_list})


def query_one(request):
    curriculum_list = Curriculum.objects.order_by('curriculum_name')
    course_list = Course.objects.order_by('course_name')
    topic_list = Topic.objects.order_by('topic_id')
    result_list = Curriculum.objects.none()
    curriculum_course_list = CurriculumCourse.objects.order_by('id')

    if request.method == 'POST':
        try:
            if 'create_query_one' in request.POST:
                post = Curriculum()
                hasCurr = False
                for aCurriculum in curriculum_list:
                    if aCurriculum.curriculum_name == request.POST.get('curriculum_name'):
                        post.curriculum_name = aCurriculum
                        hasCurr = True
                        break
                if not hasCurr:
                    print('Error: Error finding Curriculum reference!')
                result_list = Curriculum.objects.filter(curriculum_name=str(post.curriculum_name.curriculum_name))

                # print('Query=>')
                # print(result_list.query)
                print('---')
                for rCurr in result_list:
                    print('curriculum_name->' + rCurr.curriculum_name)
                    print('admin_name->' + rCurr.admin_name)
                    print('admin_ID->' + str(rCurr.admin_id))
                    print('min_credits->' + str(rCurr.min_credits))
                    print('topic_coverage->' + rCurr.topic_coverage)
                    print('goal_valid_credits->' + str(rCurr.goal_valid_credits))
                    if rCurr.goal_valid:
                        print('goal_valid->TRUE')
                    else:
                        print('goal_valid->FALSE')

        except Exception as error:
            return render(request=request,
                          template_name="main/query_one.html",
                          context={"topic_list": topic_list,
                                   "course_list": course_list,
                                   "curriculum_list": curriculum_list,
                                   "curriculum_course_list": curriculum_course_list,
                                   "result_list": result_list,
                                   "error": error})

    return render(request=request,
                  template_name="main/query_one.html",
                  context={"topic_list": topic_list,
                           "course_list": course_list,
                           "result_list": result_list,
                           "curriculum_list": curriculum_list,
                           "curriculum_course_list": curriculum_course_list})


def query_two(request):
    curriculum_list = Curriculum.objects.order_by('curriculum_name')
    course_list = Course.objects.order_by('course_name')
    topic_list = Topic.objects.order_by('topic_id')
    result_list = Course.objects.none()
    curriculum_course_list = CurriculumCourse.objects.order_by('id')

    if request.method == 'POST':
        try:
            if 'create_query_two' in request.POST:
                post = Course()
                hasCour = False
                # course_name = request.POST.get('course_name')
                for aCourse in course_list:
                    if aCourse.course_name == request.POST.get('course_name'):
                        post.course_name = aCourse
                        hasCour = True
                        break
                if not hasCour:
                    print("Error: No course name matching '" + request.POST.get('course_name') + "' found!")
                    # return HttpResponseRedirect('/course')

                # print('Course Name = ' + post.course_name.course_name)
                result_list = Course.objects.filter(course_name=str(post.course_name.course_name))

                print('Query=>')
                print(result_list.query)
                print('---')
                for rCour in result_list:
                    print('course_name->' + rCour.course_name)
                    print('subject_code->' + rCour.subject_code)
                    print('course_number->' + str(rCour.course_number))
                    print('credits->' + str(rCour.credits))
                    print('description->' + rCour.description)

        except Exception as error:
            return render(request=request,
                          template_name="main/query_two.html",
                          context={"topic_list": topic_list,
                                   "course_list": course_list,
                                   "curriculum_list": curriculum_list,
                                   "curriculum_course_list": curriculum_course_list,
                                   "result_list": result_list,
                                   "error": error})
    return render(request=request,
                  template_name="main/query_two.html",
                  context={"topic_list": topic_list,
                           "course_list": course_list,
                           "result_list": result_list,
                           "curriculum_list": curriculum_list,
                           "curriculum_course_list": curriculum_course_list})


def query_three(request):
    curriculum_list = Curriculum.objects.order_by('curriculum_name')
    course_list = Course.objects.order_by('course_name')
    topic_list = Topic.objects.order_by('topic_id')
    result_list = Goal.objects.none()
    curriculum_course_list = CurriculumCourse.objects.order_by('id')
    section_list = Section.objects.order_by('section_id')
    goal_list = Goal.objects.order_by('goal_id')
    grade_distribution_list = GradeDistribution.objects.order_by('grade_distribution_id')

    if request.method == 'POST':
        try:
            if 'create_query_three' in request.POST:
                post = Goal()
                hasCour = False
                # course_name = request.POST.get('course_name')
                for aCourse in course_list:
                    if aCourse.course_name == request.POST.get('course_name'):
                        post.course_name = aCourse
                        hasCour = True
                        break
                if not hasCour:
                    print("Error: No course name matching '" + request.POST.get('course_name') + "' found!")
                    # return HttpResponseRedirect('/course')

                print('Course Name = ' + post.course_name.course_name)
                hasCurr = False
                for aCurriculum in curriculum_list:
                    if aCurriculum.curriculum_name == request.POST.get('curriculum_name'):
                        post.curriculum_name = aCurriculum
                        hasCurr = True
                        break
                if not hasCurr:
                    print('Error: Error finding Curriculum reference!')
                print('Curriculum Name = ' + post.curriculum_name.curriculum_name)
                result_list = Goal.objects.filter(course_name=str(post.course_name.course_name),
                                                  curriculum_name=str(post.curriculum_name.curriculum_name))
                # # get rid of duplicate years
                # result_list.annotate(year_count=Count('year')).exclude(year_count=1)

                hasYear = False
                tYear = 0
                for section in section_list:
                    if str(section.year) == request.POST.get('year'):
                        tYear = section.year
                        # result_list = result_list.filter(semester=tYear)
                        hasYear = True
                        break
                if not hasYear:
                    print('Error: Error finding Section reference!')
                print('Year = ' + str(tYear))

                if request.POST.get('fall_semester') == 'on':
                    # result_list = result_list.filter(semester='FA')
                    print('FILTERED FALL')

                if request.POST.get('spring_semester') == 'on':
                    # result_list = result_list.filter(semester=str('SP'))
                    print('FILTERED SPRING')

                if request.POST.get('summer_semester') == 'on':
                    # result_list = result_list.filter(semester=str('SM'))
                    print('FILTERED SUMMER')

                if request.POST.get('winter_semester') == 'on':
                    # result_list = result_list.filter(semester=str('WT'))
                    print('FILTERED WINTER')

                # print('Query=>')
                # print(result_list.query)
                print('---')
                for rGoal in result_list:
                    print('curriculum_name->' + rGoal.curriculum_name.curriculum_name)
                    print('course_name->' + rGoal.course_name.course_name)
                    print('goal_id->' + str(rGoal.goal_id))
                    print('description->' + rGoal.description)
                    print('grade_distribution_id->' + str(rGoal.grade_distribution_id.grade_distribution_id))

        except Exception as error:
            return render(request=request,
                          template_name="main/query_three.html",
                          context={"topic_list": topic_list,
                                   "course_list": course_list,
                                   "curriculum_list": curriculum_list,
                                   "curriculum_course_list": curriculum_course_list,
                                   "result_list": result_list,
                                   "section_list": section_list,
                                   "goal_list": goal_list,
                                   "grade_distribution_list": grade_distribution_list,
                                   "error": error})
    return render(request=request,
                  template_name="main/query_three.html",
                  context={"topic_list": topic_list,
                           "course_list": course_list,
                           "result_list": result_list,
                           "curriculum_list": curriculum_list,
                           "section_list": section_list,
                           "goal_list": goal_list,
                           "curriculum_course_list": curriculum_course_list,
                           "grade_distribution_list": grade_distribution_list})