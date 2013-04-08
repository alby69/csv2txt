#!/usr/bin/env python
# coding: utf-8

import argparse

from funzioni import *



if __name__ == '__main__':


    parser = argparse.ArgumentParser(description='Conversione tracciato')
    parser.add_argument('-l',action='store_true',dest='elenco',help='Elenco Comandi')
    parser.add_argument('-c',dest='converti',nargs='+', help='Converti Tracciato')
    parser.add_argument('-e',dest='edit',nargs='+', help='Modifica Tracciato')
    parser.add_argument('-p',dest='stampa',nargs='+', help='Stampa Tracciato')

    results = parser.parse_args()

    
    diz_ini = read_ini('setup.ini') 
    path = os.path.abspath(os.path.dirname(__file__)) # valore assoluto del path 
    
    # Carico dati dal file setup.ini
    #file_tracciato = diz_ini['SETUP']['FILE_TRACCIATO']
    #file_log = diz_ini['SETUP']['FILE_LOG']
    sep_campo = diz_ini['SETUP']['SEP_CAMPO']
    id_campo = diz_ini['SETUP']['PROGRESSIVO_CAMPO']
    len_campo = diz_ini['SETUP']['LUNGHEZZA_CAMPO']
    tipo_campo = diz_ini['SETUP']['TIPO_CAMPO']
    valore_campo = diz_ini['SETUP']['VALORE_CAMPO']

    if results.elenco:
        print 'ELENCO COMANDI'
        print '(p): visualizza tracciato'
        print '(c): converti tracciato'
        print '(e): modifica tracciato'
        print '(l): visualizza questo menu'

    if results.stampa:
        args = results.stampa        
        if len(args) == 1:
            file_tracciato = args[0]
            etichette, diz_tracciato = csv_read(path + os.sep, file_tracciato, sep_campo)
            list_tracciato = multikeysort(diz_tracciato, [id_campo])
            table = []
            table.append(etichette)
            for d in list_tracciato:
                tmp_list = []
                for e in etichette:
                    tmp_list.append(d[e])
                table.append(tmp_list)
            pprintTable(table)

    if results.converti:
        args = results.converti
        if len(args) == 2:
            file_tracciato = args[0]
            file_ris = args[1]
            f_out = open(path + os.sep + file_ris, 'w')
            etichette, diz_tracciato = csv_read(path + os.sep, file_tracciato, sep_campo)
            list_tracciato = multikeysort(diz_tracciato, [id_campo])
            tracciato = leggi_tracciato(list_tracciato, id_campo, tipo_campo, len_campo, valore_campo)
            riga = crea_mess(tracciato, sep_campo, False)

            f_out.write(riga + os.linesep)
            f_out.close
        
    if results.edit:
        args = results.edit
        if len(args) == 4:
            file_tracciato = args[0]
            key_value = args[1]
            field_name = args[2]
            field_value = args[3]
            diz_values= {field_name:field_value}
            etichette, diz_tracciato = csv_read(path + os.sep, file_tracciato, sep_campo)
            rows = csv_edit(diz_tracciato, id_campo, key_value, diz_values)
            csv_writer(path+os.sep, file_tracciato, etichette, rows, sep_campo)
            print 'File '+ file_tracciato + 'modificato..' 

    

