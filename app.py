from flask import Flask, render_template, request, jsonify
from nltk.chat import Chat
from nltk.chat.util import reflections

app = Flask(__name__)

pairs = []

chatbot = Chat(pairs, reflections)

catering_types = {
    'bodas': {
        'description': 'Servicio de catering especializado para bodas',
        'details': (
            'Nuestro servicio de catering para bodas está diseñado para hacer de tu día especial algo inolvidable. '
            'Incluye una amplia variedad de platos gourmet, desde exquisitos aperitivos hasta postres de alta calidad. '
            'Trabajamos contigo para personalizar el menú según tus preferencias y requisitos. '
            'Además, nuestro personal altamente capacitado garantizará un servicio impecable durante todo el evento.'
        ),
    },
    'corporativo': {
        'description': 'Catering corporativo para eventos empresariales',
        'details': (
            'Ofrecemos catering corporativo diseñado para satisfacer las necesidades específicas de tu empresa. '
            'Desde desayunos y almuerzos de negocios hasta cenas de gala, nuestros menús profesionales son adaptables '
            'a cualquier tipo de evento empresarial. Nuestro objetivo es proporcionar opciones deliciosas y presentación impecable, '
            'creando una experiencia gastronómica que refleje la calidad de tu empresa.'
        ),
    },
    'cumpleaños': {
        'description': 'Catering para fiestas de cumpleaños',
        'details': (
            'Celebra tu cumpleaños con nosotros y deja que nos ocupemos de la comida para que tú disfrutes del día. '
            'Desde aperitivos deliciosos y platos principales festivos hasta increíbles postres, nuestros menús de catering para cumpleaños '
            'son diseñados para complacer todos los gustos. Personalizamos cada detalle para que tu celebración sea única y memorable.'
        ),
    },
    'vegetariano': {
        'description': 'Opciones vegetarianas disponibles en todos los menús',
        'details': (
            'Nos enorgullece ofrecer opciones vegetarianas en todos nuestros menús. Nuestras creaciones vegetarianas son más que una alternativa, '
            'son platos deliciosos y bien equilibrados que satisfacen tus gustos y preferencias. Ya sea en un evento corporativo o una boda, '
            'nuestras opciones vegetarianas son una elección deliciosa para todos.'
        ),
    },
    'celiacos': {
        'description': 'Menús especiales para personas con enfermedad celíaca',
        'details': (
            'Diseñamos menús especiales para personas con enfermedad celíaca, garantizando opciones sin gluten y deliciosas para que todos puedan disfrutar de la comida sin preocupaciones. '
            'Desde aperitivos hasta postres, cuidamos cada detalle para ofrecer una experiencia gastronómica segura y deliciosa. Tu salud y satisfacción son nuestra prioridad.'
        ),
    },
    'cocktail': {
        'description': 'Catering de cócteles para eventos sociales',
        'details': (
            'Impresiona a tus invitados con nuestro servicio de catering de cócteles. Ofrecemos una variedad de bocadillos y bebidas exquisitas para hacer de tu evento social una experiencia única. '
            'Desde elegantes canapés hasta estaciones de cócteles personalizadas, nuestro servicio de catering de cócteles agrega un toque sofisticado a cualquier celebración.'
        ),
    },
}

chat_started = False

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send_message', methods=['POST'])
def send_message():
    global chat_started

    user_message = request.form['message']

    if not chat_started:
        response = [
            '¡Hola! Bienvenido/a. Estoy aquí para ayudarte.',
            'Puedo proporcionarte información sobre tipos de catering, ubicación, horarios y métodos de pago. ¿En qué tema te gustaría obtener más detalles?'
        ]
        chat_started = True
    else:
        if user_message.lower() == 'catering':
            response = [
                'Puedo proporcionarte información sobre:',
                '- Tipos de catering',
                '- Ubicación',
                '- Horarios',
                '- Métodos de pago',
            ]
            response.extend([f'  - {catering_types[type_]["description"]} ({type_})' for type_ in catering_types])
            response.append('¿En qué tema te gustaría obtener más detalles? Por favor, indica el nombre.')
        elif user_message.lower() in ['tipos de catering', 'ubicacion', 'horarios', 'metodos de pago']:
            topic = user_message.lower()
            if topic == 'tipos de catering':
                response = ['Puedo proporcionarte información sobre los siguientes tipos de catering:']
                response.extend([f'- {catering_types[type_]["description"]} ({type_})' for type_ in catering_types])
            elif topic == 'ubicacion':
                response = ['Estamos ubicados en el centro de la ciudad,',
                            '18 de julio 123, Montevideo']
            elif topic == 'horarios':
                response = ['Nuestros horarios de atención son:',
                            'Lunes a Viernes: 9:00 am - 8:00 pm',
                            'Sábados y Domingos: 10:00 am - 6:00 pm']
            elif topic == 'metodos de pago':
                response = ['Aceptamos los siguientes métodos de pago:',
                            '- Tarjeta de crédito (Visa, MasterCard, Cabal)',
                            '- Transferencia bancaria',
                            '- Efectivo']
            response.append('¿En qué más puedo ayudarte?')
        else:
            response = chatbot.respond(user_message)
            response.append('¿En qué más puedo ayudarte?')

    return jsonify({'message': response})

@app.route('/reset_chat', methods=['POST'])
def reset_chat():
    global chat_started
    chat_started = False

    return jsonify({'status': 'success'})

if __name__ == '__main__':
    app.run(debug=True)
