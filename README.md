# 🤖 Automação de Análise de dados, Relatório e envio de Email
### Sobre o projeto:
Uma automação em Python que baixa uma base de dados com informações das vendas de um E-commerce, analisa os dados da base, gera gráficos das análises e um relatório com informações úteis que é enviado por email.
Base de dados utilizada: [E-Commerce Sales Dataset Kaggle](https://www.kaggle.com/datasets/thedevastator/unlock-profits-with-e-commerce-sales-data)
<br/>

## 💻 Funcionalidades do Projeto:
- Download automático da base de dados hospedada em um link do google drive
- Trata e analisa a base de dados 
- O Faturamento de cada categoria de produtos
- As Cidades com maior quantidade de pedidos
- O Faturamento ao longo dos meses
- Relatório com as informações obtidas
- Criação e download de gráficos das análises
- Criação de um arquivo PDF contendo os gráficos das análises
- Envio do relatório e pdf dos gráficos por email


## 🛠️ Tecnologias Utilizadas:
- Python
- Pandas
- gdown
- Matplotlib
- Reportlab
- smtplib


## 🗃️ Gráficos e Email enviados:
![image alt](https://github.com/jgabryelp/projeto-automacao-analise/blob/main/emailenviadoprojetoautomacao.png)
![image alt](https://github.com/jgabryelp/projeto-automacao-analise/blob/main/graficospdfautomacao.png)


## 🚀 Como Executar o Projeto:
1 - crie um arquivo de texto com o nome ".env" 
<br/>
2 - crie uma senha de aplicativo do google [aqui](https://myaccount.google.com/apppasswords)
<br/>
3 - esse arquivo deve ter o seguinte conteúdo: senha_email=sua_senha_de_app_do_google
<br/>
exemplo: [arquivo.env exemplo](https://github.com/jgabryelp/projeto-automacao-analise/blob/main/exemplo.env)
<br/>
4 - o arquivo .env deve estar na mesma pasta do arquivo main.py (código do projeto)


## 📝 Autor:
João Gabryel Caldeira: 
<br/>
Email - joaogabryelcaldeirap@gmail.com
<br/>
LinkedIn - [João Gabryel](https://www.linkedin.com/in/jo%C3%A3o-gabryelc/)
<br/>
