import kivy
import requests
import pprint


kivy.require('1.0.6')

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.core.window import  Window
from kivy.clock import Clock


LBRY_DAEMON_URL = "http://localhost:5279"

class BookNetApp(App):

    def check_lbry_status(self, dt):
        status_args_dict = {"method": "status", "params": {}}
        try:
            response = requests.post(LBRY_DAEMON_URL, json=status_args_dict)
        except requests.exceptions.RequestException:
            status_bool = False

        else:
            if response.status_code == 200:
                status_bool = True
            else:
                status_bool = False
        self.update_staus_label(status_bool)

    def update_staus_label(self, status_bool=False):
        lbry_status_str = "online" if status_bool else "down"
        status_line_str = f'[status {lbry_status_str}]'
        self.status_label.text = status_line_str

    def build(self):

        Clock.schedule_once(self.check_lbry_status, 1)

        layout = FloatLayout(size=Window.size)

        self.status_label = Label(text="", valign="bottom", halign="right", text_size=layout.size)
        booknet_label = Label(text=f'LBRY Booknet')

        layout.add_widget(booknet_label)
        layout.add_widget(self.status_label)
        self.update_staus_label()
        return layout



if __name__ == '__main__':
    BookNetApp().run()