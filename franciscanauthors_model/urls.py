from django.urls import include, path, re_path
from .views import *
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('', SearchResultsView.as_view(), name='author-show'),
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
    path('alias/link/<int:pk>/<int:a>', alias_link, name='link-alias'),
    path('alias/unlink/<int:pk>/<int:a>', alias_unlink, name='unlink-alias'),

    path('additional_info/process/<int:pk>', additional_info_process, name='additional_info-process'),
    path('additional_info/process/<int:pk>/<int:ai>', additional_info_process, name='additional_info-process'),
    path('additional_info/search/<int:pk>', additional_info_search, name='search-additional_info'),
    path('additional_info/link/<int:pk>/<int:ai>', additional_info_link, name='link-additional_info'),
    path('additional_info/unlink/<int:pk>/<int:ai>', additional_info_unlink, name='unlink-additional_info'),

    path('date_precision/process', date_precision_process, name='date_precision-process'),
    path('genre/process', genre_process, name='genre-process'),

    path('genre_group/process/<int:pk>', genre_group_process, name='genre_group-process'),
    path('genre_group/process/<int:pk>/<int:g>', genre_group_process, name='genre_group_process'),
    path('genre_group/search/<int:pk>', genre_group_search, name='search-genre_group'),
    path('genre_group/link/<int:pk>/<int:g>', genre_group_link, name='link-genre_group'),
    path('genre_group/unlink/<int:pk>/<int:g>', genre_group_unlink, name='unlink-genre_group'),

    path('genre/new/', login_required(GenreCreate.as_view()), name='genre-new'),
    path('genre/show/', login_required(GenreShow.as_view()), name='genre-show'),
    path('genre/<int:pk>/edit/', login_required(GenreUpdate.as_view()), name='genre-update'),
    path('genre/<int:pk>/delete/', GenreDelete, name='genre-delete'),

    path('date_precision/new/', login_required(DatePrecisionCreate.as_view()), name='date_precision-new'),
    path('date_precision/show/', login_required(DatePrecisionShow.as_view()), name='date_precision-show'),
    path('date_precision/<int:pk>/edit/', login_required(DatePrecisionUpdate.as_view()), name='date_precision-update'),
    path('date_precision/<int:pk>/delete/', DatePrecisionDelete, name='date_precision-delete'),
]