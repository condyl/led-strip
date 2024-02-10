from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import rainbowio
import board
import neopixel
from time import sleep
from PIL import ImageColor
import random


# initialise functions @ devices
pixelnum = 256
pixels = neopixel.NeoPixel(board.D18,pixelnum, brightness = 0.8)

colours = {'red':(255,0,0),
           'blue': (0,0,255),
           'green': (0,255,0),
           'white': (255,255,255),
           'pink': (255,20,147),
           'yellow': (255,255,0),
           'purple': (75,0,130)}
currentcolour = (0,0,0)
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)
count = 0

@app.route('/')
def index():
    return render_template('index.html')

# change colour of leds to ______
@socketio.on('colour')
def change_colour(message):
    global currentcolour
    jsdata = message['data'] # data = data from javascript file
    print(f'current color: {jsdata}')
    currentcolour = (colours[jsdata]) # current colour = colour from colour list
    fill_leds() #run fill leds function
    print(currentcolour)
    emit('my response', {'data': jsdata})


# fill led function
@socketio.on('fill')
def fill_leds():
    global currentcolour
    pixels.fill((currentcolour)) #fill colours to current colour
    print('filled')

# rainbow function
@socketio.on('rainbow')
def rainbow(message):
    speed = 10
    delta_hue = 256
    i=0
    makerainbow = True
    while makerainbow:
        for l in range(len(pixels)):
            pixels[l] = rainbowio.colorwheel( int(i*speed + l * delta_hue) % 255  )
            if l == 255:
                makerainbow = False
    pixels.show()  # only write to LEDs after updating them all
    i = (i+1) % 255
    sleep(0.05)


@socketio.on('connect')
def test_connect():
    emit('my response', {'data': 'Connected'})

@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected')

# slider/brightness function
@socketio.on('slider')
def slider(message):
    global pixelnum
    print(message['data'])
    stepdata = int(message['data'])/10 # take slider input, convert to number from 0-1
    print(stepdata)
    pixels.brightness = stepdata #change brightness
    pixels.show() #update lights


# colour picker
@socketio.on('choose')
def colour_chooser(message):
    global currentcolour
    inputcolour = ImageColor.getrgb(message['data']) # lights colour = HEX colour value converted to RGB
    currentcolour = inputcolour
    fill_leds() #update leds
    sleep(0.5)

# off function
@socketio.on('off')
def off():
    pixels.fill((0,0,0)) #change led colour to black

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0')
