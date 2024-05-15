import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

#Plot

path1 = "./data.txt"
path2 = "./settings.txt"
file = "./8-1-plot.svg"
xs = []
ys = []

with open(path2, "r") as settings_file:
    settings_data = [float(num) for num in settings_file.read().split("\n")]

time_step = settings_data[0]
volt_step = settings_data[1]

counter = 0
with open(path1, "r") as f:
    for line in f.readlines():
        y = float(line)
        ys.append(y*volt_step)
        xs.append(float(counter*time_step))
        counter = counter + 1

xs = np.array(xs)
ys = np.array(ys)

_, ax = plt.subplots(figsize=(10, 10))
ax.set_xlabel("Время, с", fontweight="bold")
ax.set_ylabel("Напряжение, В", fontweight="bold")
ax.set_title("Процесс заряда и разряда конденсатора в RC-цепочке", fontweight="bold")

my_plot = plt.plot(xs, ys, color='m', label="U(t)",marker = 'o',markevery=10)

ax.xaxis.set_major_locator(ticker.MaxNLocator(10))
ax.xaxis.set_minor_locator(ticker.MaxNLocator(10))
ax.yaxis.set_major_locator(ticker.MaxNLocator(10))
ax.yaxis.set_minor_locator(ticker.MaxNLocator(10))

plt.grid(color="blue", visible=True, which='major',axis='both',alpha=1, linestyle = ":")
plt.grid(color="blue", visible=True, which='minor',axis='both',alpha=1, linestyle = ":")

plt.legend()
plt.show()
plt.savefig(file)