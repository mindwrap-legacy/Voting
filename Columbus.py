from tkinter import *
import json
import re
import playsound
import socket
import random
from PIL import Image,ImageTk
from matplotlib.figure import Figure 
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class COLORS:
	BLUE = "#002060"
	RED = "#ff0000"
	GREEN = "#00ff00"
	GREY = "#222222"
	WHITE = "#ffffff"

class ConnectionClient:

	def __init__(self,address,port):
		self.address = address
		self.port = port
		self.connect_network()

	def connect_network(self):
		self.connection = socket.socket()
		self.connection.connect((self.address,self.port))

	def send(self,data):
		d = json.dumps(data).encode()
		total = str(len(d)).encode()
		self.connection.send(total)
		e = self.connection.recv(4)
		print(e)
		start = 0
		while start<len(d)-1:
			start += self.connection.send(d[start:])
		print("sent {}".format(total))
		# print(self.connection.recv(1024))

class MainWindow(Tk):

	def __init__(self,*args,**kwargs):
		self.interface = None if "interface" not in kwargs.keys() else kwargs.pop("interface")
		self.send_data = True
		if self.interface==None:
			self.send_data = False
		super().__init__(*args,**kwargs)
		self.width = 1336
		self.height = 768
		self.font = "Sans"
		self.current_screen = None
		self.result_duration = 5
		self.title_size = 30
		self.isBusy = False
		self.sub_size = 14
		self.results_created = False
		self.screens = []
		self.timeout_duration = 1
		self.screen_index =  0
		self.padding = 20
		self.variables = {}
		self.geometry("{0}x{1}".format(self.width,self.height))


		self.object_file = "voters.obj"
		self.description_file = "voting.desc"
		self.sound_file = "bell.mp3"

		self.var = StringVar()
		self.object_data = self.read_object()
		self.description = self.load_desc()
		self.t_data = {}
		self.candidate_list = self.object_data["candidates"].keys()
		self.voter_list = self.object_data["voters"]
		self.cand =  None
		self.t_data["name"] = self.object_data["information"]["desc"]
		self.t_data["tot_votes"] = len(self.voter_list)
		self.t_data["cat"] = {}
		for candidate,holders in self.object_data["candidates"].items():
			container = {}
			for h_id,h_val in holders.items():
				container[h_id] = [h_val["name"],len(h_val["voters"])]
			self.t_data["cat"][candidate] = container
		# print(self.t_data)


		#TODO OTHERS
		self.create_greet_page()
		self.create_login_page()
		self.create_voting_screens()
		self.create_reset()

		self.set_screen(0)

	def todo(self,event):
		print(dir(event))

	def read_object(self):
		with open(self.object_file) as f:
			object_data = json.load(f)
			f.close()
		return object_data

	def set_screen(self,screen_index):

		if self.current_screen!=None:
			self.current_screen.pack_forget()
		self.screens[screen_index].pack(fill=BOTH,expand=True)
		self.current_screen = self.screens[screen_index]

	def load_desc(self):
		with open(self.description_file) as f:
			description = f.read()
			f.close()
		return description

	def create_login_page(self):
		screen = Frame(self)
		self.voter = StringVar()
		self.warning_text = StringVar()
		body = Frame(screen,bg=COLORS.BLUE)
		Label(body,text="Students Council Elections 2022-2023",fg=COLORS.WHITE,font=(self.font,self.title_size),bg=COLORS.BLUE).pack(anchor="center",padx=10,pady=5)
		Label(body,text="Leadership is the challenge to be more than average",fg=COLORS.WHITE,font=(self.font,self.sub_size),bg=COLORS.BLUE).pack(anchor="center",pady=4)
		body.pack(padx=10,pady=10,fill=BOTH,expand=False)
		body2 = Frame(screen,bg=COLORS.BLUE)
		cont = Frame(body2,bg=COLORS.BLUE)
		Label(cont,text="Enter VoterID: ",font=(self.font,self.sub_size),fg=COLORS.WHITE,bg=COLORS.BLUE).grid(row=0,column=0,padx=4,pady=25)
		self.E1 = Entry(cont,bg=COLORS.GREY,fg=COLORS.WHITE,width=60,textvariable=self.voter,font=(self.font,self.sub_size))
		self.E1.grid(row=0,column=1,padx=4,pady=25)
		Button(cont,text="Vote",bg=COLORS.BLUE,fg=COLORS.WHITE,font=(self.font,self.sub_size-4),command=self.proceed).grid(row=0,column=2)
		self.warning_message = Label(cont,textvariable=self.warning_text,fg=COLORS.RED,bg=COLORS.BLUE,font=(self.font,self.sub_size))
		self.warning_message.grid(row=1,column=1,pady=25)
		self.screens.append(screen)
		cont.pack(anchor="center",expand=False)
		body2.pack(fill=X,padx=10)

		body3 = Frame(screen,bg=COLORS.BLUE)
		Label(body3,text="Important Note",bg=COLORS.BLUE,fg=COLORS.WHITE,font=(self.font,self.title_size)).pack(anchor="center",padx=10,pady=10)
		Label(body3,text=self.description,bg=COLORS.BLUE,fg=COLORS.WHITE,font=(self.font,self.sub_size-4)).pack(anchor="center",padx=10,pady=3)
		body3.pack(padx=10,pady=10,expand=True,fill=BOTH)

	def create_greet_page(self):
		screen = Frame(self)
		head = Frame(screen,bg=COLORS.BLUE)
		Label(head,text="Mount Litera Zee School, Naroli",fg=COLORS.WHITE,font=(self.font,self.title_size),bg=COLORS.BLUE).pack(anchor="center",padx=10,pady=5)
		head.pack(fill=X,expand=False,padx=10,side=TOP,anchor=N,pady=5)
		body = Frame(screen,bg=COLORS.BLUE)
		Label(body,text="Students Council Elections 2022-2023",fg=COLORS.WHITE,font=(self.font,self.title_size),bg=COLORS.BLUE).pack(anchor="center",padx=10,pady=5)
		Label(body,text="Leadership is the challenge to be more than average",fg=COLORS.WHITE,font=(self.font,self.sub_size),bg=COLORS.BLUE).pack(anchor="center",pady=4)
		Button(body,text="Vote",font=(self.font,self.title_size),command=self.move_next,fg=COLORS.WHITE,bg=COLORS.BLUE).place(relx=0.5,rely=0.5,anchor="center")
		body.pack(padx=10,pady=10,expand=True,fill=BOTH)
		self.screens.append(screen)


	def create_voting_screens(self):


		for candidate in self.candidate_list:
			screen = Frame(self)
			self.variables[screen] = StringVar()
			head = Frame(screen,bg=COLORS.BLUE)
			Label(head,text="Students Council Elections 2022-2023",fg=COLORS.WHITE,font=(self.font,self.title_size),bg=COLORS.BLUE).pack(anchor="center",padx=10,pady=5)
			Label(head,text="Leadership is the challenge to be more than average",fg=COLORS.WHITE,font=(self.font,self.sub_size),bg=COLORS.BLUE).pack(anchor="center",pady=4)
			head.pack(fill=X,expand=False,padx=10,side=TOP,anchor=N,pady=5)
			body = Frame(screen,bg=COLORS.BLUE)
			self.cand = Label(body,text="Elect Your {}".format(candidate),font=(self.font,self.title_size-6),bg=COLORS.GREY,fg=COLORS.WHITE)
			self.cand.pack(pady=10)
			
			vote_cont = Frame(body,bg=COLORS.BLUE)
			count = 0
			total = len(self.object_data["candidates"][candidate])
			vote_cont.columnconfigure(index=tuple(range(total)),weight=1,uniform="equal")
			vote_cont.rowconfigure(index=(0),weight=1,uniform="equal")
			for key,value in self.object_data["candidates"][candidate].items():
				node = self.create_vote_entity(value,vote_cont,key,self.width-45,total,self.variables[screen],candidate,screen)
				node.grid(row=0,column=count,padx=5,pady=5)
				count += 1
			vote_cont.pack(expand=True,fill=BOTH,anchor=NW)
			body.pack(expand=True,fill=BOTH,anchor=N,padx=10,pady=5)

			self.screens.append(screen)
		# print(self.variables)

	def create_vote_entity(self,data,parent,can_id,width,n,variable,candidate,screen):
		padding = self.padding
		# print(can_id)
		view = Frame(parent,bg=COLORS.GREY,borderwidth=1)
		image_dim = (width)//n - padding - 5 - 20
		image = Image.open(data["image"])
		crop = image.width if image.width<image.height else image.height
		margin_x = 0 if crop>=image.width else (image.width - crop)//2
		margin_y = 0 if crop>=image.height else (image.height - crop)//2 
		image = image.crop((margin_x,margin_y,crop+margin_x,crop+margin_y))
		IMAGE = ImageTk.PhotoImage(image.resize((image_dim,image_dim),Image.Resampling.LANCZOS))
		l1 = Label(view,image=IMAGE)
		l1.configure(image=IMAGE)
		l1.image = IMAGE
		l1._raw_image = image
		l2 = Radiobutton(view,text=data["name"].title(),value="{0}--{1}".format(can_id,candidate),variable=variable,bg=COLORS.GREY,fg=COLORS.WHITE,command=lambda:self.add_vote(screen),borderwidth=1,font=(self.font,self.sub_size))
		l1.pack(fill=X,expand=True,padx=padding,pady=padding)
		l2.pack(fill=X,padx=10,pady=5)
		view.bind("<Configure>",lambda event:self.resize_all(event,l1))

		return view

	def move_next(self,args=None):
		if not self.isBusy:
			self.set_screen((self.screen_index+1)%len(self.screens))
			self.screen_index += 1
			args() if callable(args) else None
	def resize_all(self,event,label):
		width,height = event.width,event.height
		if width>height:
			crop = height - self.padding
		else:
			crop = width - self.padding
		image = label._raw_image
		image = ImageTk.PhotoImage(image.resize((crop,crop)))
		label.configure(image=image)
		label.image = image

	def eval_text(self,text):
		nums = re.findall(r"\d+",text)
		if len(nums)!=2:
			self.warning_text.set("Your entered value is Invalid!")
			return False
		remain = text.replace(nums[0],"").replace(nums[1],"")
		if not 1<=int(nums[0])<=12:
			self.warning_text.set("Your class is wrong")
			return False
		if not len(remain) == 1:
			self.warning_text.set("Invalid Section")
			return False
		self.warning_text.set("")
		if text.lower() in self.object_data["voters"]:
			self.warning_text.set("You\'ve already voted.")
			return False
		return True

	def proceed(self):
		text = self.voter.get().lower()
		if self.eval_text(text):
			self.object_data["voters"].append(text)
			self.move_next()

	def add_vote(self,screen):
		# print("window is",screen)
		ent,cand = self.variables[screen].get().split("--")
		self.object_data["candidates"][cand][ent]["voters"].append(self.voter.get().lower())
		self.t_data["tot_votes"] = len(self.voter_list)
		self.t_data["cat"][cand][ent][-1] += 1
		if self.send_data:
			self.interface.send(self.t_data)
		self.save_data()
		playsound.playsound(self.sound_file)
		if self.screens.index(screen) == len(self.screens)-2:
			self.reset_data()
		else:
			self.move_next()

	def save_data(self):
		with open(self.object_file,"w") as f:
			json.dump(self.object_data,f,indent=4)
			f.close()

	def create_reset(self):
		reset_string = "Thankyou for Voting\n{0}You Can leave now and watch live results\nI will reset within {1} seconds".format(self.voter.get().upper(),self.timeout_duration)
		screen = Frame(self,bg=COLORS.BLUE)
		Label(screen,text=reset_string,font=(self.font,self.sub_size),bg=COLORS.BLUE,fg=COLORS.WHITE).place(relx=0.5,rely=0.5,anchor=CENTER)
		Button(screen,text="Thank You",font=(self.font,self.sub_size),bg=COLORS.BLUE,fg=COLORS.WHITE,command=self.show_results).place(relx=0.8,rely=0.8,anchor=CENTER)

		self.screens.append(screen)
	
	def reset_data(self):
		self.voter.set("")
		if not self.results_created:
			self.create_results()
			self.results_created = True
		else:
			self.update_result()
		self.move_next()
		self.after(self.timeout_duration*1000,self.move_next)

	def show_results(self):
		self.current_screen.pack_forget()
		self.result_window.pack(expand=True,fill=BOTH)
		self.current_screen = self.result_window
		self.isBusy = True
		self.after(self.result_duration*1000,self.end_results)

	def end_results(self):
		self.isBusy = False
		self.move_next()

	def create_results(self):
		self.result_window = Frame(self)
		self.colors = []
		Label(self.result_window,text="Result Summary",fg=COLORS.WHITE,bg=COLORS.BLUE,font=(self.font,self.title_size)).pack(fill=X,expand=True)
		# self.colors.append()
		self.figure = Figure(figsize=(10,5),dpi=100)
		self.plots =  []
		for i in range(len(self.t_data["cat"])):
			self.plots.append(self.figure.add_subplot(121+i))
		count = 0
		for cats in self.t_data["cat"].keys():
			labels = [i[0] for i in self.t_data["cat"][cats].values()]
			values = [i[1] for i in self.t_data["cat"][cats].values()]
			tmp = []
			for i in range(len(values)):
				color = ''.join([hex(random.randint(0,255)).split("x")[1] for i in range(3)])
				if len(color)<6:
					color += "f"*(6-len(color))
				tmp.append("#"+color)
			self.colors.append(tmp)

			patch = self.plots[count].pie(values,autopct="%1.1f%%",colors=self.colors[count])
			self.plots[count].legend(patch[0],labels,loc="lower right")
			self.plots[count].title.set_text(cats)
			count += 1

		self.widget = FigureCanvasTkAgg(self.figure,master=self.result_window)
		self.widget.draw()
		self.widget.get_tk_widget().pack(fill=BOTH,expand=True,pady=10,padx=10)

		# self.screens.append(self.result_window)
		result = Frame(self.result_window,bg=COLORS.BLUE)
		Label(result,text="This result is for {} seconds only".format(self.result_duration),font=(self.font,self.sub_size),bg=COLORS.BLUE,fg=COLORS.WHITE).pack(pady=3,padx=4,anchor=CENTER)
		result.pack(fill=X)

		# self.update_result()
	def update_result(self):
		count = 0
		for cats in self.t_data["cat"].keys():
			self.plots[count].clear()
			labels = [i[0] for i in self.t_data["cat"][cats].values()]
			values = [i[1] for i in self.t_data["cat"][cats].values()]
			print(labels,values)
			patch = self.plots[count].pie(values,autopct="%1.1f%%",colors=self.colors[count])
			self.plots[count].legend(patch[0],labels,loc="lower right")
			self.plots[count].title.set_text(cats)
			count += 1
		self.widget.draw()




def connect(ip,port,error,root,con):
	try:
		connection = ConnectionClient(ip.get(),port.get())
		con.append(connection)
		root.destroy()

	except Exception as e:
		error.set("Error: "+str(e))



def create_connection():
	root = Tk()
	port = IntVar()
	ip = StringVar()
	connection = []
	error = StringVar()
	frame = Frame(root)
	Label(frame,text="Want to create live connection for Columbus?").pack(padx=10,pady=10)
	frame2 = Frame(frame)
	Label(frame2,text="Enter IP of Server: ").grid(row=0,column=0)
	E1 = Entry(frame2,width=20,textvariable=ip)
	E1.grid(row=0,column=1)
	Label(frame2,text="Enter Port of Server: ").grid(row=1,column=0)
	E2 = Entry(frame2,width=20,textvariable=port)
	E2.grid(row=1,column=1)
	Button(frame2,text="No, Just Run",fg=COLORS.RED,activebackground=COLORS.RED,command=root.destroy).grid(row=2,column=0)
	Button(frame2,text="Connect",fg=COLORS.GREEN,activebackground=COLORS.GREEN,command=lambda :connect(ip,port,error,root,connection)).grid(row=2,column=1)
	frame2.pack(anchor="center")
	Label(frame,textvariable=error,fg=COLORS.RED).pack(pady=10)
	frame.pack(expand=True,fill=BOTH)
	root.mainloop()
	return connection
connection = create_connection()
window = MainWindow()
if len(connection):
	window.interface = connection[0]
	window.send_data = True

window.mainloop()
