import numpy as np
import matplotlib.pyplot as plt

def reorder_ndarray(data, new_order):
    # 데이터를 numpy 배열로 변환
    data_array = np.array(data)

    # 주어진 순서에 따라 데이터를 재배열
    reordered_data = [data_array[data_array[:, 0] == x] for x in new_order]

    # 2차원 배열로 변환하여 반환
    result = np.concatenate(reordered_data)[:, 1].tolist()
    
    return result

def filter_by_x_range(data, x_min, x_max):
    # 데이터를 numpy 배열로 변환
    data_array = np.array(data)

    # x값이 특정 범위 내에 있는 행을 선택
    filtered_data = data_array[(data_array[:, 0] >= x_min) & (data_array[:, 0] <= x_max)]

    return filtered_data[:,0].tolist(), filtered_data[:,1].tolist()

    
class DrawBandStructure:
    def __init__(self, DataFile, nk) -> None:
        self.nk = nk                # Data Per Line
        self.fermi = 0              # 
        self.DataSet = np.loadtxt(DataFile)
        self.BandLine = len(self.DataSet) // self.nk
        self.bDrawKPoints = False

        self.x_min = np.min(self.DataSet[:, 0])
        self.x_max = np.max(self.DataSet[:, 0])
        self.drawcolor = 'k'
        self.drawstyle = '-'
        self.linecolor = 'r'
        self.linestyle = ':'

        # Make Plot (Draw Image)
        plt.rcParams['xtick.bottom'] = False    # 아랫 눈금 없음
        plt.rcParams['ytick.right'] = True      # 오른쪽 눈금 있음.
        plt.rcParams['ytick.direction'] = 'in'  # 좌우 눈금은 그래프 안으로
        plt.rcParams['font.family'] = 'Times New Roman'
        plt.rcParams['font.size'] = 15          # 폰트 크기
        plt.rcParams['lines.linewidth'] = 2     # 라인 굵기

    def setDrawSize(self, width=6, height=9):
        plt.figure(figsize=(width,height))             # (Width, Height) Size

    def read_kpoints(self, filename="", norm=1):
        self.bDrawKPoints = True
        self.DataText = ""
        realVector = np.empty((3,3), dtype=np.float32)
        with open(filename, "r") as f:
            f.readline()
            # RealSpace Vectors
            for i in range(3):
                realVector[i] = np.array(f.readline().split(), dtype=np.float32)
            [f.readline() for x in range(2)]
            lineCount = int(f.readline())
            k_b = np.empty((lineCount, 3), dtype=np.float32)
            # KPoint in Reciprocal Lattice Vector Cordinate
            for i in range(lineCount):
                tmp = f.readline().split()
                k_b[i] = np.array(tmp[:-1])
                self.DataText += tmp[-1]

        # Reciprocal Lattice Vector
        bVectors = np.empty((3,3))
        Volume = np.inner(np.cross(realVector[0],realVector[1]),realVector[2])
        p = 2*np.pi
        for i in range(3):
            bVectors[i] = p*np.cross(realVector[i-2], realVector[i-1]) / Volume

        bVectors = bVectors/np.linalg.norm(bVectors[0, :norm])
        # KPoint in Cartesian Cordinate
        self.k_a = np.inner(k_b, np.transpose(bVectors))

        self.BaseOrder = self.DataText  # 기본 데이터 Set
        self.BaseKpoints = [0]          # 기본 KPoint Set
        for idx in range(len(self.k_a)-1):
            norm = self.k_a[idx+1] - self.k_a[idx]
            self.BaseKpoints.append(np.linalg.norm(norm) + self.BaseKpoints[-1])
        self.CustomKPoints = self.BaseKpoints.copy()

    def set_fermi(self, fermi):
        self.fermi = fermi

    def set_plotInfo(self, y_label = 'E (eV)', y_min=0, y_max=0):
        self.y_min = y_min
        self.y_max = y_max
        self.y_label = y_label

        plt.ylim([self.y_min, self.y_max])
        plt.ylabel(y_label)
        
    def setBandOrder(self, DataText = ""):
        # BaseOrder를 기반으로 DataText에 따른 데이터로 재구성
        # BaseKPoints를 DataText 기반으로 재구성
        self.KIdx = []
        self.CustomKPoints = [0]
        for i in range(len(DataText) - 1):
            tmp1 = self.BaseOrder.find(DataText[i] + DataText[i+1])
            tmp2 = 1
            if tmp1 == -1:
                tmp1 = self.BaseOrder.find(DataText[i+1] + DataText[i]) + 1
                tmp2 = -1
            if tmp1 == -1:
                raise ValueError("Invalid DataText : Only Allowed {}".format(self.BaseOrder))
            self.KIdx.append([tmp1, tmp2])
            self.CustomKPoints.append(abs(self.BaseKpoints[tmp1] - self.BaseKpoints[tmp1+tmp2]) + self.CustomKPoints[-1])
        self.DataText = DataText
        self.x_min = min(self.CustomKPoints)
        self.x_max = max(self.CustomKPoints)

    def SimplePlot(self):
        # Data Plot
        for i in range(self.BandLine):
            data = self.DataSet[i*nk:(i+1)*nk]
            x_val = data[:, 0]
            y_val = data[:, 1] - fermi
            plt.plot(x_val, y_val, label = "a"+str(i), color = self.drawcolor, linestyle = self.drawstyle)
        # 눈금 그리기
        plt.axhline(0, 0, 1, color=self.linecolor, linestyle=self.linestyle, linewidth=2) # 수평선
        plt.xlim([self.x_min, self.x_max])

    def CustomPlot(self):
        for i in range(self.BandLine):
            data = self.DataSet[i*nk:(i+1)*nk]
            x_val = []
            y_val = []
            for j in range(len(self.DataText)-1):
                tmp1 = self.KIdx[j][0]
                tmp2 = self.KIdx[j][1]
                if tmp2==1:
                    min_val = self.BaseKpoints[tmp1]
                    max_val = self.BaseKpoints[tmp1+tmp2]
                    x,y = filter_by_x_range(data, min_val, max_val)
                    x_val.extend(np.array(x) - min_val + self.CustomKPoints[j])
                    y_val.extend(y)
                else:
                    min_val = self.BaseKpoints[tmp1+tmp2]
                    max_val = self.BaseKpoints[tmp1]
                    x,y = filter_by_x_range(data, min_val, max_val)
                    x_val.extend(max_val - np.array(list(reversed(x))) + self.CustomKPoints[j])
                    y_val.extend(reversed(y))
            plt.plot(x_val, [y-self.fermi for y in y_val], label = "a"+str(i), color = self.drawcolor, linestyle = self.drawstyle)
        # 눈금 그리기
        plt.axhline(0, 0, 1, color=self.linecolor, linestyle=self.linestyle, linewidth=2) # 수평선
        plt.xlim([self.x_min, self.x_max])

    def KPointsPlot(self):
        for i in self.CustomKPoints[1:-1]:
            plt.axvline(i, 0, 1, color=self.linecolor, linestyle=self.linestyle, linewidth=2)
        tmp = []
        for txt in self.DataText:
            if txt=="G":
                tmp.append(r'$\Gamma$')
            else:
                tmp.append(txt)
        plt.xticks(self.CustomKPoints, labels=tmp)


    def plotBandStrcure(self):
        # Draw KPoints
        if self.bDrawKPoints:
            if self.BaseOrder == self.DataText:
                self.SimplePlot()
                self.KPointsPlot()
            # Custom KPoints
            else:
                self.CustomPlot()
                self.KPointsPlot()
        else:
            self.SimplePlot()
        plt.show()

if __name__=="__main__":
    import os
    nk=151
    folder_directory=os.path.dirname(__file__)
    DataFile = folder_directory + "/MoS2.bands.gnu"
    kpointFile = folder_directory + "/KPOINTS"
    fermi = -0.7338

    BandStructe = DrawBandStructure(DataFile,nk) # Set Data
    BandStructe.setDrawSize(6,6)                 # Set Draw Size
    BandStructe.read_kpoints(kpointFile)         # For Set KPoints
    BandStructe.set_fermi(fermi)                 # move y tick
    BandStructe.set_plotInfo("E(ev)",-4,4)       # plot range(y)
    BandStructe.setBandOrder("GKMG")             # move x tick
    BandStructe.plotBandStrcure()                # plot band structure
