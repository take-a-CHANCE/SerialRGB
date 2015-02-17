'''
Created on Mar 30, 2014

Requires PySerial and PyGTK

***************WorkLog******************
5/7/14: initial install of pyserial and pygtk, loading up of code I worked on previously
5/8/14: testing methods to make scales change when new scale selected
5/8/14: debugging
5/12/14: Completely redid arduino code, changed python to reflect changes
5/13/14: debugged problems with values changing. Increased baud rate
5/14/14: added in new line '\n' after each command sent to arduino to fix problems with colors mixing
5/15/14: Clear now sets scales to zero, switching between strands makes scales move to stored previous values 
        by making scales global variables; added brightness slider and blink functionality
5/16/14: Final debugging, added bright and speed scales to clear function
2/16/15: Added a COM Port selector and Jump button
2/16/15: work on adding text box entry for nums
2/17/15: changed text boxes to spin boxes 

****************************************

'''

import gtk
import sys
import serial
import time
import glob

global rgb1
global rgb2
global rgb3

global speed
speed=0
global brightness
brightness=0

global rScale
rScale = gtk.HScale()
global gScale
gScale = gtk.HScale()
global bScale
bScale = gtk.HScale()
global sScale
sScale = gtk.HScale()
global brightScale
brightScale = gtk.HScale()

global portList
portList = gtk.combo_box_new_text()

global rSpin
rSpin =gtk.SpinButton(gtk.Adjustment(value=0, lower=0, upper=255, step_incr=1, page_incr=5, page_size=0),0,0)
global gSpin
gSpin =gtk.SpinButton(gtk.Adjustment(value=0, lower=0, upper=255, step_incr=1, page_incr=5, page_size=0),0,0)
global bSpin
bSpin =gtk.SpinButton(gtk.Adjustment(value=0, lower=0, upper=255, step_incr=1, page_incr=5, page_size=0),0,0)
global brightSpin
brightSpin =gtk.SpinButton(gtk.Adjustment(value=0, lower=0, upper=255, step_incr=1, page_incr=5, page_size=0),0,0)
global sSpin
sSpin =gtk.SpinButton(gtk.Adjustment(value=0, lower=0, upper=1500, step_incr=1, page_incr=5, page_size=0),0,0)

rgb1 = [0,0,0]
rgb2 = [0,0,0]
rgb3 = [0,0,0]


class PyApp(gtk.Window):

    def __init__(self):

        super(PyApp, self).__init__()
        

        self.set_title("RGB Control")
        self.set_size_request(300, 275)
        self.set_position(gtk.WIN_POS_CENTER)
    
        headerVbox = gtk.VBox(True,0)
        headerLabel1 = gtk.Label("RGB Control App for Arduino")
        headerVbox.pack_start(headerLabel1)

        #Serial Selector
        ports = self.serial_ports()
        serialTable = gtk.Table(1,2,False)
        for port in ports:
            portList.append_text(port)
        connectButton = gtk.Button("Connect")
        connectButton.set_name("connect");
        connectButton.connect("clicked", self.on_button)
        serialTable.attach(portList, 0,1,0,1)
        serialTable.attach(connectButton,1,2,0,1)
        
        # Radio Buttons
        buttonTable = gtk.Table(1,3, False)
        
        button1 = gtk.RadioButton(None, "Strand 1")
        button1.connect("toggled", self.radio_buttons, "1")
     
        button2 = gtk.RadioButton(button1, "Strand 2")
        button2.connect("toggled", self.radio_buttons, "2")
        
        button3 = gtk.RadioButton(button1, "Both")
        button3.connect("toggled", self.radio_buttons, "3")
        button3.set_active(True)
        
        buttonTable.attach(button1, 0,1,0,1)
        buttonTable.attach(button2, 1,2,0,1)
        buttonTable.attach(button3, 2,3,0,1)
        
        #Red slider
        rHbox = gtk.HBox(True,0)
        rLabel = gtk.Label("Red:         ")
        rHbox.pack_start(rLabel)
        
        #spin box 
        rSpin.set_name("red")
        rSpin.connect("value-changed",self.spin_changed)
        rHbox.pack_start(rSpin)

        rScale.set_name("red")
        rScale.set_range(0, 255)
        rScale.set_increments(1, 10)
        rScale.set_digits(0)
        rScale.set_size_request(130, 35)
        rScale.set_draw_value(False)
        rScale.connect("value-changed", self.on_changed)
        rHbox.pack_end(rScale)
        
        #green slider
        gHbox = gtk.HBox(True,0)
        gLabel = gtk.Label("Green:       ")
        gHbox.pack_start(gLabel)
        
        gSpin.set_name("green")
        gSpin.connect("value-changed",self.spin_changed)
        gHbox.pack_start(gSpin) 
        
        gScale.set_name("green")
        gScale.set_range(0, 255)
        gScale.set_increments(1, 10)
        gScale.set_digits(0)
        gScale.set_size_request(130, 35)
        gScale.set_draw_value(False)
        gScale.connect("value-changed", self.on_changed)
        gHbox.pack_end(gScale)
        
        #blue slider
        bHbox = gtk.HBox(True,0)       
        bLabel = gtk.Label("Blue:        ")
        bHbox.pack_start(bLabel)
        
        bSpin.set_name("blue")
        bSpin.connect("value-changed",self.spin_changed)
        bHbox.pack_start(bSpin)   

        bScale.set_name("blue")
        bScale.set_range(0, 255)
        bScale.set_increments(1, 10)
        bScale.set_digits(0)
        bScale.set_size_request(130, 35)
        bScale.set_draw_value(False)
        bScale.connect("value-changed", self.on_changed)
        bHbox.pack_end(bScale)
        
        #speed slider
        sHbox = gtk.HBox(True,0)
        sLabel = gtk.Label("Speed:       ")
        sHbox.pack_start(sLabel)

        sSpin.set_name("speed")
        sSpin.connect("value-changed",self.spin_changed)
        sHbox.pack_start(sSpin) 
        
        sScale.set_name("speed")
        sScale.set_range(0,1500)
        sScale.set_increments(1, 5)
        sScale.set_digits(0)
        sScale.set_size_request(130, 35)
        sScale.set_draw_value(False)
        sScale.connect("value-changed", self.on_changed)
        sHbox.pack_end(sScale)
        
        #brightness slider
        brightHbox = gtk.HBox(True,0)
        brightLabel = gtk.Label("Brightness: ")
        brightHbox.pack_start(brightLabel)

        brightSpin.set_name("bright")
        brightSpin.connect("value-changed",self.spin_changed)
        brightHbox.pack_start(brightSpin) 
        
        brightScale.set_name("bright")
        brightScale.set_range(0,255)
        brightScale.set_increments(1, 10)
        brightScale.set_digits(0)
        brightScale.set_size_request(130, 35)
        brightScale.set_draw_value(False)
        brightScale.connect("value-changed", self.on_changed)
        brightHbox.pack_end(brightScale)
        
        #function buttons
        boxTable = gtk.Table(1,4,False)
        
        fadeButton = gtk.Button("Fade")
        fadeButton.set_name("fade")
        fadeButton.connect("clicked", self.on_button)
        
        clearButton = gtk.Button("Clear")
        clearButton.set_name("clear")
        clearButton.connect("clicked", self.on_button)
        
        blinkButton = gtk.Button("Blink")
        blinkButton.set_name("blink")
        blinkButton.connect("clicked", self.on_button)

        jumpButton = gtk.Button("Jump")
        jumpButton.set_name("jump")
        jumpButton.connect("clicked", self.on_button)

        boxTable.attach(fadeButton, 0,1,0,1)
        boxTable.attach(blinkButton, 1,2,0,1)
        boxTable.attach(jumpButton, 2,3,0,1)
        boxTable.attach(clearButton, 3,4,0,1)
        
        #main app building
        vbox = gtk.VBox(True,0)

        vbox.pack_start(headerVbox)
        vbox.pack_start(serialTable)
        vbox.pack_start(buttonTable)
        vbox.pack_start(rHbox)
        vbox.pack_start(gHbox)
        vbox.pack_start(bHbox)
        vbox.pack_start(sHbox)
        vbox.pack_start(brightHbox)
        vbox.pack_end(boxTable)
        
        self.add(vbox)

        self.connect("destroy", lambda w: gtk.main_quit())
        self.show_all()

    def on_changed(self, widget):        
        val = widget.get_value()
        name = widget.get_name()
        
        if name == "speed":
            sSpin.set_value(int(val))
        elif name == "bright":
            brightSpin.set_value(int(val))
            
        elif strand == 1:
            if name == "red":
                rSpin.set_value(int(val))
                rgb1[0] = int(val)
            elif name == "green":
                gSpin.set_value(int(val))
                rgb1[1] = int(val)
            elif name == "blue":
                bSpin.set_value(int(val))
                rgb1[2] = int(val)
            
            self.ser.write(str(strand) + ',' + str(rgb1[0]) + ',' +  str(rgb1[1]) + ',' + str(rgb1[2])+'\n')
                
        elif strand == 2:
            if name == "red":
                rSpin.set_value(int(val))
                rgb2[0] = int(val)
            elif name == "green":
                gSpin.set_value(int(val))
                rgb2[1] = int(val)
            elif name == "blue":
                bSpin.set_value(int(val))
                rgb2[2] = int(val)
            
            self.ser.write(str(strand) + ',' + str(rgb2[0]) + ',' +  str(rgb2[1]) + ',' + str(rgb2[2])+'\n')
                
        elif strand == 3:
            if name == "red":
                rSpin.set_value(int(val))
                rgb3[0] = int(val)
            elif name == "green":
                gSpin.set_value(int(val))
                rgb3[1] = int(val)
            elif name == "blue":
                bSpin.set_value(int(val))
                rgb3[2] = int(val)
            
            self.ser.write(str(strand) + ',' + str(rgb3[0]) + ',' +  str(rgb3[1]) + ',' + str(rgb3[2])+'\n')   
 
    def spin_changed(self,widget):
        val = widget.get_value_as_int()
        name = widget.get_name()
        global speed
        global brightness

        if name == "red":
            rScale.set_value(val)
        elif name == "green":
            gScale.set_value(val)
        elif name == "blue":
            bScale.set_value(val)
        elif name == "speed":
            speed = val
            sScale.set_value(val)
        elif name == "bright":
            brightness = val
            brightScale.set_value(val)
                           

              
    def radio_buttons(self, button, name):
        global rScale
        global gScale
        global bScale 
        if button.get_active():
            global strand    
            strand = int(name)
            if strand == 1:
                rScale.set_value(rgb1[0])
                gScale.set_value(rgb1[1])
                bScale.set_value(rgb1[2])
            elif strand == 2:
                rScale.set_value(rgb2[0])
                gScale.set_value(rgb2[1])
                bScale.set_value(rgb2[2])
            elif strand == 3:
                rScale.set_value(rgb3[0])
                gScale.set_value(rgb3[1])
                bScale.set_value(rgb3[2])
    
    
    def on_button(self, button):
        global rScale
        global gScale
        global bScale
        
        if button.get_name() == "connect":
            self.serialPort = portList.get_active_text()
            self.setup_serial()
        
        elif button.get_name() == "clear":
            self.ser.write(str(strand)+"c")
            rScale.set_value(0)
            gScale.set_value(0)
            bScale.set_value(0)
            sScale.set_value(0)
            brightScale.set_value(0)
                    
        elif button.get_name() == "fade":
            self.ser.write(str(strand)+"f,"+str(speed)+','+str(brightness)+'\n')    
            
        elif button.get_name() == "blink":
            if strand == 1:
                self.ser.write(str(strand)+"b,"+str(speed)+','+str(rgb1[0])+','+str(rgb1[1])+','+str(rgb1[2])+'\n')
            elif strand == 2:
                self.ser.write(str(strand)+"b,"+str(speed)+','+str(rgb2[0])+','+str(rgb2[1])+','+str(rgb2[2])+'\n')
            elif strand == 3:
                self.ser.write(str(strand)+"b,"+str(speed)+','+str(rgb3[0])+','+str(rgb3[1])+','+str(rgb3[2])+'\n')

        elif button.get_name() == "jump":
            self.ser.write(str(strand)+"j,"+str(speed)+'\n')
                    
    def setup_serial(self):
        self.ser = serial.Serial()
        self.ser.setPort(self.serialPort)
        self.ser.baudrate = 115200
        self.ser.open()
        if (self.ser.isOpen()):
            print "Serial Open"
        else:
            print "Serial Closed"

    def serial_ports(self):
        """Lists serial ports

        :raises EnvironmentError:
            On unsupported or unknown platforms
        :returns:
            A list of available serial ports
        """
        if sys.platform.startswith('win'):
            ports = ['COM' + str(i + 1) for i in range(256)]

        elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
            # this is to exclude your current terminal "/dev/tty"
            ports = glob.glob('/dev/tty[A-Za-z]*')

        elif sys.platform.startswith('darwin'):
            ports = glob.glob('/dev/tty.*')

        else:
            raise EnvironmentError('Unsupported platform')

        result = []
        for port in ports:
            try:
                s = serial.Serial(port)
                s.close()
                result.append(port)
            except (OSError, serial.SerialException):
                pass
        return result

PyApp()
gtk.main()