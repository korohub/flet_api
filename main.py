from flet import *
import requests


class Home(UserControl):

    def __init__(self):
        super(Home, self).__init__()
        self.listdata = Column(scroll=True)
        self.loadmore = ElevatedButton("load more", bgcolor="blue", color="white", visible=False, on_click=self.load_again)
        self.spinner = ProgressRing(width=80, height=80, stroke_width=2, visible=False)
        self.start_index = 0
        self.data_per_load = 5


    def load_again(self, e):
        self.load_data()
        self.update()

    def load_data(self):
        self.spinner.visible = True
        self.update()
        apiurl = f"https://jsonplaceholder.typicode.com/todos?_start={self.start_index}&_limit={self.data_per_load}"
        response = requests.get(apiurl)

        if response.status_code == 200:
            todos = response.json()

            for todo in todos:
                self.listdata.controls.append(
                    Text(f"{todo['id']} - {todo['title']} ")
                )
            if len(todos) == self.data_per_load:
                self.loadmore.visible = True
                self.spinner.visible = False
            else:
                self.loadmore.visible = False
            self.start_index += self.data_per_load


    def did_mount(self):
        self.load_data()
        self.update()

    def build(self):
        return Column([
            self.listdata,
            Row([
                Column([
                    self.loadmore,
                    self.spinner
                ], alignment="center")
            ], alignment="center")

        ])


def main(page: Page):
    page.window_width = 360
    page.window_height = 740
    page.scroll = True

    home = Home()
    page.add(Column([
        home
    ]))


app(main)
