from bullet import Bullet

class Turret:
    def __init__(self, canvas, x, y):
        self.canvas = canvas
        self.rect = canvas.create_rectangle(x - 10, y - 10, x + 10, y + 10, fill="purple", outline='grey', width=0)
        self.ddx=0
        self.ddy=0
        self.health=-5
        self.shoot()

    def shoot(self):
        x1, y1, x2, y2 = self.canvas.coords(self.rect)
        if abs(self.ddx)>abs(self.ddy):
            if self.ddx<0:
                c=-10
            if self.ddx>0:
                c=10
            Bullet(self.canvas, (x1 + x2) / 2, (y1 + y2) / 2, c , c*self.ddy/self.ddx )
        if abs(self.ddy)>abs(self.ddx):
            if self.ddy<0:
                c=-10
            if self.ddy>0:
                c=10
            Bullet(self.canvas, (x1 + x2) / 2, (y1 + y2) / 2, c*self.ddx/self.ddy , c )
        self.canvas.after(2000, self.shoot)