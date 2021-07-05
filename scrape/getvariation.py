import pdb

from bs4 import BeautifulSoup
import re
import bs4
import json
from collections import OrderedDict

#letters = list(map(chr, range(97, 98)))
letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'y']
bold_list = list()
filename = '../../franciscanauthors_data/heads.txt'


def get_bold(tag, bold_list):
    while True:
        if tag:
            test = tag.find('b')
        else:
            return bold_list
        if test is None or test == -1 or isinstance(test,int):
            if tag.nextSibling is None:
                return bold_list
            else:
                tag = tag.nextSibling  #.nextSibling
        elif test.name == 'b':
            text = test.text.strip()
            if text not in bold_list and "(" not in text:
                bold_list.append(text)
            tag = tag.nextSibling


for let in letters:
    #let = 'm'
    if let == 'y':
        with open("../../franciscanauthors_data/fraanony.htm", "r") as f:
            contents = f.read()

            soup = BeautifulSoup(contents, 'html')

            print(soup.h2)
            print(soup.head)
            print(soup.li)
    else:
        with open("../../franciscanauthors_data/franaut"+let+".htm", "r") as f:
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
    #if let == 'm':
    #    lemmas.pop(0)
    if let == 'u' and not lemmas:
        print("ABORT EMPTY")
        exit(1)

    for lemma in lemmas:
        tag = lemma.find('p')
        while tag is not None:
            test = tag.find('b')
            #if not isinstance(test, int) and test and 'Brandeburgensis' in test.text:
            #    pdb.set_trace()
            if test is None or test == -1 or isinstance(test,int):
                if tag: #and tag.nextSibling:
                    tag = tag.nextSibling #.nextSibling
                else:
                    break
            elif test.name == 'b':
                if tag:
                    if tag.nextSibling == "\n":
                        #pdb.set_trace()
                        tag = tag.b
                        if tag.b not in bold_list and tag.b and "(" not in tag.b:
                            bold_list.append(tag.text)
                    else:
                        tag = tag.nextSibling
                break
        if tag is None:
            continue
        #if let == 'u':
        #    x = get_bold(tag, bold_list)
        #    pdb.set_trace()

        bold_list = get_bold(tag, bold_list)
        '''
        while True:
            value = get_bold(tag)
            if value is not None:
                if not value in bold_list:
                    bold_list.append(value)
            else:
                break
        '''
with open(filename, mode="w") as outfile:  # also, tried mode="rb"
    for s in bold_list:
        outfile.write("%s\n" % s)



