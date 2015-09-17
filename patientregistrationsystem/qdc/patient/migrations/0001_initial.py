# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
import django.db.models.deletion
import patient.models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AlcoholFrequency',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='AlcoholPeriod',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='AmountCigarettes',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='ClassificationOfDiseases',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('code', models.CharField(max_length=10)),
                ('description', models.CharField(max_length=300)),
                ('abbreviated_description', models.CharField(max_length=100)),
                ('parent', models.ForeignKey(null=True, related_name='children', to='patient.ClassificationOfDiseases')),
            ],
        ),
        migrations.CreateModel(
            name='ComplementaryExam',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('date', models.DateField()),
                ('description', models.CharField(max_length=500)),
                ('doctor', models.CharField(blank=True, max_length=50, null=True)),
                ('doctor_register', models.CharField(blank=True, max_length=10, null=True)),
                ('exam_site', models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Diagnosis',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('date', models.DateField(null=True)),
                ('description', models.CharField(max_length=300, null=True)),
                ('classification_of_diseases', models.ForeignKey(to='patient.ClassificationOfDiseases')),
            ],
        ),
        migrations.CreateModel(
            name='ExamFile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('content', models.FileField(upload_to=patient.models.get_user_dir)),
                ('exam', models.ForeignKey(to='patient.ComplementaryExam')),
            ],
        ),
        migrations.CreateModel(
            name='FleshTone',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Gender',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='HistoricalPatient',
            fields=[
                ('id', models.IntegerField(verbose_name='ID', blank=True, db_index=True, auto_created=True)),
                ('name', models.CharField(max_length=50)),
                ('cpf', models.CharField(blank=True, db_index=True, max_length=15, validators=[patient.models.validate_cpf], null=True)),
                ('origin', models.CharField(blank=True, max_length=50, null=True)),
                ('medical_record', models.CharField(blank=True, max_length=25, null=True)),
                ('date_birth', models.DateField(validators=[patient.models.validate_date_birth])),
                ('rg', models.CharField(blank=True, max_length=15, null=True)),
                ('country', models.CharField(blank=True, max_length=30, null=True)),
                ('zipcode', models.CharField(blank=True, max_length=12, null=True)),
                ('street', models.CharField(blank=True, max_length=50, null=True)),
                ('address_number', models.IntegerField(blank=True, max_length=6, null=True)),
                ('address_complement', models.CharField(blank=True, max_length=50, null=True)),
                ('district', models.CharField(blank=True, max_length=50, null=True)),
                ('city', models.CharField(blank=True, max_length=30, null=True)),
                ('state', models.CharField(blank=True, max_length=30, null=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('removed', models.BooleanField(default=False)),
                ('history_id', models.AutoField(serialize=False, primary_key=True)),
                ('history_date', models.DateTimeField()),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('changed_by', models.ForeignKey(related_name='+', db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, blank=True, to=settings.AUTH_USER_MODEL)),
                ('gender', models.ForeignKey(related_name='+', db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, blank=True, to='patient.Gender')),
                ('history_user', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, null=True, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical patient',
                'get_latest_by': 'history_date',
                'ordering': ('-history_date', '-history_id'),
            },
        ),
        migrations.CreateModel(
            name='HistoricalSocialDemographicData',
            fields=[
                ('id', models.IntegerField(verbose_name='ID', blank=True, db_index=True, auto_created=True)),
                ('natural_of', models.CharField(blank=True, max_length=50, null=True)),
                ('citizenship', models.CharField(blank=True, max_length=50, null=True)),
                ('profession', models.CharField(blank=True, max_length=50, null=True)),
                ('occupation', models.CharField(blank=True, max_length=50, null=True)),
                ('benefit_government', models.NullBooleanField()),
                ('tv', models.IntegerField(blank=True, null=True)),
                ('dvd', models.IntegerField(blank=True, null=True)),
                ('radio', models.IntegerField(blank=True, null=True)),
                ('bath', models.IntegerField(blank=True, null=True)),
                ('automobile', models.IntegerField(blank=True, null=True)),
                ('wash_machine', models.IntegerField(blank=True, null=True)),
                ('refrigerator', models.IntegerField(blank=True, null=True)),
                ('freezer', models.IntegerField(blank=True, null=True)),
                ('house_maid', models.IntegerField(blank=True, null=True)),
                ('social_class', models.CharField(blank=True, max_length=10, null=True)),
                ('history_id', models.AutoField(serialize=False, primary_key=True)),
                ('history_date', models.DateTimeField()),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('changed_by', models.ForeignKey(related_name='+', db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, blank=True, to=settings.AUTH_USER_MODEL)),
                ('flesh_tone', models.ForeignKey(related_name='+', db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, blank=True, to='patient.FleshTone')),
                ('history_user', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, null=True, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical social demographic data',
                'get_latest_by': 'history_date',
                'ordering': ('-history_date', '-history_id'),
            },
        ),
        migrations.CreateModel(
            name='HistoricalSocialHistoryData',
            fields=[
                ('id', models.IntegerField(verbose_name='ID', blank=True, db_index=True, auto_created=True)),
                ('smoker', models.NullBooleanField()),
                ('ex_smoker', models.NullBooleanField()),
                ('alcoholic', models.NullBooleanField()),
                ('drugs', models.CharField(blank=True, max_length=25, null=True)),
                ('history_id', models.AutoField(serialize=False, primary_key=True)),
                ('history_date', models.DateTimeField()),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('alcohol_frequency', models.ForeignKey(related_name='+', db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, blank=True, to='patient.AlcoholFrequency')),
                ('alcohol_period', models.ForeignKey(related_name='+', db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, blank=True, to='patient.AlcoholPeriod')),
                ('amount_cigarettes', models.ForeignKey(related_name='+', db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, blank=True, to='patient.AmountCigarettes')),
                ('changed_by', models.ForeignKey(related_name='+', db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, blank=True, to=settings.AUTH_USER_MODEL)),
                ('history_user', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, null=True, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical social history data',
                'get_latest_by': 'history_date',
                'ordering': ('-history_date', '-history_id'),
            },
        ),
        migrations.CreateModel(
            name='HistoricalTelephone',
            fields=[
                ('id', models.IntegerField(verbose_name='ID', blank=True, db_index=True, auto_created=True)),
                ('number', models.CharField(max_length=15)),
                ('type', models.CharField(blank=True, choices=[('MO', 'Celular'), ('HO', 'Residencial'), ('WO', 'Comercial'), ('MA', 'Principal'), ('FW', 'Fax comercial'), ('FH', 'Fax residencial'), ('PA', 'Pager'), ('OT', 'Outros')], max_length=15)),
                ('note', models.CharField(blank=True, max_length=50)),
                ('history_id', models.AutoField(serialize=False, primary_key=True)),
                ('history_date', models.DateTimeField()),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('changed_by', models.ForeignKey(related_name='+', db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, blank=True, to=settings.AUTH_USER_MODEL)),
                ('history_user', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, null=True, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical telephone',
                'get_latest_by': 'history_date',
                'ordering': ('-history_date', '-history_id'),
            },
        ),
        migrations.CreateModel(
            name='MaritalStatus',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='MedicalRecordData',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('record_date', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'permissions': (('view_medicalrecorddata', 'Can view medical record'),),
            },
        ),
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('name', models.CharField(max_length=50)),
                ('cpf', models.CharField(unique=True, blank=True, max_length=15, validators=[patient.models.validate_cpf], null=True)),
                ('origin', models.CharField(blank=True, max_length=50, null=True)),
                ('medical_record', models.CharField(blank=True, max_length=25, null=True)),
                ('date_birth', models.DateField(validators=[patient.models.validate_date_birth])),
                ('rg', models.CharField(blank=True, max_length=15, null=True)),
                ('country', models.CharField(blank=True, max_length=30, null=True)),
                ('zipcode', models.CharField(blank=True, max_length=12, null=True)),
                ('street', models.CharField(blank=True, max_length=50, null=True)),
                ('address_number', models.IntegerField(blank=True, max_length=6, null=True)),
                ('address_complement', models.CharField(blank=True, max_length=50, null=True)),
                ('district', models.CharField(blank=True, max_length=50, null=True)),
                ('city', models.CharField(blank=True, max_length=30, null=True)),
                ('state', models.CharField(blank=True, max_length=30, null=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('removed', models.BooleanField(default=False)),
                ('changed_by', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('gender', models.ForeignKey(to='patient.Gender')),
                ('marital_status', models.ForeignKey(null=True, blank=True, to='patient.MaritalStatus')),
            ],
            options={
                'permissions': (('view_patient', 'Can view patient'),),
            },
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='QuestionnaireResponse',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('token_id', models.IntegerField()),
                ('date', models.DateField(validators=[patient.models.validate_date_questionnaire_response], default=datetime.date.today)),
                ('patient', models.ForeignKey(to='patient.Patient')),
                ('questionnaire_responsible', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='+')),
                ('survey', models.ForeignKey(to='survey.Survey', on_delete=django.db.models.deletion.PROTECT)),
            ],
            options={
                'permissions': (('view_questionnaireresponse', 'Can view questionnaire response'),),
            },
        ),
        migrations.CreateModel(
            name='Religion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Schooling',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='SocialDemographicData',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('natural_of', models.CharField(blank=True, max_length=50, null=True)),
                ('citizenship', models.CharField(blank=True, max_length=50, null=True)),
                ('profession', models.CharField(blank=True, max_length=50, null=True)),
                ('occupation', models.CharField(blank=True, max_length=50, null=True)),
                ('benefit_government', models.NullBooleanField()),
                ('tv', models.IntegerField(blank=True, null=True)),
                ('dvd', models.IntegerField(blank=True, null=True)),
                ('radio', models.IntegerField(blank=True, null=True)),
                ('bath', models.IntegerField(blank=True, null=True)),
                ('automobile', models.IntegerField(blank=True, null=True)),
                ('wash_machine', models.IntegerField(blank=True, null=True)),
                ('refrigerator', models.IntegerField(blank=True, null=True)),
                ('freezer', models.IntegerField(blank=True, null=True)),
                ('house_maid', models.IntegerField(blank=True, null=True)),
                ('social_class', models.CharField(blank=True, max_length=10, null=True)),
                ('changed_by', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('flesh_tone', models.ForeignKey(null=True, blank=True, to='patient.FleshTone')),
                ('patient', models.ForeignKey(to='patient.Patient')),
                ('payment', models.ForeignKey(null=True, blank=True, to='patient.Payment')),
                ('religion', models.ForeignKey(null=True, blank=True, to='patient.Religion')),
                ('schooling', models.ForeignKey(null=True, blank=True, to='patient.Schooling')),
            ],
        ),
        migrations.CreateModel(
            name='SocialHistoryData',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('smoker', models.NullBooleanField()),
                ('ex_smoker', models.NullBooleanField()),
                ('alcoholic', models.NullBooleanField()),
                ('drugs', models.CharField(blank=True, max_length=25, null=True)),
                ('alcohol_frequency', models.ForeignKey(default=0, null=True, blank=True, to='patient.AlcoholFrequency')),
                ('alcohol_period', models.ForeignKey(default=0, null=True, blank=True, to='patient.AlcoholPeriod')),
                ('amount_cigarettes', models.ForeignKey(default=0, null=True, blank=True, to='patient.AmountCigarettes')),
                ('changed_by', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('patient', models.ForeignKey(to='patient.Patient')),
            ],
        ),
        migrations.CreateModel(
            name='Telephone',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('number', models.CharField(max_length=15)),
                ('type', models.CharField(blank=True, choices=[('MO', 'Celular'), ('HO', 'Residencial'), ('WO', 'Comercial'), ('MA', 'Principal'), ('FW', 'Fax comercial'), ('FH', 'Fax residencial'), ('PA', 'Pager'), ('OT', 'Outros')], max_length=15)),
                ('note', models.CharField(blank=True, max_length=50)),
                ('changed_by', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('patient', models.ForeignKey(to='patient.Patient')),
            ],
        ),
        migrations.AddField(
            model_name='medicalrecorddata',
            name='patient',
            field=models.ForeignKey(to='patient.Patient'),
        ),
        migrations.AddField(
            model_name='medicalrecorddata',
            name='record_responsible',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='historicaltelephone',
            name='patient',
            field=models.ForeignKey(related_name='+', db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, blank=True, to='patient.Patient'),
        ),
        migrations.AddField(
            model_name='historicalsocialhistorydata',
            name='patient',
            field=models.ForeignKey(related_name='+', db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, blank=True, to='patient.Patient'),
        ),
        migrations.AddField(
            model_name='historicalsocialdemographicdata',
            name='patient',
            field=models.ForeignKey(related_name='+', db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, blank=True, to='patient.Patient'),
        ),
        migrations.AddField(
            model_name='historicalsocialdemographicdata',
            name='payment',
            field=models.ForeignKey(related_name='+', db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, blank=True, to='patient.Payment'),
        ),
        migrations.AddField(
            model_name='historicalsocialdemographicdata',
            name='religion',
            field=models.ForeignKey(related_name='+', db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, blank=True, to='patient.Religion'),
        ),
        migrations.AddField(
            model_name='historicalsocialdemographicdata',
            name='schooling',
            field=models.ForeignKey(related_name='+', db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, blank=True, to='patient.Schooling'),
        ),
        migrations.AddField(
            model_name='historicalpatient',
            name='marital_status',
            field=models.ForeignKey(related_name='+', db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, blank=True, to='patient.MaritalStatus'),
        ),
        migrations.AddField(
            model_name='diagnosis',
            name='medical_record_data',
            field=models.ForeignKey(to='patient.MedicalRecordData'),
        ),
        migrations.AddField(
            model_name='complementaryexam',
            name='diagnosis',
            field=models.ForeignKey(to='patient.Diagnosis'),
        ),
        migrations.AlterUniqueTogether(
            name='diagnosis',
            unique_together=set([('medical_record_data', 'classification_of_diseases')]),
        ),
    ]
