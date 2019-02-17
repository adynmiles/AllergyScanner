import kivy
kivy.require('1.10.1')
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.stacklayout import StackLayout
from kivy.uix.popup import Popup
from kivy.uix.behaviors import ButtonBehavior
from kivy.lang import Builder
from kivymd.theming import ThemeManager
import time
import table_creation
from kivy.uix.screenmanager import ScreenManager, Screen
from random import random
from kivy.config import Config
from kivy.graphics import Color, Rectangle

peanutstatus = False
treenutstatus = False
shellfishstatus = False
dairystatus = False
soystatus = False
glutenstatus = False

Config.set('graphics','width','450')
Config.set('graphics','height','800')

Builder.load_string("""
<LoginScreen>:
    GridLayout:
        rows: 3
        cols: 2
        padding: 10
        spacing: 10
        Label:
            text: 'Please enter "username": '
        
        TextInput:
            id: username
            multiline: False
        Label:
            text: 'Please enter "password": '
        TextInput:
            id: password
            password: True
            multiline: False
        Button:
            text: 'Login'
           
            on_press: root.verify_credentials()
            
   
<AllergenChoice>: 
    GridLayout:
        rows: 4
        cols: 2
        ToggleButton:
            text: 'Peanuts'
            on_press: root.update_peanut_status()
        ToggleButton:
            text: 'Tree Nuts'
            on_press: root.update_treenut_status()
        ToggleButton:
            text: 'Soy'
            on_press: root.update_soy_status()
        ToggleButton:
            text: 'Dairy'
            on_press: root.update_dairy_status()
        ToggleButton:
            text: 'Gluten'
            on_press: root.update_gluten_status()
        ToggleButton:
            text: 'Shellfish'
            on_press: root.update_shellfish_status()
        Button:
            text: 'Continue'
            on_press: root.manager.current = 'main'
     
<MainScreen>:
    GridLayout:
        rows: 4
        padding: 10 
        spacing: 10
        Button:
            text: 'Scanner'
            on_press: root.manager.current = 'scanner'
        Button:
            text: 'Allergen Info'
            on_press: root.manager.current = 'info'
        Button:
            text: 'Epipen Expiry'
            on_press: root.manager.current = 'epipen' 
        Button:
            text: 'Back'
            on_press: root.manager.current = 'allergy_choice'
 
<ScannerScreen>:
    AnchorLayout:
        anchor_x: 'center'
        anchor_y: 'center'

        Image:
            source: 'ScanningUI.jpg'
            size_hint: None, None
            size: 900,500
        
    Button:
        text: 'Capture Image'
        size_hint_y: None
        height: '48dp'
        on_release: root.allergyinfo()
        Button:
            text: 'Back'
            on_release: root.manager.current = 'main'
        
            
<InfoScreen>:
    GridLayout:
        cols: 2
        rows: 2
        Button:
            text: 'Epipen Tutorial'
            on_press: root.epitutorial()
        Button:
            text: 'Other Allergy Resources'
            on_press: root.otherallergies()
        Button:
            text: 'Facts'
            on_press: root.funfacts()
        Button:
            text: 'Back'
            on_press: root.manager.current = 'main'
            
<EpipenScreen>:
    GridLayout:
        title: 'Expiry Dates' 
        rows: 3
        Button:
            text: 'Epipen 1 - 17/02/19'
            on_press: root.epipen1info()
        Button:
            text: 'Epipen 2 - 31/03/19'   
            on_press: root.epipen2info()
        Button:
            text: 'Back'
            on_press: root.manager.current = 'main'    
""")

"""Camera:
        id: camera
        resolution: (640, 480)
        play: True
    Button:
        text: 'Capture Image'
        size_hint_y: None
        height: '48dp'
        on_release: root.capture()
        Button:
            text: 'Back'
            on_press: root.manager.current = 'main'
"""

sm = ScreenManager()
screen = Screen(name = 'Login Screen')
sm.add_widget(screen)

theme_cls = ThemeManager()
theme_cls.theme_style = 'Dark'
theme_cls.primary_palette = 'Green'
theme_cls.accent_palette = 'Pink'

class LoginScreen(Screen):
    def verify_credentials(self):
        if self.ids["username"].text == "username" and self.ids["password"].text == "password":
            self.manager.current = "allergy_choice"

class MainScreen(Screen):
    pass

class ScannerScreen(Screen):
    def allergyinfo(self):
        output = table_creation.output
        popup = Popup(title = 'Allergy Information',
                      content = Label(text = "ALERT -" + output),
                      color = (255,0,0),
                      auto_disable = True)
        popup.open()

class AllergenChoice(Screen):
    peanutstatus = False
    treenutstatus = False
    shellfishstatus = False
    dairystatus = False
    soystatus = False
    glutenstatus = False
    def update_peanut_status(self):
        self.peanutstatus = not self.peanutstatus
        return self.peanutstatus

    def update_treenut_status(self):
        self.treenutstatus = not self.treenutstatus
        return self.treenutstatus

    def update_shellfish_status(self):
        self.shellfishstatus = not self.shellfishstatus
        return self.shellfishstatus

    def update_dairy_status(self):
        self.dairystatus = not self.dairystatus
        return self.dairystatus

    def update_soy_status(self):
        self.soystatus = not self.soystatus
        return self.soystatus

    def update_gluten_status(self):
        self.glutenstatus = not self.glutenstatus
        return self.glutenstatus

class InfoScreen(Screen):
    def epitutorial(self):
        popup = Popup(title='Epipen Tutorial',
                      content=Label(text="Shows Video"))
        popup.open()

    def otherallergies(self):
        popup = Popup(title='Other Allergy Resources',
                      content=Label(text="Medic Alert - https://www.medicalert.org/\n" 
                                         "Food Allergy Research and Education - https://www.foodallergy.org/"
                                    ))
        popup.open()

    def funfacts(self):
        popup = Popup(title='Facts',
                      content=Label(text="A peanut allergy is the most common form of food allergy \n"
                                         "Approximately one in 13 children in the US have a food allergy \n"
                                         "Allergies to milk, soy, and dairy are easier to grow out of than peanut and tree nut allergies."
                                    ))
        popup.open()

class EpipenScreen(Screen):
    def epipen1info(self):
        popup = Popup(title='Epipen 1 Expiry Information',
                      content=Label(text="Purchase new EpiPen by 17/07/19"))
        popup.open()

    def epipen2info(self):
        popup = Popup(title= 'Epipen 2 Expiry Information',
                      content=Label(text = 'Purchase new EpiPen by 31/08/19'))
        popup.open()


# Create the screen manager 
sm = ScreenManager()
sm.add_widget(LoginScreen(name='login'))
sm.add_widget(MainScreen(name='main'))
sm.add_widget(ScannerScreen(name='scanner'))
sm.add_widget(AllergenChoice(name='allergy_choice'))
sm.add_widget(InfoScreen(name='info'))
sm.add_widget(EpipenScreen(name='epipen'))


class TestApp(App):
    def build(self):
        return sm
    
if __name__ == '__main__':
    TestApp().run()

""" def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
    
        self.cols = 2
        self.add_widget(Label(text='Please enter your username:'))
        self.username = TextInput(multiline=False)
        self.add_widget(self.username)
        self.add_widget(Label(text='Please enter your password'))
        self.password = TextInput(password=True, multiline=False)
        self.add_widget(self.password)
        self.login = Button(text="Login")
        self.login.bind(on_press = self.verify_credentials)
        self.add_widget(self.login)

    def verify_credentials(self, instance):
        if self.username.text == "adyn" and self.password.text == "password":
            popup = Popup(title= "Login successful!",
                content=Label(text ='Welcome to the Allergy Scanner App'),
                size_hint = (None, None),
                size = (1024, 768),
                auto_dismiss = False)
            popup.open()
            MainScreen.MainScreenApp().run()

class LoginScreenApp(App):

    def build(self):
        return LoginScreen()

if __name__ == '__main__':
    LoginScreenApp().run()
"""
