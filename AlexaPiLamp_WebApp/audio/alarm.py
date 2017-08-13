import datetime
import threading
import pygame
import os

from threading import Thread

class AlarmThread(Thread):
    _clock = None
    _running = False

    def __init__(self):
        Thread.__init__(self)
        pygame.mixer.init()
        # alarm sound from http://www.orangefreesounds.com/
        pygame.mixer.music.load(os.path.abspath(r"audio/alarm.wav"))

    def run(self):
        while True:
            continue

    def turn_off(self):
        pygame.mixer.music.stop()
        self._running = False
        self._clock = None

    def set_alarm(self, date):
        if(self._clock is not None):
            return "there is already an alarm going on"
        time = datetime.datetime.strptime(date,"%H:%M")
        self._clock = Clock()
        self._clock.set_alarm(time.hour, time.minute)
        self._clock.run()

    def set_countdown(self, milis):
        if(self._clock is not None):
            return "there is already an alarm going on"
        time = datetime.datetime.now() + datetime.timedelta(milliseconds=milis)
        self._clock = Clock()
        self._clock.set_alarm(time.hour, time.minute)
        self._clock.run()

    def ring_ring(self):
        self._running = True
        pygame.mixer.music.play(loops=-1)

    def is_running(self):
        return self._running

class Clock:

    def __init__(self):
        self.alarm_time = None
        self._alarm_thread = None
        self.update_interval = 1
        self.event = threading.Event()

    def run(self):
        while True:
            self.event.wait(self.update_interval)
            if self.event.isSet():
                break
            now = datetime.datetime.now()
            #if self._alarm_thread and self._alarm_thread.is_alive():
            #    alarm_symbol = '+'
            # else:
            #    alarm_symbol = ' '
            #sys.stdout.write("\r%02d:%02d:%02d %s"
            #    % (now.hour, now.minute, now.second, alarm_symbol))
            #sys.stdout.flush()
            #TODO show remaining time on display

    def set_alarm(self, hour, minute):
        now = datetime.datetime.now()
        alarm = now.replace(hour=int(hour), minute=int(minute))
        delta = int((alarm - now).total_seconds())
        if delta <= 0:
            alarm = alarm.replace(day=alarm.day + 1)
            delta = int((alarm - now).total_seconds())
        if self._alarm_thread:
            self._alarm_thread.cancel()
        self._alarm_thread = threading.Timer(delta, ring_ring)
        self._alarm_thread.daemon = True
        self._alarm_thread.start()
