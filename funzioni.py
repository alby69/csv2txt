#!/usr/bin/env python
# coding: utf-8

import os
import sys
import re
import csv

from ConfigParser import SafeConfigParser


def check_campo(prog_campo, val_campo, list_tracciato):
    for diz in list_tracciato:
        if diz['Progressivo'] == prog_campo:
            for v in val_campo:
              if diz['Valore'] == v:
                ris = True
              else:
                ris = False
            break


def create_diz(chiave, valore):
    diz = {}
    for c,v in zip(chiave,valore):
        diz[c]=v
    return diz


def cmp_diz(diz, diz_cmp):
    # confronta 2 diz e restituisce il primo oppure vuoto
    nr_key = len(diz_cmp.keys())
    nr_ok = 0
    ris = {}
    for k in diz_cmp.keys():
        if diz.has_key(k):
            if diz[k] == diz_cmp[k]:
                nr_ok += 1
        if nr_ok == nr_key:
            ris = diz
    return ris    


def extract_diz(list_diz, diz_filtro):
    ris = []
    for diz in list_diz:
        tmp_diz = cmp_diz(diz,diz_filtro)
        if tmp_diz <> {}:  
            ris.append(diz)
    return ris


def read_ini(file_ini, section_name=''):
    """ Legge un file ini e restiuisce un dizionario che ha per chiavi le sezioni del file
    file_ini:	nome del file ini
    section_name: nome della sezione da estrarre. Per default estrae tutte le sezioni
    """   
    diz_ini = {}

    parser = SafeConfigParser()
    parser.read(file_ini)
    sections_ini = parser.sections()

    if section_name <> '':
        if parser.has_section(section_name):
            for name in parser.options(section_name):
                diz_ini[name.upper()] = parser.get(section_name, name)
    else:
        for s in sections_ini:
            diz_ini[s] = read_ini(file_ini, s) # crea un diz con chiavi le sezioni

    return diz_ini


def csv_read(path, filename, sep='\t'):
    f_input = open(path + filename, 'rb')
    csvreader = csv.DictReader(f_input, delimiter=sep)
    nomi = csvreader.fieldnames
    #nomi.sort()		
    diz_curr = []
		
    for row in csvreader:
        diz_curr.append(row)
		
    nomi.sort()
    return nomi, diz_curr


def multikeysort(items, columns):
    from operator import itemgetter
    comparers = [ ((itemgetter(col[1:].strip()), -1) 
                    if col.startswith('-')
                    else (itemgetter(col.strip()), 1)) for col in columns]

    def comparer(left, right):
        for fn, mult in comparers:
            result = cmp(fn(left), fn(right))
            if result:
                return mult * result
        else:
            return 0
    return sorted(items, cmp=comparer)


def leggi_tracciato(list_tracciato, campo_progr, campo_tipo, campo_lunghezza, campo_valore):
    tracciato = {}
    for l in list_tracciato:
        formato = crea_formato(l[campo_tipo], l[campo_lunghezza], '0', '', 'r')
        tracciato[l[campo_progr] + ':' + formato] = l[campo_valore]

    return tracciato


def crea_formato(f_type, f_len, pad_num='0', pad_str='', f_align='r'):  
    """
    f_type: integer, float, string
    f_len: lunghezza totale campo es. decimale 10:2 lunghezza 10 di cui 2 decimali
    f_dec: numero cifre decimali
    f_align: r=right, l=left
    """

    if f_align == 'r': align = ''
    if f_align == 'l': align = '-'

    if f_type == 'integer':
        tmp = str(f_len)      
        option = 'd'
        pad = pad_num

    if f_type == 'float':
        intero, decimale = f_len.split(':')
        tmp = intero + '.' + decimale      
        option = 'f'
        pad = pad_num

    if f_type == 'string':
        tmp = str(f_len)
        option = 's'
        pad = pad_str
 
    ris = '%' + align + pad + tmp + option

    return ris


def crea_mess(tracciato, sep='', visualizza=False):
    """
    tracciato è un dizionario come da esempio
    tracciato = {'01:%02d':2, '02:%5s':'PAPPA', '03:%1s':4}
    """    
    keys = tracciato.keys()
    keys.sort()
  
    riga = ''
    for d in keys:
        i, f = d.split(':')	# i=chiave, f= formato
        tipo = f[-1]	# tipo = s, d, f
        len_campo=0

        if tipo == 'f':
            intero, decimale=f[1:-1].split('.')
            len_campo = int(intero) + 1 + int(decimale)
            tmp = str2num(tracciato[d])
            if tmp == '': tmp = 0    
        elif (tipo == 's'):
            tmp = tracciato[d]
        elif tipo == 'd':
            tmp = str2num(tracciato[d])
            if tmp == '':
                tmp = 0
            else:
                tmp = int(tmp)
        else:
            'errore formato: el[' + i + '] f =' + tipo

        if len_campo == 0:
            len_campo = int(f[1:-1])
 
        riga += (f % tmp) + sep

        if visualizza:
            print
            print 'etichetta:', d
            print 'i:', i
            print 'f:', f
            print 'len:', str(len_campo)
            print 'tipo:', tipo
            print 'valore:', "'" + (f % tmp) + sep + "'"
  
    return riga


def str2num(s):
    # check if s is number and return it
    try:
        return float(s)
    except ValueError, Argument:
        #print 'Dato non valido\n', Argument
        return ''


def write_ini(file_ini, section_name, key, value):
    
    diz_ini = {}
    parser = SafeConfigParser()
    parser.read(file_ini)
    if parser.has_section(section_name):
        list_options = parser.options(section_name)
        if key in list_options:
            parser.set(section_name, key, value)
            with open(file_ini, 'w') as config_file:
                parser.write(config_file)


def match_re(re_string, riga):
    check_field = re.compile(re_string)
    r = check_field.match(riga)
    if r <> None:
        riga = riga.replace(r.group(), '')
        riga = riga.replace('/', '-')
        return riga.strip()
    else:
        return ''    


def leggi_mess(label, mes, sep=''):
    pos = 0
    diz = {}
    mes = mes.replace(sep, '')
    for d in label:
        i,f = d.split(':')	# i=chiave, f= formato
        dim = int(f[1:-1])
        campo = mes[pos:pos+dim]
        diz['%03d'%int(i)] = campo
        pos+= dim
    return diz


def pprintTable(table):

    def get_max_width(table1, index1):
        """Get the maximum width of the given column index"""
        return max([len(format(row1[index1])) for row1 in table1])
	
    col_paddings = []
    for i in range(len(table[0])):
        col_paddings.append(get_max_width(table, i))

    for row in table:
        for i in range(len(row)):
            col = row[i].ljust(col_paddings[i] + 1)
            print col + "|",
        print	
    return


def input_campo(f):
    tipo = f[-1]	# tipo = s,d,f
    formato = f[:-1]  
    len_campo = int(formato)
    
    if tipo == 'f':
        intero,decimale = formato.split('.')
        len_campo = int(intero)+ 1 + int(decimale)
        testo = 'Inserisci un numero decimale con formato ' + formato + os.linesep
        ris = input(testo)

    if tipo == 'd':
        testo = 'Inserisci un numero intero con formato ' + formato + os.linesep
        ris = input(testo)

    if tipo == 's':
        testo = 'Inserisci un testo con formato ' + formato + os.linesep
        ris = raw_input(testo)
    
    if len(str(ris)) > len_campo:
        return 'Campo troppo lungo'
    else:
        ret = '%' + f
        return ret % ris
    

if __name__ == '__main__':
    pass
    
    
