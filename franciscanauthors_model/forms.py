from django import forms

from .models import *
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, Div, Field, Button, HTML
from crispy_forms.bootstrap import Tab, TabHolder, FieldWithButtons, StrictButton, AppendedText
from django_select2.forms import ModelSelect2MultipleWidget, Select2MultipleWidget, ModelSelect2TagWidget, \
    Select2Widget, ModelSelect2Widget, HeavySelect2MultipleWidget, ModelSelect2TagWidget

class AuthorForm(forms.ModelForm):
    '''
        Crispy form for publication create/update(edit).
        Added field with buttons for inline add. Is almost the same as PublicationForm but has a submit button.

    '''
    birth_date_precision = forms.ModelChoiceField(widget=ModelSelect2Widget(
        model=Date_precision,
        search_fields=['date_precision__icontains', ],
        attrs={'data-minimum-input-length': 0},
    ), queryset=Date_precision.objects.all(), required=False)
    death_date_precision = forms.ModelChoiceField(widget=ModelSelect2Widget(
        model=Date_precision,
        search_fields=['date_precision__icontains', ],
        attrs={'data-minimum-input-length': 0},
    ), queryset=Date_precision.objects.all())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.fields['author_name'].required = False
        self.fields['affiliation'].required = False
        self.fields['biography'].required = False
        self.fields['birth'].required = False
        self.fields['death'].required = False
        self.fields['death_date_precision'].required = False
        self.fields['birth_date_precision'].required = False
        self.fields['checked'].required = False

        self.helper.layout = Layout(
            TabHolder(
            Tab('Author',
                    'author_name',
                    'affiliation',
                    'biography',
                    'birth',
                    'death',
                    'birth_date_precision',
                    'death_date_precision',
                    HTML("""{% include "_date_precision_modal.html" %}"""),
                    'checked',
                ),
            Tab('Location times',
                HTML("""{% include "_location_time.html" %}"""),

                ),
            Tab('Works',
                HTML("""{% include "_works.html" %}"""),
                ),
            Tab('Aliases',
                    HTML("""{% include "_alias.html" %}"""),
                ),
            Tab('Literatures',
                HTML("""{% include "_literature.html" %}"""),
                ),
            ),
            ButtonHolder(
                Submit('save_add_another', 'Save and add another', css_class='btn-save btn-danger'),
                Submit('save_and_continue_editing', 'Save and continue editing', css_class='btn-save btn-danger'),
                Submit('save', 'Save', css_class='btn-save btn-danger'),
            )
        )

    # do unsubscribe
    class Meta:
        model = Author
        # See note here: https://docs.djangoproject.com/en/1.10/ref/contrib/admin/#django.contrib.admin.ModelAdmin.form
        fields = ('author_name', 'biography', 'birth', 'death', 'birth_date_precision', 'death_date_precision', \
                  'checked', 'affiliation',)

class LocationTimeForm(forms.ModelForm):
    '''
        Crispy form for publication create/update(edit).
        Added field with buttons for inline add. Is almost the same as PublicationForm but has a submit button.

    '''
    author = forms.ModelChoiceField(widget=ModelSelect2Widget(
        model=Author,
        search_fields=['author_name__icontains', ],
        attrs={'data-minimum-input-length': 0},
    ), queryset=Author.objects.all(), required=False)
    date_precision = forms.ModelChoiceField(widget=ModelSelect2Widget(
        model=Date_precision,
        search_fields=['date_precision__icontains', ],
        attrs={'data-minimum-input-length': 0},
    ), queryset=Date_precision.objects.all())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.fields['geo_location_name'].required = False
        self.fields['fr_province'].required = False
        self.fields['date'].required = False
        self.fields['date_precision'].required = False
        self.fields['author'].required = False

        self.helper.layout = Layout(
                    'author',
                    'geo_location_name',
                    'fr_province',
                    'date',
                    'date_precision',
            ButtonHolder(
                Submit('save_add_another', 'Save and add another', css_class='btn-save btn-danger'),
                Submit('save_and_continue_editing', 'Save and continue editing', css_class='btn-save btn-danger'),
                Submit('save', 'Save', css_class='btn-save btn-danger'),
            )
        )

    class Meta:
        model = Location_time
        # See note here: https://docs.djangoproject.com/en/1.10/ref/contrib/admin/#django.contrib.admin.ModelAdmin.form
        fields = ('author', 'geo_location_name', 'fr_province', 'date', 'date_precision',)


class WorkForm(forms.ModelForm):
    '''
        Crispy form for publication create/update(edit).
        Added field with buttons for inline add. Is almost the same as PublicationForm but has a submit button.

    '''

    date_precision = forms.ModelChoiceField(widget=ModelSelect2Widget(
        model=Date_precision,
        search_fields=['date_precision__icontains', ],
        attrs={'data-minimum-input-length': 0},
    ), queryset=Date_precision.objects.all())
    genre = forms.ModelChoiceField(widget=ModelSelect2Widget(
        model=Genre,
        search_fields=['date_precision__icontains', ],
        attrs={'data-minimum-input-length': 0},
    ), queryset=Genre.objects.all())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.fields['text'].required = False
        self.fields['year'].required = False
        self.fields['title'].required = False
        self.fields['publisher'].required = False
        self.fields['location'].required = False
        self.fields['detail_descriptions'].required = False
        self.fields['date_precision'].required = False
        self.fields['genre'].required = False

        self.helper.layout = Layout(
                    'text',
                    'year',
                    'title',
                    'publisher',
                    'location',
                    'detail_descriptions',
                    'date_precision',
                    HTML("""{% include "_date_precision_modal.html" %}"""),
                    'genre',
                    HTML("""{% include "_genre_modal.html" %}"""),
            ButtonHolder(
                Submit('save_add_another', 'Save and add another', css_class='btn-save btn-danger'),
                Submit('save_and_continue_editing', 'Save and continue editing', css_class='btn-save btn-danger'),
                Submit('save', 'Save', css_class='btn-save btn-danger'),
            )
        )

    # do unsubscribe
    class Meta:
        model = Works
        # See note here: https://docs.djangoproject.com/en/1.10/ref/contrib/admin/#django.contrib.admin.ModelAdmin.form
        fields = ('text', 'year', 'title', 'publisher', 'location', 'detail_descriptions', 'date_precision', 'genre',)

class AliasForm(forms.ModelForm):
    '''
        Crispy form for publication create/update(edit).
        Added field with buttons for inline add. Is almost the same as PublicationForm but has a submit button.

    '''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.fields['alias'].required = False

        self.helper.layout = Layout(
                    'alias',
            ButtonHolder(
                Submit('save_add_another', 'Save and add another', css_class='btn-save btn-danger'),
                Submit('save_and_continue_editing', 'Save and continue editing', css_class='btn-save btn-danger'),
                Submit('save', 'Save', css_class='btn-save btn-danger'),
            )
        )

    # do unsubscribe
    class Meta:
        model = Alias
        # See note here: https://docs.djangoproject.com/en/1.10/ref/contrib/admin/#django.contrib.admin.ModelAdmin.form
        fields = ('alias',)

class Literature_form(forms.ModelForm):
    '''
        Crispy form for publication create/update(edit).
        Added field with buttons for inline add. Is almost the same as PublicationForm but has a submit button.

    '''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.fields['lit_text'].required = False

        self.helper.layout = Layout(
                    'lit_text',
            ButtonHolder(
                Submit('save_add_another', 'Save and add another', css_class='btn-save btn-danger'),
                Submit('save_and_continue_editing', 'Save and continue editing', css_class='btn-save btn-danger'),
                Submit('save', 'Save', css_class='btn-save btn-danger'),
            )
        )

    # do unsubscribe
    class Meta:
        model = Literature
        # See note here: https://docs.djangoproject.com/en/1.10/ref/contrib/admin/#django.contrib.admin.ModelAdmin.form
        fields = ('lit_text',)

class Date_precision_form(forms.ModelForm):
    '''
        Crispy form for publication create/update(edit).
        Added field with buttons for inline add. Is almost the same as PublicationForm but has a submit button.

    '''
    authors_birth_date = forms.ModelMultipleChoiceField(widget=ModelSelect2MultipleWidget(
        model=Author,
        search_fields=['author_name__icontains', ],
        attrs={'data-minimum-input-length': 0},
    ), queryset=Author.objects.all(), required=False)
    authors_death_date = forms.ModelMultipleChoiceField(widget=ModelSelect2MultipleWidget(
        model=Author,
        search_fields=['author_name__icontains', ],
        attrs={'data-minimum-input-length': 0},
    ), queryset=Author.objects.all())
    works_date_list = forms.ModelMultipleChoiceField(widget=ModelSelect2MultipleWidget(
        model=Works,
        search_fields=['title__icontains', ],
        attrs={'data-minimum-input-length': 0},
    ), queryset=Works.objects.all())
    location_times_date_precision = forms.ModelMultipleChoiceField(widget=ModelSelect2MultipleWidget(
        model=Location_time,
        search_fields=['geo_location_name__icontains', ],
        attrs={'data-minimum-input-length': 0},
    ), queryset=Location_time.objects.all())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.fields['date_precision'].required = False
        self.fields['authors_birth_date'].required = False
        self.fields['authors_death_date'].required = False
        self.fields['works_date_list'].required = False
        self.fields['location_times_date_precision'].required = False


        self.helper.layout = Layout(
                    'date_precision',
                    'authors_birth_date',
                    'authors_death_date',
                    'works_date_list',
                    'location_times_date_precision',
            ButtonHolder(
                Submit('save_add_another', 'Save and add another', css_class='btn-save btn-danger'),
                Submit('save_and_continue_editing', 'Save and continue editing', css_class='btn-save btn-danger'),
                Submit('save', 'Save', css_class='btn-save btn-danger'),
            )
        )

    # do unsubscribe
    class Meta:
        model = Date_precision
        # See note here: https://docs.djangoproject.com/en/1.10/ref/contrib/admin/#django.contrib.admin.ModelAdmin.form
        fields = ('date_precision',)

class GenreForm(forms.ModelForm):
    '''
        Crispy form for publication create/update(edit).
        Added field with buttons for inline add. Is almost the same as PublicationForm but has a submit button.

    '''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.fields['genre_description'].required = False

        self.helper.layout = Layout(
            TabHolder(
                Tab('Genre',
                    'genre_description',
                    ),
                Tab('Genre groups',
                    HTML("""{% include "_genre_groups.html" %}"""),
                    ),
            ),
            ButtonHolder(
                Submit('save_add_another', 'Save and add another', css_class='btn-save btn-danger'),
                Submit('save_and_continue_editing', 'Save and continue editing', css_class='btn-save btn-danger'),
                Submit('save', 'Save', css_class='btn-save btn-danger'),
            )
        )

    # do unsubscribe
    class Meta:
        model = Genre
        # See note here: https://docs.djangoproject.com/en/1.10/ref/contrib/admin/#django.contrib.admin.ModelAdmin.form
        fields = ('genre_description',)
        #exclude = ('genre_group',)

class Genre_group_form(forms.ModelForm):
    '''
        Crispy form for publication create/update(edit).
        Added field with buttons for inline add. Is almost the same as PublicationForm but has a submit button.

    '''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.fields['genre_group'].required = False

        self.helper.layout = Layout(
                    TabHolder(
                        Tab('Genre Group',
                        'genre_group',
                            ),
                        Tab('Genres',
                            HTML("""{% include "_genres.html" %}"""),
                            ),
                    ),
            ButtonHolder(
                Submit('save_add_another', 'Save and add another', css_class='btn-save btn-danger'),
                Submit('save_and_continue_editing', 'Save and continue editing', css_class='btn-save btn-danger'),
                Submit('save', 'Save', css_class='btn-save btn-danger'),
            )
        )

    # do unsubscribe
    class Meta:
        model = Genre_group
        # See note here: https://docs.djangoproject.com/en/1.10/ref/contrib/admin/#django.contrib.admin.ModelAdmin.form
        fields = ('genre_group',)
        exclude = ('genre',)
