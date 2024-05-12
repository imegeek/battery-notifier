from tkinter import *
from tkinter.ttk import *

from typing import TypedDict, List, Union, Callable

class Bar(TypedDict):
    Ids: List[int]
    Pos: float
    Value: float

class Slider(Frame):
    LINE_COLOR = "#ababab"
    LINE_WIDTH = 3
    BAR_COLOR_INNER = "#58b4ff"
    BAR_COLOR_OUTTER = "#afd6ff"
    BAR_RADIUS = 10
    BAR_RADIUS_INNER = BAR_RADIUS - 5
    DIGIT_PRECISION = ".0f"
    STEP_SIZE: float = 0.0

    def __init__(
        self,
        master,
        width=400,
        height=80,
        min_val=0,
        max_val=1,
        init_lis=None,
        show_value=True,
        removable=False,
        addable=False,
    ):
        Frame.__init__(self, master, height=height, width=width)
        self.master = master
        if init_lis is None:
            init_lis = [min_val]
        self.init_lis = init_lis
        self.max_val = max_val
        self.min_val = min_val
        self.show_value = show_value
        self.H = height
        self.W = width
        self.canv_H = self.H
        self.canv_W = self.W
        if not show_value:
            self.slider_y = self.canv_H / 2
        else:
            self.slider_y = self.canv_H * 2 / 5
        self.slider_x = Slider.BAR_RADIUS

        self._val_change_callback = lambda lis: None

        self.bars: List[Bar] = []
        self.selected_idx = None
        for value in self.init_lis:
            pos = (value - min_val) / (max_val - min_val)
            ids = []
            bar: Bar = {"Pos": pos, "Ids": ids, "Value": value}
            self.bars.append(bar)

        self.canv = Canvas(self, height=self.canv_H, width=self.canv_W)
        self.canv.pack()
        self.canv.bind("<Motion>", self._mouseMotion)
        self.canv.bind("<B1-Motion>", self._moveBar)
        if removable:
            self.canv.bind("<3>", self._removeBar)
        if addable:
            self.canv.bind("<ButtonRelease-1>", self._addBar)

        self.__addTrack(
            self.slider_x, self.slider_y, self.canv_W - self.slider_x, self.slider_y
        )
        for bar in self.bars:
            bar["Ids"] = self.__addBar(bar["Pos"])

    def getValues(self) -> List[int]:
        values = [int(bar["Value"]) for bar in self.bars]
        return sorted(values)
    
    def setValueChangeCallback(self, callback: Callable[[List[int]], None]):
        self._val_change_callback = callback

    def _mouseMotion(self, event):
        x = event.x
        y = event.y
        selection = self.__checkSelection(x, y)
        if selection[0]:
            self.canv.config(cursor="hand2")
            self.selected_idx = selection[1]
        else:
            self.canv.config(cursor="")
            self.selected_idx = None

    def _moveBar(self, event):
        x = event.x
        y = event.y
        if self.selected_idx is None:
            return False
        pos = self.__calcPos(x)
        idx = self.selected_idx
        if self.STEP_SIZE > 0:
            curr_pos = self.bars[idx]["Pos"]
            if abs(curr_pos - pos) < self.STEP_SIZE:
                return
        self.__moveBar(idx, pos)

    def _removeBar(self, event):
        x = event.x
        y = event.y
        if self.selected_idx is None:
            return False
        idx = self.selected_idx
        ids = self.bars[idx]["Ids"]
        for _id in ids:
            self.canv.delete(_id)
        self.bars.pop(idx)

    def _addBar(self, event):
        x = event.x
        y = event.y

        if self.selected_idx is None:
            pos = self.__calcPos(x)
            ids = []
            bar = {
                "Pos": pos,
                "Ids": ids,
                "Value": int(pos * (self.max_val - self.min_val) + self.min_val),
            }
            self.bars.append(bar)

            for i in self.bars:
                ids = i["Ids"]
                for _id in ids:
                    self.canv.delete(_id)

            for bar in self.bars:
                bar["Ids"] = self.__addBar(bar["Pos"])

    def __addTrack(self, startx, starty, endx, endy):
        _id = self.canv.create_line(
            startx, starty, endx, endy, fill=Slider.LINE_COLOR, width=Slider.LINE_WIDTH
        )
        return _id

    def __addBar(self, pos):
        if pos < 0 or pos > 1:
            raise Exception("Pos error - Pos: " + str(pos))
        R = Slider.BAR_RADIUS
        r = Slider.BAR_RADIUS_INNER
        L = self.canv_W - 2 * self.slider_x
        y = self.slider_y
        x = self.slider_x + pos * L
        id_outer = self.canv.create_oval(
            x - R,
            y - R,
            x + R,
            y + R,
            fill=Slider.BAR_COLOR_OUTTER,
            width=2,
            outline="",
        )
        id_inner = self.canv.create_oval(
            x - r, y - r, x + r, y + r, fill=Slider.BAR_COLOR_INNER, outline=""
        )
        if self.show_value:
            y_value = y + Slider.BAR_RADIUS + 8
            value = int(pos * (self.max_val - self.min_val) + self.min_val)
            id_value = self.canv.create_text(
                x, y_value, text=str(value)
            )
            return [id_outer, id_inner, id_value]
        else:
            return [id_outer, id_inner]

    def __moveBar(self, idx, pos):
        ids = self.bars[idx]["Ids"]
        for _id in ids:
            self.canv.delete(_id)
        self.bars[idx]["Ids"] = self.__addBar(pos)
        self.bars[idx]["Pos"] = pos
        self.bars[idx]["Value"] = int(pos * (self.max_val - self.min_val) + self.min_val)
        self._val_change_callback(self.getValues())

    def __calcPos(self, x):
        pos = (x - self.slider_x) / (self.canv_W - 2 * self.slider_x)
        if pos < 0:
            return 0
        elif pos > 1:
            return 1
        else:
            return pos

    def __checkSelection(self, x, y):
        for idx in range(len(self.bars)):
            _id = self.bars[idx]["Ids"][0]
            bbox = self.canv.bbox(_id)
            if bbox[0] < x and bbox[2] > x and bbox[1] < y and bbox[3] > y:
                return [True, idx]
        return [False, None]

# Example usage:
if __name__ == "__main__":
    root = Tk()
    slider = Slider(root, width=400, height=80, min_val=0, max_val=100, init_lis=[25, 75], show_value=True, removable=True, addable=True)
    slider.pack(pady=20)
    values = slider.getValues()
    print("Initial Values:",values)

    def callback(new_values):
        print("Updated Values:",new_values)

    slider.setValueChangeCallback(callback)
    root.mainloop()
