import logging
import traceback

from mopidy import core

from luma.core.interface.serial import i2c, spi
from luma.core.render import canvas
from luma.oled.device import ssd1306, ssd1322, ssd1325, ssd1331, sh1106
from luma.core.virtual import viewport

from smbus import SMBus
import time,os
from PIL import ImageFont
from threading import Thread
import threading
import textwrap
import pykka

from __future__ import unicode_literals


logger = logging.getLogger(__name__)


class DisplayThread(Thread):
    #thread used for managing the display to the screen
    
    def __init__(self, device, message, fontLarge, fontSmall, scrolling=True,speed=1):
        Thread.__init__(self)
        self.device = device
        self.message = message
        self.fontLarge = fontLarge
        self.fontSmall = fontSmall
        self.speed = speed
        self.running = False
        self.scrolling = scrolling

    def start(self):
        self.running = True
        super(DisplayThread, self).start()
        
    def stop(self):
        self.running = False
        self.device.clear()
 
    def run(self):
        x = self.device.width

        # First measure the text size for both fonts
        with canvas(self.device) as draw:
            w, h = draw.textsize(self.message, self.fontLarge)

        with canvas(self.device) as draw:
            ws, hs = draw.textsize(self.message, self.fontSmall)

        #display scrolling text
        if self.scrolling:
            virtual = viewport(self.device, width=max(self.device.width, w + x + x), height=max(h, self.device.height))
            with canvas(virtual) as draw:
                draw.text((x, 30), self.message, font=self.fontLarge, fill='white')
            i = 0
            while i < x + w and self.running:
                virtual.set_position((i, 0))
                i += self.speed
                time.sleep(0.025)
        
        #display non scrolling text
        if (not self.scrolling or i >= x+w) and self.running:
            with canvas(self.device) as draw:
                offset = 0
                divider = self.device.width/float(ws)
                for line in textwrap.wrap(self.message, width=int(len(self.message) * divider)):
                    draw.text((10, offset), line, font=self.fontSmall, fill='white')
                    offset += self.fontSmall.getsize(line)[1]


class oledScreen(pykka.ThreadingActor, core.CoreListener):

    def make_font(self,name, size):
        #initialize a font from the fonts folder
        font_path = os.path.abspath(os.path.join(
            os.path.dirname(__file__), 'fonts', name))
        return ImageFont.truetype(font_path, size)

    def __init__(self, config, core):
        super(OledScreen, self).__init__()
        self.menu = False
        self.core = core
        self.config = config
        if config['bus'] and config['address']:
            self.serial = i2c(bus=SMBus(config['bus']), address=config['address'])
        else    
            self.serial = i2c(bus=SMBus(2), address=0x3c)
        self.driver = config['driver']
        if self.driver == 'ssd1306':
            self.device = ssd1306(serial)
        elif self.driver == 'ssd1322'
            self.device = ssd1322(serial)
        elif self.driver == 'ssd1325'
            self.device = ssd1325(serial)
        elif self.driver == 'ssd1331'    
            self.device = ssd1331(serial)
        elif self.driver == 'sh1106'
            self.device = sh1106(serial)
        else
            self.device = ssd1306(serial)
        
        self.font = self.make_font('Vera.ttf', 26)
        self.fontSmall = self.make_font('Vera.ttf', 15)



    def set_text_on_display(self, text, scrolling, speed):
        #display some text on the display
        self.stop_display()
        self.displayThreadObj = DisplayThread(self.device,text,self.font, self.fontSmall,scrolling,speed)
        self.displayThreadObj.start()

    def stop_display(self):
        #stop displaying text on display by killing the thread (if alive) and clearing the screen
        try:
            if self.displayThreadObj.is_alive():
                self.displayThreadObj.stop()    
        except:
            pass
        self.device.clear()


    def track_playback_started(self, tl_track):
        #display track and album name on start
        self.set_text_on_display(tl_track.track.name+' - '+tl_track.track.album.name,True,5)
        

    def track_playback_paused(self, tl_track, time_position):
        #display pause and track name on pause
        self.set_text_on_display('PAUSE - '+tl_track.track.name,False,5)
    
    def track_playback_resumed(self, tl_track, time_position):
        #display track and album name on start
        self.set_text_on_display(tl_track.track.name+' - '+tl_track.track.album.name,True,5)

    def track_playback_ended(self, tl_track, time_position):
        #stop display when playback is stopped
        self.stop_display()
       
    def playback_state_changed(self, old_state, new_state):
        #stop display when playback is stopped
        if new_state == 'stopped':
            self.stop_display()
        
    

