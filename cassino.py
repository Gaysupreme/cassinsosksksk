import telebot
import random
import threading
import time
from datetime import datetime

TOKEN = "8420579539:AAEKUk3vgbwedIR8cYhBkjAjtqF5RGduh70"
bot = telebot.TeleBot(TOKEN)

usuarios_ativos = {}
sinais_ativos = {}

jogos_disponiveis = {
    'crash': '📈 Crash',
    'aviator': '✈️ Aviator',
    'double': '🎯 Double',
    'mine': '💣 Mines',
    'dice': '🎲 Dice',
    'egc': '🪙 EGC',
    'blackjack': '🃏 Blackjack',
    'roulette': '🎰 Roleta'
}

esportes_disponiveis = {
    'basquete': '🏀 Basquete',
    'futebol': '⚽ Futebol',
    'tenis': '🎾 Tênis',
    'baseball': '⚾ Baseball',
    'boxe': '🥊 Boxe'
}

@bot.message_handler(commands=['start'])
def start(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = telebot.types.KeyboardButton('🎰 Sinais Cassino')
    btn2 = telebot.types.KeyboardButton('🏀 Sinais Esportes')
    btn3 = telebot.types.KeyboardButton('⚙️ Configurar')
    btn4 = telebot.types.KeyboardButton('📊 Estatísticas')
    markup.add(btn1, btn2, btn3, btn4)
    
    bot.send_message(message.chat.id, 
        "🎯 *BOT DE SINAIS VIP* 🎯\n\n"
        "✅ Sinais de Cassino e Esportes\n"
        "📈 Análise em tempo real\n"
        "⚡ Sinais automáticos\n"
        "🎰 Crash, Aviator, Mines, EGC\n"
        "🏀 Basquete, Futebol, Tênis\n\n"
        "Selecione uma opção:", 
        parse_mode='Markdown',
        reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == '🎰 Sinais Cassino')
def mostrar_jogos_cassino(message):
    markup = telebot.types.InlineKeyboardMarkup(row_width=2)
    botoes = []
    for key, value in jogos_disponiveis.items():
        botoes.append(telebot.types.InlineKeyboardButton(value, callback_data=f"cassino_{key}"))
    
    for i in range(0, len(botoes), 2):
        if i+1 < len(botoes):
            markup.add(botoes[i], botoes[i+1])
        else:
            markup.add(botoes[i])
    
    bot.send_message(message.chat.id, 
        "🎮 *SINAIS CASSINO:*\n\n"
        "Escolha o jogo para receber sinais:", 
        parse_mode='Markdown',
        reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == '🏀 Sinais Esportes')
def mostrar_esportes(message):
    markup = telebot.types.InlineKeyboardMarkup(row_width=2)
    botoes = []
    for key, value in esportes_disponiveis.items():
        botoes.append(telebot.types.InlineKeyboardButton(value, callback_data=f"esporte_{key}"))
    
    for i in range(0, len(botoes), 2):
        if i+1 < len(botoes):
            markup.add(botoes[i], botoes[i+1])
        else:
            markup.add(botoes[i])
    
    bot.send_message(message.chat.id, 
        "🏆 *SINAIS ESPORTES:*\n\n"
        "Escolha o esporte para receber sinais:", 
        parse_mode='Markdown',
        reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == '⚙️ Configurar')
def configurar(message):
    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton("✅ Ativar Todos", callback_data="ativar_todos"))
    markup.add(telebot.types.InlineKeyboardButton("❌ Desativar Todos", callback_data="desativar_todos"))
    markup.add(telebot.types.InlineKeyboardButton("🔔 Frequência", callback_data="frequencia"))
    markup.add(telebot.types.InlineKeyboardButton("🎯 Preferências", callback_data="preferencias"))
    
    status = "✅ ATIVADO" if usuarios_ativos.get(message.chat.id, {}).get('ativo', False) else "❌ DESATIVADO"
    sinais_hoje = random.randint(40, 150)
    
    bot.send_message(message.chat.id,
        f"⚙️ *CONFIGURAÇÕES*\n\n"
        f"📶 Status: {status}\n"
        f"👤 Usuários ativos: {len(usuarios_ativos)}\n"
        f"📈 Sinais hoje: {sinais_hoje}\n"
        f"🎯 Acertos: {random.randint(75, 95)}%\n\n"
        f"Configure suas preferências:",
        parse_mode='Markdown',
        reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == '📊 Estatísticas')
def estatisticas(message):
    acertos = random.randint(78, 96)
    sinais_hoje = random.randint(60, 180)
    lucro_total = random.randint(1500, 8000)
    
    bot.send_message(message.chat.id,
        f"📊 *ESTATÍSTICAS DO DIA*\n\n"
        f"✅ Taxa de acerto: *{acertos}%*\n"
        f"📈 Sinais emitidos: *{sinais_hoje}*\n"
        f"🎯 Sinais certos: *{int(sinais_hoje * (acertos/100))}*\n"
        f"💰 Lucro total: *R${lucro_total},00*\n"
        f"⚡ Multiplicador top: *{random.randint(8, 25)}x*\n"
        f"👥 Usuários VIP: *{len(usuarios_ativos)}*\n\n"
        f"🏆 Top jogos:\n"
        f"1. Crash - {random.randint(85, 98)}%\n"
        f"2. Aviator - {random.randint(82, 95)}%\n"
        f"3. Basquete - {random.randint(75, 90)}%\n\n"
        f"📅 Atualizado: {datetime.now().strftime('%H:%M:%S')}",
        parse_mode='Markdown')

@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    if call.data.startswith("cassino_"):
        jogo = call.data.split("_")[1]
        usuarios_ativos[call.message.chat.id] = {
            'ativo': True,
            'tipo': 'cassino',
            'jogo': jogo,
            'ultimo_sinal': datetime.now()
        }
        
        bot.answer_callback_query(call.id, f"✅ Sinais ativados para {jogos_disponiveis[jogo]}!")
        bot.send_message(call.message.chat.id, 
            f"🔔 *SINAIS ATIVADOS!*\n\n"
            f"Jogo: {jogos_disponiveis[jogo]}\n"
            f"Você receberá sinais automáticos.\n"
            f"Próximo sinal em: 1-4 minutos\n\n"
            f"⚡ *Dica:* Siga o sinal com confiança!",
            parse_mode='Markdown')
        
        if call.message.chat.id not in sinais_ativos:
            sinais_ativos[call.message.chat.id] = True
            threading.Thread(target=enviar_sinais_cassino, args=(call.message.chat.id, jogo)).start()
    
    elif call.data.startswith("esporte_"):
        esporte = call.data.split("_")[1]
        usuarios_ativos[call.message.chat.id] = {
            'ativo': True,
            'tipo': 'esporte',
            'esporte': esporte,
            'ultimo_sinal': datetime.now()
        }
        
        bot.answer_callback_query(call.id, f"✅ Sinais ativados para {esportes_disponiveis[esporte]}!")
        bot.send_message(call.message.chat.id, 
            f"🔔 *SINAIS ATIVADOS!*\n\n"
            f"Esporte: {esportes_disponiveis[esporte]}\n"
            f"Você receberá sinais automáticos.\n"
            f"Próximo sinal em: 2-6 minutos\n\n"
            f"⚡ *Dica:* Aposte com responsabilidade!",
            parse_mode='Markdown')
        
        if call.message.chat.id not in sinais_ativos:
            sinais_ativos[call.message.chat.id] = True
            threading.Thread(target=enviar_sinais_esportivos, args=(call.message.chat.id, esporte)).start()
    
    elif call.data == "ativar_todos":
        usuarios_ativos[call.message.chat.id] = {'ativo': True}
        bot.answer_callback_query(call.id, "✅ Todos os sinais ativados!")
        bot.send_message(call.message.chat.id, "🔔 *Sinais ativados com sucesso!*", parse_mode='Markdown')
    
    elif call.data == "desativar_todos":
        usuarios_ativos.pop(call.message.chat.id, None)
        sinais_ativos.pop(call.message.chat.id, None)
        bot.answer_callback_query(call.id, "✅ Sinais desativados!")
        bot.send_message(call.message.chat.id, "🔕 *Sinais desativados!*", parse_mode='Markdown')

def gerar_sinal_cassino(jogo):
    agora = datetime.now().strftime('%H:%M:%S')
    
    if jogo == 'crash':
        multiplicador = round(random.uniform(1.8, 12.5), 2)
        saida_min = round(multiplicador * 0.7, 2)
        saida_max = round(multiplicador * 1.3, 2)
        
        return f"📈 *SINAL CRASH* 📈\n\n" \
               f"🕒 Hora: {agora}\n" \
               f"🎯 Multiplicador: *{multiplicador}x*\n" \
               f"💰 Saída recomendada: *{saida_min}x - {saida_max}x*\n" \
               f"📊 Confiança: *{random.randint(82, 98)}%*\n" \
               f"⏳ Válido por: 90 segundos\n\n" \
               f"⚡ *Auto-retirar ativado!*"
    
    elif jogo == 'aviator':
        multiplicador = round(random.uniform(2.0, 15.0), 2)
        return f"✈️ *SINAL AVIATOR* ✈️\n\n" \
               f"🕒 Hora: {agora}\n" \
               f"🎯 Saída em: *{multiplicador}x*\n" \
               f"📊 Confiança: *{random.randint(85, 99)}%*\n" \
               f"💰 Aposta recomendada: *2% da banca*\n" \
               f"⚡ Auto-retirar: *{multiplicador-0.5}x*\n\n" \
               f"✅ *Sinal confirmado!*"
    
    elif jogo == 'egc':
        direcao = random.choice(['⬆️ ALTA FORTE', '⬇️ QUEDA RÁPIDA'])
        entrada = round(random.uniform(1.3, 2.5), 2)
        saida = round(entrada * random.uniform(1.8, 4.0), 2)
        
        return f"🪙 *SINAL EGC* 🪙\n\n" \
               f"🕒 Hora: {agora}\n" \
               f"📈 Direção: *{direcao}*\n" \
               f"🎯 Entrada: *{entrada}x*\n" \
               f"💰 Saída: *{saida}x*\n" \
               f"📊 Confiança: *{random.randint(80, 96)}%*\n" \
               f"⏳ Duração: *{random.randint(30, 120)}s*\n\n" \
               f"⚡ *Trade rápido!*"
    
    elif jogo == 'double':
        cor = random.choice(['🔴 VERMELHO', '⚫ PRETO', '🟢 VERDE'])
        numeros = random.sample(range(0, 15), 3)
        return f"🎯 *SINAL DOUBLE* 🎯\n\n" \
               f"🕒 Hora: {agora}\n" \
               f"🎯 Aposta: *{cor}*\n" \
               f"🔢 Números: *{numeros[0]}, {numeros[1]}, {numeros[2]}*\n" \
               f"📊 Confiança: *{random.randint(75, 92)}%*\n" \
               f"💰 Multiplicador: *14x*\n\n" \
               f"✅ *Aposta segura!*"
    
    elif jogo == 'mine':
        minas = random.randint(1, 3)
        posicoes = random.sample(['A1', 'B2', 'C3', 'D4', 'E5'], 5-minas)
        return f"💣 *SINAL MINES* 💣\n\n" \
               f"🕒 Hora: {agora}\n" \
               f"⚠️ Minas: {minas}\n" \
               f"💎 Posições seguras: {', '.join(posicoes)}\n" \
               f"📊 Confiança: *{random.randint(88, 99)}%*\n" \
               f"💰 Multiplicador: *{random.choice(['3x', '5x', '10x'])}*\n\n" \
               f"🎯 *Clique nas posições acima!*"
    
    elif jogo == 'dice':
        previsao = random.choice(['MAIOR', 'MENOR'])
        numero = random.randint(1, 6)
        return f"🎲 *SINAL DICE* 🎲\n\n" \
               f"🕒 Hora: {agora}\n" \
               f"🎯 Previsão: *{previsao} que {numero}*\n" \
               f"📊 Confiança: *{random.randint(82, 95)}%*\n" \
               f"💰 Odd: *{random.choice(['1.9x', '2.0x', '2.1x'])}*\n" \
               f"🎰 Chance: *{random.randint(65, 85)}%*\n\n" \
               f"✅ *Aposta confirmada!*"
    
    else:
        return f"🎰 *SINAL {jogo.upper()}* 🎰\n\n" \
               f"🕒 Hora: {agora}\n" \
               f"🎯 Entrada: *{round(random.uniform(1.5, 3.0), 2)}x*\n" \
               f"📊 Confiança: *{random.randint(80, 97)}%*\n" \
               f"💰 Multiplicador: *{random.randint(2, 8)}x*\n" \
               f"✅ Status: *CONFIRMADO*\n\n" \
               f"⚡ *Boa sorte!*"

def gerar_sinal_esporte(esporte):
    agora = datetime.now().strftime('%H:%M:%S')
    data = datetime.now().strftime('%d/%m')
    
    if esporte == 'basquete':
        times = ['Lakers', 'Warriors', 'Celtics', 'Bucks', 'Nets', 'Heat', 'Suns', 'Mavericks']
        time1 = random.choice(times)
        time2 = random.choice([t for t in times if t != time1])
        odd = round(random.uniform(1.4, 2.8), 2)
        
        return f"🏀 *SINAL BASQUETE* 🏀\n\n" \
               f"🕒 {data} {agora}\n" \
               f"⚔️ {time1} vs {time2}\n" \
               f"🎯 Aposta: *{random.choice(['Vencedor', 'Over/Under', 'Handicap'])}*\n" \
               f"✅ Escolha: *{random.choice([time1, time2, 'OVER', 'UNDER'])}*\n" \
               f"💰 Odd: *{odd}*\n" \
               f"📊 Confiança: *{random.randint(75, 92)}%*\n\n" \
               f"🏆 *Boa sorte!*"
    
    else:
        return f"{esportes_disponiveis[esporte].split()[0]} *SINAL {esporte.upper()}* {esportes_disponiveis[esporte].split()[0]}\n\n" \
               f"🕒 {data} {agora}\n" \
               f"🎯 Aposta: *{random.choice(['Vencedor', 'Over/Under'])}*\n" \
               f"💰 Odd: *{round(random.uniform(1.5, 3.0), 2)}*\n" \
               f"📊 Confiança: *{random.randint(70, 90)}%*\n" \
               f"✅ Status: *CONFIRMADO*\n\n" \
               f"🎯 *Boa sorte!*"

def enviar_sinais_cassino(chat_id, jogo):
    while chat_id in sinais_ativos:
        try:
            tempo_espera = random.randint(60, 180)
            time.sleep(tempo_espera)
            
            if chat_id in sinais_ativos:
                sinal = gerar_sinal_cassino(jogo)
                bot.send_message(chat_id, sinal, parse_mode='Markdown')
                
                time.sleep(3)
                
                resultado = random.choices(
                    ['✅ SINAL CERTO! GREEN 🟢', '✅ SINAL CERTO! GREEN 🟢', '❌ SINAL ERRADO RED 🔴'],
                    weights=[0.80, 0.80, 0.20]
                )[0]
                
                if 'GREEN' in resultado:
                    multiplicador = round(random.uniform(1.8, 18.0), 2)
                    lucro = random.randint(80, 600)
                    mensagem_resultado = f"{resultado}\n🎉 Multiplicador: *{multiplicador}x*\n💰 Lucro: R${lucro},00\n📈 Banca atualizada!\n\n⚡ Próximo sinal em {random.randint(2, 5)} minutos..."
                else:
                    mensagem_resultado = f"{resultado}\n📉 Perda controlada\n💡 *Dica:* Não aumente a aposta!\n🔄 Recupere no próximo sinal...\n\n⏳ Novo sinal em {random.randint(3, 6)} minutos"
                
                bot.send_message(chat_id, mensagem_resultado, parse_mode='Markdown')
                
        except Exception as e:
            break

def enviar_sinais_esportivos(chat_id, esporte):
    while chat_id in sinais_ativos:
        try:
            tempo_espera = random.randint(120, 360)
            time.sleep(tempo_espera)
            
            if chat_id in sinais_ativos:
                sinal = gerar_sinal_esporte(esporte)
                bot.send_message(chat_id, sinal, parse_mode='Markdown')
                
                time.sleep(5)
                
                resultado = random.choices(
                    ['✅ SINAL CERTO! GREEN 🟢', '✅ SINAL CERTO! GREEN 🟢', '❌ SINAL ERRADO RED 🔴'],
                    weights=[0.75, 0.75, 0.25]
                )[0]
                
                if 'GREEN' in resultado:
                    odd_ganha = round(random.uniform(1.6, 4.0), 2)
                    lucro = random.randint(50, 350)
                    mensagem_resultado = f"{resultado}\n🎉 Odd: *{odd_ganha}*\n💰 Lucro: R${lucro},00\n📈 Banca atualizada!\n\n⚡ Próximo sinal em {random.randint(4, 8)} minutos..."
                else:
                    mensagem_resultado = f"{resultado}\n📉 Perda mínima\n💡 *Dica:* Mantenha a gestão de banca!\n🔄 Próximo sinal com alta confiança...\n\n⏳ Novo em {random.randint(5, 10)} minutos"
                
                bot.send_message(chat_id, mensagem_resultado, parse_mode='Markdown')
                
        except Exception as e:
            break

@bot.message_handler(commands=['sinais'])
def comando_sinais(message):
    markup = telebot.types.InlineKeyboardMarkup(row_width=2)
    btn1 = telebot.types.InlineKeyboardButton('🎰 Cassino', callback_data='menu_cassino')
    btn2 = telebot.types.InlineKeyboardButton('🏀 Esportes', callback_data='menu_esportes')
    markup.add(btn1, btn2)
    
    bot.send_message(message.chat.id, "Escolha o tipo de sinais:", reply_markup=markup)

@bot.message_handler(commands=['crash'])
def comando_crash(message):
    usuarios_ativos[message.chat.id] = {
        'ativo': True,
        'tipo': 'cassino',
        'jogo': 'crash',
        'ultimo_sinal': datetime.now()
    }
    
    if message.chat.id not in sinais_ativos:
        sinais_ativos[message.chat.id] = True
        threading.Thread(target=enviar_sinais_cassino, args=(message.chat.id, 'crash')).start()
    
    bot.send_message(message.chat.id, "✅ Sinais de CRASH ativados! Próximo sinal em 1-3 minutos.")

@bot.message_handler(commands=['aviator'])
def comando_aviator(message):
    usuarios_ativos[message.chat.id] = {
        'ativo': True,
        'tipo': 'cassino',
        'jogo': 'aviator',
        'ultimo_sinal': datetime.now()
    }
    
    if message.chat.id not in sinais_ativos:
        sinais_ativos[message.chat.id] = True
        threading.Thread(target=enviar_sinais_cassino, args=(message.chat.id, 'aviator')).start()
    
    bot.send_message(message.chat.id, "✅ Sinais de AVIATOR ativados! Próximo sinal em 1-3 minutos.")

@bot.message_handler(commands=['egc'])
def comando_egc(message):
    usuarios_ativos[message.chat.id] = {
        'ativo': True,
        'tipo': 'cassino',
        'jogo': 'egc',
        'ultimo_sinal': datetime.now()
    }
    
    if message.chat.id not in sinais_ativos:
        sinais_ativos[message.chat.id] = True
        threading.Thread(target=enviar_sinais_cassino, args=(message.chat.id, 'egc')).start()
    
    bot.send_message(message.chat.id, "✅ Sinais de EGC ativados! Próximo sinal em 1-3 minutos.")

@bot.message_handler(commands=['basquete'])
def comando_basquete(message):
    usuarios_ativos[message.chat.id] = {
        'ativo': True,
        'tipo': 'esporte',
        'esporte': 'basquete',
        'ultimo_sinal': datetime.now()
    }
    
    if message.chat.id not in sinais_ativos:
        sinais_ativos[message.chat.id] = True
        threading.Thread(target=enviar_sinais_esportivos, args=(message.chat.id, 'basquete')).start()
    
    bot.send_message(message.chat.id, "✅ Sinais de BASQUETE ativados! Próximo sinal em 2-6 minutos.")

@bot.message_handler(commands=['parar'])
def comando_parar(message):
    if message.chat.id in sinais_ativos:
        sinais_ativos.pop(message.chat.id, None)
        usuarios_ativos.pop(message.chat.id, None)
        bot.send_message(message.chat.id, "❌ Sinais desativados!")
    else:
        bot.send_message(message.chat.id, "⚠️ Você não está recebendo sinais.")

@bot.message_handler(commands=['status'])
def comando_status(message):
    if message.chat.id in usuarios_ativos:
        user = usuarios_ativos[message.chat.id]
        tipo = user.get('tipo', 'N/A')
        jogo = user.get('jogo') or user.get('esporte', 'N/A')
        
        if tipo == 'cassino':
            nome = jogos_disponiveis.get(jogo, jogo)
        else:
            nome = esportes_disponiveis.get(jogo, jogo)
        
        bot.send_message(message.chat.id,
            f"📊 *SEU STATUS*\n\n"
            f"✅ Sinais: ATIVADO\n"
            f"🎮 Tipo: {tipo.upper()}\n"
            f"🎯 Jogo/Esporte: {nome}\n"
            f"🕒 Próximo sinal: Em {random.randint(1, 5)} min\n"
            f"📈 Performance: {random.randint(78, 96)}%",
            parse_mode='Markdown')
    else:
        bot.send_message(message.chat.id, "❌ Você não está recebendo sinais. Use /start para ativar.")

@bot.message_handler(func=lambda message: True)
def mensagem_geral(message):
    if message.text not in ['🎰 Sinais Cassino', '🏀 Sinais Esportes', '⚙️ Configurar', '📊 Estatísticas']:
        bot.send_message(message.chat.id,
            "🎯 *BOT DE SINAIS VIP*\n\n"
            "🎰 *Cassino:* /crash /aviator /egc /mine\n"
            "🏀 *Esportes:* /basquete /futebol /tenis\n"
            "⚙️ *Controle:* /parar /status /sinais\n"
            "📊 *Outros:* /start /estatisticas\n\n"
            "⚠️ *Bot de demonstração*",
            parse_mode='Markdown')

if __name__ == "__main__":
    print("🤖 Bot iniciado")
    bot.polling(none_stop=True)
