import numpy as np
import matplotlib.pyplot as plt
import PySimpleGUI as sg
import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

matplotlib.use('TkAgg')

def draw_figure(canvas, figure):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
    return figure_canvas_agg

# グラフの初期設定
a = 1
b = 0
x = np.linspace(0, 2 * np.pi, 1000)
fig, ax = plt.subplots(figsize=(3, 2))  # インチ単位で設定
line, = ax.plot(x, np.sin(a * x + b))
ax.set_xlim(0, 2 * np.pi)
ax.set_ylim(-1.5, 1.5)

# PySimpleGUIのレイアウト設定
layout = [[sg.Canvas(key='-CANVAS-', size=(300, 200))],
          [sg.Button('Exit')]]

window = sg.Window('Dynamic Matplotlib Graph in PySimpleGUI', layout, finalize=True, element_justification='center')

# FigureCanvasをPySimpleGUIウィンドウに描画
canvas_elem = window['-CANVAS-']
canvas = canvas_elem.TKCanvas
figure_canvas_agg = draw_figure(canvas, fig)

# グラフの動的更新
t = 0
while True:
    event, values = window.read(timeout=100)
    if event == 'Exit' or event == sg.WIN_CLOSED:
        break

    y = np.sin(a * x + b + t)
    line.set_ydata(y)
    figure_canvas_agg.draw()
    t += 0.1

window.close()
