from kivymd.app import MDApp
from kivy.lang.builder import Builder
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout

Window.size = (330, 500)


kv = """
#:import MDTextField kivymd.uix.textfield.MDTextField
<MyTile@SmartTileWithLabel>
    size_hint_y: None
    height: "240dp"

<S>:
    MDTextFieldRound:
        pos_hint: {"center_x": .5, "center_y": .95}
        normal_color : [1,1,1,.1]
        color_active : [1,1,1,1]
        size_hint: .8, .07
        hint_text : 'Search a product...'
        icon_left : 'magnify'

Screen:
    FloatLayout:
        BoxLayout:
            id: m5
            pos_hint: {"center_x": .5, "center_y": .371} #this will change if you change this Window.size = (330, 500)
            orientation: "vertical"

            ScrollView:
                MDGridLayout:
                    cols: 1
                    adaptive_height: True
                    padding: dp(4), dp(4)
                    spacing: dp(4)

                    MyTile:
                        source: "Photos/pro.jpg"
                        text: "[size=26]jbsidis[/size]\\n[size=14]cat-1.jpg[/size]"

                    MyTile:
                        source: "Photos/pro.jpg"
                        text: "[size=26]jbsidis[/size]\\n[size=14]cat-2.jpg[/size]"
                        tile_text_color: app.theme_cls.accent_color

                    MyTile:
                        source: "Photos/pro.jpg"
                        text: "[size=26][color=#ffffff]jbsidis[/color][/size]\\n[size=14]cat-3.jpg[/size]"
                        tile_text_color: app.theme_cls.accent_color


                    MyTile:
                        source: "a11.png"
                        text: ""
                        tile_text_color: [0,0,0,0]
                        FloatLayout:
                            AnchorLayout:
                                pos_hint: {"center_x": .5, "center_y": .9}
                                MDTextButton:
                                    halign: "center"
                                    text: "\\n\\n\\n\\n\\n\\n\\nLoading more...\\n\\n"
                                MDSpinner:
                                    size_hint: .1,.1

    MDToolbar:
        id: success_screen_toolbar
        title: "Project"
        pos_hint: {"top": 1}
        right_action_items: [["progress-check", lambda: print(6)]]


    MDBottomAppBar:
        MDToolbar:
            id: success_screen_bottomappbar
            icon: "magnify"
            on_action_button: root.add_widget(app.sbar())
            type: 'bottom'
            mode: 'center'
            #elevation: '8dp'
            left_action_items: [["calendar-text", lambda: print(6)], ["account-group", lambda: print(6)]]
            right_action_items: [["magnify", lambda: print(6)], ["menu", lambda: print(6)]]
"""
class blanks1(BoxLayout):
    pass
class S(FloatLayout):
    pass


class Main(MDApp):
    def build(self):
        return Builder.load_string(kv)
    def sbar(self):
        self.root.ids.success_screen_toolbar.md_bg_color=[1,1,1,1]
        return S()
