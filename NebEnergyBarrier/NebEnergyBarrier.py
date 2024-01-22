import os
import matplotlib.pyplot as plt
from tkinter import Tk
from tkinter.filedialog import askopenfilenames

curPath = os.path.dirname(os.path.realpath(__file__))
colors = ['b','g','r','c','m','y','k','w']
class drawEBarrier:
    def __init__(self):
        Tk().withdraw() # 이 코드는 tkinter의 기본 창을 숨깁니다.
        self.colors = iter(colors)
        self.files = []
        self.drawEBarriers()

    def drawEBarriers(self):
        path = f'{curPath}"'
        file = [*askopenfilenames(initialdir=path)]
        while file!=[]:
            for filename in file:
                if filename not in self.files:
                    self.files.append(filename)
                    try:
                        color=next(self.colors)
                    except StopIteration:  
                        self.colors = iter(colors)
                        color=next(self.colors)
                    self.drawEBarrier(filename,color)
                path = os.path.dirname(filename)
            plt.show(block=False)
            file = [*askopenfilenames(initialdir=path)]
        while len(plt.get_fignums()) > 0:
            plt.show(block=False)
            plt.pause(0)

    def drawEBarrier(self, filename:str, color):
        with open(filename,'r') as f:
            data = f.readlines()
        x_val = []
        y_val = []
        for i in data:
            x,y,z=map(float,i.split())
            x_val.append(x)
            y_val.append(y)
        #plt.xlim(0,1)
        #plt.ylim(0,max(y_val))
        plt.plot(x_val, y_val, label = filename.split('/')[-1], color=color, marker='o', linestyle='-')
        plt.legend()
        # x좌표, y좌표, 표기값, ha : 좌우 정렬값, va : 상하 정렬값
        #for i in range(len(x_val)):plt.text(x_val[i], y_val[i], y_val[i]+5, ha='center', va='bottom')

if __name__ == "__main__":
    X = drawEBarrier()