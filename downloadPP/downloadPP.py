from pathlib  import Path
from sys      import stdout
from Utils  import timer
from gethtml  import *
from constant import *

# Download url text and save it to filename in directory
def download_file(url:str, directory:Path, filename:str) -> None:
    stdout.write(filename)
    newFile = directory / filename

    # download file
    if newFile.exists():stdout.write(f'{filename} already exists\n')
    else:
        with open(newFile, 'w') as f:f.write(get_file(url))
        stdout.write(f'{filename} successfully created\n')
    stdout.flush()

# Download PP files of element
def download_element(PP:str, element:str, directory:Path) -> None:
    # get links
    files = get_file_links(f'{QEPath}/{TablePath}/{PP}/{element.lower()}')
    stdout.write(f'{element} Downloading.. (count : {len(files)})\n')

    # download PP file of element
    for file in files:
        file = file.strip('"')
        url = f'{QEPath}/{file}'
        filename = file.split('/')[-1]

        download_file(url, directory, filename)
    else:stdout.write('Result : Success')
    stdout.write('\n\n\n\n\n')

@timer
def download_PPTable(directory:Path, PP:str, element_skip=[]) -> None:
    # get existing element names
    elements = get_all_elements(f"{QEPath}/{TablePath}/{PP}")
    stdout.write(f'all elements count in {PP} : {len(elements)}\n\n')

    # download PPTable    
    for element in elements:
        if element in element_skip:continue
        Dir = directory / element
        Dir.mkdir(exist_ok=True)
        download_element(PP, element, Dir)

@timer
def main(directory:Path, tartget_PP=[], element_skip=[]):
    stdout.write("Download Start\n")
    for PP in PP_Table:
        if PP not in tartget_PP:continue
        stdout.write(f'{PP} Pseudo Potential Downloading..\n')
        PPDir = directory / PP
        PPDir.mkdir(parents=True,exist_ok=True)
        download_PPTable(PPDir, PP, element_skip)

    print('All Download Completed')

if __name__ == '__main__':
    directory = Path(__file__).parent / 'Test'
    directory.mkdir(exist_ok=True)

    import json
    with open("elements.json", "r") as file:
        data = json.load(file)
    PeriodicTable:list = data['PeriodicTable']

    t = open(directory / 'log.txt','w')
    stdout = t
    main(directory, tartget_PP=PP_Table[0])#, element_skip=PeriodicTable[:PeriodicTable.index('Cd')])
