from flask import Flask, request, render_template
from flask_socketio import SocketIO
import time
from datetime import datetime, timedelta

app = Flask(__name__)
socketio = SocketIO(app)

last_bite_time = datetime.now()

@app.route('/')
def index():
    return render_template('index.html')

def get_display_time(message):
    """Determines how long a message should be displayed based on its length."""
    length = len(message)
    if length <= 4:
        return 2
    elif length <= 7:
        return 3  
    elif length <= 15:
        return 5  
    else:
        return 


def background_task():
    counter = 1
    while True:
        now = datetime.now()
        if now - last_bite_time > timedelta(seconds=60):
            message = "Waiting for new bites..."
            socketio.emit('display_text', {'text': message})
        else:
            pass
        print(f"Sending counter: {counter}")
        socketio.emit('display_word', {'word': str(counter)})
        counter += 1
        time.sleep(1.0) 

@app.route('/send-word', methods=['POST'])
def receive_word():
    """Entry point and broadcasts words to all connected WebSocket clients"""
    word = request.json['word']
    bite_time = get_display_time(word)
    socketio.emit('display_word', {'word': word, 'time': bite_time})
    return {'message': 'Word received successfully'}

# @socketio.on('send_word')
# def handle_send_word(json, methods=['GET', 'POST']):
#     print('received word: ' + str(json))
#     socketio.emit('display_word', json)

if __name__ == '__main__':
    # socketio.start_background_task(background_task)
    socketio.run(app, debug=True)
