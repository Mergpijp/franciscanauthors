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
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.fields['author_name'].required = False
        self.fields['biography'].required = False
        self.fields['birth'].required = False
        self.fields['death'].required = False

        self.helper.layout = Layout(
            TabHolder(
            Tab('Author',
                    'author_name',
                    'biography',
                    'birth',
                    'death',
                HTML("""{% include "_author.html" %}"""),
                ),
            Tab('Location times',
                HTML("""{% include "_location_time.html" %}"""),
                ),
            Tab('Works',
                HTML("""{% include "_works.html" %}"""),
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
        fields = ('author_name', 'biography', 'birth', 'death')

class WorkForm(forms.ModelForm):
    '''
        Crispy form for publication create/update(edit).
        Added field with buttons for inline add. Is almost the same as PublicationForm but has a submit button.

    '''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.fields['year'].required = False
        self.fields['title'].required = False
        self.fields['publisher'].required = False
        self.fields['location'].required = False
        self.fields['detail_descriptions'].required = False

        self.helper.layout = Layout(
                    'year',
                    'title',
                    'publisher',
                    'location',
                    'detail_descriptions',
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
        fields = ('year', 'title', 'publisher', 'location', 'detail_descriptions',)

class LocationTimeForm(forms.ModelForm):
    '''
        Crispy form for publication create/update(edit).
        Added field with buttons for inline add. Is almost the same as PublicationForm but has a submit button.

    '''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.fields['geo_location_name'].required = False
        self.fields['fr_province'].required = False
        self.fields['date'].required = False

        self.helper.layout = Layout(
                    'geo_location_name',
                    'fr_province',
                    'date',
            ButtonHolder(
                Submit('save_add_another', 'Save and add another', css_class='btn-save btn-danger'),
                Submit('save_and_continue_editing', 'Save and continue editing', css_class='btn-save btn-danger'),
                Submit('save', 'Save', css_class='btn-save btn-danger'),
            )
        )

    # do unsubscribe
    class Meta:
        model = Location_time
        # See note here: https://docs.djangoproject.com/en/1.10/ref/contrib/admin/#django.contrib.admin.ModelAdmin.form
        fields = ('geo_location_name', 'fr_province', 'date',)

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

class Additional_info_form(forms.ModelForm):
    '''
        Crispy form for publication create/update(edit).
        Added field with buttons for inline add. Is almost the same as PublicationForm but has a submit button.

    '''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.fields['add_comments'].required = False

        self.helper.layout = Layout(
                    'add_comments',
            ButtonHolder(
                Submit('save_add_another', 'Save and add another', css_class='btn-save btn-danger'),
                Submit('save_and_continue_editing', 'Save and continue editing', css_class='btn-save btn-danger'),
                Submit('save', 'Save', css_class='btn-save btn-danger'),
            )
        )

    # do unsubscribe
    class Meta:
        model = Additional_info
        # See note here: https://docs.djangoproject.com/en/1.10/ref/contrib/admin/#django.contrib.admin.ModelAdmin.form
        fields = ('add_comments',)

class Date_precision_form(forms.ModelForm):
    '''
        Crispy form for publication create/update(edit).
        Added field with buttons for inline add. Is almost the same as PublicationForm but has a submit button.

    '''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.fields['date_precision'].required = False

        self.helper.layout = Layout(
                    'date_precision',
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
                    'genre_descr',
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
                    'genre_group',
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
