from urllib.request import urlopen
from re import compile, findall
from pathlib import Path
from functools import wraps

# Path
QEPath = 'https://pseudopotentials.quantum-espresso.org'
TablePath = 'legacy_tables'
PP_Table = ('ps-library','hartwigesen-goedecker-hutter-pp','fhi-pp-from-abinit-web-site','original-qe-pp-library')

# condition
atoms_condition = b'/%b/' % TablePath.encode()
filelink_condition = b'href="/upf'

# pattern
atoms_pattern = compile('[A-Z][a-z]*')
filelink_pattern = compile('["][/].+UPF["]')


def _get_html(url):
    response = urlopen(url)
    return response.read()

def _get_all_atoms(url):
    html = _get_html(url)
    atoms = []
    lines = html.split(b'\n')
    for line in lines:
        if atoms_condition in line:
            atoms.append(findall(atoms_pattern, str(line))[0])
    return atoms

def _get_file_links(url):
    html = _get_html(url)
    lines = html.split(b'\n')
    links = []
    for line in lines:
        if filelink_condition in line:
            links.append(findall(filelink_pattern, str(line))[0])
    return links

def _get_file(url):
    html = _get_html(url)
    return str(html, 'utf-8')

def timer(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        from time import time
        start_time = time()  # 시작 시간 측정
        result = func(*args, **kwargs)  # 원래 함수 실행
        end_time = time()  # 종료 시간 측정
        print(f"{func.__name__} 함수 실행 시간: {end_time - start_time}초")
        return result
    return wrapper

@timer
def main():
    curdir = Path(__file__).parent

    print("Download Start")
    for PP in PP_Table:
        print(f'{PP} Pseudo Potential Downloading..')

        url = f"{QEPath}/{TablePath}/{PP}"
        atoms = _get_all_atoms(url)
        PPDir = curdir / PP
        PPDir.mkdir(exist_ok=True)
        
        t = open(curdir/f'{PP}_log.txt','w')
        t.write(f'all atoms count in {PP} : {len(atoms)}')
        for atom in atoms:
            print(f'{atom} Downloading..')
            t.write(atom)

            directory = PPDir / atom
            directory.mkdir(exist_ok=True)
            url = f'{QEPath}/{TablePath}/{PP}/{atom.lower()}'
            files = _get_file_links(url)

            t.write(f'(count : {len(files)})\n')
            for file in files:
                file = file.strip('"')
                url = f'{QEPath}/{file}'
                filename = file.split('/')[-1]
                newFile = directory / filename

                t.write(filename)
                if newFile.exists():
                    t.write(f'{filename} already exists')
                else:
                    with open(newFile, 'w') as f:
                        f.write(_get_file(url))
                    t.write(f'{filename} successfully created')
                t.flush()
            t.write('\n\n\n\n\n')
    print('All Download Completed')

if __name__ == '__main__':
    main()
