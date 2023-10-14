from collections import defaultdict
import pandas as pd
from ascii_graph import colors
from ascii_graph import Pyasciigraph
import collections
from _collections_abc import Iterable 
collections.Iterable = Iterable
import random
import tqdm
import time
import rich.traceback
import rich
from rich.progress import track
import argparse
import os

rich.get_console().clear()
rich.get_console().rule('Tęczowy histogram')
x = defaultdict()
x_filtred = defaultdict()

parser = argparse.ArgumentParser(description='Simple script.')
parser.add_argument('file_name', help='Name of the file to read')
parser.add_argument('-l', '--words', default=10)
parser.add_argument('-f', '--lenght', default=0 )
parser.add_argument('-i', '--ignore', nargs='+', default=[])
parser.add_argument('-s', '--ignore_symbols', type=str, default="")
parser.add_argument('-d', '--directory', type=str, default="") #całkowita ścieżka do katalogu
parser.add_argument('-w', '--word_in_text', type=str, default="") 

args = parser.parse_args()
directory = args.directory

if directory != "":
    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)
        if os.path.isfile(f) and f.endswith('.txt'):
            with open(f, 'r') as file:
                for line in tqdm.tqdm(file):
                    words = line.split()
                    for word in words:
                        word = word.strip(args.ignore_symbols)
                        if len(word) <= int(args.lenght):
                            continue
                        if word in args.ignore:
                            continue
                        if args.word_in_text not in word:
                            continue
                        if word in x:
                            x[word] += 1  
                        else:
                            x[word] = 1 
else:
    with open(args.file_name, 'r') as file:
        for line in tqdm.tqdm(file):
            words = line.split()
            for word in words:
                word = word.strip(args.ignore_symbols)
                if len(word) <= int(args.lenght):
                    continue
                if word in args.ignore:
                    continue
                if word in x:
                    x[word] += 1  
                else:
                    x[word] = 1

for klucz, wartosc in x.items():
    if wartosc > int(args.words):
        x_filtred[klucz] = wartosc

 
graph = Pyasciigraph()
sorted_by_value= sorted(x_filtred.items(), key=lambda x:x[-1], reverse=True)

list1= list(sorted_by_value)
dostepne_kolory = [colors.Red, colors.Yel , colors.Gre,colors.Cya,colors.Blu , colors.Pur]

for i in range(len(list1)):
    kolor = dostepne_kolory[i % len(dostepne_kolory)]
    list1[i] = (list1[i][0], list1[i][1], kolor)


for line in graph.graph('Wyniki', list1):
    print(line)