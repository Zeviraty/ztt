import zte as term
import signal

def on_resize(_,__):
    term.cs()
    h = False
    mode = "Normal"
    border(h)
    statusbar()
    term.ip(3,0,"┤ZTT├")

def border(h):
    term.border("╭","╮","╰","╯",h=term.wh()[1]-1)

def statusbar(mode:str = "NORMAL",key: str =" ", file:str = "Empty", saved:bool = True):
    term.ip(3,term.wh()[1],f"-- {mode} --   ")
    term.ip(term.wh()[0]//2,term.wh()[1],f"{file}{' [+]' if not saved else ''}")
    term.ip(term.wh()[0]-3,term.wh()[1],f'({key})')

def main():
    term.echo(False)
    term.raw(True)
    term.hide()
    term.cs()

    h = False
    mode = "NORMAL"
    border(h)
    statusbar(mode)
    term.ip(3,0,"┤ZTT├")

    while True:
        # Key
        key = term.getch()
        statusbar(mode,key)
        match key:
            case "q":
                text = "Do you really want to quit?"
                term.border("╭","╮","╰","╯",w=len(text)+2,h=5,x=term.wh()[0] // 2 - (len(text) // 2), y=term.wh()[1] // 2)
                term.ip(term.wh()[0]//2-(len(text)//2)+1,term.wh()[1]//2+1,text)
                term.ip(term.wh()[0]//2-(len(text)//2)+3,term.wh()[1]//2+3,"    |y| Yes  |n| No")

                key = term.getch()
                statusbar(mode,key)
                if key == "y":
                    break
                else:
                    for i in range(5):
                        term.ip(term.wh()[0] // 2 - (len(text) // 2),term.wh()[1] // 2+i," " * (len(text)+2))
            case "?":
                h = not h
                border(h)

            case '\x1b':
                mode = "NORMAL"

            case 'p':
                mode = "PATTERN"

            case 's':
                mode = "SONG"

    term.cs()
    term.echo(True)
    term.raw(False)
    term.rh()

if __name__ == "__main__":
    signal.signal(signal.SIGWINCH, on_resize)
    main()
