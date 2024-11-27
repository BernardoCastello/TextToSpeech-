import azure.cognitiveservices.speech as speechsdk
from openai import OpenAI
from google.cloud import texttospeech
from google.oauth2 import service_account
import os, time
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# Texto a ser convertido para fala
text = """
Síntese de fala é o processo de produção artificial de fala humana. 
Um sistema informático utilizado para este propósito é denominado sintetizador de fala, e pode ser implementado em software ou hardware.
"""


def AzureTextToSpeech(text: str, timer:bool = True):
    init = None
    if timer:
        init = time.time()

    subscription_key = os.getenv("Azure_Key")
    region = os.getenv("Azure_Region")

    # Configuração do serviço
    speech_config = speechsdk.SpeechConfig(subscription=subscription_key, region=region)

    # Personalização da voz (opcional: escolha uma voz específica)
    speech_config.speech_synthesis_voice_name = "pt-BR-FranciscaNeural"

    # Nome do arquivo de saída
    file_name = "Audios\\Azure_Francisca.mp3"

    # Configuração para salvar o áudio em um arquivo
    audio_config = speechsdk.audio.AudioConfig(filename=file_name)

    # Configuração do sintetizador
    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)

    # Realiza a conversão e salva no arquivo
    print("Convertendo texto para fala...")
    result = speech_synthesizer.speak_text_async(text).get()

    # Verifica se houve sucesso ou erro
    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        pass
        #print(f"Texto convertido com sucesso! O áudio foi salvo em: {file_name}")
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        print(f"Erro: {cancellation_details.reason}")
        if cancellation_details.error_details:
            print(f"Detalhes do erro: {cancellation_details.error_details}")
    
    if time:
        print(f"Azure tempo de execução {time.time() - init}")


def OpenAiTextToSpeech(text: str, timer:bool = True):
    init = None
    if timer:
        init = time.time()

    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    speech_file_path = Path(__file__).parent / f"Audios\\OpenAI_Nova.mp3"

    response = client.audio.speech.create(
    model="tts-1",
    voice="nova",
    input=text,
    extra_query={
        "lang": "pt-br"
    })

    # Salve o áudio no arquivo especificado
    with open(speech_file_path, "wb") as f:
        f.write(response.content)

    if time:
        print(f"OpenIA tempo de execução: {time.time() - init}")



def GoogleTextToSpeech(text: str, timer:bool = True):
    init = None
    if timer:
        init = time.time()

    # Carregar credenciais diretamente do arquivo JSON
    credentials = service_account.Credentials.from_service_account_file("client_google.json")

    # Inicializar cliente com credenciais específicas
    client = texttospeech.TextToSpeechClient(credentials=credentials)

    # Configurar o texto a ser convertido
    input_text = texttospeech.SynthesisInput(text=text)

    # Configurar a voz
    voice = texttospeech.VoiceSelectionParams(
        language_code="pt-BR",
        name="pt-BR-Wavenet-A",
        ssml_gender=texttospeech.SsmlVoiceGender.FEMALE,
    )

    # Configurar o áudio de saída
    audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)

    # Fazer a requisição à API
    response = client.synthesize_speech(
        input=input_text, voice=voice, audio_config=audio_config
    )

    # Salvar o áudio
    with open("Audios\\Google_Wavenet-A.mp3", "wb") as out:
        out.write(response.audio_content)

    if time:
        print(f"Google tempo de execução: {time.time() - init}")


if __name__ == "__main__":
    AzureTextToSpeech(text=text)
    OpenAiTextToSpeech(text=text)
    GoogleTextToSpeech(text=text)