import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(12, GPIO.IN,  pull_up_down=GPIO.PUD_DOWN)

try: 
	while True:
		if GPIO.input(12):
			print 'Botao= High'
		else:
			print 'Botao= LOW'
except KeyboardInterrupt:
	GPIO.cleanup()
