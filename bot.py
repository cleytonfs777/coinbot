import json
import os
import sqlite3
from asyncio import run

from django.core import serializers
from dotenv import load_dotenv
from pyrogram import Client, filters
from pyrogram.session import Session
from pyrogram.types import (InlineKeyboardButton, InlineKeyboardMarkup,
                            Message, ReplyKeyboardMarkup)

load_dotenv()

caminho_banco = os.path.join(os.getcwd(),'db.sqlite3')

# INICIO OPERAÇÕES COM BANCO DE DADOS

def inserir_dado(p, prec, tipo, quantidade):
    # Cria a conexão com o banco de dados
    conn = sqlite3.connect(caminho_banco)

    # Insere um registro na tabela
    conn.execute(f"INSERT INTO telegramapp_coin (par, preco, tipo, qtd) VALUES ('{p}', '{prec}', '{tipo}', '{quantidade}')")

    # Salva as alterações
    conn.commit()

    # Fecha a conexão
    conn.close()

def todo_banco():
    conn = sqlite3.connect(caminho_banco)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM telegramapp_coin')
    registros = cursor.fetchall()
    cursor.close()
    conn.close()
    return registros

def atualiza_dado(id, par):

    # Cria a conexão com o banco de dados
    conn = sqlite3.connect(caminho_banco)

    # Atualiza o registro com id=1
    conn.execute(f"UPDATE telegramapp_coin SET par='{par}' WHERE id={id}")

    # Salva as alterações
    conn.commit()

    # Fecha a conexão
    conn.close()

def apagar_dado(id):
    # Cria a conexão com o banco de dados
    conn = sqlite3.connect(caminho_banco)

    # Apaga o usuário com id=1
    conn.execute(f"DELETE FROM telegramapp_coin WHERE id={id}")

    # Salva as alterações
    conn.commit()

    # Fecha a conexão
    conn.close()


# FIM OPERAÇÕES COM BANCO DE DADOS

# Crie uma classe personalizada que herda de pyrogram.Client
class MyClient(Client):
    def __init__(self):
        # Inicialize o objeto Client e defina a variável de sessão
        super().__init__(
            "ParlamentarCBMMGBot",
            api_id=os.getenv('TELEGRAM_API_ID'),
            api_hash=os.getenv('TELEGRAM_API_HASH'),
            bot_token=os.getenv('TELEGRAM_BOT_TOKEN'),
            )
        self.user_data = {}

    # Adicione um método para atualizar a variável de sessão com os dados do usuário
    def update_user_data(self, user_id, data):
        self.user_data[user_id] = data

    # Adicione um método para recuperar os dados do usuário da variável de sessão
    def get_user_data(self, user_id):
        return self.user_data.get(user_id, None)

# Crie o aplicativo
app = MyClient()

# O aplicativo captura o comando dado ao bot escolhido e oferece um texto baseado na requisição
@app.on_message(filters.command('start'))
async def inicio(Client, message):
    teclado = ReplyKeyboardMarkup(
        [
            ['Add Par', 'Meus Pares', 'Remover Par']
        ],resize_keyboard=True
    )
    await message.reply(
        '🤖 Seja Bem vindo ao Bot OB! Escolha uma das opções 🤖 ',reply_markup=teclado
    )


# O vai fazer o cadastro do parlamentar
@app.on_message(filters.regex("Add Par"))
async def cadastrar(Client, message):
    botoes = InlineKeyboardMarkup (
        [
            [
                InlineKeyboardButton('Digital', callback_data='D'),
                InlineKeyboardButton('Binario', callback_data='B'),
            ]
        ]
    )
    print(dir(InlineKeyboardMarkup))
    await message.reply('Muito bem. Escolha o tipo de moeda a cadastrar: ', reply_markup=botoes)

@app.on_callback_query()
async def callback(clinet, callback_query):
    if callback_query.data == 'D':
        await app.send_message(callback_query.message.chat.id,f'Vamos cadastrar a moeda Digital')
        await app.send_message(callback_query.message.chat.id,f'Por favor indique qual par de moeda a escolher sem utilizar barras ("Ex:. EURUSD")')
        if app.get_user_data(callback_query.message.chat.id) == None:
            app.update_user_data(callback_query.message.chat.id, {"tipo": "Digital", "par": "", "preco": "",  "qtd": ""})
        user_data = app.get_user_data(callback_query.message.chat.id)
        user_data['tipo'] = "Digital"
        app.update_user_data(callback_query.message.chat.id, user_data)

    if callback_query.data == 'B':
        await app.send_message(callback_query.message.chat.id,f'Vamos cadastrar a moeda Binária')
        await app.send_message(callback_query.message.chat.id,f'Por favor indique qual par de moeda a escolher sem utilizar barras ("Ex:. EURUSD")')
        if app.get_user_data(callback_query.message.chat.id) == None:
            app.update_user_data(callback_query.message.chat.id, {"tipo": "", "par": "", "preco": "",  "qtd": ""})
        user_data = app.get_user_data(callback_query.message.chat.id)
        user_data['tipo'] = "Binária"
        app.update_user_data(callback_query.message.chat.id, user_data)

@app.on_message()
async def messages(Client, message):
    await message.reply("Processando solicitação")
    namedep = await app.get_messages(message.chat.id, message.id-1)
    namedep2 = await app.get_messages(message.chat.id, message.id)
    if namedep.text == 'Por favor indique qual par de moeda a escolher sem utilizar barras ("Ex:. EURUSD")':
        
        # SETANDO O PAR DE MOEDAS
        if app.get_user_data(message.chat.id) == None:
            app.update_user_data(message.chat.id, {"tipo": "", "par": "", "preco": "",  "qtd": ""})
        user_data = app.get_user_data(message.chat.id)
        user_data['par'] = namedep2.text
        app.update_user_data(message.chat.id, user_data)
        # FIM SET PAR DE MOEDAS
        print(namedep.text)
        print(namedep2.text)
        await app.send_message(message.chat.id,f"Moeda cadastrada com sucesso 😀")
        await app.send_message(message.chat.id,f"Indique o preço da moeda oferdada 💸")
    elif namedep.text == 'Indique o preço da moeda oferdada 💸':
        # SETANDO O PRECO DE MOEDAS
        if app.get_user_data(message.chat.id) == None:
            app.update_user_data(message.chat.id, {"tipo": "", "par": "", "preco": "",  "qtd": ""})
        user_data = app.get_user_data(message.chat.id)
        user_data['preco'] = namedep2.text
        app.update_user_data(message.chat.id, user_data)
        # FIM SET PRECO DE MOEDAS
        print(namedep.text)
        print(namedep2.text)
        await app.send_message(message.chat.id,f"Perfeitamente....Registro e preço anotado")
        await app.send_message(message.chat.id,f"Agora, para finalizar, me informe quantas moedas vc tem ⚖")
    elif namedep.text == 'Agora, para finalizar, me informe quantas moedas vc tem ⚖':
        # SETANDO O PRECO DE MOEDAS
        if app.get_user_data(message.chat.id) == None:
            app.update_user_data(message.chat.id, {"tipo": "", "par": "", "preco": "",  "qtd": ""})
        user_data = app.get_user_data(message.chat.id)
        user_data['qtd'] = namedep2.text
        app.update_user_data(message.chat.id, user_data)
        # FIM SET PRECO DE MOEDAS
        print(namedep.text)
        print(namedep2.text)
        await app.send_message(message.chat.id,f"Cadastro realizado com sucesso")
        inserir_dado(user_data['par'], user_data['preco'], user_data['tipo'], user_data['qtd'])
        print((f"Par: {user_data['par']}, Preço: {user_data['preco']}, Tipo: {user_data['tipo']}, Quantidade: {user_data['qtd']}"))

    else:
        if app.get_user_data(message.chat.id) == None:
            app.update_user_data(message.chat.id, {"tipo": "Digital", "par": "", "preco": "",  "qtd": ""})

        await app.send_message(message.chat.id,f"Desculpe. Não entendi seu comando")
        await app.send_message(message.chat.id,f"Digite /start e escolha uma das opções")
        # user_data = app.get_user_data(message.chat.id)
        # await app.send_message(message.chat.id,f"{user_data}")
        # user_data['age'] += 1
        # app.update_user_data(message.chat.id, user_data)
        print(todo_banco())

        
    
app.run()

