'''
Rosie - Assistente Pessoal
Versão: 1.0
Autor: Ricardo Merces (twitter.com/r_merces)
Git: https://github.com/ricardomerces
'''

import json
from gtts import gTTS
import speech_recognition as sr
from subprocess import call         # MAC / LINUX
#from playsound import playsound    # WINDOWS :(
from requests import get
from bs4 import BeautifulSoup
import webbrowser as browser
from paho.mqtt import publish


##### CONFIGURAÇÕES #####

with open('config.json') as configuracao:
    configuracao = json.load(configuracao)

with open('credenciais/googleSpeech.json') as credenciais_google:
    credenciais_google = credenciais_google.read()

##### FUNÇÕES PRINCIPAIS #####

def monitora_audio():
    microfone = sr.Recognizer()
    with sr.Microphone() as source:
        while True:
            print("Aguardando o Comando: ")
            audio = microfone.listen(source)
            try:
                trigger = microfone.recognize_google_cloud(audio, credentials_json=credenciais_google, language='pt-BR')
                trigger = trigger.lower()

                if configuracao['hotword'] in trigger:
                    print('COMANDO: ', trigger)
                    responde('feedback')
                    executa_comandos(trigger)
                    break

            except sr.UnknownValueError:
                pass
            except sr.RequestError:
                pass

    return trigger

def responde(arquivo):
    call(['afplay', 'audios/' + arquivo + '.mp3'])

def cria_audio(mensagem):
    tts = gTTS(mensagem, lang='pt-br')
    tts.save('audios/mensagem.mp3')
    print('ROSIE:  ', mensagem)
    call(['afplay', 'audios/mensagem.mp3'])     # OSX
    #call(['aplay', 'audios/mensagem.mp3'])     # LINUX

def executa_comandos(trigger):

    if 'liga o bunker' in trigger:
        publica_mqtt('office/iluminacao/status', '1')

    elif 'desativa o bunker' in trigger:
        publica_mqtt('office/iluminacao/status', '0')

    elif 'notícias' in trigger:
        ultimas_noticias()

    elif 'toca' in trigger and 'bee gees' in trigger:
        playlists('bee_gees')

    elif 'toca' in trigger and 'taylor davis' in trigger:
        playlists('taylor_davis')

    elif 'tarefas' in trigger:
        todoistInbox()

    elif 'temperatura hoje' in trigger or 'previsão do tempo' in trigger:
        previsao_tempo(minmax=True)

    elif 'tempo agora' in trigger:
        previsao_tempo(tempo=True)

    else:
        mensagem = trigger.strip(configuracao['hotword'])
        if len(mensagem)<=1:
            responde('comando_nulo')

        else:
            print('esta é a mensagem: ', mensagem)
            cria_audio(mensagem)
            print('COMANDO INVÁLIDO: ', mensagem)
            responde('comando_invalido')

##### FUNÇÕES dos COMANDOS #####

def todoistInbox():
    tarefas = get(
        "https://beta.todoist.com/API/v8/tasks",
        params={
            "project_id": configuracao['todoIstProjectId']
        },
        headers={
            "Authorization": f"Bearer {configuracao['apiDoIst']}"
        }).json()

    for tarefa in tarefas:
        mensagem = tarefa['content']
        cria_audio(mensagem)

def playlists(album):
    if album == 'bee_gees':
        browser.open('https://open.spotify.com/track/33ALuUDfftTs2NEszyvJRm')
    elif album == 'taylor_davis':
        browser.open('https://open.spotify.com/track/3MKep4BfEwSlAHuFJrA9aV')

def previsao_tempo(tempo=False, minmax=False):
    site = get('http://api.openweathermap.org/data/2.5/weather?id=3451190&APPID=' + configuracao['apiOpenWeather'] + '&units=metric&lang=pt')
    clima = site.json()
    temperatura=round(clima['main']['temp'])
    minima=clima['main']['temp_min']
    maxima=clima['main']['temp_max']
    descricao=clima['weather'][0]['description']
    if tempo:
        mensagem = f'No momento fazem {temperatura} graus com: {descricao}'
    elif minmax:
        mensagem = f'Previsão para hoje: Mínima de {minima} e máxima de {maxima} graus'
    cria_audio(mensagem)

def publica_mqtt(topic, payload):
    publish.single(topic, payload=payload, qos=1, retain=True, hostname=configuracao['mqttBroker'], port=configuracao['mqttPort'], client_id='rosie', auth={'username': configuracao['mqttUser'], 'password': configuracao['mqttPassword']})
    if payload == '1':
        mensagem = 'Bunker Ligado!'
    elif payload == '0':
        mensagem = 'Bunker Desligado!'
    cria_audio(mensagem)

def ultimas_noticias():
    site = get('https://news.google.com/news/rss?ned=pt_br&gl=BR&hl=pt')
    noticias = BeautifulSoup(site.text, 'html.parser')
    for item in noticias.findAll('item')[:7]:
        mensagem = item.title.text
        cria_audio(mensagem)


def main():
    while True:
        monitora_audio()

main()




