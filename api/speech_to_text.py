from ibm_watson import SpeechToTextV1, ApiException
from ibm_cloud_sdk_core.authenticators import BasicAuthenticator

def transcricao(arquivo):
    authenticator = BasicAuthenticator('apikey','<API Key>')
    speech_to_text = SpeechToTextV1(authenticator=authenticator)
    speech_to_text.set_service_url('<URL>')

    try:
        texto_transcrito = speech_to_text.recognize(
                                                    audio=arquivo,
                                                    content_type='audio/flac',
                                                    model='pt-BR_BroadbandModel',
                                                    #keywords=[],
                                                    #keywords_threshold=0.5,
                                                    #max_alternatives=3
                                                    ).get_result()
    except ApiException as ex:
        print('Ocorreu um erro durante o processamento da informação. Status code: ' + str(ex.code) + ' => ' + ex.message)

    #print(json.dumps(texto_transcrito, indent=2))

    return texto_transcrito