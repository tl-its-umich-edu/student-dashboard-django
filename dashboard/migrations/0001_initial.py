# -*- coding: utf-8 -*-
# Generated by Django 1.11.18 on 2019-01-25 22:42
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AcademicTerms',
            fields=[
                ('id', models.BigIntegerField(primary_key=True, serialize=False, verbose_name='Term Id')),
                ('canvas_id', models.CharField(max_length=255, verbose_name='Canvas Id')),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
                ('date_start', models.DateTimeField(blank=True, null=True, verbose_name='Start Date')),
                ('date_end', models.DateTimeField(blank=True, null=True, verbose_name='End Date')),
            ],
            options={
                'verbose_name': 'Academic Terms',
                'verbose_name_plural': 'Academic Terms',
                'db_table': 'academic_terms',
            },
        ),
        migrations.CreateModel(
            name='Assignment',
            fields=[
                ('id', models.CharField(max_length=255, primary_key=True, serialize=False, verbose_name='Assignment Id')),
                ('name', models.CharField(default='', max_length=255, verbose_name='Name')),
                ('due_date', models.DateTimeField(blank=True, null=True, verbose_name='Due DateTime')),
                ('local_date', models.DateTimeField(blank=True, null=True, verbose_name='Local DateTime')),
                ('points_possible', models.CharField(blank=True, max_length=255, null=True, verbose_name='Points Possible')),
                ('course_id', models.CharField(max_length=255, verbose_name='Course Id')),
                ('assignment_group_id', models.CharField(max_length=255, verbose_name='Assignment Group Id')),
            ],
            options={
                'db_table': 'assignment',
            },
        ),
        migrations.CreateModel(
            name='AssignmentGroups',
            fields=[
                ('id', models.CharField(max_length=255, primary_key=True, serialize=False, verbose_name='Assignment Group Id')),
                ('name', models.CharField(default='', max_length=255, verbose_name='Name')),
                ('weight', models.CharField(blank=True, max_length=255, null=True, verbose_name='Weight')),
                ('group_points', models.CharField(blank=True, max_length=255, null=True, verbose_name='Group Points')),
                ('course_id', models.CharField(max_length=255, verbose_name='Course Id')),
                ('drop_lowest', models.CharField(blank=True, max_length=255, null=True, verbose_name='Drop Lowest')),
                ('drop_highest', models.CharField(blank=True, max_length=255, null=True, verbose_name='Drop Highest')),
            ],
            options={
                'verbose_name': 'Assignment Groups',
                'verbose_name_plural': 'Assignment Groups',
                'db_table': 'assignment_groups',
            },
        ),
        migrations.CreateModel(
            name='AssignmentWeightConsideration',
            fields=[
                ('course_id', models.CharField(max_length=255, primary_key=True, serialize=False, verbose_name='Course Id')),
                ('consider_weight', models.NullBooleanField(default=False, verbose_name='Consider Weight')),
            ],
            options={
                'db_table': 'assignment_weight_consideration',
            },
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.CharField(db_column='id', editable=False, max_length=255, primary_key=True, serialize=False, verbose_name='Unizin Course Id')),
                ('canvas_id', models.CharField(db_column='canvas_id', max_length=255, verbose_name='Canvas Course Id')),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
            ],
            options={
                'verbose_name': 'Course',
                'db_table': 'course',
            },
        ),
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.CharField(max_length=255, primary_key=True, serialize=False, verbose_name='File Id')),
                ('name', models.TextField(verbose_name='File Name')),
                ('course_id', models.CharField(max_length=255, verbose_name='Course Id')),
            ],
            options={
                'db_table': 'file',
            },
        ),
        migrations.CreateModel(
            name='Submission',
            fields=[
                ('id', models.CharField(max_length=255, primary_key=True, serialize=False, verbose_name='Submission Id')),
                ('assignment_id', models.CharField(max_length=255, verbose_name='Assignment Id')),
                ('course_id', models.CharField(max_length=255, verbose_name='Course Id')),
                ('user_id', models.CharField(max_length=255, verbose_name='User Id')),
                ('score', models.CharField(blank=True, max_length=255, null=True, verbose_name='Score')),
                ('graded_date', models.DateTimeField(blank=True, null=True, verbose_name='Graded DateTime')),
                ('avg_score', models.FloatField(blank=True, null=True, verbose_name='Average Grade')),
            ],
            options={
                'db_table': 'submission',
            },
        ),
        migrations.CreateModel(
            name='UnizinMetadata',
            fields=[
                ('pkey', models.CharField(max_length=20, primary_key=True, serialize=False, verbose_name='Key')),
                ('pvalue', models.CharField(blank=True, max_length=100, null=True, verbose_name='Value')),
            ],
            options={
                'db_table': 'unizin_metadata',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='Table Id')),
                ('user_id', models.CharField(blank=False, max_length=255, null=False, verbose_name='User Id')),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
                ('sis_id', models.CharField(blank=True, max_length=255, null=True, verbose_name='SIS Id')),
                ('sis_name', models.CharField(blank=True, max_length=255, null=True, verbose_name='SIS Name')),
                ('course_id', models.CharField(blank=True, max_length=255, null=True, verbose_name='Course Id')),
                ('current_grade', models.CharField(blank=True, max_length=255, null=True, verbose_name='Current Grade')),
                ('final_grade', models.CharField(blank=True, max_length=255, null=True, verbose_name='Final Grade')),
            ],
            options={
                'db_table': 'user',
            },
        ),
        migrations.CreateModel(
            name='UserDefaultSelection',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='Table Id')),
                ('course_id', models.CharField(blank=True, max_length=255, null=True, verbose_name='Course Id')),
                ('user_id', models.CharField(blank=True, max_length=255, null=True, verbose_name='User Id')),
                ('default_view_type', models.CharField(blank=True, max_length=255, null=True, verbose_name='Default Type')),
                ('default_view_value', models.CharField(blank=True, max_length=255, null=True, verbose_name='Default Value')),
            ],
            options={
                'db_table': 'user_default_selection',
            },
        ),
        migrations.CreateModel(
            name='CourseViewOption',
            fields=[
                ('course', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='dashboard.Course', verbose_name='Course View Option Id')),
                ('show_files_accessed', models.BooleanField(default=True, verbose_name='Show Files Accessed View')),
                ('show_assignment_planning', models.BooleanField(default=True, verbose_name='Show Assignment Planning View')),
                ('show_grade_distribution', models.BooleanField(default=True, verbose_name='Show Grade Distribution View')),
            ],
            options={
                'db_table': 'course_view_option',
                'verbose_name': 'Course View Option',
            },
        ),
        migrations.CreateModel(
            name='FileAccess',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='Table Id')),
                ('file_id', models.CharField(blank=True, max_length=255, null=False, verbose_name='File Id')),
                ('user_id', models.CharField(blank=True, max_length=255, null=False, verbose_name='User Id')),
                ('access_time', models.DateTimeField(verbose_name='Access Time')),
            ],
            options={
                'db_table': 'file_access',
            },
        ),
        migrations.AlterUniqueTogether(
            name='userdefaultselection',
            unique_together=set([('user_id', 'course_id', 'default_view_type')]),
        ),
        migrations.AlterUniqueTogether(
            name='user',
            unique_together=set([('id', 'course_id')]),
        ),
        migrations.AddField(
            model_name='course',
            name='term_id',
            field=models.ForeignKey(db_column='term_id', db_constraint=False, null=True, on_delete=django.db.models.deletion.SET_NULL, to='dashboard.AcademicTerms', verbose_name='Term Id'),
        ),
    ]