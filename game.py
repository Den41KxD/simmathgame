from datetime import datetime
import random
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.storage.jsonstore import JsonStore

store = JsonStore('hello.json')
file_path = "hello.json"


ZNAK = ['+', '-', '*', '/']
HARD_MULTIPLEX = {
            1: 10,
            2: 100,
            3: 500,
            4: 1000,
            5: 1500,
            6: 2000,
            7: 5000,
            8: 10000,
        }


class MyGameApp(BoxLayout):
    def __init__(self, hard):
        super(MyGameApp, self).__init__()
        self.main_layout = BoxLayout(orientation="vertical")
        self.start_time = datetime.now()
        self.hard=hard
        self.answers_label = Label(text=str(0))
        self.info_layout = BoxLayout(orientation="horizontal", size=(800, 50), size_hint=(None, None))
        self.clock = Clock.schedule_interval(self.set_time, 1)
        self.back_button = Button(text='Back', on_press=self.back_button_dis)
        self.timer_label = Label(text='0')
        self.info_layout.add_widget(self.back_button)
        self.info_layout.add_widget(Label(text='Correct answers: '))
        self.info_layout.add_widget(self.answers_label)
        self.info_layout.add_widget(Label(text='Time: '))
        self.info_layout.add_widget(self.timer_label)
        self.main_layout.add_widget(self.info_layout)
        self.all_number_layout = BoxLayout(orientation="vertical")


    def build(self):

        self.question = Button(
                    text=str(self.generate_text()),
                    pos_hint={"center_x": 0.5, "center_y": 0.5},
                    background_color=[1, 1, 0, 1])

        self.main_layout.add_widget(self.question)

        input_line = BoxLayout(orientation="horizontal")

        self.solution = TextInput(
            multiline=False, readonly=True, halign="right", font_size=55
        )

        self.clear_button = Button(
                    text='C',
                    size_hint = (0.25,1),
                    pos_hint={"center_x": 0.5, "center_y": 0.5},
                    on_press= self.delete_last,
                )

        input_line.add_widget(self.solution)
        input_line.add_widget(self.clear_button)
        self.solution.text = str('')
        self.main_layout.add_widget(input_line)

        buttons = [
            ["1", "2", "3"],
            ["4", "5", "6"],
            ["7", "8", "9"],
            ["-", "0", "."],
        ]
        for row in buttons:
            h_layout = BoxLayout()
            for label in row:
                button = Button(
                    text=label,
                    pos_hint={"center_x": 0.5, "center_y": 0.5},
                )
                h_layout.add_widget(button)
                button.bind(on_press=self.on_button_press_numbers)
            self.main_layout.add_widget(h_layout)
        self.main_layout.add_widget(Button(
            text='Check answer',
            on_press = self.on_button_press,
            background_color = [0, 1, 0.2, 0.8]
        ))

        return self.main_layout

    def on_button_press_numbers(self,button):
        self.solution.text = self.solution.text+str(button.text)

    def delete_last(self,button):
        self.solution.text = self.solution.text[0:len(self.solution.text)-1]

    def on_button_press(self,*args,**kwargs):
        question= float(eval(self.question.text))
        try:
            answer = float(self.solution.text)
        except ValueError as e:
            return 0
        question=round(question,1)
        answer=round(answer,1)
        if question == answer:
            self.answers_label.text = str(int(self.answers_label.text) + 1)
            self.question.text = self.generate_text()
            self.solution.text=''
            self.main_layout.children[0].background_color = [0, 1, 0.2, 0.8]
            self.main_layout.children[0].text = 'Check answer'
        else:
            self.main_layout.children[0].background_color=[1, 0, 0, 0.8]
            self.main_layout.children[0].text = 'Try again'

    def set_time(self, *args):
        self.timer_label.text = str(datetime.now() - self.start_time)[0:7]

    def back_button_dis(self,button):
        self.main_layout.parent.manager.current = 'settings'

    def get_random_number(self,hard=None):
        if not hard:
            a = random.randint(-1 * HARD_MULTIPLEX[self.hard], HARD_MULTIPLEX[self.hard])
        else:
            a = random.randint(-1 * HARD_MULTIPLEX[hard], HARD_MULTIPLEX[hard])
        return a

    def generate_text(self):
        new_text = ''
        for i in range(1, self.hard+1):
            new_number = self.get_random_number()
            if new_number > 0 and i != 1:
                znak = random.choice(ZNAK)
                if znak in ['/', '*']:
                    new_number = znak + str(self.get_random_number(random.randint(1, 3)))
                else:
                    new_number = znak + str(new_number)
                new_text += str(new_number)
            else:
                new_text += str(new_number)
        return new_text
