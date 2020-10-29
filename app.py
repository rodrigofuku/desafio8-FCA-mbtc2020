import json
from flask import Flask, request, jsonify
from api import speech_to_text
from api import natural_language_understanding
from api import recomendacao


app = Flask(__name__)

@app.route('/api/recommend', methods=['POST'])
def inicio():

    requisicao = json.dumps(request.form, indent=2)
    validacao = requisicao.split(':')

    if 'car' in requisicao[0:11] and len(requisicao) > 15 and len(validacao[0]) == 9:

        if len(validacao) > 2:

            if 'text' in requisicao:
                if 'text' in validacao[1]:

                    if len(validacao[2]) >= 20:
                        texto = json.loads(requisicao)

                        if texto['text'] != '':

                            try:
                                texto_analisado = natural_language_understanding.analise_sentimento(texto['text'])
                            except ValueError:
                                print('Ocorreu um erro inesperado. Tente novamente. ' + ValueError)

                            try:
                                veiculo_recomendado = recomendacao.carro_recomendado(texto['car'], texto_analisado)
                            except ValueError:
                                print('Ocorreu um erro inesperado. Tente novamente. ' + ValueError)

                            return jsonify(veiculo_recomendado)

                        else:
                            return jsonify({
                               "recommendation": "",
                               "entities": []
                                })

                    else:
                        return jsonify({
                            "recommendation": "",
                            "entities": []
                        })

                else:
                    return jsonify({
                        "recommendation": "",
                        "entities": []
                        })
            else:
                arquivo = ''
                for filename, file in request.files.items():
                    arquivo = request.files[filename]

                if arquivo:
                    if 'audio' in arquivo.content_type:

                        transcricao = speech_to_text.transcricao(arquivo)

                        try:
                            texto_transcrito = transcricao['results'][0]['alternatives'][0]['transcript']
                        except ValueError:
                            print('Ocorreu um erro inesperado. Tente novamente. ' + ValueError)

                        texto = json.loads(requisicao)

                        if len(texto_transcrito) >= 20:
                            try:
                                texto_analisado = natural_language_understanding.analise_sentimento(texto_transcrito)
                            except ValueError:
                                print('Ocorreu um erro inesperado. Tente novamente. ' + ValueError)

                            try:
                                veiculo_recomendado = recomendacao.carro_recomendado(texto['car'], texto_analisado)
                            except ValueError:
                                print('Ocorreu um erro inesperado. Tente novamente. ' + ValueError)

                            return jsonify(veiculo_recomendado)

                        else:
                            return jsonify({
                               "recommendation": "",
                               "entities": []
                                })

                    else:
                        return jsonify({
                           "recommendation": "",
                           "entities": []
                            })

                else:
                    return jsonify({
                       "recommendation": "",
                       "entities": []
                        })

        else:
            return jsonify({
                       "recommendation": "",
                       "entities": []
                   })
    else:
        return jsonify({
                       "recommendation": "",
                       "entities": []
                   })


if __name__ == '__main__':
    app.run(host='0.0.0.0',  port=8080)