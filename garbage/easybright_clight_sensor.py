import serial
from time import sleep

ser = serial.Serial(port="/dev/ttyUSB0",
                    baudrate=19200,
                    parity=serial.PARITY_NONE,
                    stopbits=serial.STOPBITS_TWO,
                    bytesize=serial.EIGHTBITS,
                    timeout=0.500,
                    )

ser.flushInput()
ser.flushOutput()

ADDR_BASE = 0x23 # nebo 0x5c pokud je ADDR pin HIGH
ADDR_READ = ADDR_BASE << 1 | 1
ADDR_WRITE = ADDR_BASE << 1

CMD_WRITE_1B = 0x53
CMD_READ_MULT = 0x54

LUX_RESOLUTION_1X = 0x10
LUX_RESOLUTION_4X = 0x13

# nastavení senzoru
ser.write(bytearray([CMD_WRITE_1B, ADDR_WRITE, LUX_RESOLUTION_1X]))

with open("/etc/clightd/sensors.d/easybright", "w") as file:
	while True:
		# požádám převodník o 2 B
		ser.write(bytearray([CMD_READ_MULT, ADDR_READ, 0x02]))
		# přečtu je
		raw = ser.read(2)
		# interpretace bytů podle datasheetu
		lx = (raw[1] << 8 | raw[0]) / 1.2
		file.seek(0) # nastavím pozici v souboru vždy na začátek, abych přepsal původní hodnotu
		file.write(str(round(lx))) # zapíšu zaokrouhlenou aktuální hodnotu
		sleep(1)
