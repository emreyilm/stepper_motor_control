
from Tkinter import Tk, Text, BOTH, W, N, E, S, StringVar, Entry
from ttk import Frame, Button, Label, Style
import serial
import time

running = True  # Global flag

class StepperDriver(Frame):
  
    def __init__(self, master):

        Frame.__init__(self, master)   
        
        self.master = master
        self.initGUI()
        self.usbport = USBport()
        
        
    def initGUI(self):
      
		self.master.title("Stepper Motor Control Panel")
		self.pack(fill=BOTH, expand=True)

		self.columnconfigure(1, weight=1)
		self.columnconfigure(3, pad=5)
		self.rowconfigure(4, weight=1)
		self.rowconfigure(5, pad=7)

		lbl = Label(self, text="Coil Sequence")
		lbl.grid(sticky=W, pady=4, padx=5)

		self.user_step = 0
		self.formed_step_list=False
		self.step_holder=[]
		self.stop=False

		self.entry1 = Text(self)
		self.entry1.grid(row=1, column=0, columnspan=2, rowspan=6, 
		    padx=5, sticky=E+W+S+N)

		self.current_step = StringVar()
		lbl2 = Label(self, text="", textvariable=self.current_step)
		lbl2.grid(row=1, column=3)

		abtn = Button(self, text="Apply Single Step", command=self.single_step)
		abtn.grid(row=2, column=3)

		lbl3 = Label(self, text="Continuous motion")
		lbl3.grid(row=3, column=3, rowspan=1, columnspan=1)

		lbl4 = Label(self, text="Delay between steps (ms)")
		lbl4.grid(row=4, column=3, rowspan=1, columnspan=1)

		self.delay = StringVar()
		entry2 = Entry(self, textvariable=self.delay)
		entry2.grid(row=5, column=3, rowspan=1, columnspan=1, sticky=W+S+N)

		bbtn = Button(self, text="Continuous Run", command=self.continuous_run)
		bbtn.grid(row=6, column=3)

		cbtn = Button(self, text="STOP", command=self.stop_motor)
		cbtn.grid(row=7, column=3)    

    def stop_motor(self):
    	self.stop=True
        self.usbport.ser.write(b'0 0 0 0 1')

    def single_step(self):
    	self.stop=False
    	if self.formed_step_list == False:
	    	step = self.entry1.get('1.0', 'end-1c').splitlines()
	    	for line in step:
	    		self.step_holder.append(line)
		self.current_step.set(str(self.step_holder[self.user_step]))
        step_data = str(self.step_holder[self.user_step]) + " 0"
        self.usbport.ser.write(bytes(step_data))
        self.user_step += 1

    def continuous_run(self):
        if self.formed_step_list == False:
	    	step = self.entry1.get('1.0', 'end-1c').splitlines()
	    	for line in step:
	    		self.step_holder.append(line)
		self.delay_time=self.delay.get()
		print(self.delay_time)

		def run_the_motor(self):
			length=len(self.step_holder)
	   		print("loop")
	   		self.current_step.set(str(self.step_holder[self.user_step]))
			step_data = str(self.step_holder[self.user_step]) + " 0"
			self.usbport.ser.write(bytes(step_data))
			self.user_step += 1
			if self.user_step == length:
				self.user_step=0
			if self.stop == False:
				#time.sleep(eval(self.delay_time)/1000.0)
				#run_the_motor(self)
				self.master.after(eval(self.delay_time), run_the_motor(self))

		run_the_motor(self)


class USBport:

	def __init__(self):
		#setup the serial port
		usbport = 'dev/ttyACM0'
		self.ser = serial.Serial('/dev/ttyACM0',9600)    

def main():
  
    root = Tk()
    root.geometry("270x300+300+300")
    app = StepperDriver(root)
    root.mainloop()  


if __name__ == '__main__':
    main()  
