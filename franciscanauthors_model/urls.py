from django.urls import include, path, re_path
from .views import *
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView

urlpatterns = [

    path('', TemplateView.as_view(template_name="main.html")),

    path('research/iicatalogueslists', TemplateView.as_view(template_name="research/iicatalogueslists.htm")),
    path('research/iiiotherimportantrecentmanuscript', TemplateView.as_view(template_name="research/iiiotherimportantrecentmanuscript.htm", content_type='text/html; charset=windows-1252')),
    path('research/iiiotherimportantrecrecentmanuscript', TemplateView.as_view(template_name="research/iiiotherimportantrecrecentmanuscript.htm")),
    path('research/ithemostimportantperiodicals', TemplateView.as_view(template_name="research/ithemostimportantperiodicals.htm")),
    path('research/ivrelevantcataloguesandreferenceworks', TemplateView.as_view(template_name="research/ivrelevantcataloguesandreferenceworks.htm")),
    path('research/ixsomemajoroldexistingcatalogues', TemplateView.as_view(template_name="research/ixsomemajoroldexistingcatalogues.htm")),
    path('research/viiiotherdocuments', TemplateView.as_view(template_name="research/viiiotherdocuments.htm")),
    path('research/viistatutes', TemplateView.as_view(template_name="research/viistatutes.htm")),
    path('research/vipapaldocuments', TemplateView.as_view(template_name="research/vipapaldocuments.htm")),
    path('research/vworksinfoonmedievalandearlymodern', TemplateView.as_view(template_name="research/vworksinfoonmedievalandearlymodern.htm")),
    path('research/vworksinfoonmedievalandern', TemplateView.as_view(template_name="research/vworksinfoonmedievalandern.htm")),
    path('research/xiiafewimportantworkswithinfo', TemplateView.as_view(template_name="research/xiiafewimportantworkswithinfo.htm")),
    path('research/xiiiimportantcurrentbibliographies', TemplateView.as_view(template_name="research/xiiiimportantcurrentbibliographies.htm")),
    path('research/ximajorcurrentbibliographies', TemplateView.as_view(template_name="research/ximajorcurrentbibliographies.htm")),
    path('research/ximajorcurrentbibliogrphies', TemplateView.as_view(template_name="research/ximajorcurrentbibliogrphies.htm")),
    path('research/xivmajorgeneraldictionaries', TemplateView.as_view(template_name="research/xivmajorgeneraldictionaries.htm")),
    path('research/xotheroldgiantreferenceworks', TemplateView.as_view(template_name="research/xotheroldgiantreferenceworks.htm")),
    path('research/xvhandbooksandimportantgeneral', TemplateView.as_view(template_name="research/xvhandbooksandimportantgeneral.htm")),
    path('research/xviigeneralbibliographyeducation', TemplateView.as_view(template_name="research/xviigeneralbibliographyeducation.htm")),
    path('research/xviparticularprovincesandconvents', TemplateView.as_view(template_name="research/xviparticularprovincesandconvents.htm")),

    path('franautvitaem/', TemplateView.as_view(template_name="franautvitaem.htm")),
    path('provinces/', TemplateView.as_view(template_name="province.htm")),
    path('virtual_publications/', TemplateView.as_view(template_name="v_art.htm")),
    path('MEvermaak/', TemplateView.as_view(template_name="MEvermaak.html")),
    path('GILLEEDS/', TemplateView.as_view(template_name="GILLEEDS.html")),
    path('bibliog/', TemplateView.as_view(template_name="bibliog.html")),

    path('bibliog/exegesis', TemplateView.as_view(template_name="bibliog/exegesis.htm")),
    path('bibliog/geogr', TemplateView.as_view(template_name="bibliog/geogr.htm")),
    path('bibliog/hstoriog', TemplateView.as_view(template_name="bibliog/hstoriog.htm")),
    path('bibliog/preaching', TemplateView.as_view(template_name="bibliog/preaching.htm")),

    path('research/', TemplateView.as_view(template_name="research.html")),
    path('Bert/', TemplateView.as_view(template_name="Bert.html")),
    path('links/', TemplateView.as_view(template_name="links.html")),
    #path('', SearchResultsView.as_view(), name='author-show'),
    path('author/show/', SearchResultsView.as_view(), name='author-show'),
    path('author/<int:pk>/detail_view/', login_required(AuthorDetailView.as_view()), name='author-detail'),
    path('author/new/', login_required(AuthorCreate.as_view()), name='author-new'),
    path('author/<int:pk>/edit/', login_required(AuthorUpdate.as_view()), name='author-update'),
    path('author/<int:pk>/delete/', AuthorDelete, name='author-delete'),
    path('author/<int:pk>/restore/', ThrashbinRestore, name='thrashbin-restore'),
    path('thrashbin/show/', login_required(ThrashbinShow.as_view()), name='thrashbin-show'),

    path('location_time/process/<int:pk>',location_time_process, name='location_time-process'),
    path('location_time/process/<int:pk>/<int:lt>', location_time_process, name='location_time-process'),
    path('location_time/search/<int:pk>',location_time_search, name='search-location_time'),
    path('location_time/link/<int:pk>/<int:lt>', location_time_link, name='link-location_time'),
    path('location_time/unlink/<int:pk>/<int:lt>', location_time_unlink, name='unlink-location_time'),
    path('select2_date_precision_id/', select2_date_precision_id, name='select2-date-precision-id'),

    path('work/show/', SearchResultsViewWorks.as_view(), name='work-show'),
    path('work/process/<int:pk>', work_process, name='work-process'),
    path('work/process/<int:pk>/<int:w>', work_process, name='work-process'),
    path('work/search/<int:pk>', work_search, name='search-work'),
    path('work/link/<int:pk>/<int:w>', work_link, name='link-work'),
    path('work/unlink/<int:pk>/<int:w>', work_unlink, name='unlink-work'),
    path('work/<int:pk>/detail_view/', login_required(WorkDetailView.as_view()), name='work-detail'),
    path('work/new/', login_required(WorkCreate.as_view()), name='work-new'),
    path('work/<int:pk>/edit/', login_required(WorkUpdate.as_view()), name='work-update'),
    path('work/<int:pk>/delete/', WorkDelete, name='work-delete'),
    path('select2_genre_id/', select2_genre_id, name='select2-genre-id'),


    path('alias/process/<int:pk>', alias_process, name='alias-process'),
    path('alias/process/<int:pk>/<int:a>', alias_process, name='alias-process'),
    path('alias/search/<int:pk>', alias_search, name='search-alias'),
    path('alias/link/<int:pk>/<int:apk>', alias_link, name='link-alias'),
    path('alias/unlink/<int:pk>/<int:a>', alias_unlink, name='unlink-alias'),

    path('literature/process/<int:pk>', literature_process, name='literature-process'),
    path('literature/process/<int:pk>/<int:lit>', literature_process, name='literature-process'),
    path('literature/search/<int:pk>', literature_search, name='search-literature'),
    path('literature/link/<int:pk>/<int:lit>', literature_link, name='link-literature'),
    path('literature/unlink/<int:pk>/<int:lit>', literature_unlink, name='unlink-literature'),

    path('date_precision/process', date_precision_process, name='date_precision-process'),
    path('genre/process', genre_process, name='genre-process'),

    path('genre_group/process/<int:pk>', genre_group_process, name='genre_group-process'),
    path('genre_group/process/<int:pk>/<int:g>', genre_group_process, name='genre_group-process'),
    path('genre_group/search/<int:pk>', genre_group_search, name='search-genre_group'),
    path('genre_group/link/<int:pk>/<int:g>', genre_group_link, name='link-genre_group'),
    path('genre_group/unlink/<int:pk>/<int:g>', genre_group_unlink, name='unlink-genre_group'),

    path('genre_group/new/', login_required(GenreGroupCreate.as_view()), name='genre-group-new'),
    path('genre_group/show/', login_required(GenreGroupShow.as_view()), name='genre-group-show'),
    path('genre_group/<int:pk>/edit/', login_required(GenreGroupUpdate.as_view()), name='genre-group-update'),
    path('genre_group/<int:pk>/delete/', GenreGroupDelete, name='genre-group-delete'),

    path('genre/process/<int:pk>', genre_process2, name='genre-process'),
    path('genre/process/<int:pk>/<int:g>', genre_process2, name='genre-process'),
    path('genre/search/<int:pk>', genre_search, name='search-genre'),
    path('genre/link/<int:pk>/<int:g>', genre_link, name='link-genre'),
    path('genre/unlink/<int:pk>/<int:g>', genre_unlink, name='unlink-genre'),

    path('genre/new/', login_required(GenreCreate.as_view()), name='genre-new'),
    path('genre/show/', login_required(GenreShow.as_view()), name='genre-show'),
    path('genre/<int:pk>/edit/', login_required(GenreUpdate.as_view()), name='genre-update'),
    path('genre/<int:pk>/delete/', GenreDelete, name='genre-delete'),

    path('date_precision/new/', login_required(DatePrecisionCreate.as_view()), name='date_precision-new'),
    path('date_precision/show/', login_required(DatePrecisionShow.as_view()), name='date_precision-show'),
    path('date_precision/<int:pk>/edit/', login_required(DatePrecisionUpdate.as_view()), name='date_precision-update'),
    path('date_precision/<int:pk>/delete/', DatePrecisionDelete, name='date_precision-delete'),
]