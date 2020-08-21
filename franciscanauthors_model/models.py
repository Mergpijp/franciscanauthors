from django.db import models

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

