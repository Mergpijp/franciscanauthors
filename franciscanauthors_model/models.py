import pdb

from django.db import models

MAX_CHARS = 120

class Genre(models.Model):
    genre_id = models.AutoField(primary_key=True)
    genre_description = models.CharField(max_length=250, blank=True)
    is_stub = models.BooleanField(default=False)

    @property
    def genre_groups(self):
        return Genre_group.objects.filter(genre=self)


class Genre_group(models.Model):
    genre_group = models.CharField(max_length=250, blank=True)
    genre = models.ForeignKey(Genre, to_field='genre_id', related_name='genre_group_list', on_delete=models.CASCADE, blank=True, null=True)


class Date_precision(models.Model):
    date_precision_id = models.AutoField(primary_key=True)
    date_precision = models.CharField(max_length=250, blank=True)

    def __str__(self):
        return self.date_precision


class Author(models.Model):
    author_id = models.AutoField(primary_key=True)
    author_name = models.CharField(max_length=250, blank=True)
    biography = models.TextField(max_length=2000, blank=True)
    birth = models.CharField(max_length=250, blank=True)
    death = models.CharField(max_length=250, blank=True)
    birth_date_precision = models.ForeignKey(Date_precision, to_field='date_precision_id', on_delete=models.CASCADE, \
                                                related_name = 'authors_birth_date', blank=True, null=True)
    death_date_precision = models.ForeignKey(Date_precision, to_field='date_precision_id', on_delete=models.CASCADE, \
                                                related_name = 'authors_death_date', blank=True, null=True)
    checked = models.NullBooleanField()
    is_deleted = models.BooleanField(default=False)
    is_stub = models.BooleanField(default=False)

    def __str__(self):
        return self.author_name

    @property
    def get_truncated_author_name(self):
        x = self.author_name
        if len(x) > MAX_CHARS:
            x = x[:MAX_CHARS] + '...'
        return x

    @property
    def get_truncated_biography(self):
        x = self.biography
        if len(x) > MAX_CHARS:
            x = x[:MAX_CHARS] + '...'
        return x

    @property
    def get_truncated_birth(self):
        x = self.birth
        if len(x) > MAX_CHARS:
            x = x[:MAX_CHARS] + '...'
        return x

    @property
    def get_truncated_death(self):
        x = self.death
        if len(x) > MAX_CHARS:
            x = x[:MAX_CHARS] + '...'
        return x

    @property
    def get_truncated_birth_date_precision_id(self):
        birth_dates = self.birth_dates
        x = ', '.join([date.date_precision for date in birth_dates.all()])
        if len(x) > MAX_CHARS:
            x = x[:MAX_CHARS] + '...'
        return x

    @property
    def get_truncated_death_date_precision_id(self):
        death_dates = self.death_dates
        x = ', '.join([date.date_precision for date in death_dates.all()])
        if len(x) > MAX_CHARS:
            x = x[:MAX_CHARS] + '...'
        return x

    @property
    def get_truncated_geo_location_name(self):
        locations_times = self.location_time_list.all()
        x = ', '.join([lt.geo_location_name for lt in locations_times.all()])
        if len(x) > MAX_CHARS:
            x = x[:MAX_CHARS] + '...'
        return x

    @property
    def get_truncated_fr_province(self):
        locations_times = self.location_time_list.all()
        x = ', '.join([lt.fr_province for lt in locations_times.all()])
        if len(x) > MAX_CHARS:
            x = x[:MAX_CHARS] + '...'
        return x

    @property
    def get_truncated_date(self):
        locations_times = self.location_time_list.all()
        x = ', '.join([lt.date for lt in locations_times.all()])
        if len(x) > MAX_CHARS:
            x = x[:MAX_CHARS] + '...'
        return x

    @property
    def get_truncated_year(self):
        works = self.works_author_list
        x = ', '.join([work.year for work in works.all() if work.year])
        if len(x) > MAX_CHARS:
            x = x[:MAX_CHARS] + '...'
        return x

    @property
    def get_truncated_title(self):
        works = self.works_author_list
        x = ', '.join([work.title for work in works.all()])
        if len(x) > MAX_CHARS:
            x = x[:MAX_CHARS] + '...'
        return x

    @property
    def get_truncated_publisher(self):
        works = self.works_author_list
        x = ', '.join([work.publisher for work in works.all()])
        if len(x) > MAX_CHARS:
            x = x[:MAX_CHARS] + '...'
        return x

    @property
    def get_truncated_location(self):
        works = self.works_author_list
        x = ', '.join([work.location for work in works.all()])
        if len(x) > MAX_CHARS:
            x = x[:MAX_CHARS] + '...'
        return x

    @property
    def get_truncated_detail_descriptions(self):
        works = self.works_author_list
        x = ', '.join([work.detail_descriptions for work in works.all()])
        if len(x) > MAX_CHARS:
            x = x[:MAX_CHARS] + '...'
        return x

    @property
    def get_truncated_detail_alias(self):
        alias = self.alias_list
        x = ', '.join([a.alias for a in alias.all()])
        if len(x) > MAX_CHARS:
            x = x[:MAX_CHARS] + '...'
        return x

    @property
    def get_truncated_detail_additional_info(self):
        ai = self.additional_info_list
        x = ', '.join([a.add_comments for a in ai.all()])
        if len(x) > MAX_CHARS:
            x = x[:MAX_CHARS] + '...'
        return x

class Works(models.Model):
    author = models.ForeignKey(Author, to_field='author_id', related_name='works_author_list', on_delete=models.CASCADE, blank=True, null=True)
    year = models.IntegerField(null=True, blank=True)
    title = models.CharField(max_length=250, blank=True)
    publisher = models.CharField(max_length=250, blank=True)
    location = models.CharField(max_length=250, blank=True)
    detail_descriptions = models.CharField(max_length=250, blank=True)
    date_precision = models.ForeignKey(Date_precision, to_field='date_precision_id', related_name='works_date_list', on_delete=models.CASCADE, blank=True, null=True)
    genre = models.ForeignKey(Genre, to_field='genre_id', related_name='works_genre_list',on_delete=models.CASCADE, blank=True, null=True)
    text = models.TextField(max_length=200000, blank=True, null=True)

    def __str__(self):
        if self.text:
            return  'title: ' + self.title + ' text: ' + self.text
        else:
            return 'title: ' + self.title

class Alias(models.Model):
    author = models.ForeignKey(Author, to_field='author_id', related_name='alias_list', on_delete=models.CASCADE, blank=True, null=True)
    alias = models.CharField(max_length=250, blank=True)

    def __str__(self):
        return  self.alias

class Additional_info(models.Model):
    author = models.ForeignKey(Author, to_field='author_id', related_name='additional_info_list', on_delete=models.CASCADE, blank=True, null=True)
    add_comments = models.TextField(max_length=200000, blank=True, null=True)

    def __str__(self):
        if self.add_comments:
            return  self.add_comments
        else:
            return ''

class Location_time(models.Model):
    author = models.ForeignKey(Author, to_field='author_id', on_delete=models.CASCADE, related_name="location_time_list", blank=True, null=True)
    geo_location_name = models.CharField(max_length=250, blank=True)
    fr_province = models.CharField(max_length=250, blank=True)
    date = models.CharField(max_length=250, blank=True)
    date_precision = models.ForeignKey(Date_precision, to_field='date_precision_id', on_delete=models.CASCADE, related_name='location_times_date_precision', blank=True, null=True)

    def __str__(self):
        return  self.geo_location_name
















class Edition(models.Model):
    entry = models.CharField(max_length=250, blank=True)

class Manuscript(models.Model):
    entry = models.CharField(max_length=250, blank=True)

class Manuscript_Edition(models.Model):
    entry = models.CharField(max_length=250, blank=True)

class Edition_Translation(models.Model):
    entry = models.CharField(max_length=250, blank=True)

class Translation(models.Model):
    entry = models.CharField(max_length=250, blank=True)

# Create your models here.
class Record(models.Model):
    name_bold = models.CharField(max_length=250, blank=True)
    name_date = models.CharField(max_length=250, blank=True, null=True)
    name_original = models.CharField(max_length=250, blank=True, null=True)
    name_latin = models.CharField(max_length=250, blank=True, null=True)
    personalia = models.TextField(max_length=500, blank=True)
    literature = models.TextField(max_length=1500, blank=True, null=True)
    #editions = models.ForeignKey(Editions, on_delete=models.CASCADE, null=True, blank=True)
    editions = models.ManyToManyField(Edition)
    #manuscripts = models.ForeignKey(Manuscript, on_delete=models.CASCADE, null=True, blank=True)
    manuscripts = models.ManyToManyField(Manuscript)
    #manuscripts_editions = models.ForeignKey(Manuscript_Editions, on_delete=models.CASCADE, null=True, blank=True)
    manuscripts_editions = models.ManyToManyField(Manuscript_Edition)
    literature_editions = models.TextField(max_length=1500, blank=True, null=True)
    vitea = models.TextField(max_length=500, blank=True, null=True)
    vitea_biographies = models.TextField(max_length=500, blank=True, null=True)
    works_editions = models.TextField(max_length=500, blank=True, null=True)
    editions_music = models.TextField(max_length=500, blank=True, null=True)
    surviving_works = models.TextField(max_length=500, blank=True, null=True)
    edities_studies = models.TextField(max_length=1500, blank=True, null=True)
    manuscripts_editions_literature = models.TextField(max_length=1500, blank=True, null=True)
    salimbenes_literary_legacy = models.TextField(max_length=1500, blank=True, null=True)
    #editions_translations = models.ForeignKey(Editions_Translations, on_delete=models.CASCADE, null=True, blank=True)
    editions_translations = models.ManyToManyField(Edition_Translation)
    studies = models.TextField(max_length=1500, blank=True, null=True)
    #translations = models.ForeignKey(Translation, on_delete=models.CASCADE, null=True, blank=True)
    translations = models.ManyToManyField(Translation)
    primo_vita_bona = models.TextField(max_length=500, blank=True, null=True)
    letter = models.CharField(max_length=1, blank=True)

