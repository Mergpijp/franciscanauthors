from bs4 import BeautifulSoup
import re
import bs4
import json
from collections import OrderedDict

with open("franauta.htm", "r") as f:
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
        if tag.name == 'p':
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
    if title == 'editions':
        return 2
    elif title == 'editions/literature':
        return 3
    elif title == 'manuscripts':
        return 4
    elif title == 'translations':
        return 5
    elif title == 'literature (selection)':
        return 6
    elif title == 'literature':
        return 7
    elif title == 'manuscripts/editions':
        return 8
    else:
        return -1

structured_data = list()

for name_bold, name, manuscripts_bold, manuscripts, edition_bold, edition, translation_bold, translation, literature_bold, literature in data:

    data_list = [name_bold, name, 'null', 'null', 'null', 'null', 'null', 'null', 'null']

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


final_data = list()
my_dict = OrderedDict()

for idx, (name_bold, name, edition, edition_literature, manuscripts, translations, literature_selection, literature, manuscripts_editions) in enumerate(structured_data):
    name_date = 'null'
    name_original = 'null'
    x = re.search('\(([^\)]+)\)', name_bold)
    if x:
        x = x.group(0)
        name_latin = re.search('^[^\(]+', name_bold)
        name_latin = name_latin.group(0)
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
    editions_literature = edition_literature.splitlines()
    manuscripts_editions = manuscripts_editions.splitlines()
    editions = edition.splitlines()
    literature = literature.splitlines()
    literature_selection = literature_selection.splitlines()
    translations = translations.splitlines()


    l = [('name_bold', name_bold) , ('name_date', name_date), ('name_original', name_original), ('name_latin', name_latin), ('personalia', personalia), \
         ('manuscripts', manuscripts), ('translations', translations), ('manuscripts_editions', manuscripts_editions), ('eidtions', editions), \
         ('editions_literature', editions_literature), ('literature', literature), ('literature_selection', literature_selection)]

    #final_data.append(l)
    my_dict[idx] = dict(l)

rs = json.dumps(my_dict)