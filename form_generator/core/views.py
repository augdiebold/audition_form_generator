from copy import deepcopy

from django.forms import model_to_dict
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, resolve_url as r
from django.contrib import messages
from form_generator.core.forms import get_audition_form
from form_generator.core.models import AuditionBase, Audition


def index(request):
    auditions = Audition.objects.all().order_by('-created_at')

    if request.htmx:
        return render(request, 'partials/audition_table.html', {'auditions': auditions})

    return render(request, 'index.html', {'auditions': auditions})


def new(request):
    if request.method == 'POST':
        return create(request)

    return empty_form(request)


def create(request):
    id = request.POST.get('audition_base')
    form = get_audition_form(id)
    form = form(request.POST)

    if not form.is_valid():
        return render(request, 'partials/audition_form.html', {'form': form})

    obj = form.save(commit=False)
    data = deepcopy(form.cleaned_data)
    del data['audition_base']
    obj.data = data
    obj.save()

    messages.success(request, "Audition successfully saved!")

    return render(request, 'partials/audition_form.html', {'form': form})


def empty_form(request):

    form = get_audition_form()

    if request.htmx:
        id = request.GET.get('audition_base')

        if id:
            form = get_audition_form(id)
            form = form(initial={'audition_base': id})

        return render(request, 'partials/audition_form.html', {'form': form})

    return render(request, 'audition_form_full.html', {'form': form})


def update(request, pk):

    audition_obj = get_object_or_404(Audition, pk=pk)
    form = get_audition_form(audition_obj.audition_base)

    form = form(request.POST or None, instance=audition_obj)

    if request.method == "POST":
        if form.is_valid():
            obj = form.save(commit=False)
            data = deepcopy(form.cleaned_data)
            del data['audition_base']
            obj.data = data
            obj.save()

            messages.success(request, "Audition successfully updated!")

    if request.htmx:
        return render(request, 'partials/audition_form.html', {'form': form, 'audition': audition_obj})

    return render(request, 'audition_form_full.html', {'form': form, 'audition': audition_obj})


def delete(request, pk):
    audition_obj = get_object_or_404(Audition, pk=pk)

    if request.htmx:
        return render(request, 'modals/delete_modal.html', {'audition': audition_obj})

    if request.method == 'POST':
        messages.info(request, f'Audition {audition_obj} succesfuly deleted!')
        audition_obj.delete()

    return HttpResponseRedirect(r('core:index'))


def detail(request, pk):
    audition_obj = get_object_or_404(Audition, pk=pk)

    if request.htmx:
        return render(request, 'partials/audition_detail.html', {'audition': audition_obj})

    return render(request, 'audition_detail_full.html', {'audition': audition_obj})