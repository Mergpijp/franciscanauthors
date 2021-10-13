import pdb

from django.shortcuts import render
from django.views.generic import TemplateView, ListView
from .models import *
from django.db.models import Q
from django.views.generic.detail import DetailView
from django.utils import timezone
import re
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from .forms import *
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.shortcuts import redirect
import django.db.models
import django.apps
from .resources import AuthorResource
from import_export_xml.formats import XML
from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger
import string

import os, sys
sys.path.append(os.pardir)
os.environ["DJANGO_SETTINGS_MODULE"] = "settings"


class XMLWriter:
    """Helper class to write out an xml file"""

    def __init__(self, pretty=True):
        """Set pretty to True if you want an indented XML file"""
        self.output = ""
        self.stack = []
        self.pretty = pretty

    def open(self, tag):
        """Add an open tag"""
        self.stack.append(tag)
        if self.pretty:
            self.output += "  " * (len(self.stack) - 1);
        self.output += "<" + tag + ">"
        if self.pretty:
            self.output += "\n"

    def close(self):
        """Close the innermost tag"""
        if self.pretty:
            self.output += "\n" + "  " * (len(self.stack) - 1);
        tag = self.stack.pop()
        self.output += "</" + tag + ">"
        if self.pretty:
            self.output += "\n"

    def closeAll(self):
        """Close all open tags"""
        while len(self.stack) > 0:
            self.close()

    def content(self, text):
        """Add some content"""
        if self.pretty:
            self.output += "  " * len(self.stack);
        self.output += str(text)

    def save(self, filename):
        """Save the data to a file"""
        self.closeAll()
        fp = open(filename, "w")
        fp.write(self.output)
        fp.close()

def export(request):
    author_resource = AuthorResource()
    dataset = author_resource.export()
    #xml = export_data(dataset)
    #authors = Author.objects.filter(is_deleted=False)
    instance = XML()
    response = HttpResponse(instance.export_data(dataset), content_type='application/xml')
    #response = HttpResponse(dataset.xml, content_type='application/xml')
    response['Content-Disposition'] = 'attachment; filename="authors.xml"'
    return response

def export_xml(request):
    writer = XMLWriter(pretty=False)
    writer.open("djangoexport")
    models = django.apps.apps.get_models()
    for model in models:
        # model._meta.object_name holds the name of the model
        writer.open(model._meta.object_name + "s")
        for item in model.objects.all():
            writer.open(model._meta.object_name)
            for field in item._meta.fields:
                writer.open(field.name)
                value = getattr(item, field.name)
                if value != None:
                    if isinstance(value, django.db.models.base.Model):
                        # This field is a foreign key, so save the primary key
                        # of the referring object
                        pk_name = value._meta.pk.name
                        pk_value = getattr(value, pk_name)
                        writer.content(pk_value)
                    else:
                        writer.content(value)
                writer.close()
            writer.close()
        writer.close()
    writer.close()
    writer.save("export.xml")
    return HttpResponse("Export succesfull!")

@login_required(login_url='/accounts/login/')
def date_precision_process(request):
    post_mutable = {'date_precision': request.POST['date_precision']}
    form = Date_precision_form(post_mutable or None, instance=None)
    if request.method == 'POST':
        if form.is_valid():
            instance = form.save()
            return HttpResponse()
    return render(request, 'error_template.html', {'form': form}, status=500)

@login_required(login_url='/accounts/login/')
def genre_process(request):
    post_mutable = {'genre_description': request.POST['genre_description']}
    form = GenreForm(post_mutable or None, instance=None)
    if request.method == 'POST':
        if form.is_valid():
            instance = form.save()
            return HttpResponse()
    return render(request, 'error_template.html', {'form': form}, status=500)

@login_required(login_url='/accounts/login/')
def location_time_process(request, pk=None, lt=None):
    data = dict()
    obj, created = Location_time.objects.get_or_create(pk=lt)

    post_mutable = {'geo_location_name': request.POST['geo_location_name'], 'fr_province': request.POST['fr_province'], \
                    'date': request.POST['date'], 'date_precision_id': request.POST['date_precision_id']}

    form = LocationTimeForm(post_mutable or None, instance=obj)

    if request.method == 'POST':
        if form.is_valid():
            instance = form.save()
            author = Author.objects.get(pk=pk)
            author.location_time_list.add(instance)
            author.save()
            if pk:
                data['table'] = render_to_string(
                    '_location_time_table.html',
                    {'author': author},
                    request=request
                )
                return JsonResponse(data)

    return render(request, 'error_template.html', {'form': form}, status=500)

@login_required(login_url='/accounts/login/')
def location_time_link(request, pk=None, lt=None):
    data = dict()
    if lt and pk:
        author = Author.objects.get(pk=pk)
        location_time = Location_time.objects.get(pk=lt)
        if not location_time in author.location_time_list.all():
            author.location_time_list.add(location_time)
            author.save()
            location_time.save()
            data['table'] = render_to_string(
                '_location_time_table.html',
                {'author': author},
                request=request
            )
            return JsonResponse(data)
        else:
            data['table'] = render_to_string(
                '_location_time_table.html',
                {'author': author},
                request=request
            )
            return JsonResponse(data)
        return HttpResponse(409)

@login_required(login_url='/accounts/login/')
def location_time_unlink(request, pk=None, lt=None):
    data = dict()
    if lt and pk:
        author = Author.objects.get(pk=pk)
        location_time = Location_time.objects.get(pk=lt)
        if location_time in author.location_time_list.all():
            author.location_time_list.remove(location_time)
            author.save()
            data['table'] = render_to_string(
                '_location_time_table.html',
                {'author': author},
                request=request
            )
            return JsonResponse(data)
        else:
            return HttpResponse(409)

@login_required(login_url='/accounts/login/')
def location_time_search(request, pk=None):
    data = dict()
    if request.method == 'POST':
        if pk:
            if 'input' in request.POST:
                input = request.POST['input']
                location_times = Location_time.objects.filter(geo_location_name__icontains=input).order_by('geo_location_name')[:10]
            else:
                location_times = Location_time.objects.none()
            author = Author.objects.get(pk=pk)
            data['table'] = render_to_string(
                '_location_time_candidates_table.html',
                {'location_times': location_times, 'author': author},
                request=request
            )
            return JsonResponse(data)

@login_required(login_url='/accounts/login/')
def select2_date_precision_id(request):
    query = request.GET.get('term', None)
    if query:
        date_precision = Date_precision.objects.filter(date_precision__icontains=query).values("pk", "date_precision")
    else:
        date_precision = Date_precision.objects.values("pk", "date_precision")
    date_precision = list(date_precision)
    for d in date_precision:
        d['id'] = d.pop('pk')
        d['text'] = d.pop('date_precision')
    return JsonResponse({'results':date_precision}, safe=False)

@login_required(login_url='/accounts/login/')
def work_process(request, pk=None, w=None):
    data = dict()
    obj, created = Works.objects.get_or_create(pk=w)

    if request.POST['year'] == 'None':
        year = None
    else:
        year = request.POST['year']

    post_mutable = {'text': obj.text, 'year': year, 'title': request.POST['title'], \
                    'publisher': request.POST['publisher'], 'location': request.POST['location'], \
                    'detail_descriptions': request.POST['detail_descriptions'], 'date_precision_id': \
                    request.POST['date_precision_id'], 'genre_id': request.POST['genre_id']}

    #pdb.set_trace()
    form = WorkForm(post_mutable or None, instance=obj)

    if request.method == 'POST':
        if form.is_valid():
            instance = form.save()
            author = Author.objects.get(pk=pk)
            author.works_author_list.add(instance)
            author.save()
            if pk:
                data['table'] = render_to_string(
                    '_works_table.html',
                    {'author': author},
                    request=request
                )
                return JsonResponse(data)

    return render(request, 'error_template.html', {'form': form}, status=500)

@login_required(login_url='/accounts/login/')
def work_link(request, pk=None, w=None):
    data = dict()
    if w and pk:
        author = Author.objects.get(pk=pk)
        work = Works.objects.get(pk=w)
        if not work in author.works_author_list.all():
            author.works_author_list.add(work)
            author.save()
            work.save()
            data['table'] = render_to_string(
                '_works_table.html',
                {'author': author},
                request=request
            )
            return JsonResponse(data)
        else:
            data['table'] = render_to_string(
                '_works_table.html',
                {'author': author},
                request=request
            )
            return JsonResponse(data)
        return HttpResponse(409)

@login_required(login_url='/accounts/login/')
def work_unlink(request, pk=None, w=None):
    data = dict()
    if w and pk:
        author = Author.objects.get(pk=pk)
        work = Works.objects.get(pk=w)
        if work in author.works_author_list.all():
            author.works_author_list.remove(work)
            author.save()
            data['table'] = render_to_string(
                '_works_table.html',
                {'author': author},
                request=request
            )
            return JsonResponse(data)
        else:
            return HttpResponse(409)

@login_required(login_url='/accounts/login/')
def work_search(request, pk=None):
    data = dict()
    if request.method == 'POST':
        if pk:
            if 'input' in request.POST:
                input = request.POST['input']
                work = Works.objects.filter(Q(title__icontains=input) | Q(text__icontains=input)).order_by('title')[:10]
            else:
                work = Works.objects.none()
            author = Author.objects.get(pk=pk)
            data['table'] = render_to_string(
                '_works_candidates_table.html',
                {'works': work, 'author': author},
                request=request
            )
            #pdb.set_trace()
            return JsonResponse(data)

@login_required(login_url='/accounts/login/')
def birth_dates_search(request, pk=None):
    data = dict()
    if request.method == 'POST':
        if pk:
            author = Author.objects.get(pk=pk)
            if 'input' in request.POST:
                input = request.POST['input']
                birth_dates = author.birth_dates.filter(date_precision__icontains=input).order_by('date_precision')[:10]
            else:
                birth_dates = Date_precision.objects.none()

            data['table'] = render_to_string(
                '_birth_Dates_candidates_table.html',
                {'birth_dates': birth_dates, 'author': author},
                request=request
            )
            return JsonResponse(data)

@login_required(login_url='/accounts/login/')
def select2_genre_id(request):
    query = request.GET.get('term', None)
    if query:
        genre = Genre.objects.filter(genre_description__icontains=query).values("pk", "genre_description")
    else:
        genre = Genre.objects.values("pk", "genre_description")
    genre = list(genre)
    for d in genre:
        d['id'] = d.pop('pk')
        d['text'] = d.pop('genre_description')
    return JsonResponse({'results':genre}, safe=False)

@login_required(login_url='/accounts/login/')
def alias_process(request, pk=None, a=None):
    data = dict()
    obj, created = Alias.objects.get_or_create(pk=a)

    post_mutable = {'alias': request.POST['alias']}

    form = AliasForm(post_mutable or None, instance=obj)

    if request.method == 'POST':
        if form.is_valid():
            instance = form.save()
            author = Author.objects.get(pk=pk)
            author.alias_list.add(instance)
            author.save()
            if pk:
                data['table'] = render_to_string(
                    '_aliases_table.html',
                    {'author': author},
                    request=request
                )
                return JsonResponse(data)

    return render(request, 'error_template.html', {'form': form}, status=500)

@login_required(login_url='/accounts/login/')
def alias_link(request, pk=None, apk=None):
    data = dict()
    if apk and pk:
        author = Author.objects.get(pk=pk)
        al = Alias.objects.get(pk=apk)
        if al not in author.alias_list.all():
            author.alias_list.add(al)
            author.save()
            al.save()

            data['table'] = render_to_string(
                '_aliases_table.html',
                {'author': author},
                request=request
            )
            return JsonResponse(data)
        else:
            data['table'] = render_to_string(
                '_aliases_table.html',
                {'author': author},
                request=request
            )
            return JsonResponse(data)
        return HttpResponse(409)

@login_required(login_url='/accounts/login/')
def alias_unlink(request, pk=None, a=None):
    data = dict()
    if a and pk:
        author = Author.objects.get(pk=pk)
        alias = Alias.objects.get(pk=a)
        if alias in author.alias_list.all():
            author.alias_list.remove(alias)
            author.save()
            data['table'] = render_to_string(
                '_aliases_table.html',
                {'author': author},
                request=request
            )
            return JsonResponse(data)
        else:
            return HttpResponse(409)

@login_required(login_url='/accounts/login/')
def alias_search(request, pk=None):
    data = dict()
    if request.method == 'POST':
        if pk:
            if 'input' in request.POST:
                input = request.POST['input']
                alias = Alias.objects.filter(alias__icontains=input).order_by('alias')[:10]
            else:
                alias = Alias.objects.none()
            author = Author.objects.get(pk=pk)
            data['table'] = render_to_string(
                '_aliases_candidates_table.html',
                {'aliases': alias, 'author': author},
                request=request
            )
            return JsonResponse(data)

@login_required(login_url='/accounts/login/')
def literature_process(request, pk=None, lit=None):
    data = dict()
    obj, created = Literature.objects.get_or_create(pk=lit)

    post_mutable = {'lit_text': request.POST['lit_text']}

    form = Literature_form(post_mutable or None, instance=obj)
    #pdb.set_trace()
    if request.method == 'POST':
        if form.is_valid():
            instance = form.save()
            author = Author.objects.get(pk=pk)
            author.literature_list.add(instance)
            author.save()
            if pk:
                data['table'] = render_to_string(
                    '_literatures_table.html',
                    {'author': author},
                    request=request
                )
                return JsonResponse(data)

    return render(request, 'error_template.html', {'form': form}, status=500)

@login_required(login_url='/accounts/login/')
def literature_link(request, pk=None, lit=None):
    data = dict()
    if lit and pk:
        author = Author.objects.get(pk=pk)
        literature = Literature.objects.get(pk=lit)
        if not literature in author.literature_list.all():
            author.literature_list.add(literature)
            author.save()
            literature.save()
            data['table'] = render_to_string(
                '_literatures_table.html',
                {'author': author},
                request=request
            )
            #pdb.set_trace()
            return JsonResponse(data)
        else:
            data['table'] = render_to_string(
                '_literatures_table.html',
                {'author': author},
                request=request
            )
            return JsonResponse(data)
        return HttpResponse(409)

@login_required(login_url='/accounts/login/')
def literature_unlink(request, pk=None, lit=None):
    data = dict()
    if lit and pk:
        author = Author.objects.get(pk=pk)
        literature = Literature.objects.get(pk=lit)
        if literature in author.literature_list.all():
            author.literature_list.remove(literature)
            author.save()
            data['table'] = render_to_string(
                '_literatures_table.html',
                {'author': author},
                request=request
            )
            return JsonResponse(data)
        else:
            return HttpResponse(409)

@login_required(login_url='/accounts/login/')
def literature_search(request, pk=None):
    data = dict()
    if request.method == 'POST':
        if pk:
            if 'input' in request.POST:
                input = request.POST['input']
                literature = Literature.objects.filter(lit_text__icontains=input).order_by('lit_text')[:10]
            else:
                literature = Literature.objects.none()
            author = Author.objects.get(pk=pk)

            data['table'] = render_to_string(
                '_literatures_candidates_table.html',
                {'literature': literature, 'author': author},
                request=request
            )
            #pdb.set_trace()
            return JsonResponse(data)
@login_required(login_url='/accounts/login/')
def genre_process2(request, pk=None, g=None):
    data = dict()
    obj, created = Genre.objects.get_or_create(pk=g)

    post_mutable = {'genre_description': request.POST['genre_description']}

    form = GenreForm(post_mutable or None, instance=obj)

    if request.method == 'POST':
        if form.is_valid():
            instance = form.save()
            genre_group = Genre_group.objects.get(pk=pk)
            genre_group.genre.add(instance)
            genre_group.save()
            if pk:
                data['table'] = render_to_string(
                    '_genres_table.html',
                    {'genre_group': genre_group},
                    request=request
                )
                return JsonResponse(data)

    return render(request, 'error_template.html', {'form': form}, status=500)

@login_required(login_url='/accounts/login/')
def genre_link(request, pk=None, g=None):
    data = dict()
    if g and pk:
        genre_group = Genre_group.objects.get(pk=pk)
        genre = Genre.objects.get(pk=g)
        #pdb.set_trace()
        if genre not in genre_group.genre.all():
            genre_group.genre.add(genre)
            genre_group.save()
            genre.save()
            data['table'] = render_to_string(
                '_genres_table.html',
                {'genre_group': genre_group},
                request=request
            )
            return JsonResponse(data)
        else:
            data['table'] = render_to_string(
                '_genres_table.html',
                {'genre_group': genre_group},
                request=request
            )
            return JsonResponse(data)
        return HttpResponse(409)

@login_required(login_url='/accounts/login/')
def genre_unlink(request, pk=None, g=None):
    data = dict()
    if g and pk:
        genre_group = Genre_group.objects.get(pk=pk)
        genre = Genre.objects.get(pk=g)
        if  genre in genre_group.genre.all():
            genre_group.genre.remove(genre)
            genre_group.save()
            data['table'] = render_to_string(
                '_genres_table.html',
                {'genre_group': genre_group},
                request=request
            )
            return JsonResponse(data)
        else:
            return HttpResponse(409)

@login_required(login_url='/accounts/login/')
def genre_search(request, pk=None):
    data = dict()
    #pdb.set_trace()
    if request.method == 'POST':
        if pk:
            if 'input' in request.POST:
                input = request.POST['input']
                genres = Genre.objects.filter(genre_description__icontains=input).order_by('genre_description')[:10]
            else:
                genres = Genre.objects.none()
            genre_group = Genre_group.objects.get(pk=pk)
            data['table'] = render_to_string(
                '_genres_candidates_table.html',
                {'genres': genres, 'genre_group': genre_group},
                request=request
            )
            return JsonResponse(data)

@login_required(login_url='/accounts/login/')
def genre_group_process(request, pk=None, g=None):
    data = dict()
    obj, created = Genre_group.objects.get_or_create(pk=g)

    post_mutable = {'genre_group': request.POST['genre_group']}

    form = Genre_group_form(post_mutable or None, instance=obj)

    if request.method == 'POST':
        if form.is_valid():
            instance = form.save()
            genre = Genre.objects.get(pk=pk)
            genre.genre_group_genres.add(instance)
            genre.save()
            if pk:
                data['table'] = render_to_string(
                    '_genre_groups_table.html',
                    {'genre': genre},
                    request=request
                )
                return JsonResponse(data)

    return render(request, 'error_template.html', {'form': form}, status=500)

@login_required(login_url='/accounts/login/')
def genre_group_link(request, pk=None, g=None):
    data = dict()
    if g and pk:
        genre = Genre.objects.get(pk=pk)
        genre_group = Genre_group.objects.get(pk=g)
        if not genre_group in genre.genre_group_genres.all():
            genre.genre_group_genres.add(genre_group)
            genre.save()
            genre_group.save()
            data['table'] = render_to_string(
                '_genre_groups_table.html',
                {'genre': genre},
                request=request
            )
            return JsonResponse(data)
        else:
            data['table'] = render_to_string(
                '_genre_groups_table.html',
                {'genre': genre},
                request=request
            )
            return JsonResponse(data)
        return HttpResponse(409)

@login_required(login_url='/accounts/login/')
def genre_group_unlink(request, pk=None, g=None):
    data = dict()
    if g and pk:
        genre = Genre.objects.get(pk=pk)
        genre_group = Genre_group.objects.get(pk=g)
        if genre_group in genre.genre_group_genres.all():
            genre.genre_group_genres.remove(genre_group)
            genre.save()
            data['table'] = render_to_string(
                '_genre_groups_table.html',
                {'genre': genre},
                request=request
            )
            return JsonResponse(data)
        else:
            return HttpResponse(409)

@login_required(login_url='/accounts/login/')
def genre_group_search(request, pk=None):
    data = dict()
    if request.method == 'POST':
        if pk:
            if 'input' in request.POST:
                input = request.POST['input']
                genre_groups = Genre_group.objects.filter(genre_group__icontains=input).order_by('genre_group')[:10]
            else:
                genre_groups = Genre_group.objects.none()
            genre = Genre.objects.get(pk=pk)
            data['table'] = render_to_string(
                '_genre_groups_candidates_table.html',
                {'genre_groups': genre_groups, 'genre': genre},
                request=request
            )
            return JsonResponse(data)

class DatePrecisionShow(ListView):
    model = Date_precision
    context_object_name = 'date_precisions'
    Date_precision = Date_precision.objects.all()
    paginate_by = 10

    def get_template_names(self):
        return ['date_precision_show.html']

    def get_ordering(self):
        ordering = self.request.GET.get('order_by')
        direction = self.request.GET.get('direction')
        if ordering is not None and ordering != "" and direction is not None and direction != "":
            if direction == 'desc':
                ordering = '-{}'.format(ordering)
        return ordering

    def get_context_data(self, **kwargs):
        context = super(DatePrecisionShow, self).get_context_data(**kwargs)
        order_by = self.request.GET.get('order_by')
        if order_by is not None and order_by != "":
            context['order_by'] = order_by
            context['direction'] = self.request.GET.get('direction')
        else:
            context['order_by'] = ''
            context['direction'] = ''
        return context

class DatePrecisionCreate(CreateView):
    '''
    Inherits CreateView uses a standard form for date_precision.
    redirects to the date_precision main page (show).
    '''
    template_name = 'authors/form.html'
    form_class = Date_precision_form

    def get_success_url(self):
        """Detect the submit button used and act accordingly"""
        if self.request.POST.get("save_add_another"):
            return '/date_precision/new/'
        elif self.request.POST.get("save_and_continue_editing") :
            return '/date_precision/' + str(self.object.pk) + '/edit/'
        elif self.request.POST.get("save"):
            url = self.request.GET.get('next')
            if self.request.GET.get('page'):
                url += '&page=' + self.request.GET.get('page')
            if self.request.GET.get('order_by'):
                url += '&order_by=' + self.request.GET.get('order_by')
            if self.request.GET.get('direction'):
                url += '&direction=' + self.request.GET.get('direction')
            if not url:
                return '/date_precision/show/'
            return url

class DatePrecisionUpdate(UpdateView):
    '''
    Inherits UpdateView uses a standard form (crispy form)
    Uses KeywordForm as layout. And model Keyword.
    redirects to local main page. (show)
    '''
    template_name = 'authors/form.html'
    form_class = Date_precision_form
    model = Date_precision

    def get_success_url(self):
        """Detect the submit button used and act accordingly"""
        if self.request.POST.get("save_add_another"):
            return '/date_precision/new/'
        elif self.request.POST.get("save_and_continue_editing") :
            return '/date_precision/' + str(self.object.pk) + '/edit/'
        elif self.request.POST.get("save"):
            url = self.request.GET.get('next')
            if self.request.GET.get('page'):
                url += '&page=' + self.request.GET.get('page')
            if self.request.GET.get('order_by'):
                url += '&order_by=' + self.request.GET.get('order_by')
            if self.request.GET.get('direction'):
                url += '&direction=' + self.request.GET.get('direction')
            if not url:
                return '/date_precision/show/'
            return url

@login_required(login_url='/accounts/login/')
def DatePrecisionDelete(request, pk):
    '''
    Arguments: request, pk
    Selects Date_precision object by id equals pk.
    Deletes the object.
    redirects to main page. (show)
    '''
    date_precision = Date_precision.objects.get(id=pk)
    date_precision.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

class GenreShow(ListView):
    model = Genre
    context_object_name = 'genres'
    genres = Genre.objects.all()
    paginate_by = 10

    def get_template_names(self):
        return ['genre_show.html']

    def get_ordering(self):
        ordering = self.request.GET.get('order_by')
        direction = self.request.GET.get('direction')
        if ordering is not None and ordering != "" and direction is not None and direction != "":
            if direction == 'desc':
                ordering = '-{}'.format(ordering)
        return ordering

    def get_context_data(self, **kwargs):
        context = super(GenreShow, self).get_context_data(**kwargs)
        order_by = self.request.GET.get('order_by')
        if order_by is not None and order_by != "":
            context['order_by'] = order_by
            context['direction'] = self.request.GET.get('direction')
        else:
            context['order_by'] = ''
            context['direction'] = ''
        return context

class GenreCreate(UpdateView):
    '''
    Inherits CreateView. Uses GenreForm as layout.
    redirects to main page (show)
    '''
    template_name = 'authors/form.html'
    form_class = GenreForm
    success_url = '/genre/show/'
    model = Genre

    def get_object(self):
        genre = Genre(is_stub=True)
        genre.save()
        return genre

    def form_valid(self, form):
        form.instance.is_stub = False
        # todo: temporal solution for double genre.
        genre = Genre.objects.get(pk=self.object.pk-1)
        form.instance.genre_group_genres.add(*genre.genre_group_genres.all())

        if form.is_valid():
            self.object = form.save()
            self.object.save()

        genre.delete()
        return redirect(self.get_success_url())

    def get_success_url(self):
        """Detect the submit button used and act accordingly"""
        if self.request.POST.get("save_add_another"):
            return '/genre/new/'
        elif self.request.POST.get("save_and_continue_editing") :
            return '/genre/' + str(self.object.pk) + '/edit/'
        elif self.request.POST.get("save"):
            url = self.request.GET.get('next')
            if self.request.GET.get('q'):
                url += '?q=' + self.request.GET.get('q')
            if self.request.GET.get('page'):
                url += '&page=' + self.request.GET.get('page')
            if self.request.GET.get('order_by'):
                url += '&order_by=' + self.request.GET.get('order_by')
            if self.request.GET.get('direction'):
                url += '&direction=' + self.request.GET.get('direction')
            if not url:
                return '/genre/show/'
            return url

@login_required(login_url='/accounts/login/')
def GenreDelete(request, pk):
    '''
    Arguments: request, pk
    Selects Genre object by id equals pk.
    Deletes the object.
    redirects to main page. (show)
    '''
    genre = Genre.objects.get(id=pk)
    genre.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

class GenreUpdate(UpdateView):
    '''
    Inherits UpdateView uses a standard form (crispy form)
    Uses GenreForm as layout. And model Genre.
    redirects to local main page. (show)
    '''
    template_name = 'authors/form.html'
    form_class = GenreForm
    model = Genre
    context_object_name = 'genre'

    def form_valid(self, form):

        genre = Genre.objects.get(pk=self.object.pk)
        form.instance.genre_group_genres.add(*genre.genre_group_genres.all())

        if form.is_valid():
            self.object = form.save()
            self.object.save()

        return redirect(self.get_success_url())

    def get_success_url(self):
        """Detect the submit button used and act accordingly"""
        if self.request.POST.get("save_add_another"):
            return '/genre/new/'
        elif self.request.POST.get("save_and_continue_editing") :
            return '/genre/' + str(self.object.pk) + '/edit/'
        elif self.request.POST.get("save"):
            url = self.request.GET.get('next')
            if self.request.GET.get('q'):
                url += '?q=' + self.request.GET.get('q')
            if self.request.GET.get('page'):
                url += '&page=' + self.request.GET.get('page')
            if self.request.GET.get('order_by'):
                url += '&order_by=' + self.request.GET.get('order_by')
            if self.request.GET.get('direction'):
                url += '&direction=' + self.request.GET.get('direction')
            if not url:
                return '/genre/show/'
            return url

class LocationTimeShow(ListView):
    model = Location_time
    context_object_name = 'location_times'
    genres = Location_time.objects.all()
    paginate_by = 10

    def get_template_names(self):
        return ['location_time_show.html']

    def get_ordering(self):
        ordering = self.request.GET.get('order_by')
        direction = self.request.GET.get('direction')
        if ordering is not None and ordering != "" and direction is not None and direction != "":
            if direction == 'desc':
                ordering = '-{}'.format(ordering)
        return ordering

    def get_context_data(self, **kwargs):
        context = super(LocationTimeShow, self).get_context_data(**kwargs)
        order_by = self.request.GET.get('order_by')
        if order_by is not None and order_by != "":
            context['order_by'] = order_by
            context['direction'] = self.request.GET.get('direction')
        else:
            context['order_by'] = ''
            context['direction'] = ''
        return context

class LocationTimeCreate(CreateView):
    '''
    Inherits CreateView. Uses GenreForm as layout.
    redirects to main page (show)
    '''
    template_name = 'authors/form.html'
    form_class = LocationTimeForm
    success_url = '/location_time/show/'
    model = Location_time

    def get_success_url(self):
        """Detect the submit button used and act accordingly"""
        if self.request.POST.get("save_add_another"):
            return '/location_time/new/'
        elif self.request.POST.get("save_and_continue_editing") :
            return '/location_time/' + str(self.object.pk) + '/edit/'
        elif self.request.POST.get("save"):
            url = self.request.GET.get('next')
            if self.request.GET.get('q'):
                url += '?q=' + self.request.GET.get('q')
            if self.request.GET.get('page'):
                url += '&page=' + self.request.GET.get('page')
            if self.request.GET.get('order_by'):
                url += '&order_by=' + self.request.GET.get('order_by')
            if self.request.GET.get('direction'):
                url += '&direction=' + self.request.GET.get('direction')
            if not url:
                return '/location_time/show/'
            return url

@login_required(login_url='/accounts/login/')
def LocationTimeDelete(request, pk):
    '''
    Arguments: request, pk
    Selects LocationTime object by id equals pk.
    Deletes the object.
    redirects to main page. (show)
    '''
    location_time = Location_time.objects.get(id=pk)
    location_time.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

class LocationTimeUpdate(UpdateView):
    '''
    Inherits UpdateView uses a standard form (crispy form)
    Uses LocationTimeForm as layout. And model Location.
    redirects to local main page. (show)
    '''
    template_name = 'authors/form.html'
    form_class = LocationTimeForm
    model = Genre
    context_object_name = 'location_time'


    def get_success_url(self):
        """Detect the submit button used and act accordingly"""
        if self.request.POST.get("save_add_another"):
            return '/location_time/new/'
        elif self.request.POST.get("save_and_continue_editing") :
            return '/location_time/' + str(self.object.pk) + '/edit/'
        elif self.request.POST.get("save"):
            url = self.request.GET.get('next')
            if self.request.GET.get('q'):
                url += '?q=' + self.request.GET.get('q')
            if self.request.GET.get('page'):
                url += '&page=' + self.request.GET.get('page')
            if self.request.GET.get('order_by'):
                url += '&order_by=' + self.request.GET.get('order_by')
            if self.request.GET.get('direction'):
                url += '&direction=' + self.request.GET.get('direction')
            if not url:
                return '/location_time/show/'
            return url

class GenreGroupShow(ListView):
    model = Genre_group
    context_object_name = 'genre_groups'
    genre_groups = Genre_group.objects.all()
    paginate_by = 10

    def get_template_names(self):
        return ['genre_group_show.html']

    def get_ordering(self):
        ordering = self.request.GET.get('order_by')
        direction = self.request.GET.get('direction')
        if ordering is not None and ordering != "" and direction is not None and direction != "":
            if direction == 'desc':
                ordering = '-{}'.format(ordering)
        return ordering

    def get_context_data(self, **kwargs):
        context = super(GenreGroupShow, self).get_context_data(**kwargs)
        order_by = self.request.GET.get('order_by')
        if order_by is not None and order_by != "":
            context['order_by'] = order_by
            context['direction'] = self.request.GET.get('direction')
        else:
            context['order_by'] = ''
            context['direction'] = ''
        return context

class GenreGroupCreate(UpdateView):
    '''
    Inherits CreateView. Uses GenreForm as layout.
    redirects to main page (show)
    '''
    template_name = 'authors/form.html'
    form_class = Genre_group_form
    success_url = '/genre_group/show/'
    model = Genre_group

    def get_object(self):
        genre_group = Genre_group()
        genre_group.save()
        return genre_group

    def form_valid(self, form):
        # todo: temporal solution for double genre.
        genre_group = Genre_group.objects.get(pk=self.object.pk-1)
        form.instance.genre.add(*genre_group.genre.all())
        #pdb.set_trace()

        if form.is_valid():
            self.object = form.save()
            self.object.save()

        genre_group.delete()
        return redirect(self.get_success_url())

    def get_success_url(self):
        """Detect the submit button used and act accordingly"""
        if self.request.POST.get("save_add_another"):
            return '/genre_group/new/'
        elif self.request.POST.get("save_and_continue_editing") :
            return '/genre_group/' + str(self.object.pk) + '/edit/'
        elif self.request.POST.get("save"):
            url = self.request.GET.get('next')
            if self.request.GET.get('q'):
                url += '?q=' + self.request.GET.get('q')
            if self.request.GET.get('page'):
                url += '&page=' + self.request.GET.get('page')
            if self.request.GET.get('order_by'):
                url += '&order_by=' + self.request.GET.get('order_by')
            if self.request.GET.get('direction'):
                url += '&direction=' + self.request.GET.get('direction')
            if not url:
                return '/genre_group/show/'
            return url

@login_required(login_url='/accounts/login/')
def GenreGroupDelete(request, pk):
    '''
    Arguments: request, pk
    Selects Genre object by id equals pk.
    Deletes the object.
    redirects to main page. (show)
    '''
    genre_group = Genre_group.objects.get(id=pk)
    genre_group.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

class GenreGroupUpdate(UpdateView):
    '''
    Inherits UpdateView uses a standard form (crispy form)
    Uses GenreForm as layout. And model Genre.
    redirects to local main page. (show)
    '''
    template_name = 'authors/form.html'
    form_class = Genre_group_form
    model = Genre_group
    context_object_name = 'genre_group'

    def form_valid(self, form):

        genre_group = Genre_group.objects.get(pk=self.object.pk)
        form.instance.genre.add(*genre_group.genre.all())

        if form.is_valid():
            self.object = form.save()
            self.object.save()

        return redirect(self.get_success_url())

    def get_success_url(self):
        """Detect the submit button used and act accordingly"""
        if self.request.POST.get("save_add_another"):
            return '/genre_group/new/'
        elif self.request.POST.get("save_and_continue_editing") :
            return '/genre_group/' + str(self.object.pk) + '/edit/'
        elif self.request.POST.get("save"):
            url = self.request.GET.get('next')
            if self.request.GET.get('q'):
                url += '?q=' + self.request.GET.get('q')
            if self.request.GET.get('page'):
                url += '&page=' + self.request.GET.get('page')
            if self.request.GET.get('order_by'):
                url += '&order_by=' + self.request.GET.get('order_by')
            if self.request.GET.get('direction'):
                url += '&direction=' + self.request.GET.get('direction')
            if not url:
                return '/genre_group/show/'
            return url

class SearchResultsViewWorks(ListView):
    model = Works
    context_object_name = 'works'
    works = Works.objects.all()
    paginate_by = 10

    def get_template_names(self):
        return ['works_show.html']

    def get_ordering(self):
        ordering = self.request.GET.get('order_by')
        direction = self.request.GET.get('direction')
        if ordering is not None and ordering != "" and direction is not None and direction != "":
            if direction == 'desc':
                ordering = '-{}'.format(ordering)
        return ordering

    def get_queryset(self):
        #authors = self.request.GET.getlist('authors')
        works = Works.objects.all()
        '''
        date_precision = self.request.GET.getlist('date_precision')
        date_precision = Date_precision.objects.filter(pk__in=date_precision).all()
        '''

        exclude = ['csrfmiddlewaretoken','search', 'order_by', 'direction']
        in_variables = []
        special_case = ['copyrights', 'page', 'is_a_translation']

        if ('q' in self.request.GET) and self.request.GET['q'].strip():
            query_string = self.request.GET['q']


            search_fields = ['author__author_name', 'author__biography', 'author__birth', 'author__death', \
                             'author__birth_date_precision__date_precision', 'author__death_date_precision__date_precision',\
                             'year', 'title', 'publisher', 'location', 'detail_descriptions', 'date_precision__date_precision', \
                             'genre__genre_description', 'text',\
                             'genre__genre_group_genres__genre_group',]
            entry_query = get_query(query_string, search_fields)
            works = works.filter(Q(entry_query))
            ordering = self.get_ordering()
            if ordering is not None and ordering != "":
                works = works.order_by(ordering)
            works = works.distinct()
            return works

        for field_name in self.request.GET:
            get_value = self.request.GET.get(field_name)
            if get_value != "" and not field_name in exclude and not field_name in [i[0] for i in in_variables] and\
               not field_name in special_case:
                get_value = get_query(get_value, [field_name])
                works = works.filter(Q(get_value))

        for field_name, list_object in in_variables:
            if list_object:
                if list(list_object) != ['']:

                    works = works.filter(**{field_name+'__in': list_object})

        ordering = self.get_ordering()
        return works

    def get_context_data(self, **kwargs):
        context = super(SearchResultsViewWorks, self).get_context_data(**kwargs)
        order_by = self.request.GET.get('order_by')
        if order_by is not None and order_by != "":
            context['order_by'] = order_by
            context['direction'] = self.request.GET.get('direction')
        else:
            context['order_by'] = ''
            context['direction'] = ''
        q = self.request.GET.get('q')
        if q is not None and q != "":
            context['q'] = q
        else:
            context['q'] = ''
        return context

class WorkCreate(CreateView):
    '''
    inherits CreateView
    Uses template for creating/updating.
    Uses standard edit/new form (WorkForm)
    redirect to author main page (work show)
    '''
    template_name = 'works/form_create.html'
    form_class = WorkForm
    context_object_name = 'works'
    model = Works

    '''
    def get_object(self):
        works = Works()
        works.save()
        return works

   
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.is_stub = False
        # todo: temporal solution for double publication.
        author = Author.objects.get(pk=self.object.pk-1)
        #if author.location_time_set.all():
        form.instance.location_time_set.add(*author.location_time_set.all())

        if form.is_valid():
            self.object = form.save()
            self.object.save()

        author.delete()
        return redirect(self.get_success_url())
    '''
    def get_success_url(self):
        """Detect the submit button used and act accordingly"""
        if self.request.POST.get("save_add_another"):
            return '/work/new/'
        elif self.request.POST.get("save_and_continue_editing") :
            return '/work/' + str(self.object.pk) + '/edit/'
        elif self.request.POST.get("save"):
            url = self.request.GET.get('next')
            if self.request.GET.get('q'):
                url += '?q=' + self.request.GET.get('q')
            if self.request.GET.get('page'):
                url += '&page=' + self.request.GET.get('page')
            if self.request.GET.get('order_by'):
                url += '&order_by=' + self.request.GET.get('order_by')
            if self.request.GET.get('direction'):
                url += '&direction=' + self.request.GET.get('direction')
            if not url:
                return '/work/show/'
            return url

class WorkUpdate(UpdateView):
    '''
    Inherits UpdateView
    Uses edit/create template and the edit/create NewCrispyForm
    Uses Publication as model
    redirects to main page of work (work show)
    '''
    template_name = 'works/form_update.html'
    form_class = WorkForm
    model = Works
    context_object_name = 'works'

    def get_success_url(self):
        url = self.request.GET.get('next')
        if self.request.GET.get('q'):
            url += '?q=' + self.request.GET.get('q')
        if self.request.GET.get('page'):
            url += '&page=' + self.request.GET.get('page')
        if self.request.GET.get('order_by'):
            url += '&order_by=' + self.request.GET.get('order_by')
        if self.request.GET.get('direction'):
            url += '&direction=' + self.request.GET.get('direction')
        return url

    def form_valid(self, form):
        if form.is_valid():
            self.object = form.save()
            self.object.save()
        return redirect(self.get_success_url())


@login_required(login_url='/accounts/login/')
def WorkDelete(request, pk):
    '''
    Deletes a work
    argument pk int value of the id of the to be deleted author
    redirect to main author page (Show)
    '''
    work = Works.objects.get(id=pk)
    work.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

class WorkDetailView(DetailView):
    '''
    Inherits DetailView
    Detailview for works
    Usess now in template thus the function get_context_data
    '''
    model = Works
    context_object_name = 'works'

class MainView(ListView):
    def get_template_names(self):
        return ['main.html']

class SearchResultsView(ListView):
    '''
    ListView of the initial search page.
    The function get_queryset works for the search bar and the search form home page.
    The search bar typically uses q for query otherwise a id for list search.
    Use a countries_dict to convert for example Netherlands to NL so that search succeeds.
    If a normal field is searched use __icontains if a list element is searched use: __in.
    '''
    model = Author
    context_object_name = 'authors'
    authors = Author.objects.all()
    #paginate_by = 1

    def get_template_names(self):
        return ['show.html']

    def post(self, request, *args, **kwargs):
        return export(request)

    def get_ordering(self):
        ordering = self.request.GET.get('order_by')
        direction = self.request.GET.get('direction')
        if ordering is not None and ordering != "" and direction is not None and direction != "":
            if direction == 'desc':
                ordering = '-{}'.format(ordering)
        return ordering

    def get_queryset(self):
        #authors = self.request.GET.getlist('authors')
        authors = Author.objects.filter(is_deleted=False, is_stub=False)
        '''
        birth_date_precision = self.request.GET.getlist('birth_date_precision')
        birth_date_precision = Date_precision.objects.filter(pk__in=birth_date_precision).all()
        death_date_precision = self.request.GET.getlist('death_date_precision')
        death_date_precision = Date_precision.objects.filter(pk__in=death_date_precision).all()
        '''

        exclude = ['csrfmiddlewaretoken','search', 'order_by', 'direction']
        in_variables = []
        special_case = ['copyrights', 'page', 'is_a_translation']

        if ('q' in self.request.GET) and self.request.GET['q'].strip():
            query_string = self.request.GET['q']


            search_fields = ['author_name', 'biography', 'birth', 'death', 'birth_date_precision__date_precision', 'death_date_precision__date_precision',\
                             'location_time_list__geo_location_name', 'location_time_list__date', 'location_time_list__fr_province', \
                             'literature_list__lit_text', 'alias_list__alias', 'works_author_list__year', 'works_author_list__title', \
                             'works_author_list__publisher', 'works_author_list__location', 'works_author_list__detail_descriptions', \
                             'works_author_list__text']
            entry_query = get_query(query_string, search_fields)
            authors = authors.filter(Q(entry_query))
            ordering = self.get_ordering()
            if ordering is not None and ordering != "":
                authors = authors.order_by(ordering)
            authors = authors.distinct()
            return authors

        for field_name in self.request.GET:
            get_value = self.request.GET.get(field_name)
            if get_value != "" and not field_name in exclude and not field_name in [i[0] for i in in_variables] and\
               not field_name in special_case:
                get_value = get_query(get_value, [field_name])
                authors = authors.filter(Q(get_value))

        for field_name, list_object in in_variables:
            if list_object:
                if list(list_object) != ['']:

                    authors = authors.filter(**{field_name+'__in': list_object})

        ordering = self.get_ordering()
        return authors

    def get_context_data(self, **kwargs):
        context = super(SearchResultsView, self).get_context_data(**kwargs)
        queryset = self.get_queryset()
        alphabet_string = string.ascii_lowercase
        alphabet_list = list(alphabet_string)
        if ('q' in self.request.GET) and self.request.GET['q'].strip():
            pages = [queryset]
        else:
            pages = [queryset.filter(Q(author_name__istartswith=i) | Q(alias_list__alias__istartswith=i)) for i in alphabet_list]
        context['pages'] = pages
        #paginator = Paginator(pages, self.paginate_by)
        page = self.request.GET.get('page')
        q_in = False
        if ('q' in self.request.GET) and self.request.GET['q'].strip():
            q_in = True
            page = self.request.GET['q'][0].lower()

            '''
            try:
                #pdb.set_trace()
                page = queryset[0].author_name[0].lower()
            except IndexError:
                page = queryset[0].alias_list[0].alias[0].lower()
           '''
        if page:
            page = string.ascii_lowercase.index(page) + 1
        elif not page:
            page = 1


        #pdb.set_trace()
        #pdb.set_trace()
        try:
            page_authors = pages[int(page)-1]
        except IndexError:
            page_authors = pages[0]
            if not q_in:
                page = 1
        if page == 1:
            previous = -1
        else:
            previous = string.ascii_lowercase[page-2]
        if page == 26:
            next = -1
        else:
            next = string.ascii_lowercase[page]

        context['first'] = 'a'
        context['last'] = 'z'
        context['next'] = next
        context['previous'] = previous
        context['current'] = string.ascii_lowercase[page-1].upper()
        context['page_authors'] = page_authors
        context['alphabet_list'] = alphabet_list

        order_by = self.request.GET.get('order_by')
        if order_by is not None and order_by != "":
            context['order_by'] = order_by
            context['direction'] = self.request.GET.get('direction')
        else:
            context['order_by'] = ''
            context['direction'] = ''
        '''
        q = self.request.GET.get('q')
        if q is not None and q != "":
            context['q'] = q
        else:
            context['q'] = ''
        '''

        #pdb.set_trace()
        return context

class AuthorCreate(UpdateView):
    '''
    inherits CreateView
    Uses template for creating/updating.
    Uses standard edit/new form (AuthorForm)
    redirect to author main page (author show)
    '''
    template_name = 'authors/form_create.html'
    form_class = AuthorForm
    context_object_name = 'author'
    model = Author

    def get_object(self):
        author = Author(is_stub=True)
        author.save()
        return author

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.is_stub = False
        # todo: temporal solution for double publication.
        author = Author.objects.get(pk=self.object.pk-1)
        #if author.location_time_set.all():
        form.instance.location_time_list.add(*author.location_time_list.all())

        if form.is_valid():
            self.object = form.save()
            self.object.save()

        author.delete()
        return redirect(self.get_success_url())

    def get_success_url(self):
        """Detect the submit button used and act accordingly"""
        if self.request.POST.get("save_add_another"):
            return '/author/new/'
        elif self.request.POST.get("save_and_continue_editing") :
            return '/author/' + str(self.object.pk) + '/edit/'
        elif self.request.POST.get("save"):
            url = self.request.GET.get('next')
            if self.request.GET.get('q'):
                url += '?q=' + self.request.GET.get('q')
            if self.request.GET.get('page'):
                url += '&page=' + self.request.GET.get('page')
            if self.request.GET.get('order_by'):
                url += '&order_by=' + self.request.GET.get('order_by')
            if self.request.GET.get('direction'):
                url += '&direction=' + self.request.GET.get('direction')
            if not url:
                return '/author/show/'
            return url

class AuthorUpdate(UpdateView):
    '''
    Inherits UpdateView
    Uses edit/create template and the edit/create NewCrispyForm
    Uses Publication as model
    redirects to main page of Publication (publication show)
    '''
    template_name = 'authors/form_update.html'
    form_class = AuthorForm
    model = Author
    context_object_name = 'author'

    def get_success_url(self):
        url = self.request.GET.get('next')
        if self.request.GET.get('q'):
            url += '?q=' + self.request.GET.get('q')
        if self.request.GET.get('page'):
            url += '&page=' + self.request.GET.get('page')
        if self.request.GET.get('order_by'):
            url += '&order_by=' + self.request.GET.get('order_by')
        if self.request.GET.get('direction'):
            url += '&direction=' + self.request.GET.get('direction')
        return url

    def form_valid(self, form):
        if form.is_valid():
            self.object = form.save()
            self.object.save()
        return redirect(self.get_success_url())


@login_required(login_url='/accounts/login/')
def AuthorDelete(request, pk):
    '''
    Deletes a author
    argument pk int value of the id of the to be deleted author
    redirect to main author page (Show)
    '''
    author = Author.objects.get(id=pk)
    author.is_deleted = True
    author.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

class AuthorDetailView(DetailView):
    '''
    Inherits DetailView
    Detailview for author
    Usess now in template thus the function get_context_data
    '''
    model = Author
    context_object_name = 'author'

class LocationTimeDetailView(DetailView):
    '''
    Inherits DetailView
    Detailview for location time
    Usess now in template thus the function get_context_data
    '''
    model = Location_time
    context_object_name = 'location_time'

class ThrashbinShow(ListView):
    '''
    Inherits ListView shows author mainpage (ThrashbinShow)
    Uses context_object_name authors for all keywords.
    '''
    model = Author
    template_name = 'authors/thrashbin_show.html'
    context_object_name = 'authors'
    paginate_by = 10

    def get_queryset(self):
        authors = Author.objects.filter(is_deleted=True)
        ordering = self.get_ordering()
        if ordering is not None and ordering != "":
            authors = authors.order_by(ordering)
        return authors

    def get_ordering(self):
        ordering = self.request.GET.get('order_by')
        direction = self.request.GET.get('direction')
        if ordering is not None and ordering != "" and direction is not None and direction != "":
            if direction == 'desc':
                ordering = '-{}'.format(ordering)
        return ordering

    def get_context_data(self, **kwargs):
        context = super(ThrashbinShow, self).get_context_data(**kwargs)
        order_by = self.request.GET.get('order_by')
        if order_by is not None and order_by != "":
            context['order_by'] = order_by
            context['direction'] = self.request.GET.get('direction')
        else:
            context['order_by'] = ''
            context['direction'] = ''
        return context

@login_required(login_url='/accounts/login/')
def ThrashbinRestore(request, pk):
    author = Author.objects.get(id=pk)
    author.is_deleted = False
    author.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def normalize_query(query_string,
    findterms=re.compile(r'"([^"]+)"|(\S+)').findall,
    normspace=re.compile(r'\s{2,}').sub):

    '''
    Splits the query string in invidual keywords, getting rid of unecessary spaces and grouping quoted words together.
    Example:
    >>> normalize_query('  some random  words "with   quotes  " and   spaces')
        ['some', 'random', 'words', 'with quotes', 'and', 'spaces']
    '''

    return [normspace(' ',(t[0] or t[1]).strip()) for t in findterms(query_string)]

def get_query(query_string, search_fields):

    '''
    Returns a query, that is a combination of Q objects.
    That combination aims to search keywords within a model by testing the given search fields.
    '''

    query = None  # Query to search for every search term
    terms = normalize_query(query_string)
    for term in terms:
        or_query = None  # Query to search for a given term in each field
        for field_name in search_fields:
            if (field_name == None or field_name == ""):
                continue
            q = Q(**{"%s__iregex" % field_name: term})
            if or_query is None:
                or_query = q
            else:
                or_query = or_query | q
        if query is None:
            query = or_query
        else:
            query = query & or_query
    # pdb.set_trace()
    return query