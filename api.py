import requests
import json
from datetime import datetime, timedelta

urlBD = ""


def cria_pergunta(pergunta, resposta):
  #cria um dicionário com a pergunta e a resposta
  dicionario_pergunta = {'pergunta': pergunta, 'resposta': resposta}

  #transforma o dicionário em json
  json_pergunta = json.dumps(dicionario_pergunta)

  #faz a requisição do tipo post na api
  requisicao = requests.post(f'{urlBD}/perguntas/.json', data = json_pergunta)

  #verifica se a requisição foi bem sucedida (200)
  return(requisicao.status_code == 200)

def edita_pergunta(id, pergunta='pergunta padrao', resposta='resposta padrao'):

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
  
  dicionario_presenca = {data: 1}

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


def add_id(aluno_id, id):
      
  dicionario_frequencia = {"id": id}

  #transforma o dicionário em json  
  json_freq = json.dumps(dicionario_frequencia)

  #faz a requisição do tipo post na api
  requisicao = requests.patch(f'{urlBD}/alunos/{aluno_id}/.json', data = json_freq)


def comparar_id(matricula):
  requisicao = le_alunos()

  matricula = int(matricula)

  for id in requisicao.json():
    if matricula == requisicao.json()[id]["matricula"]:
      return(requisicao.json()[id]["matricula"])


def get_id(matricula):
  requisicao = le_alunos()

  id_d = str(matricula)

  for id in requisicao.json():
    if id_d == requisicao.json()[id]['id']:
      return(requisicao.json()[id]["matricula"])

def reset_id(aluno_id):
      
  dicionario_frequencia = {"id": 0}

  #transforma o dicionário em json  
  json_freq = json.dumps(dicionario_frequencia)

  #faz a requisição do tipo post na api
  requisicao = requests.patch(f'{urlBD}/alunos/{aluno_id}/.json', data = json_freq)

def get_turma(matricula):
  requisicao = le_alunos()

  matricula = int(matricula)

  for id in requisicao.json():
    if matricula == requisicao.json()[id]["matricula"]:
      return(requisicao.json()[id]["turma"])
    
    
def add_resposta(aluno_id, n_teste, resposta):
      
  dicionario_miniteste = {str(n_teste): resposta}

  #transforma o dicionário em json  
  json_teste = json.dumps(dicionario_miniteste)

  #faz a requisição do tipo post na api
  requisicao = requests.patch(f'{urlBD}/alunos/{aluno_id}/miniteste/.json', data = json_teste)



def cria_aluno(nome, matricula, turma, id):
  
      
  matricula = int(matricula)
  dicionario_pergunta = {'nome': nome, 'matricula': matricula, 'turma': turma, 'id': id}

  #transforma o dicionário em json
  json_pergunta = json.dumps(dicionario_pergunta)

  #faz a requisição do tipo post na api
  requisicao = requests.post(f'{urlBD}/alunos/.json', data = json_pergunta)

  #verifica se a requisição foi bem sucedida (200)
  return(requisicao.status_code == 200)


def le_logs():
      #le perguntas
  requisicao = requests.get(f'{urlBD}/logs/.json')
  
  return(requisicao)


def deleta_logs(id):
      #deleta a pergunta com o id correspondente
  requisicao = requests.delete(f'{urlBD}/logs/{id}/.json')

  #verifica se a requisição foi bem sucedida (200)
  return(requisicao.status_code == 200)

def get_log(log):
  requisicao = le_logs()

  logs = str(log)

  for id in requisicao.json():
    if logs == requisicao.json()[id]['log']:
      return(id)

def get_teste(teste):
    
  requisicao = requests.get(f'{urlBD}/minitestes/.json')
  
  teste = "T"+teste
  
  for id in requisicao.json():
    if teste == requisicao.json()[id]["teste"]:
      return(requisicao.json()[id])
    
  return(None)

def le_permissao():
      #le perguntas
  requisicao = requests.get(f'{urlBD}/permissao/.json')
  
  return(requisicao)


def cria_permissao(nome, cargo, id):
    
  dicionario_pergunta = {'nome': nome, 'cargo': cargo, 'id': str(id)}

  #transforma o dicionário em json
  json_pergunta = json.dumps(dicionario_pergunta)

  #faz a requisição do tipo post na api
  requisicao = requests.post(f'{urlBD}/permissao/.json', data = json_pergunta)

  #verifica se a requisição foi bem sucedida (200)
  return(requisicao.status_code == 200)

def verificar_permissao(id_p):
  requisicao = le_permissao()

  id = str(id_p)

  for id in requisicao.json():
    if id_p == requisicao.json()[id]["id"]:
      return(requisicao.json()[id]["id"])
    
def get_frequencia():
      
  requisicao = le_alunos()

  #print(requisicao.json())
  dicionario_frequencia = {}

  for id in requisicao.json():
    #adiciona um aluno e sua frequência no dicionário
    if('frequencia' in requisicao.json()[id]):
      dicionario_frequencia[requisicao.json()[id]["matricula"]] = requisicao.json()[id]["frequencia"]
    else:
      dicionario_frequencia[requisicao.json()[id]["matricula"]] = {}
  
  return(dicionario_frequencia)
