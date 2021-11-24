from django import forms
from django.test import TestCase
from django.shortcuts import resolve_url as r

from form_generator.core.forms import get_audition_form
from form_generator.core.models import AuditionBase, FieldsAuditionBase, Audition


class AuditionNewGet(TestCase):
    def setUp(self):
        self.resp = self.client.get(r('form_generator.core:new_audition'))

    def test_get(self):
        self.assertEqual(200, self.resp.status_code)

    def test_template(self):
        """Must use subscriptions/subscription_form.html"""
        self.assertTemplateUsed(self.resp, 'audition_form_full.html')

    def test_html(self):
        """Html must contain input tags"""

        tags = (('<a ', 1),
                ('<form', 1),
                ('<input', 2),
                ('type="submit"', 1))

        for text, count in tags:
            with self.subTest():
                self.assertContains(self.resp, text, count)

    def test_csrf(self):
        """Html must contain csrf"""
        self.assertContains(self.resp, 'csrfmiddlewaretoken')

    def test_has_form(self):
        """Context must have subscription form"""
        form = self.resp.context['form']
        self.assertIsInstance(form(), forms.ModelForm)


class AuditionNewGetHtmx(TestCase):
    def setUp(self):
        headers = {"HTTP_HX_REQUEST": 'true'}
        self.resp = self.client.get(r('form_generator.core:new_audition'), **headers)

    def test_get(self):
        self.assertEqual(200, self.resp.status_code)

    def test_template(self):
        """Must use subscriptions/subscription_form.html"""
        self.assertTemplateUsed(self.resp, 'audition_form.html')

    def test_html(self):
        """Html must contain input tags"""

        tags = (('<form', 1),
                ('<input', 2),
                ('type="submit"', 1))

        for text, count in tags:
            with self.subTest():
                self.assertContains(self.resp, text, count)

    def test_csrf(self):
        """Html must contain csrf"""
        self.assertContains(self.resp, 'csrfmiddlewaretoken')

    def test_has_form(self):
        """Context must have subscription form"""
        form = self.resp.context['form']
        self.assertIsInstance(form(), forms.ModelForm)


class AuditionNewGetObjHtmx(TestCase):
    def setUp(self):
        self.audition_base = AuditionBase.objects.create(name='Inventory Audit')
        self.audition_base_fields = FieldsAuditionBase.objects.create(audition_base=self.audition_base, name='machine',
                                                                      field_type='CharField', label='Machine',
                                                                      required=False)

        headers = {"HTTP_HX_REQUEST": 'true'}
        self.resp = self.client.get(r('form_generator.core:new_audition'),
                                    data={'audition_base': self.audition_base.id}, **headers)

    def test_get(self):
        self.assertEqual(200, self.resp.status_code)

    def test_template(self):
        """Must use subscriptions/subscription_form.html"""
        self.assertTemplateUsed(self.resp, 'audition_form.html')

    def test_html(self):
        """Html must contain input tags"""

        tags = (('<form', 1),
                ('<input', 3),
                ('type="submit"', 1))

        for text, count in tags:
            with self.subTest():
                self.assertContains(self.resp, text, count)

    def test_csrf(self):
        """Html must contain csrf"""
        self.assertContains(self.resp, 'csrfmiddlewaretoken')

    def test_has_form(self):
        """Context must have subscription form"""
        form = self.resp.context['form']
        self.assertIsInstance(form, forms.ModelForm)


class AuditionNewPostValid(TestCase):
    def setUp(self):
        self.audition_base = AuditionBase.objects.create(name='Inventory Audit')
        self.audition_base_fields = FieldsAuditionBase.objects.create(audition_base=self.audition_base, name='machine',
                                                                      field_type='CharField', label='Machine',
                                                                      required=False)
        data = dict(audition_base=self.audition_base.id, machine='3CX')

        self.resp = self.client.post(r('form_generator.core:new_audition'), data)

    def test_save_audition(self):
        self.assertTrue(Audition.objects.exists())


class AuditionNewPostInvalid(TestCase):
    def setUp(self):
        self.resp = self.client.post(r('form_generator.core:new_audition'), {})

    def test_template(self):
        """Must use subscriptions/subscription_form.html"""
        self.assertTemplateUsed(self.resp, 'audition_form.html')

    def test_has_form(self):
        """Context must have subscription form"""
        form = self.resp.context['form']
        self.assertIsInstance(form, forms.ModelForm)

    def test_form_has_errors(self):
        form = self.resp.context['form']
        self.assertTrue(form.errors)

    def test_save_audition(self):
        self.assertFalse(Audition.objects.exists())

