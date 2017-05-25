from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.http import Http404

from FirstDiango.models import Topic, Entry
from .forms import TopicForm, EntryForm
from django.contrib.auth.decorators import login_required


# Create your views here.


def index(request):
    return render(request=request, template_name='linzhipeng/index.html')


@login_required
def topics(request):
    topics = Topic.objects.filter(owner=request.user).order_by('date_added')
    context = {'topics': topics}
    return render(request=request, template_name='linzhipeng/topics.html', context=context)

@login_required
def topic(request, topic_id):
    topic = Topic.objects.get(id=topic_id)
    if topic.owner != request.user:
        raise Http404
    entries = topic.entry_set.order_by('date_added')
    context = {'topic': topic, 'entries': entries}
    return render(request=request, template_name='linzhipeng/topic.html', context=context)

@login_required
def new_topic(request):
    if request.method != 'POST':
        form = TopicForm()
    else:
        form = TopicForm(request.POST)
        if form.is_valid():
            add_topic = form.save(commit=False)
            add_topic.owner = request.user
            add_topic.save()
            return HttpResponseRedirect(reverse(viewname='linzhipeng:topics'))
    context = {'form': form}
    return render(request=request, template_name='linzhipeng/new_topic.html', context=context)

@login_required
def new_entry(request, topic_id):
    topic = Topic.objects.get(id=topic_id)
    if request.method != 'POST':
            form = EntryForm()
    else:
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            return HttpResponseRedirect(reverse(viewname='linzhipeng:topic', args=topic_id))
    context = {'topic': topic, 'form': form}
    return render(request=request, template_name='linzhipeng/new_entry.html', context=context)

@login_required
def edit_entry(request, entry_id):
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic
    if topic.owner != request.user:
        raise Http404
    if request.method != 'POST':
        form = EntryForm()
    else:
        form = EntryForm(instance=entry)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse(viewname='linzhipeng:topic', args=topic.id))
    context = {'entry': entry, 'topic': topic, 'form':form}
    return render(request, template_name='linzhipeng/edit_entry.html', context=context)
