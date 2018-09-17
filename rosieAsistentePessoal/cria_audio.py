from gtts import gTTS
from subprocess import call     # MAC / LINUX

def cria_audio(audio):
    tts = gTTS(audio, lang='pt-br')
    tts.save('audios/comando_nulo.mp3')

    call(['afplay', 'audios/comando_nulo.mp3']) # OSX
    #call(['aplay', 'audios/hello.mp3'])  # LINUX

cria_audio('Estou meio surda, não entendi nada!')