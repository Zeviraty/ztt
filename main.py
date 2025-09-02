import zte as term
import signal
import threading
import sys
import sound
import plot

global EXIT
EXIT = False

def run_command(command: str):
    global EXIT
    match command:
        case "Q" | "q!": EXIT = True
        case "q": quit()

def quit():
    global EXIT
    text = "Do you really want to quit?"
    term.border("╭","╮","╰","╯",w=len(text)+2,h=5,x=term.wh()[0] // 2 - (len(text) // 2), y=term.wh()[1] // 2)
    term.ip(term.wh()[0]//2-(len(text)//2)+1,term.wh()[1]//2+1,text)
    term.ip(term.wh()[0]//2-(len(text)//2)+3,term.wh()[1]//2+3,"    |y| Yes  |n| No")

    key = term.getch()
    statusbar(key)
    if key == "y":
        EXIT = True
    else:
        for i in range(5):
            term.ip(term.wh()[0] // 2 - (len(text) // 2),term.wh()[1] // 2+i," " * (len(text)+2))

def on_resize(_,__):
    term.cs()
    h = False
    mode = "SONG"
    border(h)
    statusbar()
    term.ip(3,0,"┤ZTT├")

def border(h):
    term.border("╭","╮","╰","╯",h=term.wh()[1]-1)

def statusbar(mode:str = "SONG",key: str =" ", file:str = "Empty", saved:bool = True, command:bool = False):
    if key == "\n":
        key = ""
    if not command:
        term.ip(3,term.wh()[1],f"-- {mode} --   ")
        term.ip(int((term.wh()[0]/2)-(len(file)/2)),term.wh()[1],f"{file}{' [+]' if not saved else ''}")
        term.ip(term.wh()[0]-3,term.wh()[1],f'({key})')
    else:
        term.ip(1,term.wh()[1], " "*(term.wh()[0]-1))
        term.ip(1,term.wh()[1],":")
        command = ""
        while True:
            key = term.getch()
            if key == '\r' or key == '\n':
                term.ip(1,term.wh()[1], " "*(term.wh()[0]-1))
                statusbar(mode,key,file,saved)
                term.ip(1,term.wh()[1]," ")
                run_command(command)
                break
            elif key == '\x7f' or key == '\x08':
                command = command[:-1]
                term.ip(2+len(command),term.wh()[1]," ")
            elif len(key) == 1 and 32 <= ord(key) <= 126:
                command += key
            term.ip(2,term.wh()[1],command)

def main():
    global EXIT
    term.echo(False)
    term.raw(True)
    term.hide()
    term.cs()

    h = False
    mode = "SONG"
    border(h)
    statusbar(mode)
    term.ip(3,0,"┤ZTT├")

    while True:
        # Key
        key = term.getch()
        match key:
            case "q": quit()
            case "?":
                h = not h
                border(h)

            case '\x1b':
                mode = "SONG"

            case 'p':
                mode = "PATTERN"

            case ':':
                statusbar(mode,key,command=True)

            case _:
                if key.isnumeric() and mode == "PATTERN":
                    pass
                
                #print(repr(key))

        statusbar(mode,key)
        if EXIT == True:
            break

    term.cs()
    term.echo(True)
    term.raw(False)
    term.rh()

def _start_windows_resize_monitor(callback, interval=0.5):
    last_size = term.wh()
    while True:
        try:
            current_size = term.wh()
            if current_size != last_size:
                last_size = current_size
                callback(current_size,'')
        except OSError:
            pass
        import time
        time.sleep(interval)

if __name__ == "__main__":
    if sys.platform == "win32":
        threading.Thread(target=_start_windows_resize_monitor, args=(on_resize,), daemon=True).start()
    else:
        signal.signal(signal.SIGWINCH, on_resize)
    main()
