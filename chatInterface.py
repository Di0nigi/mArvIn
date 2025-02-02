from ollama import chat 
from ollama import ChatResponse 
import tkinter as tk




class App:
  def __init__(self, root,w,h,model):
    
    self.chat=[]
    self.m=model
    self.r=root
    self.w=w
    self.h=h
    self.r.geometry(f"{self.w}x{self.h}")
    self.r.title("mArvIn")

    self.mFrame=tk.Frame(self.r,bg="black",width=self.w,height=self.h)
    self.mFrame.pack()

    self.activityBar=tk.Frame(self.mFrame,bg="grey",height=self.h,width=self.w//10)
    self.activityBar.place(x=0,y=0)

    self.chatSpace=tk.Frame(self.mFrame,bg="blue",height=self.h,width=self.w-(self.w//10))
    self.chatSpace.place(x=self.w//10,y=0)

    self.chatDisplay=tk.Text(self.chatSpace,bg="black",height=self.h-(self.h//10),width=self.w-(self.w//10),font=("Arial", 12),foreground="green", wrap="word")
    self.chatDisplay.place(x=0,y=0)
    self.chatDisplay.config(state="disabled")

    self.chatField=tk.Text(self.chatSpace,height=self.h//10,width=self.w-(self.w//10)-(self.w//15))
    self.chatField.place(x=0,y=self.h-(self.h//10))

    self.sendBtn=tk.Button(self.chatSpace,width=self.w//15,height=self.h//10,command=self.sendQuery)
    self.sendBtn.place(x=self.w-(self.w//10)-(self.w//15),y=self.h-(self.h//10))

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
      if c%10==0:
        nRep+=f"{x}\n"
      else:
        nRep+=f"{x} "
      c+=1
    #self.chatDisplay.config(text=reply,foreground="white")

    self.chatDisplay.config(state="normal") 
    self.chatDisplay.insert(tk.END, f"mArvIn: {nRep}\n")
    self.chatDisplay.config(state="disabled")  
    self.chatDisplay.see(tk.END)  

    

    self.chat.append({"role": "assistant", "content": reply})
    #self.mFrame.pack()



    

    return
  
  def run(self):
     self.r.mainloop()
     return
  
  

        


def main():
  root = tk.Tk()
  app = App(root,w=700,h=700,model='llama3.2:3b')
  app.run()
  return

main()