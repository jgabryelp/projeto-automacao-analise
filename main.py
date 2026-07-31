#importando as bibliotecas
import gdown 
import pandas as pd
import matplotlib.pyplot as plt



#baixando o arquivo da base com o request pra baixar a base de dados que eu hospedei no google drive
#link = "https://drive.google.com/file/d/1bppzawcFjqZhqvvWSeaaGkYhDGDmOFJA/view?usp=drive_link" #link de compartilhamento do arquivo (contêm o ID do arquivo necessário para fazer o download com o request)

#idarquivo = link.split("/d/")[1].split("/")[0] #selecionando o id do arquivo usando a função split, que separa uma string com base em algum separador, nesse caso "/d/" e "/"
 
#linkdownload = f"https://drive.google.com/uc?id={idarquivo}" #criando o link de donwload com o ID do arquivo

#gdown.download(linkdownload, "AmazonSaleReport.csv", quiet=False) #lendo e baixando o arquivo



#importando e lendo a base de dados
basededados = pd.read_csv("AmazonSaleReport.csv")
#print(basededados)



#analisando a base e selecionando informações importantes
def formatarparadolar(valor):
    valorformatado = f"${valor:,.2f}" #criando uma função para formatar valores numéricos em dólar
    return valorformatado
    

categoriaseseusfaturamentos = basededados[["Category", "Amount"]].groupby("Category").sum() #selecionando as colunas de categoria dos produtos e valor das vendas de cada categoria 
categoriaseseusfaturamentos = categoriaseseusfaturamentos.reset_index().sort_values("Amount", ascending=False) #tirando o index da tabela e ordenando os faturamentos do maior para o menor
categoriaseseusfaturamentos["Amount"] = categoriaseseusfaturamentos["Amount"].apply(formatarparadolar) #aplicando a formatação para dólar
#print(categoriaseseusfaturamentos)


cidadescommaispedidos = basededados["ship-city"].value_counts() #selecionando o nome das cidades e quantas vezes elas aparecem nas pedidos
cidadescommaispedidos = cidadescommaispedidos.reset_index() #transformando o value counts em uma tabela comum
cidadescommaispedidos = cidadescommaispedidos[:15] #selecionando as 15 cidades com maior quantidade de pedidos
#print(cidadescommaispedidos)


evoluçaofaturamentomeses = basededados[["Date", "Amount"]] #selecionando a coluna de datas dos pedidos e valor dos pedidos
evoluçaofaturamentomeses["Date"] = pd.to_datetime(basededados["Date"], format="%m-%d-%y") #transformando a coluna de data em um Date Object (antes era um string)
evoluçaofaturamentomeses["Month"] = evoluçaofaturamentomeses["Date"].dt.month #criando uma nova coluna para os meses
evoluçaofaturamentomeses = evoluçaofaturamentomeses[["Month", "Amount"]] #selecionando apenas a coluna dos meses e valores dos pedidos

evoluçaofaturamentomeses = evoluçaofaturamentomeses.groupby("Month").sum() #selecionando os meses sem repeti-los e seus faturamentos
evoluçaofaturamentomeses = evoluçaofaturamentomeses.reset_index() #tirando o index da tabela 

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

#evoluçaofaturamentomeses["Amount"] = evoluçaofaturamentomeses["Amount"].apply(formatarparadolar) #formatando o faturamento para dólar

#print(evoluçaofaturamentomeses)



#criando o relatório da análise
categoriaseseusfaturamentosrelatorio = ""                       #formatando as tabelas que serão escritas no relatório
for indice, linha in categoriaseseusfaturamentos.iterrows():
    categoriaseseusfaturamentosrelatorio += (f"  {linha["Category"]} -"  f" Faturou: {linha["Amount"]}\n") 

cidadescommaispedidosrelatorio = ""
for indice, linha in cidadescommaispedidos.iterrows(): 
    cidadescommaispedidosrelatorio += (f"  {linha["ship-city"]} -"  f" {linha["count"]} Pedidos\n")
                                                    
evoluçaofaturamentomesesrelatorio = ""
for indice, linha in evoluçaofaturamentomeses.iterrows():
    evoluçaofaturamentomesesrelatorio += (f"  {linha["Month"]} -"  f" ${linha["Amount"]:,.2f}\n")    


relatorio = f"""
                        ==============================
                        RELATÓRIO DE VENDAS E-COMMERCE  
                        ==============================

Prezados, segue em anexo o relatório da análise das vendas com os resultados obtidos.
    

CATEGORIAS E SEUS FATURAMENTOS:
{categoriaseseusfaturamentosrelatorio}

AS 15 CIDADES COM MAIOR QUANTIDADE DE PEDIDOS:
{cidadescommaispedidosrelatorio}

FATURAMENTO AO LONGO DOS MESES:
{evoluçaofaturamentomesesrelatorio}

"""
print(relatorio)



#criando os gráficos
plt.figure(figsize=(11, 5))

plt.bar(categoriaseseusfaturamentos["Category"], categoriaseseusfaturamentos["Amount"], color="blue")

plt.title("Categorias de produtos e seus Faturamentos")
plt.xlabel("Categorias")
plt.ylabel("Faturamento em Dólar")

plt.show()


plt.figure(figsize=(12, 7))
plt.bar(cidadescommaispedidos["ship-city"], cidadescommaispedidos["count"], color="steelblue")

plt.title("As 15 Cidades com maior quantidade de Pedidos")
plt.xlabel("Cidades")
plt.ylabel("Quantidade de Pedidos")

plt.tick_params(axis="x", rotation=90)

plt.show()


plt.figure(figsize=(11, 5))
plt.plot(evoluçaofaturamentomeses["Month"], evoluçaofaturamentomeses["Amount"], marker="o")

plt.title("Faturamento total ao longo dos Meses")
plt.ylabel("Faturamento em Dólar")
plt.xlabel("Meses")

plt.yticks(evoluçaofaturamentomeses["Amount"], evoluçaofaturamentomeses["Amount"].apply(formatarparadolar))

plt.show()