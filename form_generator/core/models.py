import re

from django import forms
from django.contrib.postgres.fields import HStoreField
from django.db import models

from form_generator.core.validators import validate_name

FIELD_TYPES = [
    ('CharField', 'CharField'),
    ('EmailField', 'EmailField'),
    ('ChoiceField', 'ChoiceField'),
    ('BooleanField', 'BooleanField'),
    ('URLField', 'URLField'),
    ('TextField', 'TextField'),
]


class AuditionBase(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

    def get_audition_name(self):
        return self.name


class FieldsAuditionBase(models.Model):
    audition_base = models.ForeignKey('AuditionBase', on_delete=models.CASCADE, related_name='fields')
    name = models.CharField(max_length=100, validators=[validate_name,])
    field_type = models.CharField(max_length=100, choices=FIELD_TYPES)
    label = models.CharField(max_length=100)
    required = models.BooleanField()
    choices = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.name

    def choices_to_tuple(self):
        """
        Used to create choice options on ChoiceField
        """
        choices = re.split(r',\s*', self.choices)

        return [(choice.lower(), choice) for choice in choices]

    def generate_field(self):
        """
        :returns a field object
        """
        type_mapping = {'CharField': forms.CharField(max_length=100, label=self.label, required=self.required),
                        'ChoiceField': forms.ChoiceField(label=self.label, required=self.required),
                        'TextField': forms.CharField(widget=forms.Textarea, label=self.label, required=self.required),
                        'BooleanField': forms.BooleanField(label=self.label, required=self.required),
                        'URLField': forms.URLField(label=self.label, required=self.required),
                        'EmailField': forms.EmailField(label=self.label, required=self.required),
                        }

        if self.choices:
            setattr(type_mapping['ChoiceField'], 'choices', self.choices_to_tuple())

        return type_mapping[self.field_type]


class Audition(models.Model):
    audition_base = models.ForeignKey('AuditionBase', on_delete=models.PROTECT, related_name='auditions')
    identifier = models.CharField('identifier', blank=True, null=True, max_length=100)
    data = HStoreField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.audition_base} - {self.identifier}'

    def get_data_items(self):
        return self.data.items()