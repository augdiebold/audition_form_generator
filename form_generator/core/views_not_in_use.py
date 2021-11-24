from copy import deepcopy

from django.contrib import messages
from django.shortcuts import render, get_object_or_404

import form_generator.core.forms as f
from form_generator.core.models import Audition


def index(request):
    return render(request, 'index.html')


def new(request, **kwargs):
    if request.method == 'POST':
        return create(request)

    return empty_form(request, **kwargs)


def create(request):
    id = request.POST.get('audition_base')
    form = f.AuditionForm(id)
    #form = form(request.POST)

    if not form.is_valid():
        return render(request, 'audition_form.html', {'form': form})

    obj = form.save(commit=False)
    data = deepcopy(form.cleaned_data)
    del data['audition_base']
    obj.data = data
    obj.save()

    messages.success(request, "Audition successfully saved!")

    return render(request, 'audition_form.html', {'form': form})


def empty_form(request, **kwargs):
    #slug = kwargs.pop('slug', None)

    form = f.AuditionForm()

    #if slug:
    #    audition_base = get_object_or_404(AuditionBase, slug=slug)
    #    form = get_audition_form(audition_base)
    #    form = form(initial={'audition_base': slug})

    if request.htmx:
        id = request.GET.get('audition_base')

        if id:
            form = f.AuditionForm(audition_base=id, initial={'audition_base': id})

        return render(request, 'audition_form.html', {'form': form})

    return render(request, 'audition_form_full.html', {'form': form})


def update(request, pk):
    audition_obj = get_object_or_404(Audition, pk=pk)
    #form = get_audition_form(audition_obj.audition_base)

    data = audition_obj.data_to_form()
    form = form(request.POST or data, instance=audition_obj)

    if request.method == "POST":
        if form.is_valid():
            obj = form.save(commit=False)
            data = deepcopy(form.cleaned_data)
            del data['audition_base']
            obj.data = data
            obj.save()

            messages.success(request, "Audition successfully updated!")

    if request.htmx:
        return render(request, 'audition_form.html', {'form': form})

    return render(request, 'audition_form_full.html', {'form': form, 'audition': audition_obj})


def delete(request, pk):
    audition_obj = get_object_or_404(Audition, pk=pk)
    audition_obj.delete()
    messages.warning('Audition deleted!')

