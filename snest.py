import pygame as pg
import sys

if sys.platform == "linux" or \
sys.platform == "linux2" or \
sys.platform == "darwin":
	tui = True
	try:
		import curses
	except:	
		tui = False
		print("\nCurses module not found. Continuing as CLI...\n")		

# controller init
pg.init()
ctrl = pg.joystick.Joystick(0)
ctrl.init()
buttons = ctrl.get_numbuttons()
axes = ctrl.get_numaxes()

state = 0x000 # State of all buttons and dpad

# Button HEX codes for bitwise parsing

A     = 0x001 #0b000000000001
B     = 0x002 #0b000000000010
X     = 0x004 #0b000000000100
Y     = 0x008 #0b000000001000
LB    = 0x010 #0b000000010000
RB    = 0x020 #0b000000100000
SEL   = 0x040 #0b000001000000
ST    = 0x080 #0b000010000000
R     = 0x100 #0b000100000000
L     = 0x200 #0b001000000000
DN    = 0x400 #0b010000000000
UP	  = 0x800 #0b100000000000

def tui_init():
	stdscr = curses.initscr()
	curses.noecho()
	curses.curs_set(0)
	stdscr.keypad(1)
	stdscr.nodelay(1)
	global ss 
	ss = stdscr.getmaxyx()
	return stdscr

def tui_update(state):
	# Four rows of buttons
	strs = [' LB ',' RB ',' UP ',' X ',\
            ' L ',' R ',\
            ' SEL ',' STR ',' Y ',' A ',' DN ',\
            ' B ']
	
	if (state & LB):
		stdscr.addstr(ss[0]//2,(1)*(ss[1]//3),strs[0],curses.A_STANDOUT)
	if not (state & LB):
		stdscr.addstr(ss[0]//2,(1)*(ss[1]//3),strs[0])

	if (state & RB):
		stdscr.addstr(ss[0]//2,(2)*(ss[1]//3),strs[1],curses.A_STANDOUT)
	if not (state & RB):
		stdscr.addstr(ss[0]//2,(2)*(ss[1]//3),strs[1])
		
	if (state & UP):
		stdscr.addstr(ss[0]//2+2,(1)*(ss[1]//5),strs[2],curses.A_STANDOUT)
	if not (state & UP):
		stdscr.addstr(ss[0]//2+2,(1)*(ss[1]//5),strs[2])

	if (state & X):
		stdscr.addstr(ss[0]//2+2,(4)*(ss[1]//5),strs[3],curses.A_STANDOUT)
	if not (state & X):
		stdscr.addstr(ss[0]//2+2,(4)*(ss[1]//5),strs[3])

	if (state & L):
		stdscr.addstr(ss[0]//2+4,(1)*(ss[1]//7),strs[4],curses.A_STANDOUT)
	if not (state & L):
		stdscr.addstr(ss[0]//2+4,(1)*(ss[1]//7),strs[4])

	if (state & R):
		stdscr.addstr(ss[0]//2+4,(2)*(ss[1]//7),strs[5],curses.A_STANDOUT)
	if not (state & R):
		stdscr.addstr(ss[0]//2+4,(2)*(ss[1]//7),strs[5])

	if (state & SEL):
		stdscr.addstr(ss[0]//2+4,(3)*(ss[1]//7),strs[6],curses.A_STANDOUT)
	if not (state & SEL):
		stdscr.addstr(ss[0]//2+4,(3)*(ss[1]//7),strs[6])

	if (state & ST):
		stdscr.addstr(ss[0]//2+4,(4)*(ss[1]//7),strs[7],curses.A_STANDOUT)
	if not (state & ST):
		stdscr.addstr(ss[0]//2+4,(4)*(ss[1]//7),strs[7])

	if (state & Y):
		stdscr.addstr(ss[0]//2+4,(5)*(ss[1]//7),strs[8],curses.A_STANDOUT)
	if not (state & Y):
		stdscr.addstr(ss[0]//2+4,(5)*(ss[1]//7),strs[8])

	if (state & A):
		stdscr.addstr(ss[0]//2+4,(6)*(ss[1]//7),strs[9],curses.A_STANDOUT)
	if not (state & A):
		stdscr.addstr(ss[0]//2+4,(6)*(ss[1]//7),strs[9])

	if (state & DN):
		stdscr.addstr(ss[0]//2+6,(1)*(ss[1]//5),strs[10],curses.A_STANDOUT)
	if not (state & DN):
		stdscr.addstr(ss[0]//2+6,(1)*(ss[1]//5),strs[10])

	if (state & B):
		stdscr.addstr(ss[0]//2+6,(4)*(ss[1]//5),strs[11],curses.A_STANDOUT)
	if not (state & B):
		stdscr.addstr(ss[0]//2+6,(4)*(ss[1]//5),strs[11])

	stdscr.refresh()		
	return stdscr

#def tui_update(stdscr,state):
				

def check(state):
# Grabs input and toggles respective bits 
# in the state integer
	state = 0x000
	for i in range(0,buttons + axes):
		if i >= buttons:
			#the last bits are reserved for the dpad
			#convert dpad negatives to new bit positions
			res = int(round(ctrl.get_axis(i-buttons)))
			if res < 0:
				state ^= (abs(res) << (i + (i-buttons)+1))
			if res > 0:
				state ^= (res << (i+(i-buttons)))
		if i < buttons:
			#the first bits are buttons
			state ^= (ctrl.get_button(i) << i )
	return state		

if tui == True:
	stdscr = tui_init()
ch = ''
while(ch != ord('q')):
	ch = stdscr.getch()
	pg.event.pump()
	state = check(state)
	if tui == False:
		print("\r\x1b[K"+str(state),sep=' ',end='',flush=True)
	if tui == True:
		tui_update(state)
curses.endwin()


