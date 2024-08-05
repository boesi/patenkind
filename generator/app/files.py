#!/usr/bin/env python
from bs4 import BeautifulSoup as bs
import os
from pathlib import Path
from shutil import copytree
import sys
from jinja2 import Environment, FileSystemLoader, select_autoescape
from strictyaml import load, Map, Str


def getConfig(path):
    schema = Map({'headline': Str()})
    return load(path.joinpath('generator-config.yaml').read_text(encoding='utf8'), schema)

def getTemplate(path, config):
    env = Environment(
            loader = FileSystemLoader(path),
            autoescape = select_autoescape()
    )
    template = env.get_template("index.html")
    return template.render(headline=config['headline'])

def addFiles(path, html):
    soup = bs(html, 'html.parser')
    html_links = soup.find(class_="cb-links")

    # ignore dotted (hidden) files, needed for .gitignore, but might be useful for other files too
    pathlist = path.joinpath('files/').rglob('[!.]*')
    path_output_len = len(path.parts)
    for path in pathlist:
        path_strip = Path().joinpath(*path.parts[path_output_len:])
        link = soup.new_tag('a', href=str(path_strip))
        link.string = path_strip.stem
        html_links.append(link)
    return str(soup)

path_base = Path(sys.argv[1] if len(sys.argv) > 1 else '.')
path_output = path_base.joinpath('static/')
path_src = path_base.joinpath('src/')

config = getConfig(path_base)
html = getTemplate(path_src, config)
html = addFiles(path_base, html)

path_output.joinpath('index.html').write_text(html)
copytree(path_src.joinpath('assets'), path_output.joinpath('assets'), dirs_exist_ok=True)

