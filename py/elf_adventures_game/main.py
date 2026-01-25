import arcade
import os
import sys

os.chdir(os.path.dirname(os.path.abspath(__file__)))
#sys.path.append(os.path.dirname(os.path.abspath(__file__)))

#current_dir = os.getcwd()
#print(f"Текущая рабочая директория: {current_dir}")

from game_window import MyGame

def main():
    window = MyGame()
    arcade.run()

if __name__ == "__main__":
    main()