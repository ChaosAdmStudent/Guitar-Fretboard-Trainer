import pygame 
from pygame import display 
from time import sleep 
import os 
from random import randint
from pygame.constants import MOUSEBUTTONDOWN, QUIT

path = 'C:\\Users\\laksh\\Documents\\PyGames\\FretboardTrainer\\'
pygame.init()
screen = display.set_mode((1000, 600)) 

class Fretboard: 

    note = '' 
    notes = ['A','A#','B','C','C#','D','D#','E','F','F#','G','G#']
    
    def __init__(self):
        self.file = ''
        self.string = [7,2,10,5,0,7]
        self.rString = '' 
        self.rFret = 0
        self.answers = Fretboard.get_answers(self) 
        Fretboard.assign_note(self)

    def get_note(self): 
        return self.note 

    def assign_note(self): 
        for file, note in self.answers.items(): 
            flag = randint(0,5) 
            if flag%6 == 0:
                self.note = note 
                self.file = file 
    
    def get_answers(self): 
        answers = {}
        
        directory = os.fsencode(path + 'Fretboard_Pics\\')
        for file in os.listdir(directory):
            filename = os.fsdecode(file)
            self.rString, self.rFret = filename.split('_') 
            self.rString = int(self.rString) 
            self.rFret = int(self.rFret[0])
            answers.update({filename: self.notes[(self.string[self.rString-1] + self.rFret) % 12]}) 

        return answers 

class Game(Fretboard): 

    def __init__(self): 
        Fretboard.__init__(self) 
        display.set_caption("Fretboard Trainer") 
        screen.fill((221, 237, 128)) 
        
        self.icon = pygame.image.load(path + 'img\\' + 'guitar.png') 
        display.set_icon(self.icon)

        self.noteIndex = -1
        Game.make_quiz(self)

        self.score = 0
        self.time = [5,0]
    
    def make_quiz(self): 
        
        COLOR = (255,255,255)
        quiz_notes = [self.note] 
        while len(quiz_notes) < 4: 
            i = randint(0,11) 
            if Fretboard.notes[i] != self.note and Fretboard.notes[i] not in quiz_notes: 
                quiz_notes.append(Fretboard.notes[i]) 
        
        print('\tQuiz Notes: ',quiz_notes)

        font = pygame.font.Font('freesansbold.ttf', 50) 
        self.note_imgs = [] 

        x = i = randint(0,3) 
        while (i+1)%4 != x: 
            self.note_imgs.append(font.render(f'{quiz_notes[i%4]}', True, COLOR)) 
            if quiz_notes[i%4] == self.note: 
                self.noteIndex = len(self.note_imgs) - 1
            i += 1

        self.note_imgs.append(font.render(f'{quiz_notes[i%4]}', True, COLOR)) 
        if quiz_notes[i%4] == self.note: 
            self.noteIndex = len(self.note_imgs) - 1

    def show_quiz(self):  

        screen.blit(self.note_imgs[0], (350, 350))
        screen.blit(self.note_imgs[1], (550, 350))
        screen.blit(self.note_imgs[2], (350, 500))
        screen.blit(self.note_imgs[3], (550, 500)) 
    
    def check_answer(self, note): 
        return note == self.note

             
    def background(self): 
        screen.fill((221, 237, 128)) 
        fretboard = pygame.image.load(path + 'Fretboard_Pics\\' + f'{ self.file}') 
        screen.blit(fretboard, (100, 100))

        COLOR = (0,0,0)
        font = pygame.font.Font('freesansbold.ttf', 35)  
        scoreText = font.render(f'Score: {self.score}', True, COLOR) 
        screen.blit(scoreText, (750,500))

    def start_screen(self): 
        pass 

    def win_screen(self): 
        tick = pygame.image.load(path + 'img\\tick.png') 
        x = y = int()

        if self.noteIndex == 0: 
            x,y = 350 +70,350
        
        elif self.noteIndex == 1: 
            x,y = 550 +70,350 
        
        elif self.noteIndex == 2: 
            x,y = 350+70,500 

        elif self.noteIndex == 3: 
            x,y = 550+70,500

        screen.blit(tick, (x,y)) 

    def lose_screen(self, wrong_x, wrong_y):
        '''
        wrong_x : x-coordinate of wrong box 
        wrong_y : y-coordinate of wrong box 
        ''' 
        cross = pygame.image.load(path + 'img\\cross.png')

        Game.win_screen(self) 
        screen.blit(cross, (wrong_x+70,wrong_y)) 

    def update_score(self): 
        self.score += 1
        
    def update_time(self):     
        if self.time[0] == 0 and self.time[1] == 0: 
            print('\t Time up! ') 
        
        if self.time[1] == 0:
            self.time[1] = 59 
            if self.time[0] != 0: 
                self.time[0] -= 1 
        
        else: 
            self.time[1] -= 1

        font = pygame.font.Font('freesansbold.ttf', 35)  
        scoreText = font.render(f'{self.time[0]}:{self.time[1]}', True, (255,255,255)) 
        screen.blit(scoreText, (750,50))
    
    def update_game(self): 
        self.assign_note() 
        self.make_quiz() 


class Box(pygame.sprite.Sprite): 

    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self) 
        self.image = pygame.Surface((64,50))
        self.image.fill((28, 140, 153)) 
        self.rect = self.image.get_rect()
        self.rect.x = x 
        self.rect.y = y 

    def update(self): 
        self.image.fill((28, 140, 153))  

#Executable 
if __name__ == '__main__': 

    #Setup 
    print('Game Log: ') 
    running = True 
    
    app = Game() 
    print('\t Current Note: ', app.get_note())

    boxes = pygame.sprite.Group() 
    box1 = Box(350,350) 
    box2 = Box(550,350) 
    box3 = Box(350,500) 
    box4 = Box(550,500) 

    boxes.add(box1)
    boxes.add(box2)
    boxes.add(box3)
    boxes.add(box4)

    clock = pygame.time.Clock()

    #Loop
    while running: 
        for event in pygame.event.get(): 
            if event.type == QUIT: 
                print('\tYou quit from the app\n')
                running = False
            
            if event.type == MOUSEBUTTONDOWN: 
                pos = pygame.mouse.get_pos() 
            
                for i, box in enumerate(boxes): 
                    if i == app.noteIndex and box.rect.collidepoint(pos): 
                        print('\tYou chose the correct note!') 
                        app.update_score() 
                        app.win_screen() 
                        display.update() 
                        sleep(1) 
                        app.update_game() 
                    
                    elif box.rect.collidepoint(pos): 
                        print('\tYou chose the wrong note!')
                        app.lose_screen(box.rect.x, box.rect.y) 
                        display.update() 
                        sleep(1) 
                        app.update_game() 
        
        for box in boxes:
            if box.rect.collidepoint(pygame.mouse.get_pos()): 
                box.image.fill((207, 70, 132))

        app.background() 
        boxes.draw(screen)
        app.show_quiz() 
        boxes.update()
        # app.update_time()
        display.update()
        # clock.tick(1)

    print('Thank you for using Fretboard Trainer by Lakshya!')