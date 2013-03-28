#!/usr/bin/env python
# coding: utf-8

import os
import csv

from ConfigParser import SafeConfigParser


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


if __name__ == '__main__':

  
    diz_ini = read_ini('setup.ini') 
    path = os.path.abspath(os.path.dirname(__file__)) # valore assoluto del path 
    print diz_ini
    # Carico dati dal file setup.ini
    file_tracciato = diz_ini['SETUP']['FILE_TRACCIATO']
    file_log = diz_ini['SETUP']['FILE_LOG']
    sep_campo = diz_ini['SETUP']['SEP_CAMPO']
    id_campo = diz_ini['SETUP']['PROGRESSIVO_CAMPO']
    len_campo = diz_ini['SETUP']['LUNGHEZZA_CAMPO']
    tipo_campo = diz_ini['SETUP']['TIPO_CAMPO']
    valore_campo = diz_ini['SETUP']['VALORE_CAMPO']

    f_out = open(path + os.sep + file_log, 'w')
    etichette, diz_tracciato = csv_read(path + os.sep, file_tracciato)
    list_tracciato = multikeysort(diz_tracciato, [id_campo])
    tracciato = leggi_tracciato(list_tracciato, id_campo, tipo_campo, len_campo, valore_campo)
    riga = crea_mess(tracciato, sep_campo, True)
    print riga
  
    f_out.write(riga + os.linesep)
    f_out.close
