import os
curPath = '.'+os.path.dirname(__file__)[len(os.path.abspath('.')):] + '/'
result = []
a=0
for file in os.listdir(curPath):
    if file.endswith('.out'):
        with open(f'{curPath}/{file}', 'r') as f:
            data = f.readlines()
            celldm=a=0
            for i,line in enumerate(data):
                if 'celldm(1)' in line:
                    celldm = float(line.split('=')[1].split()[0])
                elif 'a(1) = (' in line:
                    a = float(line.split()[3])
        result.append([file[-7:-4], celldm*a])
        a+=1
with open(f'{curPath}/result.txt', 'w') as f:
    for i in range(len(result)):
        f.write(result[i][0]+'\t\t'+str(result[i][1])+'\n')