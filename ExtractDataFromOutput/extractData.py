import os
class getData:
    def __init__(self, path) -> None:
        self.path = path
        self.result = []
    def scf(self, *prefixs):
        self.result.clear()
        for file in os.listdir(self.path):
            if not file.endswith('.out'):continue
            # if not startswith prefix, continue
            for prefix in prefixs:
                if file.startswith(prefix):
                    break
            else:continue
            # get total energy
            with open(f'{self.path}/{file}', 'r') as f:
                data = f.readlines()

            energy = 0
            for i,line in enumerate(data):
                if '!    total energy' in line:
                    energy = float(line.split('=')[1].split()[0])
            # indexing by last 3 strings of file name
            self.result.append([file[-7:-4], energy])
        with open(f'{self.path}/result.txt', 'w') as f:
            for i in range(len(self.result)):
                f.write(self.result[i][0]+'\t\t'+str(self.result[i][1])+'\n')

    def vcrelax(self,*prefixs):
        self.result.clear()
        for file in os.listdir(self.path):
            # if not endswith suffix, continue
            if not file.endswith('.out'):continue
            # if not startswith prefix, continue
            for prefix in prefixs:
                if file.startswith(prefix):
                    break
            else:continue
            # get new alat
            with open(f'{self.path}/{file}', 'r') as f:
                data = f.readlines()

            celldm=a=0
            for i,line in enumerate(data):
                if 'celldm(1)' in line:
                    celldm = float(line.split('=')[1].split()[0])
                elif 'a(1) = (' in line:
                    a = float(line.split()[3])
                elif 'convergence NOT achieved' in line:
                    print(f'{file[-7:-4]} not converged. pass data')
                    break
            else:
                # indexing by last 3 strings of file name
                self.result.append([file[-7:-4], celldm*a])
                a+=1
        with open(f'{self.path}/result.txt', 'w') as f:
            for i in range(len(self.result)):
                f.write(self.result[i][0]+'\t\t'+str(self.result[i][1])+'\n')
    
    def readFile(self, resultFilePath):
        if resultFilePath.endswith('/'):resultFilePath += 'result.txt'
        self.result.clear()
        with open(resultFilePath, 'r') as f:
            data = f.readlines()
        for i,line in enumerate(data):
            self.result.append(line.split())
    
    def draw(self, ylabel=''):
        from operator import itemgetter
        import matplotlib.pyplot as plt
        fig, ax1 = plt.subplots()
        plt.ylabel(ylabel)
        x_values = []
        y_values = []
        for x,y in self.result:
            x_values.append(float(x))
            y_values.append(float(y))
        # min or max view
        sorted_result = sorted(self.result, key=itemgetter(1))
        min_value = sorted_result[-1]
        max_value = sorted_result[0]

        ax1.plot(x_values, y_values, marker='o', color='k')
        for value in min_value,max_value:
            x,y = map(float, value)
            ax1.axvline(x, 0, 1, color='gray', linestyle='--', linewidth=2)
            ax1.axhline(y, 0, 1, color='gray', linestyle='--', linewidth=2)
        ax2 = ax1.twinx()
        ax2.set_yticks([float(min_value[1]),float(max_value[1])])
        ax2.set_ylim(*ax1.get_ylim())
        ax3 = ax1.twiny()
        ax3.set_xticks([float(min_value[0]),float(max_value[0])])
        ax3.set_xlim(*ax1.get_xlim())

        plt.tight_layout()
        plt.show()

if __name__ == '__main__':
    curPath = '.'+os.path.dirname(__file__)[len(os.path.abspath('.')):] + '/'
    scfPath = f'{curPath}/scfONCV/'
    vcrelaxPath = f'{curPath}/vcRelaxONCV/'
    import matplotlib.pyplot as plt
    plt.ion()

    tmp = getData('')
    getData(scfPath).scf('scf')
    tmp.readFile(scfPath)
    tmp.draw(ylabel='E(Ry)')

    tmp = getData(vcrelaxPath)
    tmp.vcrelax('relax')
    tmp.readFile(vcrelaxPath)
    tmp.draw(ylabel='alat(Bohr)')

    plt.pause(100)