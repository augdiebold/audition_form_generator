from django import forms
from django.test import TestCase

from form_generator.core.forms import get_audition_form, AuditionFieldsForm
from form_generator.core.models import AuditionBase, FieldsAuditionBase


class AuditionFieldsFormTest(TestCase):
    def make_validated_form(self, **kwargs):
        self.audition_base = AuditionBase.objects.create(name='Inventory Audit')
        valid = dict(audition_base=self.audition_base, name='machine',
                     field_type='CharField', label='Machine',
                     required=False, choices='3CX, a4CX')

        data = dict(valid, **kwargs)
        form = AuditionFieldsForm(data)
        form.is_valid()

        return form


class GetAuditionFormTest(TestCase):
    def setUp(self):
        self.audition_base = AuditionBase.objects.create(name='Inventory Audit')
        self.audition_base_fields = FieldsAuditionBase.objects.create(audition_base=self.audition_base, name='machine',
                                                                      field_type='CharField', label='Machine',
                                                                      required=False, choices='3CX, a4CX')

    def test_is_audition_form(self):
        audition_form = get_audition_form(audition_base=self.audition_base)

        self.assertIsInstance(audition_form(), forms.ModelForm)

    def test_form_has_fields(self):
        audition_form = get_audition_form(audition_base=self.audition_base)
        expected = ['audition_base', 'machine']

        self.assertSequenceEqual(expected, list(audition_form().fields))


