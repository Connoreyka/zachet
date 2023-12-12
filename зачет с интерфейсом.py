import astropy.io.fits as pyfits
import matplotlib.pyplot as plt
import numpy as np
from tkinter import * # импортируем всё, что есть в этом модуле
from tkinter import ttk
from matplotlib import cm
from matplotlib.ticker import LinearLocator

def E_f(x, y, r, R1, R2, exp, scidata):
    E_fon = 0
    pix = 0
    for i in range(x - R1, x + R1 + 1):
        for j in range(y - R1, y + R1 + 1):
            if ((i - x) ** 2 + (j - y) ** 2 <= R1 ** 2) and ((i - x) ** 2 + (j - y) ** 2 > R2):
                E_fon += scidata[j - 1][i - 1]
                pix += 1
    E_fon /= pix
    E_fon /= exp
    return(E_fon)

def E_s():
    f = ent0.get()
    x = int(ent1.get())
    y = int(ent2.get())
    r = int(ent3.get())
    R1 = int(ent4.get())
    R2 = int(ent5.get())
    hdulist = pyfits.open(f)
    exp = hdulist[0].header['exptime']
    scidata = hdulist[0].data
    scidata = np.array(scidata)

    E_star = 0
    pix = 0
    for i in range(x - r, x + r + 1):
        for j in range(y - r, y + r + 1):
            if ((i - x) ** 2 + (j - y) ** 2 <= r ** 2):
                E_star += scidata[j - 1][i - 1]
                pix += 1
    E_star /= exp
    E_star -= E_f(x, y, r, R1, R2, exp, scidata)*pix
    lbl7['text'] = E_star

def graf():
    if g.get() == 1:
        x = int(ent1.get())
        y = int(ent2.get())
        r = int(ent3.get())
        f = ent0.get()
        hdulist = pyfits.open(f)
        scidata = hdulist[0].data
        scidata = np.array(scidata)
        hdulist.close()

        Value_x = []
        Ox = []
        for i in range(x - r, x + r + 1):
            Value_x.append(scidata[y - 1][i - 1])  # -1 потому что массив с 0, а изображение с 1
            Ox.append(i)
        plt.plot(Ox, Value_x)
        plt.xlabel('x')
        plt.ylabel('Value')
        plt.title(f'Value(x) при y={y}')
        plt.show()
    elif g.get() == 2:
        f = ent0.get()
        x = int(ent1.get())
        y = int(ent2.get())
        r = int(ent3.get())
        hdulist = pyfits.open(f)
        scidata = hdulist[0].data
        scidata = np.array(scidata)

        Value_y = []
        Oy = []
        for i in range(y - r, y + r + 1):
            Value_y.append(scidata[i - 1][x - 1])
            Oy.append(i)
        plt.plot(Oy, Value_y)
        plt.xlabel('y')
        plt.ylabel('Value')
        plt.title(f'Value(y) при x={x}')
        plt.show()
    elif g.get() == 3:
        f = ent0.get()
        x = int(ent1.get())
        y = int(ent2.get())
        r = int(ent3.get())
        hdulist = pyfits.open(f)
        scidata = hdulist[0].data
        scidata = np.array(scidata)

        Ox = []
        Oy = []
        for i in range(x - r, x + r + 1):
            Ox.append(i)
        for i in range(y - r, y + r + 1):
            Oy.append(i)
        Value_3d = np.zeros((len(Ox), len(Oy)))
        Vmax = 0
        Vmin = 999
        for i in range(len(Ox)):
            for j in range(len(Oy)):
                Value_3d[j][i] = scidata[Oy[j] - 1][Ox[i] - 1]
                if Value_3d[j][i] < Vmin:
                    Vmin = Value_3d[j][i]
                elif Value_3d[j][i] > Vmax:
                    Vmax = Value_3d[j][i]
        fig = plt.figure()
        ax = fig.add_subplot(projection='3d')
        Ox, Oy = np.meshgrid(Ox, Oy)
        surf = ax.plot_surface(Ox, Oy, Value_3d, cmap=cm.gist_earth)
        ax.set_zlim(Vmin, Vmax)
        ax.zaxis.set_major_locator(LinearLocator(5))
        fig.colorbar(surf, shrink=0.5, aspect=3)
        plt.xlabel('x')
        plt.ylabel('y')
        plt.title(f'Value_3d')
        plt.show()


root = Tk()
root.title("Новое окно")
root.geometry("400x400")
for c in range(2):
    root.columnconfigure(index=c)
for r in range(13):
    root.rowconfigure(index=r)

lbl0 = ttk.Label(text='Введите путь к файлу')
lbl0.grid(row=0, column=0)

ent0 = ttk.Entry()
ent0.grid(row=0, column=1)

lbl1 = ttk.Label(text='Введите данные звезды')
lbl1.grid(row=1, column=0)

lbl2 = ttk.Label(text='Введите x координату центра звезды')
lbl2.grid(row=2, column=0)

ent1 = ttk.Entry()
ent1.grid(row=2, column=1)

lbl3 = ttk.Label(text='Введите y координату центра звезды')
lbl3.grid(row=3, column=0)

ent2 = ttk.Entry()
ent2.grid(row=3, column=1)

lbl4 = ttk.Label(text='Введите радиус звезды в пикселях')
lbl4.grid(row=4, column=0)

ent3 = ttk.Entry()
ent3.grid(row=4, column=1)

lbl5 = ttk.Label(text='Введите внешний радиус фона')
lbl5.grid(row=5, column=0)

ent4 = ttk.Entry()
ent4.grid(row=5, column=1)

lbl6 = ttk.Label(text='Введите внутренний радиус фона')
lbl6.grid(row=6, column=0)

ent5 = ttk.Entry()
ent5.grid(row=6, column=1)

lbl7 = ttk.Label(text='0')
lbl7.grid(row=7, column=1)

btn1 = ttk.Button(text='Энергия звезды', command=E_s)
btn1.grid(row=7, column=0)

lbl8 = ttk.Label(text='Выберите интересующий график')
lbl8.grid(row=8, column=0)

g = IntVar(value=0)
rbtn1 = ttk.Radiobutton(text='Профиль по y', variable=g, value=1)
rbtn1.grid(row=9, column=1)

rbtn2 = ttk.Radiobutton(text='Профиль по x', variable=g, value=2)
rbtn2.grid(row=10, column=1)

rbtn3 = ttk.Radiobutton(text='3D график', variable=g, value=3)
rbtn3.grid(row=11, column=1)

btn2 = ttk.Button(text='Построить график', command=graf)
btn2.grid(row=12, column=1)

root.mainloop()