#!/usr/bin/env python
from html.parser import HTMLParser
from bs4 import BeautifulSoup as bs
import os
from pathlib import Path
import sys

path_base = Path(sys.argv[1] if len(sys.argv) > 1 else '.')

html = path_base.joinpath('src/index.html').open()
soup = bs(html, 'html.parser')
html_links = soup.find(class_="cb-links")

path_output = path_base.joinpath('static/')
pathlist = path_output.joinpath('files/').rglob('*')
path_output_len = len(path_output.parts)
for path in pathlist:
    print('===> path: ' + str(path))
    path_strip = Path().joinpath(*path.parts[path_output_len:])
    link = soup.new_tag('a', href=str(path_strip))
    link.string = path_strip.stem
    html_links.append(link)

print(soup)

path_output.joinpath('index.html').write_text(str(soup))

# class Files(HTMLParser):

# files = Files()
# files.feed()
