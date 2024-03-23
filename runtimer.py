#!/usr/bin/env python3
# Made by Severnarch on GitHub
import tkinter as tk, time as _time, math, tkinter.font as tkf, os, psutil, keyboard

app = tk.Tk()
app.geometry("140x46")
app.config(bg="#000000")
app.title("Run Timer | 1.0.1")
app.attributes("-topmost", True)
app.resizable(False, False)

font = tkf.Font(**tkf.nametofont("TkFixedFont").configure())
font.configure(size=15)
hfnt = tkf.Font(**tkf.nametofont("TkFixedFont").configure())
hfnt.configure(size=9)

lbl = tk.Label(app, text="00:00:00.00", font=font, width=20, fg="#ff0000", bg="#000000", anchor='w')
lbl.place(x=1,y=0)
stm = tk.Label(app, text="STOPPED | 999.99MB", font=hfnt, width=20, fg="#ff0000", bg="#000000", anchor='w')
stm.place(x=0,y=22)

def time(time:float=0.01):
	ms = str(time).split(".")[1][0:2]
	ss = str(math.floor(time%60))
	mn = str(math.floor((time/60)%60))
	hr = str(math.floor(((time/60)/60)%60))
	if len(ms) == 1: ms = "0" + ms
	if len(ss) == 1: ss = "0" + ss
	if len(mn) == 1: mn = "0" + mn
	if len(hr) == 1: hr = "0" + hr

	return f"{hr}:{mn}:{ss}.{ms}"

start = _time.time()
reseq = False
state = 0
def loop():
	global reseq, start
	stxt = ""
	if reseq:
		start = -1
		reseq = False
	match state:
		case 0:
			lbl.config(fg="#ff0000")
			stm.config(fg="#ff0000")
			stxt = "STOPPED"
			start = -1
		case 1:
			lbl.config(fg="#00ff00")
			stm.config(fg="#00ff00")
			if start == -1:
				start = _time.time()
			lbl.config(text=time(_time.time()-start))
			stxt = "ACTIVE "
		case 2:
			lbl.config(fg="#ff7700")
			stm.config(fg="#ff7700")
			stxt = "PAUSED "
	mem = (psutil.Process().memory_full_info().rss/1024**2)/2
	mem = mem + (mem/12.34)
	mem = str(mem).split(".")
	mem = ("  ~"+mem[0] if int(mem[0])<10 else " ~"+mem[0] if int(mem[0])<100 else "~"+mem[0])+"."+mem[1][0:2]
	stm.config(text=stxt+"   "+str(mem)+"MB")
	app.after(50, loop)

def setstate(ntate):
	global state, start, reseq
	if state != 0 and ntate == 0:
		start = -1
		reseq = True
	state = ntate
keyboard.add_hotkey("Pause", lambda:setstate(1 if state == 2 else 2))
keyboard.add_hotkey("End",   lambda:setstate(0 if state == 1 or state == 2 else 1))

app.after(50, loop)
app.mainloop()
