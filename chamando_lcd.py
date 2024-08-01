from teste_lcd import LCDTask

display = LCDTask()

display.stop_display()
display.start_display(word="Marlon")
print("Imprimindo outras coisas")
print("Marlon Duarte")
print("Ivo Duarte")
display.stop_display()
display.start_display(word="finalizando")
print("Imprimindo outras coisas")
print("Marlon Duarte")
print("Ivo Duarte")
display.stop_display()
