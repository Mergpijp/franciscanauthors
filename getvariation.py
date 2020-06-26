from bs4 import BeautifulSoup
import re
import bs4
import json
from collections import OrderedDict

letters = list(map(chr, range(97, 118)))
bold_list = list()
filename = '../franciscanauthors_data/heads.txt'


def get_bold(tag):
    while True:
        if tag:
            test = tag.find('b')
        else:
            return None
        if test is None or test == -1:
            if tag.nextSibling is None:
                return None
            else:
                tag = tag.nextSibling.nextSibling
        elif test.name == 'b':
            return test.text.strip()


for let in letters:
    #let = 'm'
    with open("../franciscanauthors_data/franaut"+let+".htm", "r") as f:
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
    if let == 'm':
        lemmas.pop(0)

    for lemma in lemmas:
        tag = lemma.find('p')
        if tag and tag.nextSibling:
            tag = tag.nextSibling.nextSibling
        else:
            continue
        value = get_bold(tag)
        if value is not None and not value in bold_list:
            bold_list.append(value)

with open(filename, mode="w") as outfile:  # also, tried mode="rb"
    for s in bold_list:
        outfile.write("%s\n" % s)



