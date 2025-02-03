from ollama import chat 
import tkinter as tk




class App:
  def __init__(self, root, w, h, model):
        self.chat = []
        self.m = model
        self.r = root
        self.w = w
        self.h = h
        self.r.geometry(f"{self.w}x{self.h}")
        self.r.title("mArvIn")

        
        self.mFrame = tk.Frame(self.r, bg="black")
        self.mFrame.pack(fill="both", expand=True)

       
        self.activityBar = tk.Frame(self.mFrame, bg="grey", width=self.w // 10)
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

    

    

    return
  
  def run(self):
     self.r.mainloop()
     return
  
  

        


def main():
  root = tk.Tk()
  app = App(root,w=1000,h=700,model='llama3.2:3b')
  app.run()
  return

main()