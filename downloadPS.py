from urllib.request import urlopen
from re import compile, findall
from pathlib import Path

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


def get_html(url):
    response = urlopen(url)
    return response.read()

def get_all_atoms(url):
    html = get_html(url)
    atoms = []
    lines = html.split(b'\n')
    for line in lines:
        if atoms_condition in line:
            atoms.append(findall(atoms_pattern, str(line))[0])
    return atoms

def get_file_links(url):
    html = get_html(url)
    lines = html.split(b'\n')
    links = []
    for line in lines:
        if filelink_condition in line:
            links.append(findall(filelink_pattern, str(line))[0])
    return links

def get_file(url):
    html = get_html(url)
    return str(html, 'utf-8')

if __name__ == '__main__':
    curdir = Path(__file__).parent

    for PP in PP_Table:
        url = f"{QEPath}/{TablePath}/{PP}"
        PPDir = curdir / PP
        PPDir.mkdir(exist_ok=True)
        
        atoms = get_all_atoms(url)
        t = open(curdir/f'{PP}_log.txt','w')
        for atom in atoms:
            directory = PPDir / atom
            directory.mkdir(exist_ok=True)
            t.write(atom+'\n')

            url = f'{QEPath}/{TablePath}/{PP}/{atom.lower()}'
            files = get_file_links(url)

            for file in files:
                file = file.strip('"')
                url = f'{QEPath}/{file}'
                filename = file.split('/')[-1]

                newFile = directory / filename
                t.write(filename+'\n')
                t.flush()
                if not newFile.exists():
                    with open(newFile, 'w') as f:
                        f.write(get_file(url))
            t.write('\n\n\n\n\n')
