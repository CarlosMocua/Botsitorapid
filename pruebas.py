####################el bot eliminara mensajes que se confirmen con emojis###############

@bot.message_handler(content_types=['text'])
def handle_text_message(message):
    if message.chat.type == 'group' and message.reply_to_message:
        # Verificar si el mensaje tiene una reacción de emoji
        if message.reply_to_message.sticker:
            # Eliminar el mensaje original que contiene el emoji
            bot.delete_message(chat_id=message.chat.id, message_id=message.reply_to_message.message_id)
            # Eliminar el mensaje de reacción
            bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)


########################################bot respondera a los emojis##########################

@bot.message_handler(func=lambda message: message.text and any(char in message.text for char in "😀😃😄😁😆😅🤣😂🙂🙃😉😊😇"))
def handle_message(message):
    # Responde con un emoji
    bot.reply_to(message, "¡Recibí un emoji! 😄")

######################################## obtener sugerencias###################################

@bot.message_handler(commands=['sugerencias'])
def enviar_sugerencias(message):
    # Obtén las sugerencias del menú del día (puedes personalizar esta parte según tus necesidades)
    sugerencias = obtener_sugerencias_del_menu()

    # Envía las sugerencias al usuario
    if sugerencias:
        respuesta = "¡Aquí tienes las sugerencias del menú del día!\n\n"
        respuesta += sugerencias
    else:
        respuesta = "Hoy no hay sugerencias disponibles para el menú."

    bot.reply_to(message, respuesta)

######################################## obtener sugerencias###################################

@bot.message_handler(commands=['ubicacion'])
def enviar_ubicacion(message):
    # Configura las coordenadas de la ubicación
    latitude = 37.7749
    longitude = -122.4194
    # Crea el objeto de ubicación
    location = telebot.types.Location(latitude=latitude, longitude=longitude)
    # Envía la ubicación con el mini mapa
    bot.send_location(message.chat.id, latitude, longitude)
