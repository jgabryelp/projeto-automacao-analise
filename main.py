#importando as bibliotecas
import gdown 
import pandas as pd 
import matplotlib.pyplot as plt
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4 
import smtplib
from email.message import EmailMessage
import mimetypes
import os
from dotenv import load_dotenv
load_dotenv()



#baixando o arquivo da base com o request pra baixar a base de dados que eu hospedei no google drive
link = "https://drive.google.com/file/d/1bppzawcFjqZhqvvWSeaaGkYhDGDmOFJA/view?usp=drive_link" #link de compartilhamento do arquivo (contém o ID do arquivo necessário para fazer o download com o request)

idarquivo = link.split("/d/")[1].split("/")[0] #selecionando o id do arquivo usando a função split, que separa uma string com base em algum separador, nesse caso "/d/" e "/"
 
linkdownload = f"https://drive.google.com/uc?id={idarquivo}" #criando o link de download com o ID do arquivo

gdown.download(linkdownload, "AmazonSaleReport.csv", quiet=False) #lendo e baixando o arquivo



#importando e lendo a base de dados
basededados = pd.read_csv("AmazonSaleReport.csv")



#analisando a base e selecionando informações importantes
def formatarparadolar(valor):
    valorformatado = f"${valor:,.2f}" #criando uma função para formatar valores numéricos em dólar
    return valorformatado
    

categoriaseseusfaturamentos = basededados[["Category", "Amount"]].groupby("Category").sum() #selecionando as colunas de categoria dos produtos e valor das vendas de cada categoria 
categoriaseseusfaturamentos = categoriaseseusfaturamentos.reset_index().sort_values("Amount", ascending=False) #tirando o index da tabela e ordenando os faturamentos do maior para o menor
categoriaseseusfaturamentos["Amount"] = categoriaseseusfaturamentos["Amount"].apply(formatarparadolar) #aplicando a formatação para dólar


cidadescommaispedidos = basededados["ship-city"].value_counts() #selecionando o nome das cidades e quantas vezes elas aparecem nos pedidos
cidadescommaispedidos = cidadescommaispedidos.reset_index() #transformando o resultado do value_counts() em uma tabela comum
cidadescommaispedidos = cidadescommaispedidos[:15] #selecionando as 15 cidades com maior quantidade de pedidos


evoluçaofaturamentomeses = basededados[["Date", "Amount"]] #selecionando a coluna de datas dos pedidos e valor dos pedidos
evoluçaofaturamentomeses["Date"] = pd.to_datetime(basededados["Date"], format="%m-%d-%y") #transformando a coluna de data em um DateTime Object (antes era uma string)
evoluçaofaturamentomeses["Month"] = evoluçaofaturamentomeses["Date"].dt.month #criando uma nova coluna para os meses
evoluçaofaturamentomeses = evoluçaofaturamentomeses[["Month", "Amount"]] #selecionando apenas a coluna dos meses e valores dos pedidos

evoluçaofaturamentomeses = evoluçaofaturamentomeses.groupby("Month").sum() #selecionando os meses sem repeti-los e seus faturamentos
evoluçaofaturamentomeses = evoluçaofaturamentomeses.reset_index() #retirando o index da tabela 

nomesmeses = {
    1: "Janeiro",
    2: "Fevereiro",
    3: "Março",
    4: "Abril",
    5: "Maio",
    6: "Junho",       #dicionário com os nomes de cada mês
    7: "Julho",
    8: "Agosto",
    9: "Setembro",
    10: "Outubro",
    11: "Novembro",
    12: "Dezembro"
}

evoluçaofaturamentomeses["Month"] = evoluçaofaturamentomeses["Month"].map(nomesmeses) #aplicando os nomes dos meses na ordem do calendário



#criando o relatório da análise
categoriaseseusfaturamentosrelatorio = ""                       #formatando as tabelas que serão escritas no relatório
for indice, linha in categoriaseseusfaturamentos.iterrows():
    categoriaseseusfaturamentosrelatorio += (f"  {linha["Category"]}  -"  f"  Faturou: {linha["Amount"]}\n") 

cidadescommaispedidosrelatorio = ""
for indice, linha in cidadescommaispedidos.iterrows(): 
    cidadescommaispedidosrelatorio += (f"  {linha["ship-city"]}  -"  f"  {linha["count"]} Pedidos\n")
                                                    
evoluçaofaturamentomesesrelatorio = ""
for indice, linha in evoluçaofaturamentomeses.iterrows():
    evoluçaofaturamentomesesrelatorio += (f"  {linha["Month"]}  -"  f"  ${linha["Amount"]:,.2f}\n")    


relatorio = f"""
                        =================================
                        RELATÓRIO DE VENDAS E-COMMERCE  
                        =================================

Prezados, segue em anexo o relatório da análise das vendas com os resultados obtidos.
    

CATEGORIAS E SEUS FATURAMENTOS:
{categoriaseseusfaturamentosrelatorio}

AS 15 CIDADES COM MAIOR QUANTIDADE DE PEDIDOS:
{cidadescommaispedidosrelatorio}

FATURAMENTO AO LONGO DOS MESES:
{evoluçaofaturamentomesesrelatorio}

"""



#criando os gráficos
plt.figure(figsize=(11, 5)) #selecionando o tamanho do gráfico

plt.bar(categoriaseseusfaturamentos["Category"], categoriaseseusfaturamentos["Amount"], color="blue") #selecionando as informações do gráfico e sua cor

plt.title("Categorias de produtos e seus Faturamentos") #título do gráfico
plt.xlabel("Categorias") #o que aparece na horizontal do gráfico (eixo X)
plt.ylabel("Faturamento em Dólar") #o que aparece na vertical do gráfico (eixo Y)

plt.savefig("graficocategorias.png", dpi=300) #salvando o gráfico em um arquivo png

plt.close() #fechando o gráfico pra economizar memória


plt.figure(figsize=(12, 7)) #selecionando o tamanho do gráfico

plt.bar(cidadescommaispedidos["ship-city"], cidadescommaispedidos["count"], color="steelblue") #selecionando as informações do gráfico e sua cor

plt.title("As 15 Cidades com maior quantidade de Pedidos") #título do gráfico
plt.xlabel("Cidades") #o que aparece na horizontal do gráfico (eixo X)
plt.ylabel("Quantidade de Pedidos") #o que aparece na vertical do gráfico (eixo Y)

plt.tick_params(axis="x", rotation=90) #girando a legenda horizontal pra facilitar a visualização

plt.savefig("graficoscidadespedidos.png", dpi=300) #salvando o gráfico em um arquivo png

plt.close() #fechando o gráfico pra economizar memória



plt.figure(figsize=(11, 5)) #selecionando o tamanho do gráfico
plt.plot(evoluçaofaturamentomeses["Month"], evoluçaofaturamentomeses["Amount"], marker="o") #selecionando as informações do gráfico e sua estilização

plt.title("Faturamento total ao longo dos Meses") #título do gráfico
plt.ylabel("Faturamento em Dólar") #o que aparece na horizontal do gráfico (eixo X)
plt.xlabel("Meses") #o que aparece na vertical do gráfico (eixo Y)

plt.yticks(evoluçaofaturamentomeses["Amount"], evoluçaofaturamentomeses["Amount"].apply(formatarparadolar)) #formatando o faturamento para dólares

plt.savefig("graficoevoluçaofaturamento.png", dpi=300) #salvando o gráfico em um arquivo png

plt.close() #fechando o gráfico para economizar memória



#criando o pdf

pdf = canvas.Canvas("relatoriovendasecommerce.pdf") #criando o pdf e armazenando em uma variável

pdf.drawString(10, 820, "Quanto cada Categoria Faturou em Dólares (US$)") 
pdf.drawImage("graficocategorias.png", 20, 615, width=430, height=200)

pdf.drawString(10, 600, "O Faturamento em Dólares (US$) ao longo dos Meses")
pdf.drawImage("graficoevoluçaofaturamento.png", 20, 370, width=510, height=220)  #adicionando os gráficos e seus nomes no pdf

pdf.drawString(10, 355, "As 15 Cidades com maiores quantidades de pedidos")
pdf.drawImage("graficoscidadespedidos.png", 20, 100, width=550, height=250)

pdf.save() #salvando o pdf

#enviando o email
remetente = "joaoogabryelc@gmail.com" #quem vai enviar o email
destinatario = "joaogabryelcaldeirap@gmail.com" #quem vai receber o email
assunto = "Relatório da Análise do E-commerce" #o assunto do email

corpodoemail = f"""{relatorio}""" #o conteúdo do email

senha = os.getenv("senha_email") #senha de app do Google que está guardada em um arquivo .env
anexo = "./relatoriovendasecommerce.pdf" #o arquivo que será anexado (pdf)

emailrelatorio = EmailMessage()
emailrelatorio["From"] = remetente
emailrelatorio["To"] = destinatario  #selecionando as informações do email
emailrelatorio["Subject"] = assunto
emailrelatorio.set_content(corpodoemail)

mime_type, _ = mimetypes.guess_type(anexo) #buscando o tipo principal do pdf
mime_type, mime_subtype = mime_type.split("/") #buscando o sub-tipo do pdf

with open(anexo, "rb") as arquivo:
    emailrelatorio.add_attachment(arquivo.read(),maintype=mime_type,subtype=mime_subtype,filename=anexo) #adicionando o pdf como anexo

with smtplib.SMTP_SSL("smtp.gmail.com", 465) as email:
    email.login(remetente, senha)        #logando no google usando a senha de app criada e enviando o email
    email.send_message(emailrelatorio)

print("Email Enviado!")