# -*- coding: UTF-8 -*-
import datetime

from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from simple_history.models import HistoricalRecords

from patient.models import Patient, User, ClassificationOfDiseases


def validate_date_questionnaire_response(value):
    if value > datetime.date.today():
        raise ValidationError('Data de preenchimento não pode ser maior que a data de hoje.')


class Subject(models.Model):
    patient = models.ForeignKey(Patient)


class TimeUnit(models.Model):
    name = models.CharField(max_length=30, null=False, blank=False)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ["id"]


class StimulusType(models.Model):
    name = models.CharField(max_length=30, null=False, blank=False)

    def __unicode__(self):
        return self.name


class Keyword(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False)

    def __unicode__(self):
        return self.name


class ResearchProject(models.Model):
    title = models.CharField(max_length=150, null=False, blank=False)
    description = models.CharField(max_length=1500, null=False, blank=False)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    keywords = models.ManyToManyField(Keyword)

    def __unicode__(self):
        return self.title

    class Meta:
        permissions = (
            ("view_researchproject", "Can view research project"),
        )


class Experiment(models.Model):
    title = models.CharField(null=False, max_length=50, blank=False)
    description = models.CharField(max_length=150, null=False, blank=False)

    # ToDo: notice that it's been added as null=True; once it has data, we can alter it to be null=False
    research_project = models.ForeignKey(ResearchProject, null=True, blank=True)

    # Audit trail - Simple History
    history = HistoricalRecords()
    # changed_by = models.ForeignKey('auth.User')

    class Meta:
        permissions = (
            ("view_experiment", "Can view experiment"),
        )

    def __unicode__(self):  # Python 3: def __str__(self):
        return self.title

    @property
    def _history_user(self):
        return self.changed_by

    @_history_user.setter
    def _history_user(self, value):
        self.changed_by = value


class Component(models.Model):
    identification = models.CharField(null=False, max_length=50, blank=False)
    description = models.CharField(max_length=1500, null=True, blank=True)
    experiment = models.ForeignKey(Experiment, null=False)
    component_type = models.CharField(null=False, max_length=15,
                                      choices=(("task", "Task component"),
                                               ("instruction", "Instruction component"),
                                               ("pause", "Pause component"),
                                               ("stimulus", "Stimulus component"),
                                               ("questionnaire", "Questionnaire component"),
                                               ("sequence", "Sequence component"),
                                               ("parallel_block", "Parallel block component")))


class Task(Component):
    instruction_text = models.CharField(max_length=150, null=False, blank=False)

    def save(self, *args, **kwargs):
        super(Component, self).save(*args, **kwargs)


class Instruction(Component):
    text = models.TextField(null=False, blank=False)

    def save(self, *args, **kwargs):
        super(Component, self).save(*args, **kwargs)


class Pause(Component):
    duration = models.IntegerField(null=False, blank=False)
    duration_unit = models.ForeignKey(TimeUnit, null=True, blank=True)

    def save(self, *args, **kwargs):
        super(Component, self).save(*args, **kwargs)


class Stimulus(Component):
    stimulus_type = models.ForeignKey(StimulusType, null=False, blank=False)

    def save(self, *args, **kwargs):
        super(Component, self).save(*args, **kwargs)


class Questionnaire(Component):
    lime_survey_id = models.IntegerField(null=False, blank=False)

    def save(self, *args, **kwargs):
        super(Component, self).save(*args, **kwargs)


class Block(Component):
    number_of_mandatory_components = models.IntegerField(null=True, blank=True)

    def save(self, *args, **kwargs):
        super(Component, self).save(*args, **kwargs)


class Sequence(Block):
    has_random_components = models.BooleanField(null=False, blank=False)

    def save(self, *args, **kwargs):
        super(Block, self).save(*args, **kwargs)


# No need for this class. We simply use a Block with component_type = parallel_block
# class ParallelBlock(Block):
#     def save(self, *args, **kwargs):
#         super(Block, self).save(*args, **kwargs)


class ComponentConfiguration(models.Model):
    name = models.CharField(max_length=50, null=True, blank=True)
    number_of_repetitions = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(1)])
    interval_between_repetitions_value = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(1)])
    interval_between_repetitions_unit = models.ForeignKey(TimeUnit, null=True, blank=True)
    # https://docs.djangoproject.com/en/1.7/topics/db/models/#be-careful-with-related-name
    component = models.ForeignKey(Component, null=False, related_name="%(app_label)s_%(class)s_configuration")
    parent = models.ForeignKey(Block, null=True, related_name='%(app_label)s_%(class)s_children')

    class Meta:
        abstract = True

class BlockConfiguration(ComponentConfiguration):
    pass

class SequenceConfiguration(ComponentConfiguration):
    order = models.IntegerField(null=False, blank=False, validators=[MinValueValidator(1)])

    class Meta:
        unique_together = ('parent', 'order',)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if not self.pk:
            top = ComponentConfiguration.objects.filter(parent=self.parent).order_by('-order').first()
            self.order = top.order + 1 if top else 1
        super(SequenceConfiguration, self).save()


class Group(models.Model):
    experiment = models.ForeignKey(Experiment, null=False, blank=False)
    title = models.CharField(null=False, max_length=50, blank=False)
    description = models.CharField(max_length=150, null=False, blank=False)
    classification_of_diseases = models.ManyToManyField(ClassificationOfDiseases, null=True)
    experimental_protocol = models.ForeignKey(Component, null=True)


def get_dir(instance, filename):
    return "consent_forms/%s/%s/%s/%s" % \
           (instance.group.experiment.id, instance.group.id, instance.subject.id, filename)


class SubjectOfGroup(models.Model):
    subject = models.ForeignKey(Subject, null=False, blank=False)
    group = models.ForeignKey(Group, null=False, blank=False)
    consent_form = models.FileField(upload_to=get_dir, null=True)

    class Meta:
        unique_together = ('subject', 'group',)


class QuestionnaireConfiguration(models.Model):
    lime_survey_id = models.IntegerField(null=False, blank=False)
    group = models.ForeignKey(Group, null=False, on_delete=models.PROTECT)
    number_of_fills = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(1)])
    interval_between_fills_value = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(1)])
    interval_between_fills_unit = models.ForeignKey(TimeUnit, null=True, blank=True)

    # Audit trail - Simple History
    history = HistoricalRecords()
    # changed_by = models.ForeignKey('auth.User')

    @property
    def _history_user(self):
        return self.changed_by

    @_history_user.setter
    def _history_user(self, value):
        self.changed_by = value

    def __unicode__(self):  # Python 3: def __str__(self):
        return self.experiment.title + " - " + str(self.lime_survey_id)

    class Meta:
        unique_together = ('lime_survey_id', 'group',)


class QuestionnaireResponse(models.Model):
    subject_of_group = models.ForeignKey(SubjectOfGroup, null=False)
    questionnaire_configuration = models.ForeignKey(QuestionnaireConfiguration, null=False, on_delete=models.PROTECT)
    token_id = models.IntegerField(null=False)
    date = models.DateField(default=datetime.date.today, null=False,
                            validators=[validate_date_questionnaire_response])
    questionnaire_responsible = models.ForeignKey(User, null=False, related_name="+")

    # Audit trail - Simple History
    history = HistoricalRecords()
    # changed_by = models.ForeignKey('auth.User')

    class Meta:
        permissions = (
            ("view_questionnaireresponse", "Can view questionnaire response"),
        )

    @property
    def _history_user(self):
        return self.changed_by

    @_history_user.setter
    def _history_user(self, value):
        self.changed_by = value

    def __unicode__(self):  # Python 3: def __str__(self):
        return "token id: " + str(self.token_id)
