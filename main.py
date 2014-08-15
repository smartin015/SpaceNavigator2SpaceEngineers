######################################################################
# SpaceDevice demo
#
# This demo demonstrates the usage of the SpaceDevice object in the
# cgkit.spacedevice module which can be used to access events from
# a SpaceMouse or SpaceBall. You can use this module to add support
# for a SpaceDevice in your own Python application. The demo simply
# prints the events generated from a SpaceDevice to the console.
#
# This demo uses pygame as GUI toolkit (v1.7.1 is required).
# You can use any other GUI toolkit as long as it 1) lets you obtain
# the native window handle of a window and 2) provides access to
# system events.
######################################################################

import sys
import pygame
from pygame.locals import *
from cgkit import spacedevice
from control import *
import time
import threading

current_milli_time = lambda: int(round(time.time() * 1000))

class KeyWriter(threading.Thread):

  def __init__(self):
    threading.Thread.__init__(self)
    self.trans = (0,0,0)
    self.rot = (0,0,0)
    self.keypress = [False, False]
    
  def run(self):
    # Change duty cycle of keypresses 
    TH = 600
    MOUSE_TH = 2
    WKEY = 87
    AKEY = 65
    SKEY = 83
    DKEY = 68
    FKEY = 70
    CKEY = 67
    QKEY = 81
    EKEY = 69
    KKEY = 75
    TKEY = 84
    
    NKEYS = 10
    MOUSE_UPDATE_PD = 30
    
    keyState = [False]*NKEYS
    prevKeyState = list(keyState)
    keys = [WKEY, AKEY, SKEY, DKEY, FKEY, CKEY, QKEY, EKEY, KKEY, TKEY]
    mouseState = [0,0]
    mouseButtonState = [False, False]
    prevMouseButtonState = list(mouseButtonState)
    
    t = current_milli_time()
    
    while True:
      now = current_milli_time()
      (x,z,y) = self.trans
      (p,w,r) = self.rot
      keyState = [
          y > TH, x < -TH, y < -TH, x > TH,  # WASD movement
          z > TH, z < -TH, # FC movement
          r > TH, r < -TH, # QE movement
          self.keypress[0], self.keypress[1]
        ]
        
      mouseState[0] = float(w) / 100
      mouseState[1] = float(p) / 100
        
      for i in xrange(NKEYS):
        if keyState[i] != prevKeyState[i]:
          if keyState[i]:
            KeyDown(keys[i])
          else:
            KeyUp(keys[i])
                  
      if now - t > MOUSE_UPDATE_PD:
        MouseMoveRel(mouseState[0], mouseState[1])
        prevKeyState = list(keyState)
        t = now
      
     
  def set_trans(self, trans):
    self.trans = trans
  
  def set_rot(self, rot):
    self.rot = rot
    
  def set_button(self, k, is_pressed):
    if k == K_F6:
      self.keypress[0] = is_pressed
    elif k == K_F7:
      self.keypress[1] = is_pressed

# handleSystemEvent
def handleSystemEvent(evt):
  """Handle a system event.
  evt is a pygame event object that contains a system event. The function
  first checks if the event was generated by a SpaceDevice and if it was,
  it prints the event data.
  """
  # sdev is the global SpaceDevice object
  global sdev
  
  # Writes the keyboard and mouse data
  global writer 
  
  # Translate the system event into a SpaceDevice event...
  res, evttype, data = sdev.translateWin32Event(evt.msg, evt.wparam, evt.lparam)
  # Check if the event actually was an event generated from
  # the SpaceMouse or SpaceBall...
  
  if res!=spacedevice.RetVal.IS_EVENT:
    return

  if evttype==spacedevice.EventType.MOTION_EVENT:
    t,r,period = data
    writer.set_trans(t)
    writer.set_rot(r)
  elif evttype==spacedevice.EventType.BUTTON_EVENT:
    pass # Doesn't work on spacenavigator - using F keys instead
  elif evttype==spacedevice.EventType.ZERO_EVENT:
    writer.set_trans((0,0,0))
    writer.set_rot((0,0,0))


def handleKeyEvent(evt):
    global running
    global writer
    if evt.key==27:
        running = False
        
    if evt.type==KEYDOWN:
      writer.set_button(evt.key, True)
    else:
      writer.set_button(evt.key, False)
        
    
######################################################################

# Check if cgkit was compiled with SpaceDevice support...
if not spacedevice.available():
    print "No SpaceDevice functionality available"
    sys.exit(1)

# Initialize pygame...
passed, failed = pygame.init()
if failed>0:
    print "Error initializing pygame"
    sys.exit(1)

# Open a window...
pygame.display.set_caption("SpaceDevice demo")
srf = pygame.display.set_mode((640,480))

# Enable system events...
pygame.event.set_allowed(SYSWMEVENT)

# Initialize the Space Device...
sdev = spacedevice.SpaceDevice()
info = pygame.display.get_wm_info()
hwnd = info["window"]
sdev.open("Demo", hwnd)

# Print some information about the driver and the device...
major, minor, build, versionstr, datestr = sdev.getDriverInfo()
print "Driver info:"
print "------------"
print "%s, v%d.%d.%d, %s\n"%(versionstr, major, minor, build, datestr)

devtyp, numbuttons, numdegrees, canbeep, firmware = sdev.getDeviceInfo()
print "Device info:"
print "------------"
print "Device ID:",sdev.getDeviceID()
print "Type     :",devtyp
print "#Buttons :",numbuttons
print "#Degrees :",numdegrees
print "Can beep :",canbeep
print "Firmware :",firmware
print ""

writer = KeyWriter()
writer.daemon = True
writer.start()

# Event loop...
running = True
while running:

  # Get a list of events...
  events = pygame.event.get()

  # Process the events...
  for evt in events:

      # Close button?
      if evt.type==QUIT:
          running=False

      # Escape key?
      elif evt.type==KEYDOWN or evt.type==KEYUP:
          handleKeyEvent(evt)

      # System event?
      elif evt.type==SYSWMEVENT:
          handleSystemEvent(evt)
          
# Close the SpaceDevice
sdev.close()