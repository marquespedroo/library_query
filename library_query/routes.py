from library_query import app
from flask import Flask, render_template, request
from unidecode import unidecode
import string
import re
from fuzzywuzzy import process
import csv

def read_csv(nome_arquivo):
    with open(nome_arquivo, 'r', encoding='UTF-8-SIG') as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=';')
        dados = [line for line in csv_reader]
    return dados

data = read_csv('acervo.csv')

for line in data:
    line['titulo'] = unidecode(str(line['titulo']))
    line['autor'] = unidecode(str(line['autor']))
    line['editora'] = unidecode(str(line['editora']))


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/consulta', methods=['POST'])
def consultar_livro():
    search_query = request.form['livro']
    search_query = unidecode(search_query).lower()
    search_query = search_query.translate(str.maketrans('', '', string.punctuation))

    default = re.compile(re.escape(search_query), re.IGNORECASE)

    matches = []
    for line in data:
        for key, value in line.items():
            if isinstance(value, str) and default.search(unidecode(str(value)).lower().translate(str.maketrans('', '', string.punctuation))):
                matches.append(line)
                break

    table_data = []
    if matches:
        for line in matches:
            table_data.append({
                'titulo': line['titulo'],
                'autor': line['autor'],
                'editora': line['editora']
            })

    return render_template('index.html', table_data=table_data)