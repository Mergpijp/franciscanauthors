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

@login_required(login_url='/accounts/login/')
def location_time_process(request, pk=None, lt=None):
    data = dict()
    obj, created = Location_time.objects.get_or_create(pk=lt)

    post_mutable = {'geo_location_name': request.POST['geo_location_name'], 'fr_province': request.POST['fr_province'], \
                    'date': request.POST['date']}

    form = LocationTimeForm(post_mutable or None, instance=obj)

    if request.method == 'POST':
        if form.is_valid():
            instance = form.save()
            author = Author.objects.get(pk=pk)
            author.location_time_set.add(instance)
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
        if not location_time in author.location_time_set.all():
            author.location_time_set.add(location_time)
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
        if location_time in author.location_time_set.all():
            author.location_time_set.remove(location_time)
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
def work_process(request, pk=None, w=None):
    data = dict()
    obj, created = Works.objects.get_or_create(pk=w)

    post_mutable = {'year': request.POST['year'], 'title': request.POST['title'], \
                    'publisher': request.POST['publisher'], 'location': request.POST['location'], \
                    'detail_descriptions': request.POST['detail_descriptions']}

    form = WorkForm(post_mutable or None, instance=obj)

    if request.method == 'POST':
        if form.is_valid():
            instance = form.save()
            author = Author.objects.get(pk=pk)
            author.works_set.add(instance)
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
        if not work in author.works_set.all():
            author.works_set.add(work)
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
        if work in author.works_set.all():
            author.works_set.remove(work)
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
                work = Works.objects.filter(title__icontains=input).order_by('title')[:10]
            else:
                work = Works.objects.none()
            author = Author.objects.get(pk=pk)
            data['table'] = render_to_string(
                '_works_candidates_table.html',
                {'works': work, 'author': author},
                request=request
            )
            return JsonResponse(data)

# Create your views here.
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
    paginate_by = 10

    def get_template_names(self):
        return ['show.html']


    def get_ordering(self):
        ordering = self.request.GET.get('order_by')
        direction = self.request.GET.get('direction')
        if ordering is not None and ordering != "" and direction is not None and direction != "":
            if direction == 'desc':
                ordering = '-{}'.format(ordering)
        return ordering

    def get_queryset(self):
        authors = self.request.GET.getlist('authors')
        authors = Author.objects.filter(pk__in=authors).all()
        birth_date_precision_id = self.request.GET.getlist('birth_date_precision_id')
        birth_date_precision_id = Date_precision.objects.filter(pk__in=birth_date_precision_id).all()
        death_date_precision_id = self.request.GET.getlist('death_date_precision_id')
        death_date_precision_id = Date_precision.objects.filter(pk__in=death_date_precision_id).all()

        exclude = ['csrfmiddlewaretoken','search', 'order_by', 'direction']
        in_variables = [('authors', authors),]
        special_case = ['copyrights', 'page', 'is_a_translation']

        if ('q' in self.request.GET) and self.request.GET['q'].strip():
            query_string = self.request.GET['q']


            search_fields = ['author_name', 'biograsphy', 'birth', 'death', 'birth_date_precision_id', 'death_date_precision_id']
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
        author = Author.objects.get(pk=self.object.id-1)
        form.instance.location_time_set.add(*author.location_time_set.all())

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
            return '/author/' + str(self.object.id) + '/edit/'
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
    template_name = 'authors/form_create.html'
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
    Detailview for publication
    Usess now in template thus the function get_context_data
    '''
    model = Author
    context_object_name = 'author'

    def get_queryset(self):
        authors = Author.objects.filter(is_deleted=False)
        return authors

    def get_context_data(self, **kwargs):
        self.object = []
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context

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