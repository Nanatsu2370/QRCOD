import telebot
import qrcode

# Replace 'YOUR_TELEGRAM_BOT_TOKEN' with your actual Telegram bot token
bot = telebot.TeleBot('6570483766:AAFdWIlSVvvjza-lNHo4N6ySwNFjlZfBOw0')

# Replace 'YOUR_CHANNEL_USERNAME' with your actual channel username


# Initialize a list to keep track of the Telegram user IDs
user_ids = []

# Tuple to store the admin ID
admin_id = ('6829735291',)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    chat_id = message.chat.id

    # Replace 'YOUR_CHANNEL_ID' with your actual channel ID
    channel_id = '-1002072259855'  # Replace with the actual channel ID

    # Check if the user is subscribed to the channel
    try:
        user_info = bot.get_chat_member(channel_id, message.from_user.id)
        if user_info.status == "member" or user_info.status == "creator" or user_info.status == "administrator":
            bot.send_message(chat_id, "Hola soy un bot para generar QRCode de enlaces. ✨")
            # Store the user's ID in the list
            user_id = message.from_user.id
            if user_id not in user_ids:
                user_ids.append(user_id)
        else:
            bot.send_message(chat_id, "No eres miembro del canal , Unete a https://t.me/FreeedownChan para usar este bor.")
    except Exception as e:
        bot.send_message(chat_id, "Ocurrió un error al verificar la suscripción al canal. Por favor inténtalo de nuevo más tarde.")
        print("Exception:", e)


@bot.message_handler(commands=['count'])
def show_count(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, f"Hay un total de: {len(user_ids)} Usuarios activos  👥 ")		
		
		
		
		
# Modifica la tupla para almacenar el nombre de usuario del administrador
admin_username = ('Nanatsu2370',)

# Luego, en la función send_broadcast, puedes verificar el nombre de usuario del remitente

@bot.message_handler(commands=['broadcast'])
def send_broadcast(message):
    sender_username = message.from_user.username  # Obtén el nombre de usuario del remitente

    # Verifica si el remitente es el administrador
    if sender_username in admin_username:
        broadcast_text = message.text.replace('/broadcast', '').strip()  # Extrae el mensaje del comando y elimina espacios en blanco al inicio y final
        if broadcast_text:  # Verifica si el mensaje no está vacío
            for user_id in user_ids:
                bot.send_message(user_id, broadcast_text)
        else:
            bot.send_message(sender_username, "Por favor proporciona un mensaje para transmitir a los usuarios.")
    else:
        bot.send_message(sender_username, "Solo el administrador puede utilizar el comando de transmisión.")


	
@bot.message_handler(func=lambda message: True)
def generate_qr(message):
    text = message.text
    chat_id = message.chat.id
    if text.startswith('http://') or text.startswith('https://'):
        print("Link detectado, creando QRCode...")
        
        processing_msg = bot.send_message(chat_id, "Generando código QR...")

        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(text)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")

        img_path = 'qr_code.png'
        img.save(img_path)

        bot.send_photo(chat_id, open(img_path, 'rb'))
        
        # Edita el mensaje existente para indicar que se ha generado el código QR
        bot.edit_message_text("Código QR generado.", chat_id, processing_msg.message_id)
    else:
        bot.send_message(chat_id, "Por favor envía un enlace válido para generar el código QR.")





bot.polling()
