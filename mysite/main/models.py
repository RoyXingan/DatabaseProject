from django.db import models


# curriculum model
class Curriculum(models.Model):
    Extensive = 'Extensive'
    Inclusive = 'Inclusive'
    BasicPlus = 'BasicPlus'
    Basic = 'Basic'
    Unsatisfactory = 'Unsatisfactory'
    Substandard = 'Substandard'
    TOPIC_COVERAGE = (
        (Extensive, 'Extensive'),
        (Inclusive, 'Inclusive'),
        (BasicPlus, 'BasicPlus'),
        (Basic, 'Basic'),
        (Unsatisfactory, 'Unsatisfactory'),
        (Substandard, 'Substandard'),
    )
    curriculum_name = models.CharField(max_length=50, primary_key=True)
    admin_name = models.CharField(max_length=100)
    admin_id = models.PositiveIntegerField(default=0)
    min_credits = models.PositiveSmallIntegerField(default=0)
    topic_coverage = models.CharField(
        max_length=15,
        choices=TOPIC_COVERAGE,
        default=Basic,
    )
    goal_valid_credits = models.PositiveSmallIntegerField(default=0)
    goal_valid = models.BooleanField(default=False)

    class Meta:
        db_table = 'curriculum'

    def __str__(self):
        return self.curriculum_name


# Course model
class Course(models.Model):
    course_name = models.CharField(max_length=50, primary_key=True)
    subject_code = models.CharField(max_length=4)
    course_number = models.PositiveIntegerField(default=0)
    credits = models.PositiveSmallIntegerField(default=0)
    description = models.TextField(blank=True)

    class Meta:
        db_table = 'course'
        constraints = [
            models.UniqueConstraint(fields=['subject_code', 'course_number'], name='unique_course')
        ]

    def __str__(self):
        return str(self.subject_code) + str(self.course_number) + ' ' + str(self.course_name)


# Topic model
class Topic(models.Model):
    LEVELS = (
        (1, 'Level 1'),
        (2, 'Level 2'),
        (3, 'Level 3'),
    )
    topic_id = models.AutoField(primary_key=True)
    topic_name = models.CharField(max_length=50)
    curriculum_name = models.ForeignKey(Curriculum, on_delete=models.CASCADE)
    level = models.PositiveSmallIntegerField(choices=LEVELS)
    subject_area = models.CharField(max_length=50)
    units = models.DecimalField(max_digits=10, decimal_places=1)

    class Meta:
        db_table = 'topic'
        constraints = [
            models.UniqueConstraint(fields=['topic_id', 'curriculum_name'], name='unique_topic')
        ]

    def __str__(self):
        return 'Topic ' + str(self.topic_name) + ' related to ' + str(self.curriculum_name)


# TopicSet model
class TopicSet(models.Model):
    topic_set_id = models.IntegerField(default=0)
    assign_course_name = models.ForeignKey(Course, on_delete=models.CASCADE)
    topic_id = models.ForeignKey(Topic, on_delete=models.CASCADE)

    class Meta:
        db_table = 'topic_set'
        constraints = [
            models.UniqueConstraint(fields=['topic_set_id', 'assign_course_name', 'topic_id'],
                                    name='unique_topic_set')
        ]

    def __str__(self):
        return 'Topic set ' + str(self.topic_set_id)


# CurriculumCourse model
class CurriculumCourse(models.Model):
    curriculum_name = models.ForeignKey(Curriculum, on_delete=models.CASCADE)
    course_name = models.ForeignKey(Course, on_delete=models.CASCADE)
    required = models.BooleanField(default=False)
    topic_set_id = models.IntegerField(default=0)
    units_of_topic = models.PositiveSmallIntegerField(default=0)

    class Meta:
        db_table = 'curriculum_course'
        constraints = [
            models.UniqueConstraint(fields=['curriculum_name', 'course_name'],
                                    name='unique_curriculum_course')
        ]

    def __str__(self):
        return str(self.curriculum_name) + ' ' + str(self.course_name)


# Section model
class Section(models.Model):
    Spring = 'SP'
    Summer = 'SM'
    Fall = 'FA'
    Winter = 'WT'
    SEMESTERS = (
        (Spring, 'Spring'),
        (Summer, 'Summer'),
        (Fall, 'Fall'),
        (Winter, 'Winter'),
    )
    id = models.AutoField(primary_key=True)
    section_id = models.PositiveIntegerField(default=0)
    course_name = models.ForeignKey(Course, on_delete=models.CASCADE)
    semester = models.CharField(max_length=2, choices=SEMESTERS)
    student_count = models.PositiveIntegerField(default=0)
    comment1 = models.TextField(blank=True)
    comment2 = models.TextField(blank=True)
    grade_distribution_id = models.ForeignKey('GradeDistribution', on_delete=models.CASCADE, null=True)
    year = models.IntegerField(default=2019)

    class Meta:
        db_table = 'section'
        constraints = [
            models.UniqueConstraint(fields=['section_id', 'course_name', 'semester'],
                                    name='unique_section')
        ]

    def __str__(self):
        return str(self.course_name) + ' section ' + str(self.section_id)


# Goal model
class Goal(models.Model):
    goal_id = models.AutoField(primary_key=True)
    curriculum_name = models.ForeignKey(Curriculum, on_delete=models.CASCADE)
    course_name = models.ForeignKey(Course, on_delete=models.CASCADE)
    description = models.CharField(max_length=255)
    grade_distribution_id = models.ForeignKey('GradeDistribution', on_delete=models.CASCADE, null=True)

    class Meta:
        db_table = 'goal'

    def __str__(self):
        return str(self.goal_id) + ' ' + str(self.curriculum_name) + ' ' + str(self.course_name)


# GradeDistribution model
class GradeDistribution(models.Model):
    grade_distribution_id = models.AutoField(primary_key=True)
    total_student = models.PositiveIntegerField(default=0)
    A_plus = models.PositiveIntegerField(default=0)
    A = models.PositiveIntegerField(default=0)
    A_minus = models.PositiveIntegerField(default=0)
    B_plus = models.PositiveIntegerField(default=0)
    B = models.PositiveIntegerField(default=0)
    B_minus = models.PositiveIntegerField(default=0)
    C_plus = models.PositiveIntegerField(default=0)
    C = models.PositiveIntegerField(default=0)
    C_minus = models.PositiveIntegerField(default=0)
    D_plus = models.PositiveIntegerField(default=0)
    D = models.PositiveIntegerField(default=0)
    D_minus = models.PositiveIntegerField(default=0)
    Fail = models.PositiveIntegerField(default=0)
    Withdraw = models.PositiveIntegerField(default=0)
    Incomplete = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = 'grade_distribution'

    def __str__(self):
        return 'Grade distribution ID: ' + str(self.grade_distribution_id)
