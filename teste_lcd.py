# lcd_threaded.py

import threading
import RPi.GPIO as GPIO  # type: ignore
from time import sleep
import lcd1602gpio  # type: ignore

class LCDTask:
    def __init__(self):
        self._thread = None
        self._running = threading.Event()
        self._running.clear()
        self.word = ""
        self.row = 0
        self.time = 2

    def _setup_lcd(self):
        """Configura o LCD para uso."""
        # Disable GPIO warnings
        GPIO.setwarnings(False)
        # Set GPIO pin mode. RPi pins described in this example use BCM.
        GPIO.setmode(GPIO.BCM)
        # create an instance of LCD1602GPIO_4BIT for 4-bit mode.
        # the LCD module must be already powered on here.
        # the instance initializes the LCD module immediately during init.
        return lcd1602gpio.LCD1602GPIO_4BIT(
            rs=8,
            e=7,
            db7=25,
            db6=24,
            db5=23,
            db4=18
        )

    def _back_light(self, button: bool):
        """Controla a luz de fundo do LCD."""
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(12, GPIO.OUT, initial=GPIO.HIGH)
        GPIO.output(12, GPIO.HIGH if button else GPIO.OUT)

    def _display_task(self):
        """Executa a tarefa de exibição no LCD."""
        self._back_light(True)
        lcd = self._setup_lcd()

        try:
            find_arroba = self.word.find('@')
        except Exception:
            find_arroba = -1

        if find_arroba != -1:
            lcd.write_line(self.word[:find_arroba], 0)
            lcd.write_line(self.word[find_arroba + 1:], 1)
        elif len(self.word) > 16:
            lcd.write_line(self.word[:16], 0)
            lcd.write_line(self.word[16:], 1)
        else:
            lcd.write_line(self.word, self.row)

        sleep(self.time)
        lcd.clear_lcd()
        self._back_light(False)
        GPIO.cleanup()

    def start_display(self, word: str, row: int = 0, time: int = 2):
        """Inicia a tarefa de exibição no LCD em uma thread separada."""
        if self._thread is None or not self._thread.is_alive():
            self.word = word
            self.row = row
            self.time = time
            self._running.set()
            self._thread = threading.Thread(target=self._display_task)
            self._thread.start()

    def stop_display(self):
        """Para a tarefa de exibição no LCD."""
        if self._thread is not None and self._thread.is_alive():
            self._running.clear()
            self._thread.join()

# Exemplo de uso:
if __name__ == "__main__":
    lcd_task = LCDTask()
    lcd_task.start_display(word="Marlon @Duarte")
    sleep(5)  # Deixa a tarefa rodar por 5 segundos
    lcd_task.stop_display()
