from kivymd.app import MDApp
from kivy.uix.carousel import Carousel
from kivy.uix.image import Image
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.label import MDLabel
from kivy.utils import rgba
from kivy.clock import Clock

from kivy.core.window import Window

Window.size = (310, 580)

class TestApp(MDApp):
    def build(self):
        # Create the Carousel
        carousel = Carousel(
        )

        # Slide 1
        slide1 = MDFloatLayout()
        image1 = Image(
            source="1.jpg",
            pos_hint={"center_x": .5, "center_y": .6},
            size_hint=(.3, .3)
        )
        label1 = MDLabel(
            text="Slide 1",
            pos_hint={"center_x": .5, "center_y": .47},
            halign="center",
            # Uncomment and use the correct path to the font
            font_name="Poppins-Regular",
            font_size="25sp",
            color=rgba(1, 3, 23, 225)
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
        label2 = MDLabel(
            text="Slide 2 bbbbbbbbbbbbbbbbb bbbbbbbbbbbbbb bbbbbbbbbbbbb",
            pos_hint={"center_x": .5, "center_y": .47},
            halign="center",
            # Uncomment and use the correct path to the font
            # font_name="Poppins-Regular",
            font_size="25sp",
            color=rgba(1, 3, 23, 225)
        )
        slide2.add_widget(image2)
        slide2.add_widget(label2)

        # Add slides to the Carousel
        carousel.add_widget(slide1)
        carousel.add_widget(slide2)

        # Bind the on_current_slide event to the method
        carousel.bind(on_current_slide=self.current_slide)

        return carousel

    def current_slide(self, instance, index):
        print(f"Current slide index: {index}")
    
    def on_start(self):
        # Access the carousel.
        # Set infinite looping (optional).
        self.root.loop = True
        # Schedule after every 3 seconds.
        Clock.schedule_interval(self.root.load_next, 3.0)


TestApp().run()
