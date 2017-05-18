#!/usr/bin/env python
# -*- coding: utf-8 -*-

import telebot
import sys
import platform
import time
import random
import requests
import time
from lxml import html

apiKey = '' #apiKey here

bot = telebot.TeleBot(apiKey)

@bot.message_handler(commands=['hola'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Probando, probando... Son las %s:%s:%s, ¡Una hora menos en Canarias!" % (time.localtime()[3], time.localtime()[4], time.localtime()[5]))

@bot.message_handler(commands=['acercade'])
def send_sysinfo(message):
    meminfo = dict((i.split()[0].rstrip(':'),int(i.split()[1])) for i in open('/proc/meminfo').readlines())
    for i in open('/proc/cpuinfo').readlines():
        if(i.startswith("model name")):
            cpu_model = i.split(':')
    bot.send_message(message.chat.id, "Soy el bot de TecnoUAB y actualmente funciono bajo Python %s ejecutado en %s. Dispongo de %sMB de RAM (tengo libres %sMB) y mi CPU es %s. Este grupo es del tipo %s" % (sys.version, platform.platform(), meminfo['MemTotal']/1024, meminfo['MemFree']/1024, cpu_model[1][:-1].lstrip(), message.chat.type))

@bot.message_handler(commands=['ordena'])
def send_sorted(message):
    numbers = message.text[8:].split(' ')
    numbers2 = []
    try:
        init = time.time()
        for i in numbers:
            numbers2.append(int(i))
        numbers2.sort()
        numbers_to_send = ' '.join(str(e) for e in numbers2)
        end = time.time()
        bot.send_message(message.chat.id, "Aquí tienes los números ordenados: %s. He tardado %ss en ordenarlos" % (numbers_to_send, str(end-init)))
    except ValueError:
        bot.send_message(message.chat.id, "¡No me trolees y pon solo números!")

@bot.message_handler(commands=['dado'])
def tirar_dado(message):
    dados = message.text.split(' ')
    caras = 0
    if(len(dados) > 1):
        try:
            caras = int(dados[1])
            bot.send_message(message.chat.id, ("Tirando dado de %s caras... ¡%s!" % (caras ,random.randint(1,caras))))
        except ValueError:
            bot.send_message(message.chat.id, "¡No existe ese tipo de dado!")
    else:
        bot.send_message(message.chat.id, "Tirando dado de 6 caras... ¡%s!" % random.randint(1,6))

@bot.message_handler(commands=['esquemas'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Estos son los esquemas")
    bot.sendPhoto(chat_id, 'https://github.com/Jocaru/tecnouabbot/blob/master/css_puns_01.png')

@bot.message_handler(commands=['profesor'])
def buscar_profesor(message):
    try:
        nombre_profesor = message.text[10:].replace(' ', '+')
        nombre_separado = nombre_profesor.split('+')
        r = requests.get('https://siastd.uab.es/pcde/resultats_cerca.jsf?busqueda=%s&selectBusqueda=1&idioma=ca&pais=ES' % nombre_profesor)
        html_busqueda = html.fromstring(r.content)
        inicio = r.content.find('fitxa_')
        nombre = nombre_separado[0].title()
        nombre = nombre.encode('ascii', 'ignore')
        fin = r.content.find(nombre)
        url = r.content[inicio:fin-2]
        t = requests.get('https://siastd.uab.es/pcde/%s' % url)
        html_profesor = html.fromstring(t.content)
        datos = html_profesor.xpath('//a[@class="list-group-item"]/text()')
        dato = datos[7]
        despacho = datos[9]
        telefono = datos[11]
        direccion = datos[13]

        bot.send_message(message.chat.id, ("%s %s %s %s" % (dato, despacho, telefono, direccion)))
    except ValueError:
        bot.send_message(message.chat.id, 'Ha habido algún error... %s' % ValueError)
    except IndexError:
        bot.send_message(message.chat.id, 'Ha habido algún error... %s' % IndexError)

bot.polling(none_stop=True, interval=0)

