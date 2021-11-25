from django import forms
from django.test import TestCase

from form_generator.core.models import AuditionBase, FieldsAuditionBase, Audition


class AuditionBaseModelTest(TestCase):
    def setUp(self):
        self.obj = AuditionBase.objects.create(name='Inventory Audit')

    def test_create(self):
        self.assertTrue(AuditionBase.objects.exists())

    def test_get_audition_name(self):
        self.assertEqual(self.obj.get_audition_name(), 'Inventory Audit')


class FieldsAuditionBaseModelTest(TestCase):
    def setUp(self):
        self.audition_base = AuditionBase.objects.create(name='Inventory Audit')
        self.field_obj = FieldsAuditionBase.objects.create(audition_base=self.audition_base, name='machine', field_type='CharField',
                                          label='Machine', required=False)

    def test_create(self):
        self.assertTrue(FieldsAuditionBase.objects.exists())

    def test_generate_field(self):
        form_field = self.field_obj.generate_field()

        self.assertEqual(form_field.label, 'Machine')
        self.assertEqual(form_field.required, False)
        self.assertIsInstance(form_field, forms.CharField)


class AuditionModelTest(TestCase):
    def test_create(self):
        audition_base = AuditionBase.objects.create(name='Inventory Audit')
        FieldsAuditionBase.objects.create(audition_base=audition_base, name='machine', field_type='CharField',
                                          label='Machine', required=False)
        Audition.objects.create(audition_base=audition_base, data=dict(machine='3cx'))

        self.assertTrue(FieldsAuditionBase.objects.exists())