# ROSIE
![rosie](imagens/rosie.png)

## Sua assistente pessoal
Últimas Notícias, Todoist, Previsão do tempo, Spotify, Controle de dispositivos IoT (MQTT)...

CARISMA 100%, FRANQUEZA  1000%

## Dependências
- bs4 (BeautifulSoup4)
- gtts
- gcloud
- google-api-python-client
- paho.mqtt
- pyaudio
- playsound
- requests
- speech_recognition
- subprocess
- webbrowser 

## Instalação

Clonar o Repositório:

`git clone https://github.com/ricardomerces/RosieAssistentePessoal.git`

Entrar no diretório RosieAssistentePessoal:

`cd RosieAssistentePessoal`

Criar um ambiente virtual:

`python3 -m virtualenv venv`

Ativar o ambiente virtual:

`source venv/bin/activate`

Instalar as dependências:

`pip install -r requirements.txt`

Instalar a Rosie

`python3 setup.py install`


## Como utilizar a ROSIE ?

Escolha a API a ser utilizada com o Speech Recognition (Speech to Text)
https://github.com/Uberi/speech_recognition

Crie o arquivo **`config.json`** a partir do template **`config.json.template`**  e configure **TODOS os parâmetros!**(hotword, mqtt, Openweather(key), todoist(key/projeto), etc).


## Quickstart

`cd RosieAssistentePessoal`

`python3 rosieAsistentePessoal/rosie.py`

Cria Áudios (mensagens pré gravadas)

`python3 rosieAsistentePessoal/cria_audio`

## Comandos / Módulos

- **_liga/desativa BUNKER_**        Controla iluminação do escritório (IoT com MQTT)
- **_notícias_**                    Reproduz as últimas notícias
- **_tarefas_**                     Lista as tarefas não concluídas do INBOX (todoist)
- **_previsão do tempo_**           Informações sobre mínima e máxima (openweather)
- **_tempo agora_**                 Informações sobre temperatura e condição Climática (openweather)
- **_toca <NOME DO ÁLBUM>_**        Reproduz o álbum no spotify (web player)