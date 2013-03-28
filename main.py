#!/usr/bin/env python
# coding: utf-8

from funzioni import *



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

