

## Relatório

### Aluno

- nome: Anderson Henrique Silva Santos 
- matrícula: 20232014040014  

### Relato

**Introdução**

Neste relatório, documentei a configuração e implementação de um ambiente conteinerizado para um projeto Django, utilizando Docker e PostgreSQL. A atividade envolveu a criação de um Dockerfile para o projeto, um docker-compose.yml para gerenciar os serviços e ajustes na configuração do Django para utilizar o banco de dados PostgreSQL em um container.

**Etapas Realizadas**

Criei um Dockerfile para a aplicação Django, utilizando Python 3.10 e o Gunicorn como servidor de aplicação. O arquivo realiza as seguintes ações: define o diretório de trabalho como /app, copia o requirements.txt e instala as dependências, copia os arquivos do projeto para dentro do container e define o comando de inicialização com Gunicorn.
Criei um arquivo docker-compose.yml para gerenciar dois serviços: Web (Django), que usa a imagem do Dockerfile e roda o servidor Gunicorn, e DB (PostgreSQL), que usa a imagem oficial do PostgreSQL, configurada com variáveis de ambiente para o banco de dados. O arquivo também define volumes para persistência de dados e um .env para armazenar credenciais sensíveis.
Atualizei o settings.py do Django para utilizar o banco de dados PostgreSQL, lendo as credenciais do arquivo .env. A configuração usa ENGINE: django.db.backends.postgresql, NAME, USER, PASSWORD definidos via variáveis de ambiente, HOST: db (nome do serviço no docker-compose.yml) e PORT: 5432.
Para testar e validar a configuração, criei os containers com o comando docker-compose up --build, executei migrações para garantir a conexão do banco com docker-compose exec web python manage.py migrate, criei um superusuário e acessei o Django Admin, além de testar a aplicação em um navegador (localhost:8000).

**Conclusão**

A atividade demonstrou a conteinerização eficiente de um projeto Django com PostgreSQL, garantindo portabilidade e facilidade de configuração. O uso de Docker simplifica a implantação e o gerenciamento do ambiente de desenvolvimento.

### Arquivos docker e de configuração do django

