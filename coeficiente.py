import PyPDF2

def verificaOpt( c ) :
    if c >= '0' and c <= '9':
        return False
    return True

def extraiDados(st) :
    i = 0
    table = [[],[],[]]
    for c in st :
        notaAtual = ''
        chAtual = ''
        if c == ',' or  (c == '-' and st[i+1] == '-') :
            j = i+2
            for c2 in st[i+2:i+9] :
                notaAtual = notaAtual + c2
                if c2 == '.' :
                    notaAtual = notaAtual + '0'
                    offset = 2
                    if verificaOpt(st[j+2]) :
                        offset = 3
                    chAtual = st[j+offset:j+offset+2]
                    break
                j = j + 1
            table[0].append(notaAtual)
            table[1].append(chAtual)
        elif c == '.' and st[i-4]=='2' and st[i-3]=='0' and (st[i+1]=='1' or st[i+1]=='2' ) :
            table[2].append(st[i-4:i+2])
        i = i+1 
    return table

def extraiTabela(filepath) :
    pdf_file = open(filepath,'rb')
    read_pdf = PyPDF2.PdfFileReader(pdf_file)
    tabelaFinal = [[],[],[]]
    for n in range (read_pdf.getNumPages()) :
        page = read_pdf.getPage(n)
        txt = page.extractText()
        if 'Carga Horária Integralizada/Pendente' in txt :
            break
        splited = txt.split(' %MédiaCHCRConceitoSE')
        if n == 0 :
            spl2 = splited[1].split('PARTICIPAÇÕES NO ENADE')
        else :
            spl2 = splited[1].split('Página') 
        tabelaParcial = extraiDados(spl2[0])
        tabelaFinal[0] = tabelaFinal[0] + tabelaParcial[0]
        tabelaFinal[1] = tabelaFinal[1] + tabelaParcial[1]
        tabelaFinal[2] = tabelaFinal[2] + tabelaParcial[2]
    return tabelaFinal

def calculaCG(tabela, periodo='2019.1'):
    tam = len(tabela[0])
    sumCh = 0
    sumParcial = 0
    if tam==len(tabela[1]):
        for i in range (tam) :
            if float(tabela[2][i]) <= float(periodo):
                ch = int(tabela[1][i])
                nota = float(tabela[0][i])
                sumParcial = sumParcial + nota*ch
                sumCh = sumCh + ch
        return sumParcial/sumCh
    else :
        print('Houve erro na extracao dos dados, tamanho lista CH != tam lista notas')

#coloque abaixo o caminho do arquivo do historico.
tabelaFinal = extraiTabela('..\coef_arquivos\historico.pdf')
# para calcular CG de semestres anteriores basta 
# fazer a chamada : calculaCG(tabelaFinal, periodo='2018.2')
# será calculado o CG até o periodo especificado(inclusive)
print(calculaCG(tabelaFinal))