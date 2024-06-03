from kivy.core.window import Window
from kivy.metrics import dp
from kivy.properties import StringProperty

from kivymd.uix.fitimage import FitImage
from kivymd.uix.screen import MDScreen
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.navigationbar import (
    MDNavigationBar,
    MDNavigationItem,
    MDNavigationItemLabel,
    MDNavigationItemIcon,
)
from kivymd.app import MDApp
from kivy.uix.carousel import Carousel
from kivymd.uix.floatlayout import MDFloatLayout
from kivy.uix.image import Image
from kivymd.uix.label import MDLabel
from kivy.uix.label import Label
from kivy.utils import rgba
from kivy.clock import Clock

from kivymd.uix.textfield import MDTextField, MDTextFieldHelperText, MDTextFieldMaxLengthText
from kivymd.uix.widget import MDWidget
from kivymd.uix.button import MDButton, MDButtonText, MDButtonIcon

# Window.fullscreen = 'auto'
Window.size = (310, 580)
screen_width = Window.width
screen_height = Window.height

from kivy.graphics import Color, Rectangle
from kivy.properties import StringProperty, NumericProperty
from kivy.core.text import Label as CoreLabel

class BaseMDNavigationItem(MDNavigationItem):
    icon = StringProperty()
    text = StringProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(MDNavigationItemIcon(icon=self.icon))
        self.add_widget(MDNavigationItemLabel(text=self.text))

class TextField(MDTextField):
    def insert_text(self, substring, from_undo=False):
        if substring == "\n":
            self.text = "" 
        elif len(self.text) + len(substring) <= 200:
            return super().insert_text(substring, from_undo=from_undo)
        else:
            return super().insert_text("", from_undo=from_undo)

class BaseScreen(MDScreen):
    image_size = StringProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(
            FitImage(
                source=f"https://picsum.photos/{self.image_size}/{self.image_size}",
                size_hint=(0.9, 0.9),
                pos_hint={"center_x": 0.5, "center_y": 0.5},
                radius=dp(24),
            ),
        )

class HomeScreen(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

class CreateScreen(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        main_bl = MDBoxLayout(
            orientation="vertical",
            pos_hint={"center_x": 0.5, "center_y": 0.55},
            spacing=dp(15),
        )
        bl = MDBoxLayout(orientation="horizontal")
        bl.add_widget(MDWidget(size_hint_x=None, width=dp(70)))
        bl.add_widget(
            TextField(
                MDTextFieldHelperText(text="Input Text", mode="persistent"),
                MDTextFieldMaxLengthText(max_text_length=200),
                mode="filled",
                theme_bg_color="Custom",
                theme_text_color="Custom",
                text_color_focus="black",
                fill_color_focus=(1, 1, 1, .95),
                multiline=True,
                max_height="300dp",
                radius=12,
            ),
        )
        bl.add_widget(MDWidget(size_hint_x=None, width=dp(70)))
        main_bl.add_widget(bl)
        main_bl.add_widget(
            MDButton(
                MDButtonIcon(icon="access-point", padding=0),
                MDButtonText(text="convert"),
                style="elevated",
                pos_hint={"center_x": 0.5, "center_y": 0.5},
                size_hint=(None, None),
                width=5,
            ),
        )
        self.add_widget(main_bl)

class ManualScreen(BaseScreen):
    pass

class OutlineLabel(MDLabel):
    outline_color = [1, 1, 1, 1]  # White color for the outline
    outline_width = 2

    def __init__(self, **kwargs):
        self.outline_color = kwargs.pop('outline_color', self.outline_color)
        self.outline_width = kwargs.pop('outline_width', self.outline_width)
        super(OutlineLabel, self).__init__(**kwargs)
        self.bind(pos=self.update_texture, size=self.update_texture, text=self.update_texture, font_size=self.update_texture, font_name=self.update_texture)
        self.bind(width=self.update_text_size)
        self.text_size = (self.width, None)

    def update_text_size(self, *args):
        self.text_size = (self.width, None)

    def update_texture(self, *args):
        if not self.text:
            self.texture = None
            return

        # Create the core label
        core_label = CoreLabel(text=self.text, font_size=self.font_size, font_name=self.font_name, text_size=self.text_size, halign=self.halign, valign=self.valign)
        core_label.refresh()
        self.texture = core_label.texture
        self.texture_size = list(self.texture.size)

        # Draw the outline and main text
        with self.canvas:
            self.canvas.clear()
            outline_x = self.x - self.outline_width
            outline_y = self.y - self.outline_width
            outline_width = self.width + 2 * self.outline_width
            outline_height = self.height + 2 * self.outline_width

            # Draw the outline
            Color(*self.outline_color)
            for dx in range(-self.outline_width, self.outline_width + 1):
                for dy in range(-self.outline_width, self.outline_width + 1):
                    if dx == 0 and dy == 0:
                        continue
                    Rectangle(texture=self.texture, pos=(self.x + dx, self.y + dy), size=self.texture_size)

            # Draw the main text
            Color(*self.color)
            Rectangle(texture=self.texture, pos=self.pos, size=self.texture_size)

class Test(MDApp):
    def on_switch_tabs(self, bar: MDNavigationBar, item: MDNavigationItem, item_icon: str, item_text: str):
        screen_manager = self.root.children[1]
        screen_manager.current = item_text

    def build(self):
        box_layout = MDBoxLayout(orientation="vertical", md_bg_color=self.theme_cls.backgroundColor)

        # Create the ScreenManager
        screen_manager = MDScreenManager(id="screen_manager")

        # Create and add the HomeScreen
        home_screen = HomeScreen(name="home", image_size="1024")

        # Create the Carousel and store the reference
        self.carousel = Carousel(loop=True)

        # Slide 1
        slide1 = MDFloatLayout()
        image1 = Image(
            source="1.jpg",
            pos_hint={"center_x": .5, "center_y": .6},
            size_hint=(.3, .3)
        )
        label1 = OutlineLabel(
            text="Slide 1 wwwwwwwwwwwwwwwwwwwwwwwwwwww bbbbbbbbbb bbbbbbbbbbbbb",
            pos_hint={"center_x": 0.5, "center_y": 0.9},
            size_hint_x=.5,  # Adjust this value as needed
            halign="center",
            valign="middle",
            font_size="25sp",
            color=[0.0039, 0.0118, 0.0902, 0.8824],  # rgba(1, 3, 23, 225) in Kivy format
            outline_color=[1, 1, 1, 1],  # White outline
            outline_width=1
        )
        slide1.add_widget(image1)
        slide1.add_widget(label1)

        # Slide 2
        slide2 = MDFloatLayout()
        image2 = Image(
            source="2.jpg",
            pos_hint={"center_x": .5, "center_y": .6},
            size_hint=(.3, .3)
        )
        label2 = OutlineLabel(
            text="Slide 2 bbbbbbbbbbbbbbbbb bbbbbbbbbbbbbb bbbbbbbbbbbbb",
            pos_hint={"center_x": 0.5, "center_y": 0.9},
            size_hint_x=.5,  # Adjust this value as needed
            halign="center",
            valign="middle",
            font_size="25sp",
            color=[0.0039, 0.0118, 0.0902, 0.8824],  # rgba(1, 3, 23, 225) in Kivy format
            outline_color=[1, 1, 1, 1],  # White outline
            outline_width=1,
        )
        slide2.add_widget(image2)
        slide2.add_widget(label2)

        # Add slides to the Carousel
        self.carousel.add_widget(slide1)
        self.carousel.add_widget(slide2)

        # Bind the on_current_slide event to the method
        self.carousel.bind(on_current_slide=self.current_slide)

        # Add Carousel to HomeScreen
        home_screen.add_widget(self.carousel)

        # Add HomeScreen to ScreenManager
        screen_manager.add_widget(home_screen)

        # Create and add the CreateScreen
        create_screen = CreateScreen(name="create", image_size="800")
        screen_manager.add_widget(create_screen)

        # Create and add the ManualScreen
        manual_screen = ManualScreen(name="manual", image_size="600")
        screen_manager.add_widget(manual_screen)

        # Add the ScreenManager to the layout
        box_layout.add_widget(screen_manager)

        # Create the NavigationBar
        navigation_bar = MDNavigationBar(on_switch_tabs=self.on_switch_tabs)

        # Create and add navigation items
        home_nav_item = BaseMDNavigationItem(icon="home", text="home", active=True)
        create_nav_item = BaseMDNavigationItem(icon="plus", text="create")
        manual_nav_item = BaseMDNavigationItem(icon="help", text="manual")

        navigation_bar.add_widget(home_nav_item)
        navigation_bar.add_widget(create_nav_item)
        navigation_bar.add_widget(manual_nav_item)

        # Add the NavigationBar to the layout
        box_layout.add_widget(navigation_bar)

        return box_layout

    def on_start(self):
        # Access the carousel and set infinite looping (optional)
        self.carousel.loop = True
        # Schedule after every 3 seconds
        Clock.schedule_interval(self.carousel.load_next, 3.0)

    def current_slide(self, instance, value):
        print(f"Current slide index: {self.carousel.index}")

if __name__ == '__main__':
    Test().run()
