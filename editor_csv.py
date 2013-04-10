from Tkinter import *
import ttk
import tkMessageBox
import os, string, datetime
from funzioni import *

path = os.path.abspath(os.path.dirname(__file__)) # valore assoluto del path 


class Application:
    tabella = ""
    id_campo = ''
    sep_campo = ''
    nrec = 0
    curr_rec = 0
    step = 1
    nomi = []
    elenco_tabelle = []
    diz_tracciato = []
    diz_curr = {}
    campi = {}
    valori = []
    active_wnd = ''
    
    def __init__(self,master,title="Senza Titolo",id_campo='id',sep_campo='|'):
        main_form = Frame(master,width=200,height=100)
        main_form.master.title(title)
        main_form.grid()
        self.id_campo = id_campo
        self.sep_campo = sep_campo
        self.crea_menu(master)
        
        
    def ok(self):
        csv_writer(path+os.sep, self.tabella+'.csv', self.nomi, self.diz_tracciato, sel.sep_campo)
        print 'Registrazione effettuata...'

        


    def muovi(self,direzione):
        
        if self.diz_curr == {}:
            rec = 1
        else:
            rec = int(self.diz_curr[self.id_campo])

        self.curr_rec = 0
        
        if direzione == "inizio": self.curr_rec = 1
        if direzione == "fine":   self.curr_rec = self.nrec       
            
        if direzione == "prec":
          if ((rec-self.step) >= 1):
            self.curr_rec = rec-self.step  

        if direzione == "succ":
          if ((rec+self.step) <= self.nrec):
            self.curr_rec = rec+self.step  

        if self.curr_rec <> 0:
            tmp_list = []
            tmp_diz = self.leggi_maschera()
            for d in self.diz_tracciato:
                if d[self.id_campo] == '%03d' % rec:
                    if tmp_diz <> {}:
                        d = tmp_diz
                if d[self.id_campo] == '%03d' % self.curr_rec:
                    self.diz_curr = d
                tmp_list.append(d)

            self.diz_tracciato = tmp_list
            self.riempi_maschera(self.diz_curr)
                  
            
    def leggi_maschera(self):
        tmp_diz = {}
        nulli = 0        
        nr_campi = len(self.nomi)
        for e in self.nomi:
            valore = self.campi[e].get()
            tmp_diz[e] = valore
            if valore == '': nulli += 1
            
        if nulli == nr_campi:
            return {}        
        else:
            return tmp_diz
        
        
    def riempi_maschera(self,res):
        if res <> {}:
            for e in self.nomi:
                self.campi[e].delete(0,END)
                self.campi[e].insert(0,res[e])
              

    def svuota_maschera(self):
        for e in self.nomi:
            self.campi[e].delete(0,END)


    def btn_action(self,value):
      if value == "nuovo": self.svuota_maschera()
      if value == "<<":    self.muovi("inizio")        
      if value == "<":     self.muovi("prec")
      if value == ">":     self.muovi("succ")
      if value == ">>":    self.muovi("fine")
      if value == "cancella":
        risp = tkMessageBox.askyesno("ATTENZIONE", "Elimino record?")
        if risp == True:
          res = db.delete(path+self.tabella+".tbl",['recno'],[self.curr_rec])
          #res = db.pack(path+self.tabella+".tbl")
          self.nrec = db.len(path+self.tabella+".tbl")
          #self.svuota_maschera()
          self.muovi("succ")

      #if value == "esci":  self.active_wnd.destroy()
      if value == "ok":    self.ok()
                
    def crea_toolbar(self,master):
        # ToolBar
        tb = Frame(master)
        #btn_label_list = ["nuovo","<<","<",">",">>","esci","ok"]
        btn_label_list = ["nuovo","<<","<",">",">>","cancella","ok"]
        i = 0
        for l in btn_label_list:
          btn = Button(tb,text=l.upper(),width=5,command=lambda value=l:self.btn_action(value))
          btn.grid(row=0,column=i,sticky=W)
          i += 1

        tb.grid()

    def crea_menu(self,master):
        menu = Menu(master)
        master.config(menu=menu)
        edit_menu = Menu(menu)
        gest_menu = Menu(menu)
        
        menu.add_cascade(label="Edit",menu=edit_menu)
        #edit_menu.add_command(label="New Table",command=lambda:self.apri_maschera("tmp_campi"))
        edit_menu.add_command(label="New Table",command=lambda:self.nuova_tabella())
        menu.add_cascade(label="Gestione",menu=gest_menu)
        # Creo gli elementi leggendo le tabelle esistenti nel path
        dirList = os.listdir(path)
        i = 0
        for tab in dirList:
          if tab.endswith('.csv'):
            t =  tab[:-4].upper()
            self.elenco_tabelle.append(t)
            gest_menu.add_command(label=self.elenco_tabelle[i],command=lambda value=self.elenco_tabelle[i].lower(): self.apri_maschera(value))
            i += 1
        
   
  
    def apri_maschera(self,nome_tab):
        self.tabella = nome_tab
        self.nomi, list_tracciato = csv_read(path+os.sep, nome_tab+'.csv', self.sep_campo)
        self.diz_tracciato = multikeysort(list_tracciato, [self.id_campo])  
        self.nrec = len(self.diz_tracciato)
  
        cboCombo = []
        varCombo_lst = []
        if self.nrec > 0: 
          wnd = Toplevel()
          wnd.title(self.tabella.upper())
          self.crea_toolbar(wnd)
        
          form = Frame(wnd)
          for i in range(len(self.nomi)):
            """varCombo = StringVar()
            varCombo.set(self.tipi[i])
            varCombo_lst.append(varCombo)
            cbo = ttk.Combobox(form, values=tipi_std, textvariable=varCombo_lst[i])
            cbo.set(self.tipi[i])
             
            cboCombo.append(cbo)                
            cboCombo[i].grid(row=i+2,column=2,sticky=W)
            """
            # Etichette
            Label(form,text=self.nomi[i],width=15).grid(row=i+2,sticky=W)           
            # nomi
            self.campi[self.nomi[i]] = Entry(form,width=30)
            self.campi[self.nomi[i]].grid(row=i+2,column=1,sticky=W)
            

          form.grid()
          self.active_wnd = wnd
          self.muovi("inizio")
        else:
          self.apri_maschera("tmp_campi")

    
    def crea_tabella(self,path,tabella):
      try:
        db.create(path+tabella+".tbl",[])
      except KBError as e:
        tkMessageBox.showerror("ERRORE", "Tabella esistente")
      self.btn_action('esci')
       
    def nuova_tabella(self):
        
        wnd = Toplevel()
        wnd.title('NUOVA TABELLA')
        
        form = Frame(wnd)
        Label(form,text='Nome Tabella',width=15).grid(row=1,sticky=W)    
        tabella = Entry(form,width=30)
        tabella.grid(row=2,sticky=W)        
        Button(form,text='Ok',width=5,command=lambda:self.crea_tabella(path,tabella.get())).grid(row=3,sticky=W)
        form.grid()
        self.active_wnd = wnd  


if __name__ == '__main__':
    root = Tk()    
    app = Application(root,'CSV2TXT')
    root.mainloop()

