from kivy.lang import Builder

from kivymd.app import MDApp
from kivymd.uix.tab import MDTabsItemText, MDTabsItem

KV = '''
MDScreen:
    md_bg_color: self.theme_cls.backgroundColor

    MDTabsPrimary:
        id: tabs
        pos_hint: {"center_x": .5, "center_y": .5}
        size_hint_x: .6
        allow_stretch: False
        label_only: True

        MDDivider:
'''


class Example(MDApp):
    def on_start(self):
        for tab_name in [
            "Moscow",
            "Saint Petersburg",
            "Novosibirsk",
            "Yekaterinburg",
            "Kazan",
            "Nizhny Novgorod",
            "Chelyabinsk",
        ]:
            self.root.ids.tabs.add_widget(
                MDTabsItem(
                    MDTabsItemText(
                        text=tab_name,
                    ),
                )
            )
        self.root.ids.tabs.switch_tab(text="Moscow")

    def build(self):
        self.theme_cls.primary_palette = "Olive"
        return Builder.load_string(KV)


Example().run()