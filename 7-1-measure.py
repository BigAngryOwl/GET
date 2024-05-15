import RPi.GPIO as gp
import time
import matplotlib.pyplot as plt

# Объявляем переменные и подготавливаем GPIO
gp.setmode(gp.BCM)
dac = [8, 11, 7, 1, 0, 5, 12, 6]
leds = [2, 3, 4, 17, 27, 22, 10, 9]
comp = 14
troyka = 13
bits = 8
levels = 2**bits
maxV = 3.3

gp.setup(dac, gp.OUT)
gp.setup(comp, gp.IN)
gp.setup(troyka, gp.OUT, initial=gp.LOW)

gp.output(troyka, 0)

# Необходимые функции 

def dec2bin(inpI): # Из десятичной в двоичную систему
    return [int(i) for i in bin(inpI)[2:].zfill(8)]

def num2dac(num): # Выводит число на dac
    signal = dec2bin(num)
    gp.output(dac, signal)
    return

def adc(): # преобразовывает аналоговый сигнал в цифровой
    level = 0
    for i in range(bits - 1, -1, -1):
        level += 2**i
        gp.output(dac, dec2bin(level))
        time.sleep(0.01)
        comp_val = gp.input(comp)
        if comp_val == 0:
            level -= 2**i
    return level

data_volts = []
data_times = []

try: 
    start_time = time.time()
    val = 0
    while val < 255:
        val = adc()
        print("Volts: {:3}".format(val / levels * maxV))
        num2dac(val)
        data_volts.append(val)
        data_times.append(time.time() - start_time)
    
    gp.output(troyka, 1)

    while val > 1:
        val = adc()
        print("Volts: {:3}".format(val / levels * maxV))
        num2dac(val)
        data_volts.append(val)
        data_times.append(time.time() - start_time)

    end_time = time.time()

    with open("/home/b01-303/Desktop/settings.txt", "w") as file:
        file.write(str((end_time - start_time) / len(data_volts)))
        file.write("\n")
        file.write(str(maxV / 256))

    print(end_time - start_time, "Secs\n", len(data_volts) / (end_time - start_time), "\n", maxV/256)

finally:
    gp.output(dac, gp.LOW)
    gp.output(troyka, gp.LOW)
    gp.cleanup()

data_times_str = [str(item) for item in data_times]
data_volts_str = [str(item) for item in data_volts]

with open("/home/b01-303/Desktop/data.txt", "w") as file:
    file.write("\n".join(data_volts_str))

plt.plot(data_times, data_volts)
plt.show()