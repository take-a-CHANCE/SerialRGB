'''
Created on Mar 30, 2014

Requires PySerial and PyGTK

***************WorkLog******************
5/7: initial install of pyserial and pygtk, loading up of code I worked on previously
5/8: testing methods to make scales change when new scale selected
5/8: debugging
5/12: Completely redid arduino code, changed python to reflect changes
5/13: debugged problems with values changing. Increased baud rate
5/14: added in new line '\n' after each command sent to arduino to fix problems with colors mixing
5/15: Clear now sets scales to zero, switching between strands makes scales move to stored previous values 
        by making scales global variables; added brightness slider and blink functionality
5/16: Final debugging, added bright and speed scales to clear function

****************************************

@author: Chance
'''

'''
****************ARDUINO CODE********************

//Pin Declarations
int red1=3;
int green1=5;
int blue1=6;

int red2=9;
int green2=10;
int blue2=11; 

int badLED = 13;

int strand;
int red;
int green;
int blue;

int slow;
int bright;
boolean getOut = true;

void setup() {
  //Yo set thos Pins default
  pinMode(red1, OUTPUT);
  pinMode(blue1, OUTPUT);
  pinMode(green1, OUTPUT);
  pinMode(red2, OUTPUT);
  pinMode(blue2, OUTPUT);
  pinMode(green2, OUTPUT);
  
  pinMode(badLED, OUTPUT);
  
  analogWrite(red1, 0);
  analogWrite(blue1, 0);
  analogWrite(green1, 0);
  analogWrite(red2, 0);
  analogWrite(blue2, 0);
  analogWrite(green2, 0);
  
  digitalWrite(badLED, LOW);

  Serial.begin(115200);
  
  //Print Instructions
  Serial.println("                    INSTRUCTIONS");
  Serial.println("    (Strand#'s 1=1, 2=2, 3=1+2; max color values 255)");
  Serial.println("Solid color:  Strand#, Red Value, Green Value, Blue Value");
  Serial.println("Blink:        Strand#b, Delay Value, R, G, B");
  Serial.println("Fade:         Strand#f, Delay Value, Brightness");
  Serial.println("Clear:        Strand#c");
}

void loop() {
  // put your main code here, to run repeatedly:
  while(Serial.available()>=2) {
    strand = Serial.parseInt();
    switch( Serial.read()) {
      case 'f':
        slow=Serial.parseInt();
        bright=Serial.parseInt();
        if (Serial.read() == '\n')
          fade(strand,slow,bright);
        getOut = false;
        break;
      case 'c':
        //if (Serial.read() == '\n')
          setColor(strand,0,0,0);
        break;
      case 'b':
        getOut = false;
        slow=Serial.parseInt();
        red = Serial.parseInt();
        green = Serial.parseInt();
        blue = Serial.parseInt();
        if (Serial.read() == '\n')
          blinky(strand,slow,red,green,blue);
        break;  
      case ',':
        red = Serial.parseInt();
        green = Serial.parseInt();
        blue = Serial.parseInt();
        if (Serial.read() == '\n')
          setColor(strand,red,green,blue);
        break;
      default:
        digitalWrite(badLED,HIGH);
        break;
    }
    delay(20);
    Serial.flush();
  }
  
}

void setColor(int s, int r , int g, int b) {
  if (s == 1) {
    analogWrite(red1, r);
    analogWrite(green1, g);
    analogWrite(blue1, b);
    digitalWrite(badLED, LOW);
  }
  else if (s == 2) {
    analogWrite(red2, r);
    analogWrite(green2, g);
    analogWrite(blue2, b);
    digitalWrite(badLED, LOW);
  }
  else if (s == 3) {
    analogWrite(red1, r);
    analogWrite(green1, g);
    analogWrite(blue1, b);
    analogWrite(red2, r);
    analogWrite(green2, g);
    analogWrite(blue2, b);
    digitalWrite(badLED, LOW);
  }
  else 
    digitalWrite(badLED, HIGH);
}


void blinky(int s, int delayVal, int r, int g, int b) {
   while(getOut!=true) {
     setColor(s,r,g,b);
     delay(delayVal);
     if (Serial.available()>0){
       getOut=true;
       break;
     }
     setColor(s,0,0,0);
     delay(delayVal);
     if (Serial.available()>0){
       getOut=true;
       break;
     }
   }
}


void fade(int strand, int delayVal, int brightness){
   int r, g, b;
   constrain(brightness, 1,255);
   while(getOut!=true){
     if (Serial.available()>0){
       getOut=true;
       break;
     }
     if (strand==1){
       
      // fade from blue to violet
      for (r = 0; r <= brightness; r++) { 
        analogWrite(red1, r);
        delay(delayVal);
      }
     if (Serial.available()>0){
       getOut=true;
       break;
     } 
      // fade from violet to red
      for (b = brightness; b >= 0; b--) { 
        analogWrite(blue1, b);
        delay(delayVal);
      } 
      if (Serial.available()>0){
       getOut=true;
       break;
     }
      // fade from red to yellow
      for (g = 0; g <= brightness; g++) { 
        analogWrite(green1, g);
        delay(delayVal);
      } 
      if (Serial.available()>0){
       getOut=true;
       break;
     }
      // fade from yellow to green
      for (r = brightness; r >= 0; r--) { 
        analogWrite(red1, r);
        delay(delayVal);
      } 
      if (Serial.available()>0){
       getOut=true;
       break;
     }
      // fade from green to teal
      for (b = 0; b <= brightness; b++) { 
        analogWrite(blue1, b);
        delay(delayVal);
      } 
      if (Serial.available()>0){
       getOut=true;
       break;
     }
      // fade from teal to blue
      for (g = brightness; g >= 0; g--) { 
        analogWrite(green1, g);
        delay(delayVal);
      } 
      if (Serial.available()>0){
       getOut=true;
       break;
     }
     }
     else if (strand==2){
   
      // fade from blue to violet
      for (r = 0; r <= brightness; r++) { 
        analogWrite(red2, r);
        delay(delayVal);
      } 
      if (Serial.available()>0){
       getOut=true;
       break;
     }
      // fade from violet to red
      for (b = brightness; b >= 0; b--) { 
        analogWrite(blue2, b);
        delay(delayVal);
      } 
      if (Serial.available()>0){
       getOut=true;
       break;
     }
      // fade from red to yellow
      for (g = 0; g <= brightness; g++) { 
        analogWrite(green2, g);
        delay(delayVal);
      } 
      if (Serial.available()>0){
       getOut=true;
       break;
     }
      // fade from yellow to green
      for (r = brightness; r >= 0; r--) { 
        analogWrite(red2, r);
        delay(delayVal);
      } 
      if (Serial.available()>0){
       getOut=true;
       break;
     }
      // fade from green to teal
      for (b = 0; b <= brightness; b++) { 
        analogWrite(blue2, b);
        delay(delayVal);
      } 
      if (Serial.available()>0){
       getOut=true;
       break;
     }
      // fade from teal to blue
      for (g = brightness; g >= 0; g--) { 
        analogWrite(green2, g);
        delay(delayVal);
      } 
      if (Serial.available()>0){
       getOut=true;
       break;
     }
     }
     else if (strand==3){
   
      // fade from blue to violet
      for (r = 0; r <= brightness; r++) { 
        analogWrite(red1, r);
        analogWrite(red2, r);
        delay(delayVal);
      } 
      if (Serial.available()>0){
       getOut=true;
       break;
     }
      // fade from violet to red
      for (b = brightness; b >= 0; b--) { 
        analogWrite(blue1, b);
        analogWrite(blue2, b);
        delay(delayVal);
      } 
      if (Serial.available()>0){
       getOut=true;
       break;
     }
      // fade from red to yellow
      for (g = 0; g <= brightness; g++) { 
        analogWrite(green1, g);
        analogWrite(green2, g);
        delay(delayVal);
      } 
      if (Serial.available()>0){
       getOut=true;
       break;
     }
      // fade from yellow to green
      for (r = brightness; r >= 0; r--) { 
        analogWrite(red1, r);
        analogWrite(red2, r);
        delay(delayVal);
      } 
      if (Serial.available()>0){
       getOut=true;
       break;
     }
      // fade from green to teal
      for (b = 0; b <=brightness; b++) { 
        analogWrite(blue1, b);
        analogWrite(blue2, b);
        delay(delayVal);
      } 
      if (Serial.available()>0){
       getOut=true;
       break;
     }
      // fade from teal to blue
      for (g = brightness; g >= 0; g--) { 
        analogWrite(green1, g);
        analogWrite(green2, g);
        delay(delayVal);
      } 
     }
     if (Serial.available()>0){
       getOut=true;
       break;
     }
   }
}

********************END*************************
'''

import gtk
import sys
import serial
import time

global rgb1
global rgb2
global rgb3
       
rgb1 = [0,0,0]
rgb2 = [0,0,0]
rgb3 = [0,0,0]


class PyApp(gtk.Window):

    def __init__(self):
        global rScale
        global gScale
        global bScale 
        global sScale
        global brightScale
        
        super(PyApp, self).__init__()

        #self.serialPort = "/dev/tty.usbmodem621"
        self.serialPort = "COM5"
        
        self.set_title("RGB Control")
        self.set_size_request(260, 240)
        self.set_position(gtk.WIN_POS_CENTER)
        self.setup_serial()
    
        headerVbox = gtk.VBox(True,0)
        headerLabel1 = gtk.Label("RGB Control App for Arduino")
        headerVbox.pack_start(headerLabel1)
        
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
        
        rHbox = gtk.HBox(True,0)
        rLabel = gtk.Label("Red: ")
        rHbox.pack_start(rLabel)   
             
        rScale = gtk.HScale()
        rScale.set_name("red")
        rScale.set_range(0, 255)
        rScale.set_increments(1, 10)
        rScale.set_digits(0)
        rScale.set_size_request(180, 35)
        rScale.set_value_pos(gtk.POS_LEFT)
        rScale.connect("value-changed", self.on_changed)
        rHbox.pack_end(rScale)
        
        gHbox = gtk.HBox(True,0)
        gLabel = gtk.Label("Green: ")
        gHbox.pack_start(gLabel)   
        
        gScale = gtk.HScale()
        gScale.set_name("green")
        gScale.set_range(0, 255)
        gScale.set_increments(1, 10)
        gScale.set_digits(0)
        gScale.set_size_request(180, 35)
        gScale.set_value_pos(gtk.POS_LEFT)
        gScale.connect("value-changed", self.on_changed)
        gHbox.pack_end(gScale)
        
        bHbox = gtk.HBox(True,0)       
        bLabel = gtk.Label("Blue: ")
        bHbox.pack_start(bLabel)   
        
        bScale = gtk.HScale()
        bScale.set_name("blue")
        bScale.set_range(0, 255)
        bScale.set_increments(1, 10)
        bScale.set_digits(0)
        bScale.set_size_request(180, 35)
        bScale.set_value_pos(gtk.POS_LEFT)
        bScale.connect("value-changed", self.on_changed)
        bHbox.pack_end(bScale)
        
        sHbox = gtk.HBox(True,0)
        sLabel = gtk.Label("Speed: ")
        sHbox.pack_start(sLabel)
        
        sScale = gtk.HScale()
        sScale.set_name("speed")
        sScale.set_range(0,255)
        sScale.set_increments(1, 5)
        sScale.set_digits(0)
        sScale.set_size_request(180, 35)
        sScale.set_value_pos(gtk.POS_LEFT)
        sScale.connect("value-changed", self.on_changed)
        sHbox.pack_end(sScale)
        
        brightHbox = gtk.HBox(True,0)
        brightLabel = gtk.Label("Brightness: ")
        brightHbox.pack_start(brightLabel)
        
        brightScale = gtk.HScale()
        brightScale.set_name("bright")
        brightScale.set_range(0,255)
        brightScale.set_increments(1, 10)
        brightScale.set_digits(0)
        brightScale.set_size_request(180, 35)
        brightScale.set_value_pos(gtk.POS_LEFT)
        brightScale.connect("value-changed", self.on_changed)
        brightHbox.pack_end(brightScale)
        
        boxTable = gtk.Table(1,3,False)
        
        fadeButton = gtk.Button("Fade")
        fadeButton.set_name("fade")
        fadeButton.connect("clicked", self.on_button)
        
        clearButton = gtk.Button("Clear")
        clearButton.set_name("clear")
        clearButton.connect("clicked", self.on_button)
        
        blinkButton = gtk.Button("Blink")
        blinkButton.set_name("blink")
        blinkButton.connect("clicked", self.on_button)
        
        
        boxTable.attach(fadeButton, 0,1,0,1)
        boxTable.attach(blinkButton, 1,2,0,1)
        boxTable.attach(clearButton, 2,3,0,1)
        
        vbox = gtk.VBox(True,0)

        vbox.pack_start(headerVbox)
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
        
        global speed
        global brightness

        
        val = widget.get_value()
        name = widget.get_name()
        
        if strand == 1:
            if name == "red":
                rgb1[0] = int(val)
            elif name == "green":
                rgb1[1] = int(val)
            elif name == "blue":
                rgb1[2] = int(val)
            elif name == "speed":
                speed = int(val)
            elif name == "bright":
                brightness = int(val)
            
            if not (name == "speed" or name == "bright"):
                self.ser.write(str(strand) + ',' + str(rgb1[0]) + ',' +  str(rgb1[1]) + ',' + str(rgb1[2])+'\n')
                
        elif strand == 2:
            if name == "red":
                rgb2[0] = int(val)
            elif name == "green":
                rgb2[1] = int(val)
            elif name == "blue":
                rgb2[2] = int(val)
            elif name == "speed":
                speed = int(val)
            elif name == "bright":
                brightness = int(val)
            
            if not (name == "speed" or name == "bright"):
                self.ser.write(str(strand) + ',' + str(rgb2[0]) + ',' +  str(rgb2[1]) + ',' + str(rgb2[2])+'\n')
                
        elif strand == 3:
            if name == "red":
                rgb3[0] = int(val)
            elif name == "green":
                rgb3[1] = int(val)
            elif name == "blue":
                rgb3[2] = int(val)
            elif name == "speed":
                speed = int(val)
            elif name == "bright":
                brightness = int(val)
            
            if not (name == "speed" or name == "bright"):
                self.ser.write(str(strand) + ',' + str(rgb3[0]) + ',' +  str(rgb3[1]) + ',' + str(rgb3[2])+'\n')   
        
        
    def radio_buttons(self, button, name):
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
        if button.get_name() == "clear":
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
                    
    def setup_serial(self):
        self.ser = serial.Serial()
        self.ser.setPort(self.serialPort)
        self.ser.baudrate = 115200
        self.ser.open()
        if (self.ser.isOpen()):
            print "Serial Open"
        else:
            print "Serial Closed"

PyApp()
gtk.main()