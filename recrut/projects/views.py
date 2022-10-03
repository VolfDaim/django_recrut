from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from .forms import ProjectForm
from .models import Project, Tag


def projects(request):
    projects_obj = Project.objects.all()
    context = {'projects': projects_obj}
    return render(request, 'projects/projects.html', context)


def project(request, project_slug):
    project_obj = Project.objects.get(slug=project_slug)
    tags = project_obj.tags.all()
    context = {'project': project_obj}
    return render(request, 'projects/simple-project.html', context)


def createProject(request):
    form = ProjectForm()
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('projects')
    return render(request, 'projects/project_form.html', {'form': form})


def updateProject(request, pk):
    project_obj = Project.objects.get(id=pk)
    form = ProjectForm(instance=project_obj)

    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project_obj)
        if form.is_valid():
            form.save()
            return redirect('projects')
    return render(request, 'projects/project_form.html', {'form': form})


def deleteProject(request, pk):
    project_obj = Project.objects.get(id=pk)
    if request.method == 'POST':
        project_obj.delete()
        return redirect('projects')
    context = {'object': project_obj}
    return render(request, 'projects/delete.html', context)


def projects_by_tag(request, tag_slug):
    tag = get_object_or_404(Tag, slug=tag_slug)
    projects = Project.objects.filter(tags__in=[tag])
    context = {
        'projects': projects
    }
    return render(request, 'projects/projects.html', context)
