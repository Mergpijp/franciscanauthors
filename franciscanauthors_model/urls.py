from django.urls import include, path, re_path
from .views import *
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('', SearchResultsView.as_view(), name='author-show'),
    path('author/show/', SearchResultsView.as_view(), name='author-show'),
    path('author/<int:pk>/detail_view/', AuthorDetailView.as_view(), name='author-detail'),
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

    path('work/process/<int:pk>', work_process, name='work-process'),
    path('work/process/<int:pk>/<int:w>', work_process, name='work-process'),
    path('work/search/<int:pk>', work_search, name='search-work'),
    path('work/link/<int:pk>/<int:w>', work_link, name='link-work'),
    path('work/unlink/<int:pk>/<int:w>', work_unlink, name='unlink-work'),
    ]