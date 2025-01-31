import tkinter as tk
import customtkinter as ctk

from PIL import ImageTk, Image
from authtoken import auth_token  # Ensure this module is available and correctly set up

import torch
from torch import autocast
from diffusers import StableDiffusionPipeline

# Create the app
app = tk.Tk()
app.geometry("532x632")
app.title("Stable Bud")
ctk.set_appearance_mode("dark")

prompt = ctk.CTkEntry(app, height=40, width=512, font=("Arial", 20), text_color="black", fg_color="white")
prompt.place(x=10, y=10)

lmain = ctk.CTkLabel(app, height=512, width=512)
lmain.place(x=10, y=110)

modelid = "CompVis/stable-diffusion-v1-4"
#device = "cuda"
device = "cpu"  # Change from "cuda" to "cpu"
pipe = StableDiffusionPipeline.from_pretrained(modelid, revision="fp16", torch_dtype=torch.float16, use_auth_token=auth_token)
pipe.to(device)

def generate_old():
    with autocast(device):
        result = pipe(prompt.get(), guidance_scale=8.5)
        image = result["images"][0]
    
    image.save('generatedimage.png')
    img = ImageTk.PhotoImage(Image.open('generatedimage.png'))
    lmain.configure(image=img)
    lmain.image = img  # Keep a reference to avoid garbage collection

def generate():
    with torch.no_grad():
        result = pipe(prompt.get(), guidance_scale=8.5)
        image = result["images"][0]
    
    image.save('generatedimage.png')
    img = ImageTk.PhotoImage(Image.open('generatedimage.png'))
    lmain.configure(image=img)
    lmain.image = img  # Keep a reference to avoid garbage collection

trigger = ctk.CTkButton(app, height=40, width=120, font=("Arial", 20), text_color="white", fg_color="blue", command=generate)
trigger.configure(text="Generate")
trigger.place(x=206, y=60)

app.mainloop()
