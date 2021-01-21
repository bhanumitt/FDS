import kivy

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from database import DataBase


class CreateAccountWindow(Screen):
    namee = ObjectProperty(None)
    email = ObjectProperty(None)
    password = ObjectProperty(None)

    def submit(self):
        if self.namee.text != "" and self.email.text != "" and self.email.text.count("@") == 1 and self.email.text.count(".") > 0:
            if self.password != "":
                db_user.add_user(self.email.text, self.password.text, self.namee.text, "")

                self.reset()

                sm.current = "login"
            else:
                invalidForm()
        else:
            invalidForm()

    def login(self):
        self.reset()
        sm.current = "login"

    def reset(self):
        self.email.text = ""
        self.password.text = ""
        self.namee.text = ""

class PartnerCreateAccountWindow(Screen):
    namee = ObjectProperty(None)
    address = ObjectProperty(None)
    email = ObjectProperty(None)
    password = ObjectProperty(None)

    def submit(self):
        if self.namee.text != "" and self.email.text != "" and self.email.text.count("@") == 1 and self.email.text.count(".") > 0 and self.address.text != "":
            if self.password != "":
                db_partner.add_partner(self.email.text, self.password.text, self.namee.text, self.address.text, "100", "[]")

                self.reset()

                sm.current = "partnerlogin"
            else:
                invalidForm()
        else:
            invalidForm()

    def login(self):
        self.reset()
        sm.current = "partnerlogin"

    def reset(self):
        self.email.text = ""
        self.address.text = ""
        self.password.text = ""
        self.namee.text = ""

class LoginWindow(Screen):
    email = ObjectProperty(None)
    password = ObjectProperty(None)

    def loginBtn(self):
        if db_user.validate(self.email.text, self.password.text):
            MainWindow.current = self.email.text
            ViewWindow.current = self.email.text
            self.reset()
            sm.current = "main"
        else:
            invalidLogin()

    def reset(self):
        self.email.text = ""
        self.password.text = ""

class PartnerLoginWindow(Screen):
    email = ObjectProperty(None)
    password = ObjectProperty(None)

    def loginBtn(self):
        if db_partner.validate_partner(self.email.text, self.password.text):
            PartnerMainWindow.current = self.email.text
            AddFood.current = self.email.text
            UpdateFood.current = self.email.text
            self.reset()
            sm.current = "partnermain"
        else:
            invalidLogin()

    def reset(self):
        self.email.text = ""
        self.password.text = ""

class HomeWindow(Screen):
    pass

class PartnerMainWindow(Screen):
    value = ObjectProperty(None)
    current = ""
    
    def limitSet(self):
        db_partner.limitSet(self.value.text, self.current)
        self.reset()
        
    def reset(self):
        self.value.text = ""
        
class AddFood(Screen):
    namee = ObjectProperty(None)
    cuisine = ObjectProperty(None)
    price = ObjectProperty(None)
    current = ""
    
    def addition(self):
        try:
            if self.namee.text != "" and self.cuisine.text != "" and self.price.text != "" and self.price.text.isdigit():
                db_partner.add_food(self.namee.text, self.cuisine.text, self.price.text, self.current)
                self.reset()
                updateDatabase()
            else:
                raise Exception()
        except: 
            invalidForm()
            
    
    def reset(self):
        self.namee.text = ""
        self.cuisine.text = ""
        self.price.text = ""
    
class UpdateFood(Screen):
  
    oldName = ObjectProperty(None)
    namee = ObjectProperty(None)
    cuisine = ObjectProperty(None)
    price = ObjectProperty(None) 
    current = ""
    
    def match(self):
        if self.oldName.text != "":
            self.namee.text, self.cuisine.text, self.price.text = db_partner.match_food(self.oldName.text, self.current)
            if self.namee.text == -1:
                self.reset()
                invalidFood()
        else:
            self.reset()
            invalidFood() 
    
    def update(self):
        try:
            if self.namee.text != "" and self.cuisine.text != "" and self.price.text != "" and self.price.text.isdigit():
                db_partner.update_food(self.oldName.text, self.namee.text, self.cuisine.text, self.price.text, self.current)
                self.reset()
                updateDatabase()
            else:
                raise Exception()
        except:
            invalidFoodUpdate() 
            
    def reset(self):
        self.oldName.text = ""
        self.namee.text = ""
        self.cuisine.text = ""
        self.price.text = ""

class MainWindow(Screen):
    current = ""
    
    def delete(self):
        db_user.delete_user(self.current)
        updateDatabase()

class ViewWindow(Screen):
    current = ""
    
    namee = ObjectProperty(None)
    address = ObjectProperty(None)
    
    def on_enter(self, *args):
        _, n, a, _ = db_user.get_user(self.current)
        self.namee.text = n
        self.address.text = a
    
    def update(self):
        if self.namee.text != "" and self.address.text != "":
            db_user.update_user(self.current, self.namee.text, self.address.text)
            updateDatabase()
            self.reset()
        else:
            invalidForm()
            
    def reset(self):
        self.namee.text = ""
        self.address.text = ""        

class OrderWindow(Screen):
    
    namee = ObjectProperty(None)
    cuisine = ObjectProperty(None)
    current = ""
    
    def match_restaurant(self):
        if self.namee.text != "":
            food = db_partner.match_restaurant(self.namee.text)
            if food == -1:
                self.reset()
                invalidRestaurant()
        else:
            self.reset()
            invalidRestaurant()
            
    def match_cuisine(self):
        if self.cuisine.text != "":
            food = db_partner.match_restaurant(self.namee.text)
            if not db_partner.match_cuisine(food, self.cuisine.text):
                self.reset()
                invalidCuisine()
        else:
            self.reset()
            invalidCuisine()
    
    
    
    def reset(self):
        self.cuisine.text = ""
        self.namee.text = ""
    
class WindowManager(ScreenManager):
    pass


def invalidLogin():
    pop = Popup(title='Invalid Login',
                  content=Label(text='Invalid username or password.'),
                  size_hint=(None, None), size=(400, 400))
    pop.open()


def invalidForm():
    pop = Popup(title='Invalid Form',
                  content=Label(text='Please fill in all inputs with valid information.'),
                  size_hint=(None, None), size=(400, 400))

    pop.open()
    
def invalidCuisine():
    pop = Popup(title='Invalid Cuisine',
                  content=Label(text='The restaurant does not serve any dish belonging to this cuisine.'),
                  size_hint=(None, None), size=(500, 400))

    pop.open()

def invalidFood():
    pop = Popup(title='Invalid Entry',
                  content=Label(text='This dish is not available in records.'),
                  size_hint=(None, None), size=(400, 400))

    pop.open()
    
def invalidRestaurant():
    pop = Popup(title='Invalid Entry',
                  content=Label(text='This restaurant is not available in records.'),
                  size_hint=(None, None), size=(400, 400))

    pop.open()
    
def invalidFoodUpdate():
    pop = Popup(title='Invalid Entry',
                  content=Label(text='Please check the updated entries. '),
                  size_hint=(None, None), size=(400, 400))

    pop.open()

def updateDatabase():
    db_user = DataBase("users.txt")
    db_partner = DataBase("restaurants.txt")

kv = Builder.load_file("my.kv")

sm = WindowManager()

db_user = DataBase("users.txt")
db_partner = DataBase("restaurants.txt")


screens = [LoginWindow(name="login"), CreateAccountWindow(name="create"),MainWindow(name="main"), HomeWindow(name="home"), PartnerLoginWindow(name="partnerlogin"), PartnerCreateAccountWindow(name="partnercreate"), PartnerMainWindow(name="partnermain"), AddFood(name="addfood"), UpdateFood(name="updatefood"), ViewWindow(name="view"), OrderWindow(name="order")]
for screen in screens:
    sm.add_widget(screen)

sm.current = "home"


class MyMainApp(App):
    def build(self):
        return sm


if __name__ == "__main__":
    MyMainApp().run()
