# Configuração mongodb
Este repositório contém uma lista detalhada e organizada dos comandos Docker e MongoCompass, explicando suas funções de forma simplificada. <br>


# 🐋 Comandos Docker:

```bash
## Iniciar uma network na docker.
docker network create mongoCluster

## Criação dos nós.
docker run -d -p 27017:27017 --name mongo1 --network mongoCluster mongodb/mongodb-community-server:latest --replSet myReplicaSet --bind_ip localhost,mongo1

docker run -d  -p 27018:27017 --name mongo2 --network mongoCluster mongodb/mongodb-community-server:latest --replSet myReplicaSet --bind_ip localhost,mongo2

docker run -d  -p 27019:27017 --name mongo3 --network mongoCluster mongodb/mongodb-community-server:latest --replSet myReplicaSet --bind_ip localhost,mongo3

docker run -d  -p 27020:27017 --name mongo4 --network mongoCluster mongodb/mongodb-community-server:latest --replSet myReplicaSet --bind_ip localhost,mongo4

## Inicia o Mongo Shell dentro do Docker.
docker exec -it mongo1 mongosh

##Salvamos a conexão no retorno do comando acima.
Connection_to: mongodb://127.0.0.1:27020/?directConnection=true&serverSelectionTimeoutMS=2000&appName=mongosh+2.4.2

## Valida funciomento do container.
db.runCommand({hello:1})

## Inicia o sistema de reduncia contra falhas.
rs.initiate ({ _id: "myReplicaSet", members:[{_id:0, host: "mongo1"}, {_id:1, host: "mongo2"}, {_id:3, host: "mongo3"}, {_id:4, host: "mongo4"}]})

## Sair do Shell.
exit

## Exibe o status do myReplicaSet.
docker exec -it mongo1 mongosh --eval "rs.status()"

##Após estes comandos a conexão será estabelecida através do mongoCompass
```

# 🍃MongoCompass

```bash
## Clique em Add New Connection.

##No campo 'new connection' insira a conexão que foi salva anteriormente
mongodb://127.0.0.1:27020/?directConnection=true&serverSelectionTimeoutMS=2000&appName=mongosh+2.4.2

## Clique em >_ para abrir o terminal.

```

# 🔄 Inserindo dados:

```bash
## No terminal do nó primario.
##Este comando especifica qual base será utilizada.
use Sistema

## Insere vários usuarios ao mesmo tempo.
db.cliente.insertMany([{"first_name":"Adrianne","last_name":"Fulton","email":"afulton0@un.org"},
{"first_name":"Birgit","last_name":"Tuke","email":"btuke1@surveymonkey.com"}])

##Utilizamos o https://www.mockaroo.com/ para gerar os dados utilizados.

##Consultar se os dados foram inseridos.
db.cliente.find()

##Consulta através de um filtro.
db.cliente.findOne()

##Os comandos devem retornar os dados existentes e/ou o dado filtrado.

```


# 🌍 Trabalhando com queda de um nó secundario

```bash
## Volte no docker para derubar um dos nós.
docker stop 'nome do container'

## Volte ao Mongo Compass
db.cliente.insertOne({"first_name":"Cleiton","last_name":"Rasta","email":"cabecadegelo@gmail.com"})

## Abre o terminal de um nó secundario e valide a replicação dos dados
db.cliente.findOne({last_name:"Rasta"})
```

# 🌍 Trabalhando com queda do nó primario

```bash
## Volte no docker para derubar o nó primario(vamos considerar mongo4).
docker stop mongo4

##Valide qual nó assumiu a posição de primario.
docker exec -it mongo1 mongosh --eval "rs.status()"

## Voltamos ao Mongo Compass e acessamos a conexão que foi exibida como 'PRIMARY'

##Realizamos uma inserção de teste
db.cliente.insertOne({"first_name":"Alessandro","last_name":"Jose","email":"alessandro.jose@gmail.com"})

## Abre o terminal de um nó secundario e valide a replicação dos dados
db.cliente.findOne({last_name:"Jose"})
```

# 🐍 Logs de alteração em python

```bash
##Abrimos um prompt de comando/terminal

##Instala a biblioteca necessaria para o funcionamento
pip install pymongo

##Executa o arquivo(caminho exemplo)
python C:\Users\Exemplo\Documents\FunctionMongo.py

##Com isso quando uma alteração for realizada no Mongo Compass
##ela será exibida no prompt de comando.
[2025-03-29 14:59:15] Operação: n | Banco:  | Dados: {'msg': 'periodic noop'}
[2025-03-29 14:59:17] Operação: i | Banco: Sistema.cliente | Dados: {'_id': ObjectId('67e834f5e29d44b98cf059c3'), 'first_name': 'Alessandro', 'last_name': 'Jose', 'email': 'alessandro.jose@gmail.com'}
[2025-03-29 14:59:35] Operação: n | Banco:  | Dados: {'msg': 'periodic noop'}

##Mostramos detalhes como operação (i para insert, u para update, d para delete), banco/coleção, dados alterados, e timestamp.
Operação: i | Banco: Sistema.cliente | Dados: {'_id': ObjectId('67e834a2e29d44b98cf059c2'), 'first_name': 'Alessandro', 'last_name': 'Jose', 'email': 'alessandro.jose@gmail.com'}

```
