from re import compile

# Path
QEPath = 'https://pseudopotentials.quantum-espresso.org'
TablePath = 'legacy_tables'
PP_Table = ('ps-library','hartwigesen-goedecker-hutter-pp','fhi-pp-from-abinit-web-site','original-qe-pp-library')

# condition
elements_condition = b'"/%b/' % TablePath.encode()
filelink_condition = b'href="/upf'

# pattern
elements_pattern = compile('[A-Z][a-z]*')
filelink_pattern = compile('["][/].+UPF["]')

