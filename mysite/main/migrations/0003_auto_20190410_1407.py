# Generated by Django 2.2 on 2019-04-10 19:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_auto_20190405_0042'),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('course_name', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('subject_code', models.CharField(max_length=4)),
            ],
            options={
                'db_table': 'course',
            },
        ),
        migrations.CreateModel(
            name='Curriculum',
            fields=[
                ('curriculum_name', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('admin_name', models.CharField(max_length=100)),
                ('topic_coverage', models.CharField(choices=[('EX', 'Extensive'), ('IN', 'Inclusive'), ('BP', 'BasicPlus'), ('BC', 'Basic'), ('US', 'Unsatisfactory'), ('SB', 'Substandard')], default='BC', max_length=2)),
            ],
            options={
                'db_table': 'curriculum',
            },
        ),
        migrations.CreateModel(
            name='CurriculumCourse',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.Course')),
                ('curriculum_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.Curriculum')),
            ],
            options={
                'db_table': 'curriculum_course',
            },
        ),
        migrations.CreateModel(
            name='Goal',
            fields=[
                ('goal_id', models.AutoField(primary_key=True, serialize=False)),
                ('description', models.CharField(max_length=255)),
                ('course_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.Course')),
                ('curriculum_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.Curriculum')),
            ],
            options={
                'db_table': 'goal',
            },
        ),
        migrations.CreateModel(
            name='GradeDistribution',
            fields=[
                ('grade_distribution_id', models.AutoField(primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'grade_distribution',
            },
        ),
        migrations.CreateModel(
            name='Section',
            fields=[
                ('section_id', models.IntegerField(primary_key=True, serialize=False)),
                ('semester', models.CharField(choices=[('SP', 'Spring'), ('SM', 'Summer'), ('FA', 'Fall'), ('WT', 'Winter')], max_length=2)),
                ('course_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.Course')),
                ('grade_distribution_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.GradeDistribution')),
            ],
            options={
                'db_table': 'section',
            },
        ),
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('topic_id', models.AutoField(primary_key=True, serialize=False)),
                ('subject_area', models.CharField(max_length=50)),
                ('units', models.DecimalField(decimal_places=1, max_digits=10)),
                ('curriculum_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.Curriculum')),
            ],
            options={
                'db_table': 'topic',
            },
        ),
        migrations.CreateModel(
            name='TopicName',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('topic_name', models.CharField(max_length=50)),
                ('topic_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.Topic')),
            ],
            options={
                'db_table': 'topic_name',
            },
        ),
        migrations.CreateModel(
            name='TopicSet',
            fields=[
                ('topic_set_id', models.AutoField(primary_key=True, serialize=False)),
                ('course_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.Course')),
                ('curriculum_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.Curriculum')),
                ('topic_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.Topic')),
            ],
            options={
                'db_table': 'topic_set',
            },
        ),
        migrations.DeleteModel(
            name='Model',
        ),
        migrations.AddField(
            model_name='curriculumcourse',
            name='topic_set_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.TopicSet'),
        ),
        migrations.AddConstraint(
            model_name='topicset',
            constraint=models.UniqueConstraint(fields=('topic_set_id', 'course_name', 'topic_id', 'curriculum_name'), name='unique_topic_set'),
        ),
        migrations.AddConstraint(
            model_name='topic',
            constraint=models.UniqueConstraint(fields=('topic_id', 'curriculum_name'), name='unique_topic'),
        ),
        migrations.AddConstraint(
            model_name='section',
            constraint=models.UniqueConstraint(fields=('section_id', 'course_name'), name='unique_section'),
        ),
        migrations.AddConstraint(
            model_name='curriculumcourse',
            constraint=models.UniqueConstraint(fields=('curriculum_name', 'course_name'), name='unique_curriculum_course'),
        ),
    ]