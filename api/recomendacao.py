import json
import pandas as pd

def carro_recomendado(carro, texto_analisado):

    veiculo_base = carro.upper()

    entidades_sentimentos = []
    for entidade in texto_analisado['entities']:
        sentiment = entidade['sentiment']['score']
        mention = entidade['text']
        entity = entidade['type']
        entidades_sentimentos.append({
                                    "entity": entity,
                                    "sentiment": sentiment,
                                    "mention": mention
                                    })

    if entidades_sentimentos:
        dataframe_veiculo_base = pd.DataFrame(entidades_sentimentos)
        sentimento_geral = dataframe_veiculo_base['sentiment'].mean()

        if sentimento_geral > 0:
            return {
                       "recommendation": "",
                       "entities": []
                   }
        else:

            entidades_sentimentos2 = dataframe_veiculo_base.groupby(by='entity').mean().sort_values(by='sentiment', ascending=True)

            prioridade = {
                'SEGURANCA': 1,
                'CONSUMO': 2,
                'DESEMPENHO': 3,
                'MANUTENCAO': 4,
                'CONFORTO': 5,
                'DESIGN': 6,
                'ACESSORIOS': 7,
                "MODELO": 8
            }

            primeiro = entidades_sentimentos2.head(1)

            if len(entidades_sentimentos2) > 1:

                cont = True
                while cont:
                    ultimo = entidades_sentimentos2.tail(1)
                    diferenca = primeiro['sentiment'].values[0] - ultimo['sentiment'].values[0]

                    if abs(diferenca) >= 0.1:
                        entidades_sentimentos2 = entidades_sentimentos2.iloc[:-1, :]

                    else:
                        cont = False
                        lista_escolha_prioridade = []

                        for escolha in entidades_sentimentos2.iterrows():
                            lista_escolha_prioridade.append(prioridade[escolha[0]])
                        lista_escolha_prioridade.sort()
                        escolha_final = lista_escolha_prioridade[0]

                        for key, value in prioridade.items():
                            if value == escolha_final:
                                entidade_recomendacao = key

            else:
                prioridade_final = primeiro

                prioridade_final = prioridade_final.to_json()
                prioridade_final = json.dumps(prioridade_final).split('\"')
                entidade_recomendacao = prioridade_final[4][:-1]

            recomendacoes = {
                'ACESSORIOS': ['CRONOS', 'FIAT 500', 'ARGO', 'TORO'],
                'CONFORTO': ['LINEA', 'MAREA', 'FIAT 500', 'TORO', 'CRONOS', 'ARGO'],
                'CONSUMO': ['FIORINO', 'LINEA', 'FIAT 500', 'ARGO', 'MAREA', 'CRONOS'],
                'DESEMPENHO': ['FIAT 500', 'TORO', 'ARGO', 'LINEA', 'MAREA', 'CRONOS'],
                'DESIGN': ['ARGO', 'LINEA', 'FIORINO', 'TORO', 'MAREA', 'CRONOS', 'FIAT 500'],
                'MANUTENCAO': ['ARGO', 'TORO'],
                'MODELO': ['LINEA', 'CRONOS', 'FIORINO', 'ARGO', 'TORO', 'MAREA', 'FIAT 500'],
                'SEGURANCA': ['ARGO', 'TORO', 'CRONOS', 'FIAT 500', 'MAREA']
                }

            possiveis_recomendacoes = recomendacoes[entidade_recomendacao]

            for veiculo_recomendado in possiveis_recomendacoes:
                if veiculo_recomendado != veiculo_base:
                    resultado_recomendacao = veiculo_recomendado

                    return {
                            "recommendation": resultado_recomendacao,
                            "entities": entidades_sentimentos
                            }
    else:
        return {
                "recommendation": "",
                "entities": entidades_sentimentos
                }