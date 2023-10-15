import telebot
from docxtpl import DocxTemplate
from docx2pdf import convert

doc = DocxTemplate('bots\official_file.docx')
bot = telebot.TeleBot('6413252125:AAEYB4Qw0GltfdKBGBfGhemN4WqRFqn_Qiw')

@bot.message_handler(commands=['start'])
def first_text(message):
    m = bot.send_message(message.from_user.id, "Введите имя")
    bot.register_next_step_handler(m, second_text)

def second_text(m):
  name = m.text
  print(name)
  second_name = bot.send_message(m.from_user.id, "Введите фамилию")
  bot.register_next_step_handler(second_name, third_text, name)

def third_text(second_name, name):
  phone_num = bot.send_message(second_name.from_user.id, 'Введите номер телефона')
  bot.register_next_step_handler(phone_num, fourth_text, name, second_name)

def fourth_text(phone_num, name, second_name):
  special = bot.send_message(phone_num.from_user.id, 'Введите свою специальность')
  bot.register_next_step_handler(special, five_text, phone_num, name, second_name)

def five_text(specical,phone_num, name, second_name):
  j_t = bot.send_message(specical.from_user.id, 'Введите Опыт Работы')
  bot.register_next_step_handler(j_t, six_text, specical,phone_num, name, second_name)

def six_text(j_t,specical,phone_num, name, second_name):
  job_time = j_t.text
  specialnost = specical.text
  number = phone_num.text
  n = name
  s_n = second_name.text
  context = {"name" : n, 
             "s_n" : s_n, 
             "num" : number, 
             "spec" : specialnost, 
             "job_time" : job_time
             }
  print(context)
  doc.render(context)
  doc.save("final.docx")
  bot.send_message(j_t.from_user.id, 'Ожидайте PDF файл...')
  
#отправка pdf
  uis_pdf = open("final.docx", 'rb')
  bot.send_document(j_t.chat.id, uis_pdf)
  uis_pdf.close()


bot.polling()