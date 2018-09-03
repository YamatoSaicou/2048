import wx
import copy
import random


class MyFrame(wx.Frame):
    PANEL_ORIG_POINT = wx.Point(15, 15)
    VALUE_COLOR_DEF = {
        0: "#CCC0B3",
        2: "#EEE4DA",
        4: "#EDE0C8",
        8: "#F2B179",
        16: "#F59563",
        32: "#F67C5F",
        64: "#F65E3B",
        128: "#EDCF72",
        256: "#EDCF72",
        512: "#EDCF72",
        1024: "#EDCF72",
        2048: "#EDCF72",
        4096: "#EDCF72",
        8192: "#EDCF72",
        16384: "#EDCF72",
        32768: "#EDCF72"
    }
    tile_values = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
    is_inited = False

    def __init__(self, title):
        super(MyFrame,self).__init__(None, title=title, size=(500, 550))
        self.Bind(wx.EVT_PAINT, self.on_paint)
        self.Bind(wx.EVT_KEY_DOWN, self.on_key)
        self.Centre()
        self.SetFocus()
        self.Show()

    def on_paint(self, e):
        if not self.is_inited:
            self.start_game()
            self.is_inited = True

    def add_random_tile(self):
        empty_tiles = [(row, col) for row in range(len(self.tile_values)) for col in range(len(self.tile_values[0]))
                       if self.tile_values[row][col] == 0]
        if len(empty_tiles) != 0:
            row, col = empty_tiles[random.randint(0, len(empty_tiles) - 1)]
            # value should be 2 or 4
            self.tile_values[row][col] = 2 ** random.randint(1, 2)
            return True
        else:
            return False

    def on_key(self, event):
        key_code = event.GetKeyCode()
        temp_tile_values = copy.deepcopy(self.tile_values)
        if key_code == wx.WXK_UP:
            self.on_key_up()
        elif key_code == wx.WXK_DOWN:
            self.on_key_down()
        elif key_code == wx.WXK_LEFT:
            self.on_key_left()
        elif key_code == wx.WXK_RIGHT:
            self.on_key_right()
        else:
            return
        self.add_random_tile()
        self.draw_tiles()
        return
    def update_single_row_value(self, row_value, positive):
        num_cols = len(row_value)
        if not positive:
            temp_data = copy.deepcopy(row_value)
            row_value = [temp_data[num_cols - 1 - i] for i in range(num_cols)]
        for i in range(num_cols):
            if row_value[i] == 0:
                continue
            for j in range(i + 1, num_cols):
                if row_value[j] == row_value[i]:
                    row_value[i] *= 2
                    row_value[j] = 0
                    break
                elif row_value[j] > row_value[i]:
                    break
        for i in range(num_cols):
            if row_value[i] != 0:
                continue
            for j in range(i + 1, num_cols):
                if row_value[j] != 0:
                    row_value[i] = row_value[j]
                    row_value[j] = 0
                    break
        if not positive:
            temp_data = copy.deepcopy(row_value)
            row_value = [temp_data[num_cols - 1 - i] for i in range(num_cols)]
        return row_value

    def on_key_up(self):
        temp_tile_values = [[row[i] for row in self.tile_values] for i in range(len(self.tile_values[0]))]
        for row in range(len(self.tile_values)):
            temp_tile_values[row] = self.update_single_row_value(temp_tile_values[row], True)
        self.tile_values = [[row[i] for row in temp_tile_values] for i in range(len(temp_tile_values[0]))]

    def on_key_down(self):
        temp_tile_values = [[row[i] for row in self.tile_values] for i in range(len(self.tile_values[0]))]
        for row in range(len(self.tile_values)):
            temp_tile_values[row] = self.update_single_row_value(temp_tile_values[row], False)
        self.tile_values = [[row[i] for row in temp_tile_values] for i in range(len(temp_tile_values[0]))]

    def on_key_left(self):
        for row in range(len(self.tile_values)):
            self.tile_values[row] = self.update_single_row_value(self.tile_values[row], True)

    def on_key_right(self):
        for row in range(len(self.tile_values)):
            self.tile_values[row] = self.update_single_row_value(self.tile_values[row], False)

    def init_screen(self):
        dc = wx.ClientDC(self)
        dc.SetBackground(wx.Brush("#FAF8EF"))
        dc.Clear()
        dc.SetBrush(wx.Brush("#C0B0A0"))
        dc.SetPen(wx.Pen("", 1, wx.TRANSPARENT))
        dc.DrawRoundedRectangle(self.PANEL_ORIG_POINT.x, self.PANEL_ORIG_POINT.y, 450, 450, 5)

    def draw_tiles(self):
        dc = wx.ClientDC(self)
        dc.SetBackground(wx.Brush("#F0F0E0"))
        dc.SetBrush(wx.Brush("#C0B0A0"))
        dc.SetPen(wx.Pen("", 1, wx.TRANSPARENT))
        for row in range(4):
            for column in range(4):
                tile_value = self.tile_values[row][column]
                tile_color = self.VALUE_COLOR_DEF[tile_value]
                dc.SetBrush(wx.Brush(tile_color))
                dc.DrawRoundedRectangle(self.PANEL_ORIG_POINT.x + 110 * column + 10,
                                        self.PANEL_ORIG_POINT.y + 110 * row + 10, 100, 100, 5)
                dc.SetTextForeground("#707070")
                text_font = wx.Font(30, wx.SWISS, wx.NORMAL, wx.BOLD, faceName=u"Roboto")
                dc.SetFont(text_font)
                if tile_value != 0:
                    size = dc.GetTextExtent(str(tile_value))
                    if size[0] > 100:
                        text_font = wx.Font(24, wx.SWISS, wx.NORMAL, wx.BOLD, faceName=u"Roboto")
                        dc.SetFont(text_font)
                        size = dc.GetTextExtent(str(tile_value))
                    dc.DrawText(str(tile_value), self.PANEL_ORIG_POINT.x + 110 * column + 10 + (100 - size[0]) / 2,
                                self.PANEL_ORIG_POINT.y + 110 * row + 10 + (100 - size[1]) / 2)

    def start_game(self):
        self.tile_values = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
        self.init_screen()
        self.add_random_tile()
        self.add_random_tile()
        self.draw_tiles()

    def test_update_tiles(self):
        self.tile_values = [[0, 2, 4, 8], [16, 32, 64, 128], [256, 512, 1024, 2048], [4096, 8192, 16384, 32768]]
        self.draw_tiles()


    def is_game_over(self):
        # exist 0 or there is a neighbour with the same value
        print ("is_game_over")
        num_rows = len(self.tile_values)
        num_cols = len(self.tile_values[0])
        for i in range(num_rows):
            for j in range(num_cols):
                if self.tile_values[i][j] == 0 or \
                        (j < num_cols-1 and self.tile_values[i][j] == self.tile_values[i][j + 1]) or \
                        (i < num_rows-1 and self.tile_values[i][j] == self.tile_values[i + 1][j]):
                    return False
        return True

    def game_over(self):
        if wx.MessageBox(u"游戏结束，是否再来一局？", u"Game Over", wx.YES_NO) == wx.YES:
            self.start_game()

class MyApp(wx.App):
    def OnInit(self):
        frame = MyFrame('2048')
        frame.Show(True)
        return True


if __name__ == "__main__":
    app = MyApp()
    app.MainLoop()