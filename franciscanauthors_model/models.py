from django.db import models

class Genre(models.Model):
    genre_id = models.AutoField(primary_key=True)
    genre_description = models.CharField(max_length=250, blank=True)

    @property
    def genre_groups(self):
        return Genre_group.objects.filter(genre=self)

class Genre_group(models.Model):
    genre_group = models.CharField(max_length=250, blank=True)
    genre_id = models.ForeignKey(Genre, to_field='genre_id', on_delete=models.CASCADE)

class Date_precision(models.Model):
    date_precision_id = models.AutoField(primary_key=True)
    date_precision = models.CharField(max_length=250, blank=True)

class Author(models.Model):
    author_id = models.AutoField(primary_key=True)
    author_name = models.CharField(max_length=250, blank=True)
    biography = models.CharField(max_length=250, blank=True)
    birth = models.CharField(max_length=250, blank=True)
    death = models.CharField(max_length=250, blank=True)
    birth_date_precision_id = models.ForeignKey(Date_precision, to_field='date_precision_id', on_delete=models.CASCADE, \
                                                related_name = 'birth_dates')
    death_date_precision_id = models.ForeignKey(Date_precision, to_field='date_precision_id', on_delete=models.CASCADE, \
                                                related_name = 'death_dates')
    checked = models.NullBooleanField()

class Works(models.Model):
    author_id = models.ForeignKey(Author, to_field='author_id', on_delete=models.CASCADE)
    year = models.IntegerField()
    title = models.CharField(max_length=250, blank=True)
    publisher = models.CharField(max_length=250, blank=True)
    location = models.CharField(max_length=250, blank=True)
    detaiL_descriptions = models.CharField(max_length=250, blank=True)
    date_precision_id = models.ForeignKey(Date_precision, to_field='date_precision_id', on_delete=models.CASCADE)
    genre_id = models.ForeignKey(Genre, to_field='genre_id', on_delete=models.CASCADE)

class Alias(models.Model):
    author_ID = models.ForeignKey(Author, to_field='author_id', on_delete=models.CASCADE)
    alias = models.CharField(max_length=250, blank=True)

class Additional_info(models.Model):
    author_ID = models.ForeignKey(Author, to_field='author_id', on_delete=models.CASCADE)
    add_comments = models.CharField(max_length=250, blank=True)

class Location_time(models.Model):
    author_ID = models.ForeignKey(Author, to_field='author_id', on_delete=models.CASCADE)
    geo_location_name = models.CharField(max_length=250, blank=True)
    fr_province = models.CharField(max_length=250, blank=True)
    date = models.CharField(max_length=250, blank=True)
    date_precision_id = models.ForeignKey(Date_precision, to_field='date_precision_id', on_delete=models.CASCADE)






















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

