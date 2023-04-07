import requests
import json

urlBD = "https://ave-bot-2d2d3-default-rtdb.firebaseio.com/"


def cria_pergunta(pergunta, resposta):
  """
  pergunta: String
  resposta: String

  Armazena uma pergunta e sua resposta na api. 
  Retorna um booleano indicando se a operação foi bem sucedida ou não.
  """
  #cria um dicionário com a pergunta e a resposta
  dicionario_pergunta = {'pergunta': pergunta, 'resposta': resposta}

  #transforma o dicionário em json
  json_pergunta = json.dumps(dicionario_pergunta)

  #faz a requisição do tipo post na api
  requisicao = requests.post(f'{urlBD}/perguntas/.json', data = json_pergunta)

  #verifica se a requisição foi bem sucedida (200)
  return(requisicao.status_code == 200)

def edita_pergunta(id, pergunta='pergunta padrao', resposta='resposta padrao'):
  """
  id: String
  pergunta: String
  resposta: String

  Recebe o id de uma das perguntas da api e altera sua pergunta, sua resposta ou ambos.
  Retorna um booleano indicando se a operação foi bem sucedida ou não.
  """
  #edita apenas a resposta
  #cria um dicionário com a resposta
  if(pergunta == 'pergunta padrao'): dicionario_pergunta = {'resposta': resposta}
  #edita apenas a pergunta
  #cria um dicionário com a pergunta
  elif(resposta == 'resposta padrao'): dicionario_pergunta = {'pergunta': pergunta} 
  #edita a pergunta e a resposta
  #cria um dicionário com a pergunta e a resposta
  else: dicionario_pergunta = {'pergunta': pergunta, 'resposta': resposta}

  #transforma o dicionário em json  
  json_pergunta = json.dumps(dicionario_pergunta)
  #faz a requisição do tipo patch na api
  requisicao = requests.patch(f'{urlBD}/perguntas/{id}/.json', data = json_pergunta)

  #verifica se a requisição foi bem sucedida (200)
  return(requisicao.status_code == 200)

def deleta_pergunta(id):
  #deleta a pergunta com o id correspondente
  requisicao = requests.delete(f'{urlBD}/perguntas/{id}/.json')

  #verifica se a requisição foi bem sucedida (200)
  return(requisicao.status_code == 200)

def le_perguntas():
  #le perguntas
  requisicao = requests.get(f'{urlBD}/perguntas/.json')
  
  return(requisicao)

def get_pergunta_id(pergunta):
  requisicao = le_perguntas()

  for id in requisicao.json():
    if pergunta == requisicao.json()[id]['pergunta']:
      return(id)


def le_alunos():
  #le perguntas
  requisicao = requests.get(f'{urlBD}/alunos/.json')
  
  return(requisicao)

def get_aluno_id(matricula):
  requisicao = le_alunos()

  matricula = int(matricula)

  for id in requisicao.json():
    if matricula == requisicao.json()[id]['matricula']:
      return(id)

def set_presenca(data, aluno_id):
  
  dicionario_presenca = {data: True}

  #transforma o dicionário em json  
  json_presenca = json.dumps(dicionario_presenca)

  #faz a requisição do tipo post na api
  requisicao = requests.patch(f'{urlBD}/alunos/{aluno_id}/frequencia/.json', data = json_presenca)

def get_nome(matricula):
  requisicao = le_alunos()

  matricula = int(matricula)

  for id in requisicao.json():
    if matricula == requisicao.json()[id]["matricula"]:
      return(requisicao.json()[id]["nome"])
