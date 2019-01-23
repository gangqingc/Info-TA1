from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.core.window import Window
from random import random, randrange
from kivy.graphics import Color, Rectangle
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from functools import partial
from kivy.graphics.instructions import InstructionGroup
from kivy.uix.spinner import Spinner, SpinnerOption


class Mywidget(Widget):
    SnakeX = [300, 280, 260, 240]     # définir des attributs
    SnakeY = [300, 300, 300, 300]
    direction = [0, 20]
    snake = InstructionGroup()
    food = InstructionGroup()
    foodx = randrange(0, 200, 20)
    foody = randrange(100, 300, 20)
    score = 0
    count = 1
    speed = 1

    def __init__(self, **kwargs):
        super(Mywidget, self).__init__(**kwargs)
        self.canvas.clear()
        Clock.schedule_once(self.get_speed)

    def get_speed(self, args):     #définir la vitesse
        Clock.unschedule(self.draw_snake)
        Clock.schedule_interval(self.draw_snake, 1. / (len(self.SnakeX) + self.speed))  #plus longue le serpent, plus vite il se déplace

    def play_again(self, args):     #définir la fonction de rejouer
        print ('rejouer')
        self.canvas.clear()
        self.SnakeX = [300, 280, 260, 240]    #initialiser la position du serpent
        self.SnakeY = [300, 300, 300, 300]
        self.direction = [0, 20]
        self.snake = InstructionGroup()
        self.food = InstructionGroup()
        self.foodx = randrange(0, 300, 20)
        self.foody = randrange(100, 300, 20)
        self.count = 1
        self.score = 0        #initialiser le score
        self.getscore()

    def on_touch_down(self, touch):   #la fonction combinée la positon du touch et la direction du serpent
        if self.direction[0] == 0:
           if self.SnakeX[0] - touch.x > 0:
              self.direction = [-20, 0]
           else:
              self.direction = [20, 0]
        else:
           if self.SnakeY[0] - touch.y > 0:
              self.direction = [0, -20]
           else:
              self.direction = [0, 20]


    def changelevel(self, instance, value):  #les 3 degrés de difficulté qui ont 3 différent vitesses
         if value == 'level':
            return
         instance.text = value
         if value == 'easy':
            self.speed = 5
            self.get_speed(self)
         elif value == 'normal':
             self.speed = 30
             self.get_speed(self)
         else:
             self.speed = 100
             self.get_speed(self)


    def draw_snake(self, args):      #définir la forme du serpent

          if (self.SnakeX[0] + self.direction[0] == self.SnakeX[1] and self.SnakeY[0] + self.direction[1] == self.SnakeY[1]):
              self.direction *= -1                       #définir la direction du serpent
          if self.isdead() == False:
              self.snakefunc(self)
              self.canvas.remove(self.snake)
              self.snake = InstructionGroup()
              for i in range(len(self.SnakeX)):
                  self.snake.add(Color(1, 0, 0, 1))        #définir la couleur du serpent
                  self.snake.add(Rectangle(pos=(self.SnakeX[i], self.SnakeY[i]), size=(20, 20)))

              self.draw_food()
              self.canvas.add(self.snake)
          else:
              self.gameover()

    def draw_food(self):             #définir la forme du petit carreau
        self.canvas.remove(self.food)
        self.food = InstructionGroup()
        self.food.add(Color(1, 0, 1, 1))
        self.food.add(Rectangle(pos=(self.foodx, self.foody), size=(20, 20)))
        self.canvas.add(self.food)


    def random_food(self):          # définir la distribution aléatoire du petit carreau

         self.foodx = randrange(0, self.width, 20)
         self.foody = randrange(100, self.height, 20)
         for i in range(0, len(self.SnakeX) - 1):
             if self.foodx == self.SnakeX[i] and self.foody == self.SnakeY[i]:
                self.random_food()


    def snakefunc(self, args):   # définir les fonctions de base du serpent
         new_X = self.SnakeX[0] + self.direction[0]
         new_Y = self.SnakeY[0] + self.direction[1]
         self.SnakeX.insert(0, new_X)
         self.SnakeY.insert(0, new_Y)

         if self.iseated() == True:
            self.random_food()
            self.get_speed(self)
         else:

           del self.SnakeX[-1]
           del self.SnakeY[-1]


    def iseated(self):     # définir le résultat de manger un aliment
        if self.foodx == self.SnakeX[0] and self.foody == self.SnakeY[0]:
            self.score += 10
            print(self.score)
            self.getscore()
            return True


    def isdead(self):   # définir les situations de mort de serpent
        if self.SnakeX[0] < 0 or self.SnakeX[0] > Window.width or self.SnakeY[0] < self.y or self.SnakeY[0] > Window.height:
            return True
        for i in range(1, len(self.SnakeX) - 1):
            if self.SnakeX[i] == self.SnakeX[0] and self.SnakeY[i] == self.SnakeY[0]:
                return True
        return False


    def gameover(self):  # définir la situation de "game over"
        self.canvas.clear()
        with self.canvas:
            Rectangle(source='mali.jpg', pos=self.pos, size=self.size)


    def getscore(self):
        self.label.text = 'score  ' + str(self.score)


class SnakeApp(App):

    def build(self):  # définir la structure de base de ce jeu
        wid = Mywidget()

        btn = Button(text='rejouer', on_press=partial(wid.play_again))
        speedlevel = Spinner(
            text='level',
            values=('easy', 'normal', 'hard'))
        speedlevel.bind(text=wid.changelevel)

        layout = BoxLayout(size_hint=(1, None), height=100)
        label = Label(text='score  0')
        wid.label = label
        layout.add_widget(label)
        layout.add_widget(speedlevel)
        layout.add_widget(btn)
        root = BoxLayout(orientation='vertical')
        root.add_widget(wid)
        root.add_widget(layout)

        return root


if __name__ == '__main__':
    SnakeApp().run()