import zte as term
import random
import sound

def braille(dots):
    mask = 0
    for d in dots:
        mask |= 1 << (d - 1)
    return chr(0x2800 + mask)

DOT_MAP = {
    (0,0): 1, (1,0): 2, (2,0): 3, (3,0): 7,
    (0,1): 4, (1,1): 5, (2,1): 6, (3,1): 8,
}

def scale_list(lst: list, new_min: int, new_max: int, new_length: int):
    old_min, old_max = min(lst), max(lst)
    scale = (new_max - new_min) / (old_max - old_min)
    lst = [round(new_min + (x - old_min) * scale) for x in lst]

    old_length = len(lst)
    result = []
    for i in range(new_length):
        pos = i * (old_length - 1) / (new_length - 1)
        low = int(pos)
        high = min(low + 1, old_length - 1)
        frac = pos - low
        val = lst[low] + (lst[high] - lst[low]) * frac
        result.append(round(val))
    return result

def plot_list(lst, x:int, y:int, w:int, h:int):
    pixel_w = w * 2
    pixel_h = h * 4

    scaled = scale_list(lst, 0, pixel_h-1, pixel_w)

    grid = [[[] for _ in range(w)] for _ in range(h)]

    def set_pixel(px, py):
        row = pixel_h - 1 - py
        cell_row, dot_row = divmod(row, 4)
        cell_col, dot_col = divmod(px, 2)
        if 0 <= cell_row < h and 0 <= cell_col < w:
            grid[cell_row][cell_col].append(DOT_MAP[(dot_row, dot_col)])

    for col, val in enumerate(scaled[:-1]):
        next_val = scaled[col+1]
        py1, py2 = val, next_val
        x1, x2 = col, col+1

        set_pixel(x1, py1)

        if py1 != py2:
            step = 1 if py2 > py1 else -1
            for py in range(py1, py2+step, step):
                set_pixel(x2, py)
        else:
            set_pixel(x2, py2)

    for r, row in enumerate(grid):
        for c, dots in enumerate(row):
            ch = braille(dots) if dots else " "
            term.ip(x+c, y+r, ch)
