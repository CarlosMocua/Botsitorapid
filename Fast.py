from config import * #importamos el token
import telebot  #para manejar la API de telegram
import yaml     #para manejar base de conocimiento yaml
import random   #biblioteca para manejar las respuestas
import codecs   #para que se acepten caracteres especiales
from telegram.ext import Updater, CommandHandler # para recibir y actualizar mensajes
from telebot.types import ForceReply # para citar un mensaje
from telebot.types import InlineKeyboardButton # se ocupa para los botones inline
from telebot.types import InlineKeyboardMarkup # se ocupa para los botones inline
from telebot import types


#instanciasmos el bot de telegram
bot = telebot.TeleBot(TELEGRAM_TOKEN)


usuarios={}        #diccionario de datos del usuario
selecciones={}     #donde se almacena la seleccion del menu
grupo_id = -1001895538269   #grupo donde se mandan los pedidos

#variable para almacenar los comandos disponibles
commands = {
    "pedido": "Realiza un pedido",
    "promos": "Muestra las promociones disponibles",
    "info": "Obtiene información adicional",
    "ubicacion": "Conoce nuestro local"
}

###################################### Comandos ########################################
#responder al comando promo
@bot.message_handler(commands=["promos","promociones"])
def send_promos(message):
    # Lista de rutas de las imágenes
    image_paths = ['imgs/oferta1.png', 'imgs/oferta2.png','imgs/oferta3.png']
    # Envía las imágenes al usuario
    for image_path in image_paths:
        with open(image_path, 'rb') as f:
            bot.send_photo(message.chat.id, f,caption="Aprovecha nuestras OFERTAS!!!")

#responder al comando info
@bot.message_handler(commands=["info","informacion"])
def cmd_info(message):
    response_text = "Rapid Food es una empresa de comida rápida que te ofrece una experiencia culinaria rápida, sabrosa y conveniente. Nuestro menú está lleno de deliciosas opciones para satisfacer todos los antojos. Desde hamburguesas jugosas y papas fritas crujientes hasta sabrosos tacos y refrescantes batidos, tenemos algo para todos los amantes de la comida rápida. Utilizamos ingredientes frescos y de alta calidad para garantizar que cada bocado sea una explosión de sabor. Además, nuestro servicio amable y eficiente te asegurará una experiencia sin complicaciones. ¡Ven a visitarnos y disfruta de la mejor comida rápida en la ciudad en Rapid Food!"
    with open('imgs/info1.jpg', 'rb') as photo:
        bot.send_photo(message.chat.id, photo, caption=response_text)

#responder al mensaje comandos
@bot.message_handler(func=lambda message: 'comandos' in message.text.lower())
def cmd_start(message):
    response_text = "Comandos disponibles:\n"
    for command, description in commands.items():
        response_text += f"/{command}: {description}\n"
    with open('imgs/intro.jpg', 'rb') as photo:
        bot.send_photo(message.chat.id, photo, caption=response_text)

#responder al Comando ubicacion
@bot.message_handler(commands=['ubicacion'])
def mostrar_ubicacion(message):
    latitude = 15.524935
    longitude = -89.334238
    enlace_maps = f'https://www.google.com/maps?q={latitude},{longitude}'
    mensaje = f'Puedes ubicarnos en esta dirección:\n{enlace_maps}'
    bot.send_message(message.chat.id, mensaje)

#responder al Comando opciones
@bot.message_handler(func=lambda message: 'opciones' in message.text.lower())
def cmd_start(message):
    response_text = "Comandos disponibles:\n"
    for command, description in commands.items():
        response_text += f"/{command}: {description}\n"
    with open('imgs/intro.jpg', 'rb') as photo:
        bot.send_photo(message.chat.id, photo, caption=response_text)

################################## incio del telegram ######################################
@bot.message_handler(commands=["start"])
def cmd_start(message):
    response_text = "Bienvenido a Rapid Food es un placer tenerte acá, puedo responder dudas sobre nuestros productos o bien utiliza alguno de nuestros comandos disponibles:\n"
    for command, description in commands.items():
        response_text += f"/{command}: {description}\n"
    with open('imgs/intro.jpg', 'rb') as photo:
        bot.send_photo(message.chat.id, photo, caption=response_text)
########################################## pedidos#########################################

#al inicias el pedido pregunta como se llama
@bot.message_handler(commands=["pedido"])
def cmd_pedido(message):
    markup = ForceReply()
    msg = bot.send_message(message.chat.id, "Buen dia, con que nombre registraras tu orden?", reply_markup=markup)
    bot.register_next_step_handler(msg, intermediario)

#ocupamos la funcion para guardar el nombre y saludarlo
def intermediario(message):
    usuarios[message.chat.id] = {}
    usuarios[message.chat.id]["nombre"]= message.text
    markup = ForceReply()
    msg = bot.send_message(message.chat.id,"Hola" + " " +usuarios[message.chat.id]["nombre"])
    mostrar_menu(message.chat.id)

#desplegamos el menu con botones inline de telegram
def mostrar_menu(chat_id):
    markup = types.InlineKeyboardMarkup(row_width=2) #numero de columnas para los botones
    item1 = types.InlineKeyboardButton("Pierna - Q15", callback_data='pierna')
    item2 = types.InlineKeyboardButton("Cuadril - Q20", callback_data='cuadril')
    item3 = types.InlineKeyboardButton("Papas Rapid - Q25", callback_data='papasr')
    item4 = types.InlineKeyboardButton("Salchipapas - Q23", callback_data='salchipapa')
    item5 = types.InlineKeyboardButton("Papas Locas - Q21", callback_data='papasl')
    item6 = types.InlineKeyboardButton("Nachos - Q25", callback_data='nachos')
    item7 = types.InlineKeyboardButton("Hamburguesa Class- Q14", callback_data='hamburguesacs')
    item8 = types.InlineKeyboardButton("Hamburguesa c/ Papas - Q20", callback_data='hamburguesacp')
    item9 = types.InlineKeyboardButton("Good Burguer - Q35", callback_data='goodb')
    item10 = types.InlineKeyboardButton("Gaseosa lata - Q8", callback_data='gaseosal')
    item11 = types.InlineKeyboardButton("Refresco Natural - Q4", callback_data='refrescon')
    item12 = types.InlineKeyboardButton("Total de Pedido", callback_data='ver_selecciones')
    item13 = types.InlineKeyboardButton("Finalizar Pedido", callback_data='finalizar_pedido')
    item14 = types.InlineKeyboardButton("Cancelar", callback_data='cancelar')
#manera de distribuir los botones por grupos
    markup.add(item1, item2, item3, item4, item5, item6, item7, item8, item9, item10, item11)
    markup.add(item12, item13, item14)
#saludo para la bienvenida al menu
    bot.send_message(chat_id, "Bienvenido al menú del restaurante. ¿Qué te gustaría ordenar?", reply_markup=markup)

# Obtener el precio de la selección
def obtener_precio(seleccion):
    precios = {
        'pierna': 15,
        'cuadril': 20,
        'papasr': 25,
        'salchipapa': 23,
        'papasl': 21,
        'nachos': 25,
        'hamburguesacs': 14,
        'hamburguesacp': 20,
        'goodb': 35,
        'gaseosal': 8,
        'refrescon': 4,
    }
    return precios.get(seleccion, 0)


# Manejar la selección del botón inline
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    global selecciones
    seleccion = call.data
    chat_id = call.message.chat.id

    if seleccion == 'cancelar':
        if chat_id in selecciones:
            del selecciones[chat_id]
        bot.send_message(chat_id, "Has cancelado la selección. Se ha vaciado el pedido.")
    elif seleccion == 'ver_selecciones':
        ver_selecciones(call.message)
    elif seleccion == 'finalizar_pedido':
        solicitar_direccion(call.message)
    else:
        if chat_id not in selecciones:
            selecciones[chat_id] = []

        precio = obtener_precio(seleccion)
        selecciones[chat_id].append({'seleccion': seleccion, 'precio': precio})

# Mensaje de seleccion
        if seleccion == 'pierna':
            bot.send_message(chat_id, "Has seleccionado una Pierna.")
        elif seleccion == 'cuadril':
            bot.send_message(chat_id, "Has seleccionado una Cuadril.")
        elif seleccion == 'papasr':
            bot.send_message(chat_id, "Has seleccionado una Papas Rapid.")
        elif seleccion == 'salchipapa':
            bot.send_message(chat_id, "Has seleccionado una Salchipapas.")
        elif seleccion == 'papasl':
            bot.send_message(chat_id, "Has seleccionado una Papas Locas.")
        elif seleccion == 'nachos':
            bot.send_message(chat_id, "Has seleccionado una Nachos.")
        elif seleccion == 'hamburguesacs':
            bot.send_message(chat_id, "Has seleccionado una Hamburguesa Clasica.")
        elif seleccion == 'hamburguesacp':
            bot.send_message(chat_id, "Has seleccionado una Hamburguesa con Papas.")
        elif seleccion == 'goodb':
            bot.send_message(chat_id, "Has seleccionado una Good Burguer.")
        elif seleccion == 'gaseosal':
            bot.send_message(chat_id, "Has seleccionado una Gaseosa lata.")
        elif seleccion == 'refrescon':
            bot.send_message(chat_id, "Has seleccionado una Refresco Natural.")
# vuelve a mostrar el menu
        mostrar_menu(chat_id)

# Función para desplegar las selecciones almacenadas en variable
def ver_selecciones(message):
    global selecciones
    chat_id = message.chat.id

    if chat_id not in selecciones or not selecciones[chat_id]:
        bot.send_message(chat_id, "Aún no has realizado ninguna selección.")
    else:
        total = 0
        mensaje = "Tus selecciones actuales son:\n"
        for seleccion in selecciones[chat_id]:
            mensaje += f"{seleccion['seleccion']} - Q{seleccion['precio']}\n"
            total += seleccion['precio']
        mensaje += f"Total: Q{total}"
        bot.send_message(chat_id, mensaje)

# Función para solicitar la dirección
def solicitar_direccion(message):
    markup = types.ForceReply()
    msg = bot.send_message(message.chat.id, "Por favor, ingresa tu dirección de envío:", reply_markup=markup)
    bot.register_next_step_handler(msg, solicitar_telefono)

# Función para solicitar el número de teléfono de contacto
def solicitar_telefono(message):
    chat_id = message.chat.id
    direccion = message.text

    markup = types.ForceReply()
    msg = bot.send_message(chat_id, "Por favor, ingresa tu número de teléfono de contacto:", reply_markup=markup)
    bot.register_next_step_handler(msg, mostrar_informacion, direccion)

# Función para mostrar la dirección, número de teléfono y enviar la información al grupo
def mostrar_informacion(message, direccion):
    chat_id = message.chat.id
    telefono = message.text

    usuarios[chat_id]["direccion"] = direccion
    usuarios[chat_id]["telefono"] = telefono

    texto = 'Tu pedido será enviado a:\n'
    texto += f'Enviar a: {usuarios[chat_id]["direccion"]}\n'
    texto += f'Teléfono de contacto: {usuarios[chat_id]["telefono"]}\n'

    bot.send_message(chat_id, texto, parse_mode="html")
    ver_selecciones(message)

    # Enviar información al grupo
    if chat_id in usuarios and usuarios[chat_id]["nombre"] and usuarios[chat_id]["direccion"] and usuarios[chat_id]["telefono"]:
        nombre = usuarios[chat_id]["nombre"]
        direccion = usuarios[chat_id]["direccion"]
        telefono = usuarios[chat_id]["telefono"]
        pedido = selecciones[chat_id] if chat_id in selecciones else []
        enviar_informacion_grupo(nombre, direccion, telefono, pedido)

# Función para enviar la información al grupo
def enviar_informacion_grupo(nombre, direccion, telefono, pedido):
    mensaje = f'Nuevo pedido:\n\nNombre: {nombre}\nDirección: {direccion}\nTeléfono: {telefono}\n\nPedido:\n'
    total = 0
    for item in pedido:
        mensaje += f'{item["seleccion"]} - Q{item["precio"]}\n'
        total += item["precio"]
    mensaje += f'\nTotal: Q{total}'

    bot.send_message(grupo_id, mensaje)

####################################### Mensajes ######################################

#contestar enviando una imagen del menu si mencionan menu
@bot.message_handler(func=lambda message: 'menú' in message.text.lower())
def send_images(message):
    image_path = ['imgs/menu.jpg']
    for image_path in image_path:
        with open(image_path, 'rb') as f:
            bot.send_photo(message.chat.id, f,caption="Este es nuestro menu sera un gusto atenderte")

#contestar enviando un pdf del menu si mencionan pdf
@bot.message_handler(func=lambda message: 'pdf' in message.text.lower())
def send_pdf(message):
    pdf_path = 'docs/Menu.pdf'

    with open(pdf_path, 'rb') as f:
        bot.send_document(message.chat.id, f, caption="Es un placer servirte")

#contestar con imagenes si mencionan ofertas
@bot.message_handler(func=lambda message: 'ofertas' in message.text.lower())
def send_images(message):
    # Lista de rutas de las imágenes
    image_paths = ['imgs/oferta1.png', 'imgs/oferta2.png','imgs/oferta3.png']
    # Envía las imágenes al usuario
    for image_path in image_paths:
        with open(image_path, 'rb') as f:
            bot.send_photo(message.chat.id, f,caption="Aprovecha nuestras OFERTAS!!!")

# responde a los mensajes que no son comandos y que esten en la base de conocimiento
@bot.message_handler(content_types=["text"])
#busca la respuesta que corresponda al mensaje
def obtener_respuesta(mensaje):
    text = mensaje.text.lower()
    datos = cargar_base_datos()
    respuestas_coincidentes = []
    for entry in datos['respuestas']:
        pregunta = entry.get('pregunta', '').lower()
        response = entry.get('response', [])

        if pregunta and pregunta in text:
            respuestas_coincidentes.extend(response)

    if respuestas_coincidentes:
        respuesta_aleatoria = random.choice(respuestas_coincidentes)
        bot.reply_to(mensaje, respuesta_aleatoria)
    else:
        bot.reply_to(mensaje, "Lo siento, no puedo entender tu mensaje :(")

def cargar_base_datos():
    with codecs.open('./res.yml', 'r', 'utf-8') as archivo:
        datos = yaml.safe_load(archivo)
    return datos

#################################### MAIN #############################################
if __name__ == '__main__':
    bot.set_my_commands([
        telebot.types.BotCommand("/pedido", "Listo para hacer tu pedido"),
        telebot.types.BotCommand("/promos", "Conoce nuestras Promociones"),
        telebot.types.BotCommand("/ubicacion", "Conoce nuestro local"),
        telebot.types.BotCommand("/info", "Quienes somos")
    ])
try:
    print('Iniciando el bot')
    bot.polling()
except KeyboardInterrupt:
    print('fin')

