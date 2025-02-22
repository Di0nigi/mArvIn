from ollama import chat 
import tkinter as tk
from tkinter import filedialog
import genanki as gk
import pyttsx3
from joblib import Parallel, delayed
import threading



class App:
  def __init__(self, root, w, h, model):
    self.chat = []
    self.currentFile=None
    self.m = model
    self.r = root
    self.w = w
    self.h = h
    self.r.geometry(f"{self.w}x{self.h}")
    self.r.title("mArvIn")

    self.engine = pyttsx3.init()
    self.engine.setProperty('rate', 290)
    #self.engine.setProperty('voice', 1)
    self.initModel()
     
    self.mFrame = tk.Frame(self.r, bg="black")
    self.mFrame.pack(fill="both", expand=True)
       
    self.activityBar = tk.Frame(self.mFrame, bg="black", width=self.w // 10)
    self.activityBar.pack(side="left", fill="y")
   
    self.chatSpace = tk.Frame(self.mFrame, bg="blue")
    self.chatSpace.pack(side="right", fill="both", expand=True)

        
    self.chatDisplay = tk.Text(
    self.chatSpace,
            bg="black",
            font=("Courier New", 12),
            foreground="light green",
            wrap="word",
            state="disabled"
        )
    self.scrollbar = tk.Scrollbar(self.chatSpace, command=self.chatDisplay.yview)
    self.chatDisplay.config(yscrollcommand=self.scrollbar.set)

    self.scrollbar.pack(side="right", fill="y")
    self.chatDisplay.pack(side="top", fill="both", expand=True)

        
    self.inputFrame = tk.Frame(self.chatSpace, bg="blue")
    self.inputFrame.pack(side="bottom", fill="x")

    self.chatField = tk.Text(self.inputFrame, height=3, font=("Courier New", 12))  
    self.chatField.pack(side="left", fill="x", expand=True, ipady=5)  

    self.sendBtn = tk.Button(
          self.inputFrame,
            text="Send",
            font=("Courier New", 9),
            command=self.sendQuery
        )
    self.sendBtn.pack(side="right", fill="y", ipady=5)
    self.docBtn = tk.Button(
          self.inputFrame,
            text="Doc",
            font=("Courier New", 9),
            command=self.importFile
        )
    self.docBtn.pack(side="right", fill="y", ipady=5)

    self.intiSettingsBar()
      
  def intiSettingsBar(self):
    self.elaBtn = tk.Button(
          self.activityBar,
            text="Elab",
            font=("Courier New", 9),
            command=self.elaborateFile
        )
    self.elaBtn.pack(side="top", fill="x", ipady=5)

    self.cardBtn = tk.Button(
          self.activityBar,
            text="Cards",
            font=("Courier New", 9),
            command=self.makeCards
        )
    self.cardBtn.pack(side="top", fill="x", ipady=5)



    return
  def importFile(self):
    self.currentFile=filedialog.askopenfilename(
        title="Select a File",
        filetypes=[("All files", "*.*")]
    )
    self.fileContent=""
    with open(self.currentFile, mode="r",encoding="utf-8") as f:
      for line in f:
        self.fileContent+=line
    
    self.chatDisplay.config(state="normal") 
    self.chatDisplay.insert(tk.END, f"----File uploaded----\n")
    self.chatDisplay.config(state="disabled")  
    self.chatDisplay.see(tk.END) 

    self.chatDisplay.config(state="normal") 
    self.chatDisplay.insert(tk.END, f"\n")
    self.chatDisplay.config(state="disabled")  
    self.chatDisplay.see(tk.END) 
    self.chatDisplay.update()

  def elaborateFile(self):

    if self.currentFile:
      
      contextMessage = "Read the following file content, remember it and tell me now VERY shortly, just to now you read it what is it about the file starts now: "
      self.chatDisplay.config(state="normal") 
      self.chatDisplay.insert(tk.END, f"You: Elaborate the file \n")
      self.chatDisplay.config(state="disabled")  
      self.chatDisplay.see(tk.END)

      self.chatDisplay.config(state="normal") 
      self.chatDisplay.insert(tk.END, f"\n")
      self.chatDisplay.config(state="disabled")  
      self.chatDisplay.see(tk.END)

      query = contextMessage+self.fileContent
      self.chat.append({"role": "user", "content": query})

      response = chat(model=self.m, messages=self.chat)

      reply = response['message']['content']

      reply= reply.split(" ")
      nRep=""
      c=1
      for x in reply:
        if c%12==0:
          nRep+=f"{x}\n"
        else:
          nRep+=f"{x} "
        c+=1
      
      self.chatDisplay.config(state="normal") 
      self.chatDisplay.insert(tk.END, f"mArvIn: {nRep}\n")
      self.chatDisplay.config(state="disabled")  
      self.chatDisplay.see(tk.END)  

      self.chatDisplay.update()

      self.talk(nRep)

      self.chat.append({"role": "assistant", "content": nRep})
      #self.mFrame.pack()


    return
  def makeCards(self):
    contextMessage="Use the following file I gave you to extract ALL the most important topics and formulate questions about them, make at least 3 or 4 question per topic wit hdedicated answers and make them different from each other. This is for an anki deck on the topic so they will become cards through an automated method. IT IS CRUCIAL THAT YOUR RESPONSE ONLY CONTAIN THE QUESTIONS IN THE FOLLOWING FORMAT <('Question', 'Answer')> AND NOTHING MORE AT ALL JUST THE QUESTIONS AND ANSWERS FOLLOWING THE FORMAT SEPARATED BY A NEW LINE CHARACTER, AND MAKE SURE TO PUT SINGLE QUOTATION MARKS AROUND THE ANSWER AND QUESTION. The file starts now: "
    if self.currentFile:
      self.chatDisplay.config(state="normal") 
      self.chatDisplay.insert(tk.END, f"You: Make an anki deck\n")
      self.chatDisplay.config(state="disabled")  
      self.chatDisplay.see(tk.END)

      self.chatDisplay.config(state="normal") 
      self.chatDisplay.insert(tk.END, f"\n")
      self.chatDisplay.config(state="disabled")  
      self.chatDisplay.see(tk.END)

      query = contextMessage+self.fileContent
      self.chat.append({"role": "user", "content": query})

      response = chat(model=self.m, messages=self.chat)

      reply = response['message']['content']

      rep = reply.split("\n")
      cards=[]
      for l in rep:
        l=l.replace("(","")
        l=l.replace("\\","")
        l=l.replace(")","")
        t=tuple(l.split(","))
        cards.append(t)
      print(cards)
      

      

      
      #print(reply)
      makeDeck(cards=cards,file="D:\dionigi\Documents\Python scripts\mArvIn\prova.apkg")

      self.chatDisplay.config(state="normal") 
      self.chatDisplay.insert(tk.END, f"mArvIn: I'm done!\n")
      self.chatDisplay.config(state="disabled")  
      self.chatDisplay.see(tk.END)

      self.chatDisplay.config(state="normal") 
      self.chatDisplay.insert(tk.END, f"\n")
      self.chatDisplay.config(state="disabled")  
      self.chatDisplay.see(tk.END) 
      self.chatDisplay.update()

      self.talk("I'm done")


    return
       
  def sendQuery(self):

    query=self.chatField.get("1.0", tk.END).strip()

    self.chatField.delete("1.0", tk.END)
    
    self.chatDisplay.config(state="normal") 
    self.chatDisplay.insert(tk.END, f"You: {query}\n")
    self.chatDisplay.config(state="disabled")  
    self.chatDisplay.see(tk.END)  
    

   
    
    
    #self.mFrame.pack()
    #print(query)

    self.chat.append({"role": "user", "content": query})

    self.chatDisplay.config(state="normal") 
    self.chatDisplay.insert(tk.END, f"\n")
    self.chatDisplay.config(state="disabled")  
    self.chatDisplay.see(tk.END) 
    

    response = chat(model=self.m, messages=self.chat)

    reply = response['message']['content']

    reply= reply.split(" ")
    nRep=""
    c=1
    for x in reply:
      if c%12==0:
        nRep+=f"{x}\n"
      else:
        nRep+=f"{x} "
      c+=1
    
    self.chatDisplay.config(state="normal") 
    self.chatDisplay.insert(tk.END, f"mArvIn: {nRep}\n")
    self.chatDisplay.config(state="disabled")  
    self.chatDisplay.see(tk.END)  

    self.chat.append({"role": "assistant", "content": nRep})
    #self.mFrame.pack()
    self.chatDisplay.config(state="normal") 
    self.chatDisplay.insert(tk.END, f"\n")
    self.chatDisplay.config(state="disabled")  
    self.chatDisplay.see(tk.END) 
    #threading.Thread(target=self.talk, args=("hello world",), daemon=True).start()
    #process=Parallel(n_jobs=1,backend="loky",prefer='processes')
    #process([delayed(self.talk)(nRep)])
    self.chatDisplay.update()
    self.talk(nRep)
    
    

    

    return
  
  def initModel(self):
    initMessage="You are a personal study assistant. Your name is mArvIn and you will help me complete various study and working related task. Feel free to be a bit snarky and funny but always helpful and thorough. this is the first message to which you do not need to reply. From the next message on the conversation will start. When asked to code it is crucial you ALWAYS use camelCase notation unless specifically asked to do otherwise and no matter the language or best practices. Keep the comments on the code separate and after the code. When asked to make anki card or whatever with a strict format it is crucial that you follow it to the letter. In general when I give you a piece of code to fix do not change the variable names or order as much as possible. Thank you for your help."


    self.chat.append({"role": "user", "content": initMessage})
    response = chat(model=self.m, messages=self.chat)
    reply = response['message']['content']
    #print(reply)
    self.chat.append({"role": "assistant", "content": reply})


    return
  
  def talk(self,string):
    self.engine.say(string)
    self.engine.runAndWait()
    return 

  def run(self):
     self.r.mainloop()
     return
  
  

def makeDeck(cards,file):
  model = gk.Model(
    1607392319,
    'Simple Model',
    fields=[
        {'name': 'Question'},
        {'name': 'Answer'}
    ],
    templates=[
        {
            'name': 'Card 1',
            'qfmt': '{{Question}}',  # Front of the card
            'afmt': '{{FrontSide}}<hr id="answer">{{Answer}}',  # Back of the card
        },
    ]
    )

  # Create a deck
  deck = gk.Deck(
      2059400110,
      'My First Anki Deck'
  )
  for question, answer in cards:
    note = gk.Note(
        model=model,
        fields=[question, answer]
    )
    deck.add_note(note)
    
    gk.Package(deck).write_to_file(file)

        


def main():
  root = tk.Tk()
  app = App(root,w=1000,h=700,model='llama3.2:3b')
  app.run()
  return

main()