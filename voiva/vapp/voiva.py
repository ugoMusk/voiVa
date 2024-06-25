#!/bin/bash/env python3.9
''' Module contains both frontend and backend code. In the  future, 
i intend to refactor it for more clarity to employ modular programing
and unit testing
'''

from kivy.core.window import Window
from kivy.metrics import dp
from kivy.properties import StringProperty
from kivy.uix.spinner import Spinner

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
from kivymd.uix.widget import MDWidget
from kivymd.uix.divider import MDDivider

from kivy.utils import rgba
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle
from kivy.properties import StringProperty, NumericProperty
from kivy.core.text import Label as CoreLabel
from kivy.uix.scrollview import ScrollView

# from kivymd.theming import ThemeManager
from kivymd.uix.textfield import (
    MDTextField, MDTextFieldHelperText,
    MDTextFieldMaxLengthText)
from kivymd.uix.widget import MDWidget
from kivymd.uix.button import MDButton, MDButtonText, MDButtonIcon
from kivymd.uix.navigationrail import(
    MDNavigationRail, MDNavigationRailItem,
    MDNavigationRailItemIcon, MDNavigationRailItemLabel)

from kivymd.uix.behaviors import HoverBehavior
from kivymd.uix.button import MDIconButton

from espnet2.bin.tts_inference import Text2Speech
import sounddevice as sd
import numpy as np
import torch


###############################################
# Candidate parameters for the utils module
###############################################

# Set automatic size for app window'
Window.size = (310, 580)

# get both width and height of app window
screen_width = Window.width
screen_height = Window.height

########################################################
# This class defines an item for the MDNavigationBar
########################################################

class BaseMDNavigationItem(MDNavigationItem):
    ''' defines a navigation item for the MDNavigationBar '''
    icon = StringProperty()
    text = StringProperty()

    def __init__(self, **kwargs):
        '''  class entry point, sets icon and text for each item of the MDNavigationBar '''
        super().__init__(**kwargs)
        self.add_widget(MDNavigationItemIcon(icon=self.icon))
        self.add_widget(MDNavigationItemLabel(text=self.text))

class BaseNavigationRailItem(MDNavigationRailItem, HoverBehavior):
    icon = StringProperty()
    text = StringProperty()

    def __init__(self, icon="", text="", **kwargs):
        super().__init__(**kwargs)
        self.icon = icon
        self.text = text

        # Create and add an icon button to the item
        self.icon_button = MDIconButton(icon=self.icon)
        self.add_widget(self.icon_button)

        # Create and add a label to the item
        self.label = MDLabel(text=self.text, halign="center")
        self.add_widget(self.label)

    def on_enter(self, *args):
        # Custom hover behavior: Change icon and text color
        self.icon_button.icon = "mouse"
        self.label.text = "Hovered"

    def on_leave(self, *args):
        # Restore original icon and text
        self.icon_button.icon = self.icon
        self.label.text = self.text

class TextField(MDTextField):
    ''' defines a text input field '''
    def insert_text(self, substring, from_undo=False):
        '''inserts'''
        if substring == "\n":
            self.text = "" 
        elif len(self.text) + len(substring) <= 200:
            return super().insert_text(substring, from_undo=from_undo)
        else:
            return super().insert_text("", from_undo=from_undo)

class BaseScreen(MDScreen):
    '''This screen class is inherited by multiple other screens'''
    image_size = StringProperty()

    def __init__(self, **kwargs):
        '''class entry point, sets a random background image for all child screens'''
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
    '''defines the home screen'''
    def __init__(self, **kwargs):
        '''class entry point'''
        super().__init__(**kwargs)
        pass

class CreateScreen(BaseScreen):
    '''defines the create screen'''
    def __init__(self, **kwargs):
        '''class entry point'''
        super().__init__(**kwargs)

        # Set up a dictionary of voices 
        self.voices = {
            "Voice 1": ("kan-bayashi/ljspeech_tacotron2", "parallel_wavegan/ljspeech_parallel_wavegan.v1"),
            "Voice 2": ("kan-bayashi/jsut_tacotron2", "parallel_wavegan/jsut_parallel_wavegan.v1")
            # more voices here
        }
        
        # Select model and vocoder to download by tag name
        self.current_model_tag = "kan-bayashi/ljspeech_tacotron2"
        self.current_vocoder_tag = "parallel_wavegan/ljspeech_parallel_wavegan.v1"
        
        # call the espnet2 Text2Speech pretrained method with the tags above to initiate the download
        self.model = Text2Speech.from_pretrained(
            model_tag=self.current_model_tag,
            vocoder_tag=self.current_vocoder_tag
        )

        main_bl = MDBoxLayout(
            orientation="vertical",
            pos_hint={"center_x": 0.5, "center_y": 0.55},
            spacing=dp(15),
        )
        bl = MDBoxLayout(orientation="horizontal")
        bl.add_widget(MDWidget(size_hint_x=None, width=dp(70)))

        # create a text input field
        self.text_input = TextField(
                MDTextFieldHelperText(text="Input Text", mode="persistent"),
                MDTextFieldMaxLengthText(max_text_length=200),
                mode="filled",
                theme_bg_color="Custom",
                theme_text_color="Custom",
                text_color_focus="black",
                fill_color_focus=(1, 1, 1, .95),
                multiline=True,
                max_height="300dp",
                radius=12
        )
        
        # add text input to the parent Layout
        bl.add_widget(self.text_input)

        # add an empty widget to the parent Layout
        bl.add_widget(MDWidget(size_hint_x=None, width=dp(70)))

        # add boxlayout to main Layout
        main_bl.add_widget(bl)

        # add button to the main Layout
        main_bl.add_widget(
            MDButton(
                MDButtonIcon(icon="access-point", padding=0),
                MDButtonText(text="speak"),
                style="elevated",
                pos_hint={"center_x": 0.5, "center_y": 0.5},
                size_hint=(None, None),
                width=5,
                on_press=self.speak,
            ),
        )

        # add main Layout to root Layout
        self.add_widget(main_bl)
    
    def speak(self, instance):
        '''plays the converted audio output from the tts model'''
        text = self.text_input.text
        if text:
            outputs = self.model(text)
            wav = outputs['wav']

            # Check if wav is a torch or tensor
            if isinstance(wav, torch.Tensor):
                audio_data = wav.view(-1).cpu().numpy()  # Convert to 1D numpy array
            elif isinstance(wav, np.ndarray):
                audio_data = wav
            else:
                print(f"Unexpected type for wav: {type(wav)}")
                return

            sample_rate = 22050  # Assume the sample rate is 22050 Hz
            
            # Play the audio
            sd.play(audio_data, samplerate=sample_rate)
            sd.wait()  # Wait until the audio is done playing
            print("Audio playback finished.")
        else:
            print("Please enter some text.")

class ManualScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = "manual"
        
        # Create a BoxLayout
        bl = MDBoxLayout(orientation="horizontal")
        
        # Create a NavigationRail
        nav_rail = MDNavigationRail()
        
        # Create NavigationRailItems
        rail_item1 = BaseNavigationRailItem(icon="home", text="Home")
        rail_item2 = BaseNavigationRailItem(icon="help", text="Help")
        rail_item3 = BaseNavigationRailItem(icon="account", text="Account")
        
        # Add items to the navigation rail
        nav_rail.add_widget(rail_item1)
        nav_rail.add_widget(rail_item2)
        nav_rail.add_widget(rail_item3)

        # Add NavigationRail to the BoxLayout
        bl.add_widget(nav_rail)

        bl.add_widget(
            MDDivider(
                size_hint_y = .5,
                orientation = "vertical"
            )
        )
        # Create a FloatLayout for the main content
        float_layout = MDFloatLayout()
        
        # Add a centered Label
        label = MDLabel(
            text="Hello, KivyMD!",
            halign="center",
            pos_hint={"center_x": 0.5, "center_y": 0.5}
        )
        float_layout.add_widget(label)
        
        # Add the main content layout to the BoxLayout
        bl.add_widget(float_layout)


        # Add BoxLayout to the screen
        self.add_widget(bl)


class OutlineLabel(MDLabel):
    '''defines an outline for text Labels'''
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
            outline_width = self.width + 1 * self.outline_width
            outline_height = self.height + 1 * self.outline_width

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

class VoiVa(MDApp):
    '''defines the application instance'''
    # theme_cls = ThemeManager()

    def on_spinner_select(self, spinner, text):
        self.current_model_tag, self.current_vocoder_tag = self.create_screen.voices[text]
        self.model = Text2Speech.from_pretrained(
            model_tag=self.current_model_tag,
            vocoder_tag=self.current_vocoder_tag
        )
        print(f"Selected voice: {text}, Model: {self.current_model_tag}, Vocoder: {self.current_vocoder_tag}")

    def on_switch_tabs(self, bar: MDNavigationBar, item: MDNavigationItem, item_icon: str, item_text: str):
        screen_manager = self.root.children[1]
        screen_manager.current = item_text

    def build(self):
        '''application entry point '''
        box_layout = MDBoxLayout(orientation="vertical", md_bg_color=self.theme_cls.backgroundColor)

        # Create the ScreenManager
        screen_manager = MDScreenManager(id="screen_manager")

        # Create and add the HomeScreen
        self.home_screen = HomeScreen(name="home", image_size="1024")

        ####################################################
        # Everything for HomeScreen
        ####################################################

        # Create the Carousel and store the reference
        self.carousel = Carousel(loop=True)

        # Slide 1
        slide1 = MDFloatLayout()
        image1 = Image(
            source="11.jpg",
            pos_hint={"center_x": .5, "center_y": .6},
            size_hint=(.3, .3)
        )
        label1 = OutlineLabel(
            text="JUST A TAP!\
                From documents to daily musings, transform text into speach that speak volume",
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
            text="DON'T JUST READ-LISTEN!\
                Our tts engine elevates your reading experience  by turning text into clear talk. Choose from a range of voices or train the ai to produces custom speech paterns",
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
        self.home_screen.add_widget(self.carousel)

        # Add HomeScreen to ScreenManager
        screen_manager.add_widget(self.home_screen)

        # Create and add the CreateScreen
        self.create_screen = CreateScreen(name="create", image_size="800")
        screen_manager.add_widget(self.create_screen)

        ####################################################
        # Everything for CreateScreen
        ####################################################

        # create and add spiner to CreateScreen for voice selection
        self.vspiner = Spinner(
            text='Select Voice',
            values=list(self.create_screen.voices.keys()),
            size_hint=(None, None),
            size=(200, 44),
            pos_hint={'center_x': .5, 'center_y': .5}
        )
        self.vspiner.bind(text=self.on_spinner_select)

        self.create_screen.add_widget(self.vspiner)

        # Create and add the ManualScreen
        manual_screen = ManualScreen()
        # manual_screen = ManualScreen(name="manual", image_size="600")
        screen_manager.add_widget(manual_screen)

        ####################################################
        # Everything for ManualScreen
        ####################################################


        # Add the ScreenManager to the layout
        box_layout.add_widget(screen_manager)

        # Create the NavigationBar
        navigation_bar = MDNavigationBar(on_switch_tabs=self.on_switch_tabs)
        # Create and add navigation items
        home_nav_item = BaseMDNavigationItem(icon="home", text="home", active=True)
        create_nav_item = BaseMDNavigationItem(icon="microphone", text="create")
        manual_nav_item = BaseMDNavigationItem(icon="help", text="manual")

        # add all screens to the navigation bar
        navigation_bar.add_widget(home_nav_item)
        navigation_bar.add_widget(create_nav_item)
        navigation_bar.add_widget(manual_nav_item)

        # Add the NavigationBar to the layout
        box_layout.add_widget(navigation_bar)

        return box_layout

    def on_start(self):
        '''metthod fires th first time the application kicks of'''
        # Access the carousel and set infinite looping (optional)
        self.carousel.loop = True
        # Schedule after every 3 seconds
        Clock.schedule_interval(self.carousel.load_next, 6.0)

    def current_slide(self, instance, value):
        print(f"Current slide index: {self.carousel.index}")

if __name__ == '__main__':
    VoiVa().run()
