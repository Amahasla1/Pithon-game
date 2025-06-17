class Golden_key:
    def __init__(self, canvas, x, y):
        self.canvas = canvas
        self.rect = canvas.create_rectangle(x-5, y-5, x+5, y+5, fill = "yellow", outline= 'grey', width=0,)