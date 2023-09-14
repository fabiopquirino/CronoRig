from tkinter import *
import time
from datetime import datetime
import os as os
import pickle
import numpy as np

#1 - Criando a janela do programa
root = Tk()
root.title('CronoRig 2')
root.geometry('500x600')
root.resizable(False,False)

#2 - Definindo todos os widgets (labels, buttons, canvas (barra de carregamento), entry's, check's, etc.

##Botões -> FICAM POR ÚLTIMO!!!
#botão_iniciar = Button(root, text= "Iniciar", font=("Helvetica", 12), command = COMEÇAR)
#botão_pausar = Button(root, text= "Pausar/Despausar", font=("Helvetica", 12), command = PausarExperimento)
#botão_finalizar = Button(root, text= "Finalizar", font=("Helvetica", 12), command = FinalizarExperimento)

#Entry's (vazao do experimento e duracao do mesmo)
InputVazao = Entry(root)
InputDuracao = Entry(root)

##Labels e suas "StringVar"'s

###Timer de 30 segundos
segundo = StringVar()
segundo.set("")
tempo = Label(root, textvariable= segundo, font=("Helvetica", 40), fg='red', bg='black')
###Cronometro (tempo de experimento)
cronometro = StringVar()
cronometro.set("")
tempo_de_exp = Label(root, textvariable= cronometro, font=("Helvetica", 14), fg='white', bg='blue')
###valvulas abertas
valvulas_abertas = StringVar()
valvulas_abertas.set("")
valvulas = Label(root, textvariable= valvulas_abertas, font=("Helvetica",24), bg = 'white')
###prox valvulas abertas
prox_valvulas_abertas = StringVar()
prox_valvulas_abertas.set("")
prox_valvulas = Label(root, textvariable=prox_valvulas_abertas, font=("Helvetica",16), bg = 'white')

###Horário de início e final
Horario_De_Inicio = Label(root, text= "", font=("Helvetica",14), fg='white', bg='green')
Horario_De_Finalizacao = Label(root, text= "", font=("Helvetica",14), fg='white', bg='red')

###Textos
#### Associados à tela 1(início)
Txt_VazaoDoExperimento = Label(root, text= "Vazão do experimento:", font=("Helvetica",12))
Txt_instrucoes = Label(root, text= "Insira um número entre 300 e 900", font=("Helvetica",8), fg = 'red')
Txt_DuracaoDoExperimento = Label(root, text= "Duração do experimento:", font=("Helvetica",11))
Txt_instrucoes2 = Label(root, text= "Insira a quantidade de minutos", font=("Helvetica",8), fg = 'red')
Txt_Lh = Label(root, text= "L/h", font=("Helvetica",12))
Txt_minutos = Label(root, text= "minutos", font=("Helvetica",12))

#### Associados à tela 2 (atraso vazao)
Txt_AtrasoVazao = Label(root, text='Tempo até a solução chegar na injeção:'\
                            , font=("Helvetica", 16))

#### Associados à tela 3(aquisição)
Txt_ValvulasAbertas = Label(root, text="Válvulas a serem abertas:", font=("Helvetica",13))
Txt_ProxValvulasAbertas = Label(root, text="Próximas Válvulas a serem abertas:", font=("Helvetica",8))

DadosEsperadoss = ''
Txt_DadosEsperados = Label(root, text=DadosEsperadoss , font=("Helvetica",14), bg = 'white')

#### Associados à tela 4 (intervalo)
Txt_IntervaloAquisicao = Label(root, text = '-> Feche todas as válvulas \n\
-> Aguarde o intervalo para a próxima aquisição de dados',\
                               font=("Helvetica",12))

#### Associados à tela 5 (finalizacao)
Txt_IntervaloAquisicaoFIM = Label(root, text = '-> Feche todas as válvulas \n\
-> Prepare-se para encerrar o experimento',\
                               font=("Helvetica",12))

#### Associados a várias telas
Txt_AvisoComecarAquisicao = Label(root, text = '-> Abra as seguintes válvulas:\n\
P01 e Pdif01', font=("Helvetica",16), bg = 'white') #(tela 2 e 4)
Txt_Observações = Label(root, text="Observações:", font=("Helvetica",14)) #(tela 3 a 5)
ExperimentoPausado = Label(root, text= "", font=("Helvetica",20)) #(tela 3 a 5)
ExperimentoFinalizado = Label(root, text= "Experimento Finalizado"\
                               , font=("Helvetica",20),fg="white", bg = 'red')
VerificarVazao = Label(root, text= "Verifique a vazão das bombas",\
                                       font=("Helvetica",20), bg='white') #(tela 3 a 5)
Txt_Atencao = Label(root, text= "ATENÇÃO: Não arrastar a janela do programa depois de iniciado.",\
                   font=("Helvetica",12), fg = 'red') #(tela 1 a 5)
Txt_HorarioInicio = Label(root, text= "Horário de Início do Experimento:", font=("Helvetica",10)) #(tela 3 a 5)
Txt_Horario_De_Finalizacao = Label(root, text= "Horário do Fim do Experimento:",
                                   font=("Helvetica",10))
Txt_TempoExperimento = Label(root, text= "Tempo Útil de Experimento:", font=("Helvetica",10)) #(tela 3 a 5)

## Canva (barrinha de carregamento (tela 2 a 5)
canvas = Canvas(root, width= 500, height = 15, bg = 'white')

# 3 - Variáveis globais
## Editáveis
IntervaloAvisoVazao = 5*60
DuracaoAvisoVazao = 15
ti = 30 #intervalo entre valvulas
NumeroDeAquisicoesI = 9 #numero padrao de aquisicoes
IntervaloAquisicoesI = 10*60
IntervaloAquisicoesII = 4*60 + 30
IntervaloFinal = 30
## Não Editáveis
c = 0
v = 0
n = 9
## Diretórios
#CaminhoPEsperadas = "./PEsperadas"
##Dicionário com dados
dados = {}

timer_ON = False

                       
# 4 - Funções

## Cospe dados ao finalizar experimento
def cuspirDados():
    global c
    global n
    now = datetime.now()
    nome_arquivo = now.strftime("%Y_%m_%d %H-%M-%S")
    #diretorio_arquivo = "./"
    #nome_completo = os.path.join("./", nome_arquivo+".txt")
    #print (nome_arquivo)
    arquivo = open(nome_arquivo+".txt", "w+")
    
    # Escrevendo dados no arquivo 
    arquivo.write('Tempo de espera para o encher o Rig: ' + str(dados["Atraso"]) + ' segundos')
    arquivo.write('\n\n')
    arquivo.write('Vazão do experimento: ' + str(dados["Vazão"]) + ' L/h')
    arquivo.write('\n\n')
    arquivo.write('Horário de início do experimento: ' + dados["HoraInício"]  )
    arquivo.write('\n\n')
    arquivo.write('Horário do final do experimento: ' + dados["HoraFinal"] )
    arquivo.write('\n\n')
    arquivo.write('Duração total: ' + ConverteFormato(dados["DuraçãoTotal"], 2))
    arquivo.write('\n\n')
    arquivo.write('Número de Aquisicoes: ' + str(dados["NúmeroDeAquisições"]))
    arquivo.close()

##Inicia programa (tela 1)

##Esta função faz a transição de telas entre os modos de tela usando o método .place
def Transicao(tela, x=21):
    
    #0 para o 1 (inicia o programa)
    if tela == 0:
        botão_iniciar.grid(row=0, column = 0, padx = (0, 500))
        
        InputVazao.place(x=178,y=44)
        Txt_VazaoDoExperimento.place(x=10,y=40)
        Txt_instrucoes.place(x=175, y=60)
        Txt_Lh.place(x=300,y=40)

        InputDuracao.place(x=178,y=80)
        Txt_DuracaoDoExperimento.place(x=10,y=76)
        Txt_instrucoes2.place(x=175, y=96)
        Txt_minutos.place(x=300,y=76)
        
        #Txt_Atencao.place(x=10,y=570)

    #1 para o 2 (vai pra tela de AtrasoVazao de acordo com as infos inseridas)
    if tela == '12':
        #destruição
        botão_iniciar.destroy()
        InputVazao.destroy()
        Txt_VazaoDoExperimento.destroy()
        Txt_Lh.destroy()
        Txt_instrucoes.destroy()
        Txt_DuracaoDoExperimento.destroy()
        Txt_instrucoes2.destroy()
        InputDuracao.destroy()
        Txt_minutos.destroy()
        #Posicionando
        #botão_pausar.grid(row=0, column = 1, padx = (0, 280))
        botão_finalizar.grid(row=0, column = 2)
        Txt_AtrasoVazao.place(x=60,y=115)
        tempo.place(x=185,y=150)

    #2 ou 4 para o 3 (vai de AtrazoVazao ou intervalo para aquisicao)
    if tela == '2ou43':
        #destruição e ocultação
        Txt_AtrasoVazao.place(x=35,y=840)
        Txt_AvisoComecarAquisicao.place(x=35,y=840)
        Txt_IntervaloAquisicao.place(x=35,y=840)
        Txt_AvisoComecarAquisicao.place(x=35,y=840)
        #Posicionando
        ##Permanentes
        Horario_De_Inicio.place(x=210,y=35)
        Txt_HorarioInicio.place(x=10,y=37)
        tempo_de_exp.place(x=179,y=68)
        Txt_TempoExperimento.place(x=10,y=70)
        Txt_Observações.place(x=190,y=340)
        canvas.place(x = 0, y = 315)
        
        ##Apenas na tela 3
        Txt_ValvulasAbertas.place(x=10,y=240)
        Txt_ProxValvulasAbertas.place(x=60,y=283)
        valvulas.place(x=210,y=230)
        prox_valvulas.place(x=240,y=280)

    #3 para o 4 (de aquisicao para intervalo)
    if tela == '34':
        #print (x)
        #tira aviso de intervalo e avisa pra preparara quisicao
        if x<=20:
            Txt_AvisoComecarAquisicao.place(x=110,y=240)
            Txt_IntervaloAquisicao.place(x=35,y=840)
        else:
            #destruição e ocultação
            Txt_ValvulasAbertas.place(x=10,y=940)
            Txt_ProxValvulasAbertas.place(x=60,y=983)
            valvulas.place(x=210,y=930)
            prox_valvulas.place(x=240,y=980)
            Txt_DadosEsperados.place(x = 35 , y = 980)
            canvas.delete("all")
            #Posicionando
            Txt_IntervaloAquisicao.place(x=35,y=240)
        
    #3 para o 5 (de aquisicao para intervalo final)
    if tela == '35':
        #destruição e ocultação
        Txt_ValvulasAbertas.place(x=10,y=940)
        Txt_ProxValvulasAbertas.place(x=60,y=983)
        valvulas.place(x=210,y=930)
        prox_valvulas.place(x=240,y=980)
        canvas.delete("all")
        #Posicionando
        Txt_IntervaloAquisicaoFIM.place(x=105,y=240)

    if tela == "finalizar":
        horafinal = datetime.today().strftime('%H:%M:%S')
        Horario_De_Finalizacao.config(text = horafinal)
        dados["HoraFinal"] = horafinal
        cuspirDados()
        '''ocultação'''
        Txt_ValvulasAbertas.place(x=800,y=240)
        Txt_ProxValvulasAbertas.place(x=800,y=295)
        valvulas.place(x=800,y=230)
        prox_valvulas.place(x=800,y=295)
        canvas.place(x = 0, y = 815)
        tempo.place(x=885,y=150)
        Txt_IntervaloAquisicaoFIM.place(x=105,y=940)
        Txt_Observações.place(x=190,y=940)
        canvas.delete("all")
        '''posicionamento'''
        Horario_De_Finalizacao.place(x=200,y=102)
        Txt_Horario_De_Finalizacao.place(x=10,y=105)
        ExperimentoFinalizado.place(x=105,y=200)
        #if x = 'forçada':
        #if x = 'natural':
    root.update()

    

def ConfiguraAvisoVazao(c):
    if (c)%IntervaloAvisoVazao==0 and (c)//IntervaloAvisoVazao>=1:
            VerificarVazao.place(x=70,y=400)

    if (c)%IntervaloAvisoVazao>=DuracaoAvisoVazao:
            VerificarVazao.place(x=800,y=400)

def ConfiguraAvisoAquisicao(x):
    if x<=20:
            Txt_AvisoComecarAquisicao.place(x=110,y=240)
            Txt_IntervaloAquisicao.place(x=35,y=840)

    if x==0:
            Txt_AvisoComecarAquisicao.place(x=110,y=940)

## Converte um tempo no formato de segundos para formato string (Formato 1 ou 2)
def ConverteFormato(segundos, formato):
    if formato == 1:
        m, s = divmod(segundos, 60)
        min_sec_format = '{:02d}:{:02d}'.format(m, s)
        return min_sec_format
    if formato == 2:
        h, m, s = (divmod(segundos, 3600)[0], int(divmod(segundos, 3600)[1]/60) ,\
            divmod(segundos, 60)[1])
        min_sec_format = '{:02d}:{:02d}:{:02d}'.format(h, m, s)
        return min_sec_format

##Função da barrinha de carregamento
dados["DuraçãoTotal"] = 0
def cria_retangulo(q):
    global ti
    c = dados["DuraçãoTotal"]
    t = ti - c%(ti)
    if t == ti:
        canvas.delete("all")
    else:
        canvas.create_rectangle((50*(q-6), 0), (50*(q-5), 17), fill = 'green')
        canvas.create_rectangle((50*(q-5), 0), (50*(q-4), 17), fill = 'green')
        canvas.create_rectangle((50*(q-4), 0), (50*(q-3), 17), fill = 'green')
        canvas.create_rectangle((50*(q-3), 0), (50*(q-2), 17), fill = 'green')
        canvas.create_rectangle((50*(q-2), 0), (50*(q-1), 17), fill = 'green')
        canvas.create_rectangle((50*(q-1), 0), (50*q, 17), fill = 'green')

'''Esta função carrega um dicionário proveniente de um arquivo pck que contém todas as curvas de pressão para as diferentes 
vazões com as quais já fizemos experimentos. Em seguida, ela define quais pressões serão usadas em função da vazão que o usuário
definiu ao iniciar o experimento'''
'''def criaPEsperadas(vazao):
    global CaminhoPEsperadas
    # este caminho é mutável em função do PC a ser utilizado. Ele pode ser modificado no início do código

    with open(CaminhoPEsperadas, 'rb') as f:
        PEsperadas = pickle.load(f)
        f.close()
    
    Vazão = str(vazao)+'lh'
    if Vazão in PEsperadas:
        pass
    else:
        Vazão = '300lh' '''


'''  ## Dados esperados em função da vazão (vai pro timer)
    texto = 'DADOS ESPERADOS PARA ESTA AQUISIÇÃO:\n\nPRS-146: {a}\nPRS-145: {b}\nPRS-143: \
{c}\nPRS-144: {d}'
    dados['Txt_PEsperadas'] = [texto.format(a=PEsperadas[Vazão][0,0], b=PEsperadas[Vazão][0,1], c=PEsperadas[Vazão][0,2], d=PEsperadas[Vazão][0,3]),\
                               texto.format(a=PEsperadas[Vazão][1,0], b=PEsperadas[Vazão][1,1], c=PEsperadas[Vazão][1,2], d=PEsperadas[Vazão][1,3]),\
                               texto.format(a=PEsperadas[Vazão][2,0], b=PEsperadas[Vazão][2,1], c=PEsperadas[Vazão][2,2], d=PEsperadas[Vazão][2,3]),\
                               texto.format(a=PEsperadas[Vazão][3,0], b=PEsperadas[Vazão][3,1], c=PEsperadas[Vazão][3,2], d=PEsperadas[Vazão][3,3]),\
                               texto.format(a=PEsperadas[Vazão][4,0], b=PEsperadas[Vazão][4,1], c=PEsperadas[Vazão][4,2], d=PEsperadas[Vazão][4,3]),\
                               texto.format(a=PEsperadas[Vazão][5,0], b=PEsperadas[Vazão][5,1], c=PEsperadas[Vazão][5,2], d=PEsperadas[Vazão][5,3]),\
                               texto.format(a=PEsperadas[Vazão][6,0], b=PEsperadas[Vazão][6,1], c=PEsperadas[Vazão][6,2], d=PEsperadas[Vazão][6,3]),\
                               texto.format(a=PEsperadas[Vazão][7,0], b=PEsperadas[Vazão][7,1], c=PEsperadas[Vazão][7,2], d=PEsperadas[Vazão][7,3]),\
                               texto.format(a=PEsperadas[Vazão][8,0], b=PEsperadas[Vazão][8,1], c=PEsperadas[Vazão][8,2], d=PEsperadas[Vazão][8,3]),\
                               texto.format(a=PEsperadas[Vazão][9,0], b=PEsperadas[Vazão][9,1], c=PEsperadas[Vazão][9,2], d=PEsperadas[Vazão][9,3])]
    #print (dados['Txt_PEsperadas']) '''
            


##Funções que iniciam tela
def AtrasoVazao():
    #Pega os dados de entrada pelo usuario e converte pra int
    vazao = InputVazao.get()
    vazao = int(vazao)
    Duracao = InputDuracao.get()
    Duracao = int(Duracao)*60
    # Cria tabela de PEsperadas em função da vazao definida pelo usuário
    #criaPEsperadas(vazao)
    #define tempo de atraso até o experimento realmente começar
    atraso = 126600//vazao
    tempo_atraso = ConverteFormato(atraso, 1) #str para ir no timer
    # Adicionando dados ao dicionário
    dados["Duração"] = Duracao
    dados["Vazão"] = vazao
    dados["Atraso"] = atraso
    #dados['DadosEsperados'] = DadosEsperados[vazao]
    #posiciona o timer na tela e seta ele
    Transicao('12')
    a0 = int(time.time())
    a1 = a0
    t = atraso - (a1-a0)
    while t > 0:
        segundo.set(ConverteFormato(t, 1))
        ConfiguraAvisoAquisicao(t)
        root.update()
        time.sleep(0.1)
        a1 = int(time.time())
        t = atraso - (a1-a0)

def timer(): 
    global ti
    global IntervaloAvisoVazao
    global DuracaoAvisoVazao
    global IntervaloAquisicoesI
    global IntervaloAquisicoesII
    global NumeroDeAquisicoesI
    global IntervaloFinal

    print ('INICIO EXP')
    #Adiciona dados ao dicionário
    a0 = int(time.time())# - (179*60 + 29 )
    dados["SegundoInicial"] = a0
    horainicial = datetime.today().strftime('%H:%M:%S')
    dados["HoraInício"] = horainicial
    #Configura horário inicial e mostra no app, além de fazer a transição
    Horario_De_Inicio.config(text= horainicial)

    lista_valvulas = ['P01 e Pdif01', 'P02 e Pdif01', 'P03 e Pdif02', 'P04 e Pdif02',\
                      'P05 e Pdif03', 'P06 e Pdif03', 'P07 e Pdif04', 'P08 e Pdif04',\
                      'P09', 'P10','   ']

    duracao = dados["Duração"]
    t = ti
    c = 0
    n = 0
    v = 0
    dados["NúmeroDeAquisições"] = 0
    DadosEsperados = '       '#dados['Txt_PEsperadas']
    #aa = tempo do término da última aquisição
    #ai = tempo do término do último intervalo
    #ae = tempo do término do intervalo especial
    #af = tempo do término da aquisição final

    dados['timer_ON'] = True
    CondicaoUltimaAquisicao = True

    while dados['timer_ON']==True:
        n = c//(10*ti+IntervaloAquisicoesI) + (c//(duracao-IntervaloFinal-10*ti))
        #print (c)
        if c >= (duracao-IntervaloFinal):
            t = IntervaloFinal - c%IntervaloFinal
            if c >= duracao:
                dados["NúmeroDeAquisições"] = n
                Transicao('finalizar')
                #timer_ON=False
                print (ConverteFormato(c, 2), 'acabou')
                break
            Transicao('35')
            #if c%30==0: print (ConverteFormato(c, 2), 'intervalo final')

        elif c >= (duracao-IntervaloFinal-10*ti-IntervaloAquisicoesII)\
             and c<(duracao-IntervaloFinal-10*ti):
            t = IntervaloAquisicoesII - \
                (c-(duracao-IntervaloFinal-10*ti-IntervaloAquisicoesII))%IntervaloAquisicoesII
            #print (ConverteFormato(c, 2), 'penultimo intervalo')
            Transicao('34', t)
            #if c%30==0: print (ConverteFormato(c, 2), 'penultimo intervalo')

        elif c >= (duracao-IntervaloFinal-10*ti):          
            t = ti - (c -(duracao-IntervaloFinal-10*ti))%ti
            #print (n)
            q = int(10*((ti-t)/ti))
            cria_retangulo(q)
            n = c//(10*ti+IntervaloAquisicoesI) + 2*(c//(duracao-IntervaloFinal-10*ti))
            v = (c-(duracao-IntervaloFinal-10*ti))//ti
            Transicao('2ou43')
            Txt_DadosEsperados.place(x =35 , y = 880)
            #if c%30==0: print (ConverteFormato(c, 2), 'ultima aquisição')

        elif c%(10*ti+IntervaloAquisicoesI)<10*ti and c<(duracao-IntervaloFinal-10*ti-IntervaloAquisicoesII):
            t = ti - c%(ti)
            q = int(10*((ti-t)/ti))
            cria_retangulo(q)
            #print (n)
            dados["NúmeroDeAquisições"] = n
            n = c//(10*ti+IntervaloAquisicoesI) + 2*(c//(duracao-IntervaloFinal-10*ti))
            v = (c-n*(IntervaloAquisicoesI+10*ti))//ti
            Transicao('2ou43')
            # Dados esperados na tela
            if n==0:
                DadosEsperadoss = DadosEsperados[v]
                Txt_DadosEsperados.config(text=DadosEsperadoss)
                Txt_DadosEsperados.place(x =35 , y = 380)
            else:
                Txt_DadosEsperados.place(x =35 , y = 880)
            #if c%30==0: print (ConverteFormato(c, 2), 'aquisicao', n+1)
        else:
            n = c//(10*ti+IntervaloAquisicoesI) + 2*(c//(duracao-IntervaloFinal-10*ti))
            t = (n+1)*(10*ti + IntervaloAquisicoesI) - c
            Transicao('34', t)
            #if c%30==0: print (ConverteFormato(c, 2), 'intervalo', n+1)
            

        
        #configura variaveis q aparecem na tela
        n = c//(10*ti+IntervaloAquisicoesI) + 2*(c//(duracao-IntervaloFinal-10*ti))
        ConfiguraAvisoVazao(c)
        segundo.set(ConverteFormato(t, 1))
        cronometro.set(ConverteFormato(c, 2))
        valvulas_abertas.set(lista_valvulas[v])
        prox_valvulas_abertas.set(lista_valvulas[(v+1)])
        #atualiza
        root.update
        #dorme x=1 segundos
        time.sleep(0.1)
        #if c%30==0:
        #   if c%(10*ti+IntervaloAquisicoesI)<10*ti: print (ConverteFormato(c, 2), v)
        #    else: print(ConverteFormato(c, 2), "intervalo")
        c = int(time.time()) - a0
        dados["DuraçãoTotal"] = c
        
def COMEÇAR():
    AtrasoVazao()
    timer()

def termina():
    dados['timer_ON'] = False
    Transicao('finalizar')

##Botões
botão_iniciar = Button(root, text= "Iniciar", font=("Helvetica", 12), command = COMEÇAR)
#botão_pausar = Button(root, text= "Pausar/Despausar", font=("Helvetica", 12))#, command = PausarExperimento)
botão_finalizar = Button(root, text= "Finalizar", font=("Helvetica", 12), command = termina)
Transicao(0)
root.mainloop()
    







































