import pdb

from bs4 import BeautifulSoup
import re
import bs4
import json
from collections import OrderedDict

letters = list(map(chr, range(97, 118)))
anonymous = ['fraanony.htm']

pk = 1
#pk_manuscripts = 1
#pk_manuscripts_editions = 1
#pk_editions = 1
#pk_translations = 1
#pk_editions_translations = 1

pk_author = 1
pk_works = 1
pk_literature = 1
pk_date_precision = 1
pk_additional_info = 1
pk_alias = 1

final_data = list()

for let in letters:
#for any in anonymous:

    with open("../../franciscanauthors_data/franaut"+let+".htm", "r") as f:
    #with open("../franciscanauthors_data/"+any, "r") as f:
        contents = f.read()

        soup = BeautifulSoup(contents, 'html')

        print(soup.h2)
        print(soup.head)
        print(soup.li)
    urls = []
    for url in soup.find_all('a'):
        if url.get('name') != None:
            urls.append(url)
    lemmas = []
    for url in urls:
        p = url.parent
        p = p.parent
        lemmas.append(p)

    def var_bold_and_next_sentence(variable, stop, tag):
        variable = ''
        if not stop:
            print(tag)
            if tag and tag.name == 'p':
                variable = tag.text
            try:
                tag = tag.nextSibling.nextSibling
                if tag is None:
                    stop = True
            except AttributeError:
                stop = True
        return variable, stop, tag

    def has_four_digits(str):
        succ = 0
        for index, char in enumerate(str):
            if char.isdigit():
                succ += 1
            else:
                succ = 0
            if succ == 4:
                if index+1 < len(str):
                    return not(str[index+1].isdigit())
                else:
                    return True
        return False

    def has_century(str):
        succ = 0
        for index, char in enumerate(str):
            if char.isdigit():
                succ += 1
            else:
                succ = 0
            if succ == 2:
                if index+2 < len(str):
                    return str[index+1] == 't' and str[index+2] == 'h'
                else:
                    return False
        return False

    def extract_year(str):
        regex = re.compile(r'\d{4}-\d{4}')
        matchobj = regex.search(str)
        if matchobj:
            return matchobj.group(0)
        else:
            regex = re.compile(r'\d{4}')
            m = regex.search(str)
            if m:
                return m.group(0)
        return None


    def find_content(variable, stop, tag):
        variable = ''
        while not stop:
            if isinstance(tag, bs4.element.Tag):
                test = tag.find('b')
                if test is None or test == -1:
                    if tag.nextSibling is None:
                        variable = variable + tag.text + '\n'
                        stop = True
                        break
                    else:
                        if isinstance(tag.nextSibling, bs4.element.Tag):
                            variable = variable + tag.text
                        else:
                             variable = variable + tag.text + tag.nextSibling
                    try:
                        tag = tag.nextSibling.nextSibling
                        if tag is None:
                            stop = True
                            break
                    except AttributeError:
                        stop = True
                        break
                elif test.name == 'b':
                    break
            else:
                break
        return variable, stop, tag

    data = list()

    for lemma in lemmas:
        end = False
        tag = lemma.find('p')
        name_bold = ''
        name = ''
        literature_bold = ''
        literature = ''
        works_bold = ''
        works = ''

        (name_bold, end, tag) = var_bold_and_next_sentence(name_bold, end, tag)
        (name, end, tag) = find_content(name, end, tag)
        (literature_bold, end, tag) = var_bold_and_next_sentence(literature_bold, end, tag)
        (literature, end, tag) = find_content(literature, end, tag)
        (works_bold, end, tag) = var_bold_and_next_sentence(works_bold, end, tag)
        (works, end, tag) = find_content(works, end, tag)
        data.append((name_bold, name, works_bold, works, literature_bold, literature))

    def helper(title):
        match = re.search('^works', title)
        if match:
            return 2
        match = re.search('^(L|l)iterature((?!(/|&)).)*$|literatuur', title)
        if match:
            return 3
        return -1

    structured_data = list()

    for name_bold, name, work_bold, works, literature_bold, literature in data:

        data_list = [name_bold, name, None, None]
        index = helper(work_bold)
        if index != -1:
            data_list[index] = works
        index = helper(literature_bold)
        if index != -1:
            data_list[index] = literature
        structured_data.append(tuple(data_list))

    for idx, (name_bold, name, works, literature) in enumerate(structured_data):
        name_date = None
        name_original = None
        x = re.search('\(([^\)]+)\)', name_bold)
        if x:
            x = x.group(0)
            name_latin = re.search('^[^\(]+', name_bold)
            if name_latin:
                name_latin = name_latin.group(0)
            else:
                name_latin = None
            name_date = re.search('(fl\.|d\.)(.*)', x)
            if name_date:
                substract = name_date.group(0)
                name_date = name_date.group(2)
                name_date = name_date[:-1]
                if substract in x:
                    name_original = x.replace(substract, '')
                    if len(name_original) == 1:
                        name_original = None
                    else:
                        name_original = name_original[1:]
            else:
                name_date = x
        personalia = name

        '''
        list_manuscripts = []
        if manuscripts:
            manuscripts = manuscripts.splitlines()


            for mscr in manuscripts:
                if not mscr:
                    break
                my_dict = dict()
                my_dict['model'] = 'franciscanauthors_model.manuscript'
                my_dict['pk'] = pk_manuscripts
                list_manuscripts.append(pk_manuscripts)
                pk_manuscripts += 1
                f = [('entry', mscr)]
                my_dict['fields'] = dict(f)
                final_data.append(my_dict)

        list_manuscripts_editions = []
        if manuscripts_editions:
            manuscripts_editions = manuscripts_editions.splitlines()

            for mscre in manuscripts_editions:
                if not mscre:
                    break
                my_dict = dict()
                my_dict['model'] = 'franciscanauthors_model.manuscript_edition'
                my_dict['pk'] = pk_manuscripts_editions
                list_manuscripts_editions.append(pk_manuscripts_editions)
                pk_manuscripts_editions += 1
                f = [('entry', mscre)]
                my_dict['fields'] = dict(f)
                final_data.append(my_dict)

        list_editions = []
        if editions:
            editions = editions.splitlines()
            for edition in editions:
                if not edition:
                    break
                my_dict = dict()
                my_dict['model'] = 'franciscanauthors_model.edition'
                my_dict['pk'] = pk_editions
                list_editions.append(pk_editions)
                pk_editions += 1
                f = [('entry', edition)]
                my_dict['fields'] = dict(f)
                final_data.append(my_dict)

        list_translations = []
        if translations:
            translations = translations.splitlines()
            for translation in translations:
                if not translation:
                    break
                my_dict = dict()
                my_dict['model'] = 'franciscanauthors_model.translation'
                my_dict['pk'] = pk_translations
                list_translations.append(pk_translations)
                pk_translations += 1
                f = [('entry', translation)]
                my_dict['fields'] = dict(f)
                final_data.append(my_dict)

        list_editions_translations = []
        if editions_translations:
            editions_translations = editions_translations.splitlines()
            for et in editions_translations:
                if not et:
                    break
                my_dict = dict()
                my_dict['model'] = 'franciscanauthors_model.edition_translation'
                my_dict['pk'] = pk_editions_translations
                list_editions_translations.append(pk_editions_translations)
                pk_editions_translations += 1
                f = [('entry', et)]
                my_dict['fields'] = dict(f)
                final_data.append(my_dict)


        l = [('name_bold', name_bold) , ('name_date', name_date), ('name_original', name_original), ('name_latin', name_latin), ('personalia', personalia), \
             ('literature', literature), ('editions', list_editions), ('manuscripts', list_manuscripts),('manuscripts_editions', list_manuscripts_editions), \
             ('literature_editions', literature_editions), ('vitea', vitea), ('vitea_biographies', vitea_biographies), ('works_editions', works_editions),\
             ('editions_music', editions_music), ('surviving_works', surviving_works),('edities_studies', edities_studies), \
             ('manuscripts_editions_literature', manuscripts_editions_literature), ('salimbenes_literary_legacy', salimbenes_literary_legacy), \
             ('editions_translations', list_editions_translations), ('studies', studies), ('translations', list_translations), ('primo_vita_bona', primo_vita_bona), ('letter', let)]
        '''
        #list_date = []
        list_date = 0
        if name_date:
            my_dict = dict()
            my_dict['model'] = 'franciscanauthors_model.date_precision'
            my_dict['pk'] = pk_date_precision
            #list_date.append(str(pk_date_precision))
            list_date = pk_date_precision
            date_precision = ''
            if name_date:
                date_precision = name_date
            elif has_four_digits(name_original):
                date_precision = name_original
            my_dict['fields'] = {'date_precision_id': pk_date_precision ,
                                 'date_precision': date_precision}
            pk_date_precision += 1
            final_data.append(my_dict)


        my_dict = dict()
        my_dict['model'] = 'franciscanauthors_model.author'
        if name_original == None:
            name_original = ""
        my_dict['fields'] = {'author_name': name_original.rstrip(','),
                  'biography': personalia,
                  'birth': '', 'death': '',
                  'checked': False,
                  }
        if list_date != 0:
            my_dict['fields']['birth_date_precision'] = list_date
            my_dict['fields']['death_date_precision'] = list_date
        my_dict['pk'] = pk_author
        final_data.append(my_dict)

        if name_latin == None:
            name_latin = ""

        my_dict = dict()
        my_dict['model'] = 'franciscanauthors_model.alias'
        my_dict['fields'] = {'author_id': pk_author, 'alias': name_latin}
        my_dict['pk'] = pk_alias
        final_data.append(my_dict)

        pk_alias += 1

        my_dict = dict()
        my_dict['model'] = 'franciscanauthors_model.works'
        my_dict['fields'] = {'author_id':pk_author ,'text': works}
        my_dict['pk'] = pk_works
        final_data.append(my_dict)

        my_dict = dict()
        my_dict['model'] = 'franciscanauthors_model.works'
        my_dict['fields'] = {'author_id':pk_author ,'text': works}
        my_dict['pk'] = pk_works
        final_data.append(my_dict)

        my_dict = dict()
        my_dict['model'] = 'franciscanauthors_model.additional_info'
        my_dict['fields'] = {'author_id':pk_author ,'add_comments': literature}
        my_dict['pk'] = pk_additional_info
        final_data.append(my_dict)

        pk_author += 1
        pk_works += 1
        pk_additional_info += 1

        #my_dict['fields'] = {'year': }

        '''
        my_dict = dict()
        my_dict['model'] = 'franciscanauthors_model.record'
        my_dict['pk'] = pk
        pk += 1
        my_dict['fields'] = dict(l)
        final_data.append(my_dict)
        '''

with open('../../franciscanauthors_data/fixtures/fixture_5-07.json', 'w') as f:
    json.dump(final_data, f, indent=2)