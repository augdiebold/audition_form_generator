from django import forms
from django.shortcuts import resolve_url as r
from form_generator.core.models import Audition, FieldsAuditionBase


class AuditionFieldsForm(forms.ModelForm):
    class Meta:
        model = FieldsAuditionBase
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['field_type'].widget.attrs['onchange'] = "toggleChoices(id)"

    def clean_name(self):
        name = self.cleaned_data['name']
        return name.lower()


def get_audition_form(audition_base=None):
    """
    Generate a form class for the Audition Model.

    The template depends on an AuditionBase Object. The fields are generated
    based on the FieldsAuditionBase objects.

    """
    audition_fields = FieldsAuditionBase.objects.filter(audition_base=audition_base)

    class AuditionForm(forms.ModelForm):
        class Meta:
            model = Audition
            fields = ['audition_base', 'identifier']
            widgets = {
                'audition_base': forms.Select(attrs={'hx-get': r('form_generator.core:new_audition'),
                                                     'hx-trigger': 'change',
                                                     'hx-target': '#audition-form',
                                                     'hx-swap': "outerHTML",
                                                     'hx-push-url': "true",
                                                     })
            }

        def __init__(self, *args, **kwargs):
            super(forms.ModelForm, self).__init__(*args, **kwargs)
            if self.instance and self.instance.pk:
                self.fields['audition_base'] = forms.CharField(widget=(forms.TextInput(attrs={'type': 'hidden'})))
                for k, v in self.instance.data.items():
                    self.fields[k].initial = v

        def clean_audition_base(self):
            if self.instance and self.instance.pk:
                return self.instance.audition_base
            else:
                return self.cleaned_data['audition_base']

    for field in audition_fields:
        setattr(AuditionForm, field.name, field.generate_field())

    return type('AuditionForm', (forms.ModelForm, ), dict(AuditionForm.__dict__))



