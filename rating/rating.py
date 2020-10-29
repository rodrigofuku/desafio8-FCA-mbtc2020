import json
from flask import Flask, request, jsonify
from api import speech_to_text
from api import natural_language_understanding
from api import recomendacao

import os
import csv


@app.route('/api/dataset', methods=['GET'])
def dataset():
    path = 'C:/Users/RODRIGO/Documents/Profissional/IBM/train_dataset/'
    arquivos = os.listdir(path)
    dataset = []
    indice = 0
    with open('dataset.csv', 'w', encoding='utf-8') as dataset1:
        dataset1.write('indice,entity,sentiment,mention\n')

    for arquivo in arquivos:
        path_arquivo = path + arquivo
        with open(path_arquivo, 'r', encoding='utf-8') as texto:
            texto_arquivo = texto.read()

        texto_analisado = natural_language_understanding.analise_sentimento(texto_arquivo)

        for entidade in texto_analisado['entities']:
            sentiment = entidade['sentiment']['score']
            mention = entidade['text']
            entity = entidade['type']
            with open('dataset.csv', 'a', newline='', encoding='utf-8') as dataset2:
                gravacao = csv.writer(dataset2)
                gravacao.writerow([indice, entity, sentiment, mention])

        indice += 1


    return jsonify(arquivos)

