import enchant
import random
from graphics import *
import time, random
d=enchant.Dict("en_US")
win=GraphWin("Cows & Bulls",1500,2000)
win.setBackground(color_rgb(100,100,200))

def word_gen():    
    word="aaaa"
    while(d.check(word)==False or word=="QUIT" or len(set(word))!=4 ): #or len(set(word))!=4
        word=""
        for i in range(4):
            word+=chr(random.randrange(65,90))
    #print(word)
    return word

def game():
    def check(w,g):
        bulls=0
        cows=0
        for i in range(4):
            if w[i]==g[i]:
                bulls+=1
            elif w[i] in g:
                cows+=1
        return(cows,bulls)
    w=word_gen()
    w=w.lower()
    #print("\n"*5)
    i=0
    listw=dict()
    while True:
        i+=1
        g="aaaa"
        while(d.check(g)==False or len(g)!=4):
              #g=input("Enter guess #"+str(i))
              win.flush()
              entry1 = Entry(Point(win.getWidth()/2, 380),10)
              entry1.draw(win)
              Text(Point(win.getWidth()/2, 400),'Guess#'+str(i)).draw(win) # label for the Entry
              win.getMouse()  # To know the user is finished with the text.
              g= entry1.getText() 

        if(g=="quit"):
            win.delete("all")
            t=Text(Point(win.getWidth()/2, 330),"The word was "+str(w)).draw(win)
            t.setStyle("bold")
            t.setSize(25)
            win.getMouse()
            break
        
        g=g.lower()
        #print(list)
        win.flush()
        
        cows,bulls= check(w,g)
        listw.setdefault(g,str(cows)+"C "+str(bulls)+"B")
        Text(Point(win.getWidth()/2, 230),listw).draw(win)
        if bulls==4:
            win.delete("all")
            #print("CORRECT")
            Text(Point(win.getWidth()/2, 250),"CORRECT").draw(win)
            if i==1:
                #print("First try")
                Text(Point(win.getWidth()/2, 280),"First Try").draw(win)
            else:
                #print("You got it in", i, "tries")
                Text(Point(win.getWidth()/2, 280),"You got it in"+str(i)+ "tries").draw(win)
            break
        else:
            win.delete("all")
            Text(Point(win.getWidth()/2, 230),list).draw(win)
            Text(Point(win.getWidth()/2, 300),g+":"+str(cows)+" COWS").draw(win)
            Text(Point(win.getWidth()/2, 350),g+":"+str(bulls)+" BULLS").draw(win)
            #print(cows,"COWS")
            #print(bulls,"BULLS")
choice="y"
while(choice=="y" or choice=="Y"):
    #choice=input("Do you want to play? Enter Y/N")
    choice_e = Entry(Point(win.getWidth()/2, 290),10)
    win.delete("all")
    choice_e.draw(win)   
    t=Text(Point(win.getWidth()/2, 230),"Do you want to play? Enter Y/N")
    t.setStyle("bold italic")
    t.setSize(20)
    t.draw(win)
    win.getMouse()
      # To know the user is finished with the text.
    choice = choice_e.getText()
    win.flush()

    if(choice=="y" or choice=="Y"):
        #system("cls")
        win.delete("all")
        game()
    elif(choice=="n" or choice=="N"):
        #print("OK bye")
        win.delete("all")
        t=Text(Point(win.getWidth()/2, 230),"OK BYE").draw(win)
        t.setStyle("bold")
        t.setSize(25)
        break
    else:
        choice="y"

    
