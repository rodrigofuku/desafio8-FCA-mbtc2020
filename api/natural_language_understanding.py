from ibm_watson import NaturalLanguageUnderstandingV1, ApiException
from ibm_cloud_sdk_core.authenticators import BasicAuthenticator
from ibm_watson.natural_language_understanding_v1 import Features, EntitiesOptions

def analise_sentimento(texto):

    authenticator = BasicAuthenticator('apikey', '<API Key>')

    natural_language_understanding = NaturalLanguageUnderstandingV1(
        version='2020-09-14',
        authenticator=authenticator
    )

    natural_language_understanding.set_service_url('<URL>')

    try:
        texto_analisado = natural_language_understanding.analyze(
            text=texto,
            features=Features(entities=EntitiesOptions(sentiment=True, mentions=True, model='<model>'))).get_result()

    except ApiException as ex:
        print('Ocorreu um erro durante o processamento da informação. Status code: ' + str(ex.code) + ' => ' + ex.message)

    #print(json.dumps(texto_analisado, indent=2))

    return texto_analisado