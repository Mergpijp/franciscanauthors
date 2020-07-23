from bs4 import BeautifulSoup
import re
import bs4
import json
from collections import OrderedDict

letters = list(map(chr, range(97, 118)))
anonymous = ['fraanony.htm']

pk = 1
pk_manuscripts = 1
pk_manuscripts_editions = 1
pk_editions = 1
pk_translations = 1
pk_editions_translations = 1
final_data = list()

for let in letters:
#for any in anonymous:

    with open("../franciscanauthors_data/franaut"+let+".htm", "r") as f:
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
        manuscripts_bold = ''
        manuscripts = ''
        editions_bold = ''
        editions = ''
        translations_bold = ''
        translations = ''
        literature_bold = ''
        literature = ''

        (name_bold, end, tag) = var_bold_and_next_sentence(name_bold, end, tag)
        (name, end, tag) = find_content(name, end, tag)
        (manuscripts_bold, end, tag) = var_bold_and_next_sentence(manuscripts_bold, end, tag)
        (manuscripts, end, tag) = find_content(manuscripts, end, tag)
        (editions_bold, end, tag) = var_bold_and_next_sentence(editions_bold, end, tag)
        (editions, end, tag) = find_content(editions, end, tag)
        (translations_bold, end, tag) = var_bold_and_next_sentence(translations_bold, end, tag)
        (translations, end, tag) = find_content(translations, end, tag)
        (literature_bold, end, tag) = var_bold_and_next_sentence(literature_bold, end, tag)
        (literature, end, tag) = find_content(literature, end, tag)

        data.append((name_bold, name, manuscripts_bold, manuscripts, editions_bold, editions, translations_bold, translations,
                     literature_bold, literature))

    def helper(title):
        match = re.search('^(L|l)iterature((?!(/|&)).)*$|literatuur', title)
        if match:
            return 2
        match = re.search('^(E|e)diti?ons?((?!(/| and )).)*$|(E|e)dities((?!(/|en)).)*$|^Partial editions|editions/editions', title)
        if match:
            return 3
        match = re.search('^(m|M)anus?c?r?ipt?s?((?!(/|&| and )).)*$|(Latin|Some) manuscripts|mss|manuscripts \(predominantly based on Brady and Bougerol\)' \
                          , title)
        if match:
            return 4
        match = re.search('(m|M)anus(c?)(r?)ip(t?)s(/| and | & |/partial )(.?)edition(s?)((?!(/literature)).)*$|(E|e)ditions(/| and )manuscripts' \
                          , title)
        if match:
            return 5
        match = re.search('^editions( and |/)literature|^literature( and |/| & )editions', title)
        if match:
            return 6
        match = re.search('^vitae?((?!(biographies)).)*$', title)
        if match:
            return 7
        match = re.search('^vitae/biographies', title)
        if match:
            return 8
        match = re.search('^works/editions', title)
        if match:
            return 9
        match = re.search('^editions and music', title)
        if match:
            return 10
        match = re.search('^surviving works', title)
        if match:
            return 11
        match = re.search('^edities en studies^', title)
        if match:
            return 12
        match = re.search('^manuscripts/editions/literature', title)
        if match:
            return 13
        match = re.search('^Salimbene’s literary legacy.', title)
        if match:
            return 14
        match = re.search('^editions and translations', title)
        if match:
            return 15
        match = re.search('^studies', title)
        if match:
            return 16
        match = re.search('^translations((?!(edities)).)*$', title)
        if match:
            return 17
        match = re.search('^Primo, vita bona', title)
        if match:
            return 18
        return -1

    structured_data = list()

    for name_bold, name, manuscripts_bold, manuscripts, edition_bold, edition, translation_bold, translation, literature_bold, literature in data:

        data_list = [name_bold, name, 'null', 'null', 'null', 'null', 'null', 'null', 'null', 'null', 'null', 'null', 'null' \
                     , 'null', 'null', 'null', 'null', 'null', 'null']

        index = helper(manuscripts_bold)
        if index != -1:
            data_list[index] = manuscripts
        index = helper(edition_bold)
        if index != -1:
            data_list[index] = edition
        index = helper(translation_bold)
        if index != -1:
            data_list[index] = translation
        index = helper(literature_bold)
        if index != -1:
            data_list[index] = literature

        structured_data.append(tuple(data_list))

    for idx, (name_bold, name, literature, editions, manuscripts, manuscripts_editions, literature_editions, \
              vitea, vitea_biographies, works_editions, editions_music, surviving_works, edities_studies, \
              manuscripts_editions_literature, salimbenes_literary_legacy, editions_translations, \
              studies, translations, primo_vita_bona) in enumerate(structured_data):
        name_date = 'null'
        name_original = 'null'
        x = re.search('\(([^\)]+)\)', name_bold)
        if x:
            x = x.group(0)
            name_latin = re.search('^[^\(]+', name_bold)
            if name_latin:
                name_latin = name_latin.group(0)
            else:
                name_latin = 'null'
            name_date = re.search('(fl\.|d\.)(.*)', x)
            if name_date:
                substract = name_date.group(0)
                name_date = name_date.group(2)
                name_date = name_date[:-1]
                if substract in x:
                    name_original = x.replace(substract, '')
                    if len(name_original) == 1:
                        name_original = 'null'
                    else:
                        name_original = name_original[1:]
            else:
                name_date = x
        personalia = name
        manuscripts = manuscripts.splitlines()

        list_manuscripts = []
        for mscr in manuscripts:
            my_dict = dict()
            my_dict['model'] = 'franciscanauthors.manuscript_record'
            my_dict['pk'] = pk_manuscripts
            list_manuscripts.append(pk_manuscripts)
            pk_manuscripts += 1
            f = [('record', mscr)]
            my_dict['fields'] = dict(f)
            final_data.append(my_dict)

        manuscripts_editions = manuscripts_editions.splitlines()
        list_manuscripts_editions = []

        for mscre in manuscripts_editions:
            my_dict = dict()
            my_dict['model'] = 'franciscanauthors.manuscript_edition_record'
            my_dict['pk'] = pk_manuscripts_editions
            list_manuscripts.append(pk_manuscripts_editions)
            pk_manuscripts_editions += 1
            f = [('record', mscre)]
            my_dict['fields'] = dict(f)
            final_data.append(my_dict)

        editions = editions.splitlines()
        list_editions = []
        for edition in editions:
            my_dict = dict()
            my_dict['model'] = 'franciscanauthors.edition_record'
            my_dict['pk'] = pk_editions
            list_manuscripts.append(pk_editions)
            pk_editions += 1
            f = [('record', edition)]
            my_dict['fields'] = dict(f)
            final_data.append(my_dict)

        translations = translations.splitlines()
        list_translations = []
        for translation in translations:
            my_dict = dict()
            my_dict['model'] = 'franciscanauthors.translation_record'
            my_dict['pk'] = pk_translations
            list_manuscripts.append(pk_translations)
            pk_translations += 1
            f = [('record', translation)]
            my_dict['fields'] = dict(f)
            final_data.append(my_dict)

        editions_translations = editions_translations.splitlines()
        list_editions_translations = []
        for et in editions_translations:
            my_dict = dict()
            my_dict['model'] = 'franciscanauthors.edition_translation_record'
            my_dict['pk'] = pk_editions_translations
            list_manuscripts.append(pk_editions_translations)
            pk_editions_translations += 1
            f = [('record', et)]
            my_dict['fields'] = dict(f)
            final_data.append(my_dict)


        l = [('name_bold', name_bold) , ('name_date', name_date), ('name_original', name_original), ('name_latin', name_latin), ('personalia', personalia), \
             ('literature', literature), ('editions', list_editions), ('manuscripts', list_manuscripts),('manuscripts_editions', list_manuscripts_editions), \
             ('literature_editions', literature_editions), ('vitea', vitea), ('vitea_biographies', vitea_biographies), ('work_editions', works_editions),\
             ('editions_music', editions_music), ('surviving works', surviving_works),('edities_studies', edities_studies), \
             ('manuscripts_editions_literature', manuscripts_editions_literature), ('salimbenes_literary_legacy', salimbenes_literary_legacy), \
             ('editions_translations', list_editions_translations), ('studies', studies), ('translations', list_translations), ('primo_vita_bona', primo_vita_bona), ('letter', let)]

        my_dict = dict()
        my_dict['model'] = 'franciscanauthors.record'
        my_dict['pk'] = pk
        pk += 1
        my_dict['fields'] = dict(l)
        final_data.append(my_dict)


with open('../franciscanauthors_data/fixture_good.json', 'w') as f:
    json.dump(final_data, f, indent=2)