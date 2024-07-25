from xmlrpc.client import Boolean
import RPi.GPIO as GPIO
from time import sleep
import lcd1602gpio



'''
pin = 24
iterations = 10
interval = .25

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(pin, GPIO.OUT)

for x in range(1, iterations+1):
    print(f"Loop {x}: LED on")
    GPIO.output(pin, GPIO.HIGH)
    sleep(interval)
    
    print(f"Loop {x}: LED off")
    GPIO.output(pin, GPIO.LOW)
    sleep(interval)
    

'''
def back_light(button: Boolean):
    GPIO.setmode(GPIO.BCM)
    
    GPIO.setup(12, GPIO.OUT, initial=GPIO.HIGH)
    if button:
        GPIO.output(12, GPIO.HIGH)
    else:
        GPIO.output(12, GPIO.OUT)

def display_lcd(
    word: str = '--------------------------------',
    row: int = 0 | 1,
    time: int = 2
):
    '''
    Exibir mensagens em um display de 16 segmentos com 2 linhas
    Para quebrar linha use o caracter '@'
    Se mais de 32 caracteres forem repassados, a partir do 33º não será exibido
    
    Args:
        word:(string com tamanho maximo de 16 caracteres) Recebe uma string que será exibida no display
        row: (0 | 1) indica a linha em que a mensagem será exibida
    
    Exemplo: display_lcd(word="Marlon @Duarte") --> Marlon
                                                    Duarte
                                                    
    '''
    
    back_light(True)
    
    try:
        find_arroba = word.find('@')
    except:
        find_arroba = -1
    
    if (find_arroba != -1):
        # Disable GPIO warnings
        GPIO.setwarnings(False)
        # Set GPIO pin mode. RPi pins described in this example use BCM.
        GPIO.setmode(GPIO.BCM)

        # create an instance of LCD1602GPIO_4BIT for 4-bit mode.
        # the LCD module must be already powered on here.
        # the instance initializes the LCD module immediately during init.
        lcd = lcd1602gpio.LCD1602GPIO_4BIT(
                rs=8,
                e=7,
                db7=25,
                db6=24,
                db5=23,
                db4=18)
        # write texts to Line 0 of the LCD.
        lcd.write_line(word[:word.index('@')], 0)
        # write texts to Line 1 of the LCD.
        lcd.write_line(word[word.index('@')+1:], 1)
        sleep(time)
        # Do GPIO cleanup manually before exiting.
        lcd.clear_lcd()
        back_light(button=False)
        GPIO.cleanup()
    elif(len(word) > 16):
        # Disable GPIO warnings
        GPIO.setwarnings(False)
        # Set GPIO pin mode. RPi pins described in this example use BCM.
        GPIO.setmode(GPIO.BCM)

        # create an instance of LCD1602GPIO_4BIT for 4-bit mode.
        # the LCD module must be already powered on here.
        # the instance initializes the LCD module immediately during init.
        lcd = lcd1602gpio.LCD1602GPIO_4BIT(
                rs=8,
                e=7,
                db7=25,
                db6=24,
                db5=23,
                db4=18)

        # write texts to Line 0 of the LCD.
        lcd.write_line(word[:16], 0)
        # write texts to Line 1 of the LCD.
        lcd.write_line(word[16:], 1)
        sleep(time)
        # Do GPIO cleanup manually before exiting.
        back_light(button=False)
        lcd.clear_lcd()
        GPIO.cleanup()
    else:
        # Disable GPIO warnings
        GPIO.setwarnings(False)
        # Set GPIO pin mode. RPi pins described in this example use BCM.
        GPIO.setmode(GPIO.BCM)

        # create an instance of LCD1602GPIO_4BIT for 4-bit mode.
        # the LCD module must be already powered on here.
        # the instance initializes the LCD module immediately during init.
        lcd = lcd1602gpio.LCD1602GPIO_4BIT(
                rs=8,
                e=7,
                db7=25,
                db6=24,
                db5=23,
                db4=18)

        # write texts to Line 0 of the LCD.
        lcd.write_line(word, 0)
        sleep(time)
        # Do GPIO cleanup manually before exiting.
        back_light(button=False)
        lcd.clear_lcd()
        GPIO.cleanup()
    
display_lcd("SCA - UFC@Marlon Duarte")