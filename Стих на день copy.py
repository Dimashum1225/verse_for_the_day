#устанавливаем библиотеки
from bs4 import BeautifulSoup#для парсинга
import requests
import re
from datetime import datetime#для определения времени
import tkinter as tk
import os
from tkinter import font as tkfont
import sys

# Создание пользовательского виджета label для возможности использовать атрибут wrap=word 
class WordWrapLabel(tk.Label):
    def __init__(self, master=None, **kwargs):
        tk.Label.__init__(self, master, **kwargs)
        self.bind('<Configure>', self._wrap_text)

    def _wrap_text(self, event=None):
        wrap_length = self.winfo_width()
        text = self['text']
        self['text'] = self._wrap_by_word(text, wrap_length)

    def _wrap_by_word(self, text, wrap_length):
        lines = []
        line = []
        for word in text.split():
            if self._get_text_width(' '.join(line + [word])) <= wrap_length:
                line.append(word)
            else:
                lines.append(' '.join(line))
                line = [word]
        lines.append(' '.join(line))
        return '\n'.join(lines)

    def _get_text_width(self, text):
        font = tkfont.Font(font=self['font'])
        return font.measure(text)


#сразу устанавливаем некоторые значения
now=datetime.now()
now_day=now.strftime("%Y-%m-%d")# выводим значения времени в формате год-месяц-день
now_day=now_day.replace('-','/')# меняем знак - на /
def get_day_of_week():
    today = datetime.today()
    days_dict = {
        'Monday': 'понедельник',
        'Tuesday': 'вторник',
        'Wednesday': 'среда',
        'Thursday': 'четверг',
        'Friday': 'пятница',
        'Saturday': 'суббота',
        'Sunday': 'воскресенье'
    }
    day_of_week = today.strftime('%A')  # Получаем название дня недели на английском
    return days_dict.get(day_of_week, '')  # Возвращаем название дня на русском из словаря, если есть

day_of_week=get_day_of_week()


def display_error(error):
    window = tk.Tk()
    window.geometry("250x200")
    window.minsize(250, 200)

    text_widget = tk.Text(window, wrap="word")
    text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    text = str(error)
    text_widget.insert(tk.END, text)
    text_widget.config(state="disabled")

    window.mainloop()
def output_window(day,verse_for_the_day,description):
        window= tk.Tk()
        window.geometry("250x200")
        window.minsize(250,200)
        window.maxsize(600,400)
        window.title("Стих на день")
        window['padx'] = 5
        window['pady'] = 5
        frame_labels = tk.Frame(window)         
        frame_labels.pack(fill=tk.BOTH, expand=True)
        lbl1 = tk.Label(frame_labels, text=day)
        lbl1.pack()

        wrap_label = WordWrapLabel(window, text=verse_for_the_day)
        wrap_label.pack(fill='both', expand=True)
        
        frame_text = tk.Frame(window,)  
        frame_text.pack()

        scrollbar = tk.Scrollbar(frame_text)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        text_widget = tk.Text(frame_text, wrap="word", yscrollcommand=scrollbar.set)
        text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=text_widget.yview)

        text = description
        # text_widget.insert(tk.END,verse_for_the_day+"\n"+"\n")
        text_widget.insert(tk.END, text)

        text_widget.config(state="disabled")
        window.mainloop()
filename="jw_page.html"

def create_html_file(filename):
    exe_dir = os.path.dirname(sys.executable) if getattr(sys, 'frozen', False) else os.path.dirname(__file__)
    file_path = os.path.join(exe_dir, filename)

    try:
        if not os.path.exists(file_path):
            with open(file_path, "w", encoding="utf-8") as file:
                file.write("")
             
        
    except Exception as e:
        display_error('Произошла ошибка при создании файла, Попробуйте сами создать файл "jw_page.html" и перенести его в папку в которой находится приложение :)' )
create_html_file(filename)
try:
     with open(filename,"r",encoding="utf-8") as file:# если  первая строка в файле совпадает с сегодняшним днем то
       firstline = next(file, '').strip()
       if firstline.strip() == day_of_week:
                    
        
        jwa=file.read()
                
        soup=BeautifulSoup(jwa,"lxml")# устанавливаем обьект библиотеки beautiful soup


        # Устанавливаем русскую локаль

        #поиск на страничке по регулярному выражению
        pattern = re.compile(rf'\b{day_of_week}\b', re.IGNORECASE)
        day = soup.find(text=pattern) #поиск дня недели
       
        verse_for_the_day=day.find_next('p').text#поиск стиха на день
        description=day.find_next(class_='sb').text#поиск обьяснения стиха
        
        # day = str(day.text)
        output_window(day,verse_for_the_day,description)
       else:
            file.close()
            url = "https://wol.jw.org/ru/wol/h/r2/lp-u/"+now_day # формируем ссылку
            print(url)# проверяем
            #пытаемся походить на обычного пользователя
            headers = {
                 "accept": "image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8",
                 "User-Agent":"Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Mobile Safari/537.36 Edg/119.0.0.0"
                 }
            req = requests.get(url,headers=headers)

            src= req.text #присваиваем переменной значенией всей странички в формате BeautifulSoup
            with open(filename, "w", encoding='utf-8') as file_obj:
                file_obj.write(day_of_week)
                file_obj.write("\n")
                file_obj.write(src)
                print("файл успешно записан")
           
            with open(filename,'r',encoding="utf-8") as file:       
                jwa=file.read()
                    
            soup=BeautifulSoup(jwa,"lxml")
            
            pattern = re.compile(rf'\b{day_of_week}\b', re.IGNORECASE)
            day = soup.find(text=pattern) #поиск дня недели
            one= day.find_next("p")
            two = one.find_next('p')
            day = two.find_next('h2').text
            verse_for_the_day=two.find_next('p').text#поиск стиха на день
            description=two.find_next(class_='sb').text#поиск обьяснения стиха

            # day = str(day.text)
            output_window(day,verse_for_the_day,description)
            
except Exception as e:
        display_error(e)
        
