from display import *
from matrix import *


def add_circle(matrix, cx, cy, cz, r):
  t = 0
  while t <= 1:
    x = r * math.cos(2*math.pi * t) + cx
    y = r * math.sin(2*math.pi * t) + cy
    z = cz
    add_point(matrix, x, y, z)
    if t != 0: add_point(matrix, x, y, z)
    t += TSTEP
  add_point(matrix, r + cx, cy, cz)

def add_sector(matrix, cx, cy, cz, r, theta_i, theta_f):
    theta_i *= math.pi / 180
    theta_f *= math.pi / 180
    t = theta_i / (2*math.pi)
    while t <= theta_f / (2*math.pi):
        x = r * math.cos(2*math.pi * t) + cx
        y = r * math.sin(2*math.pi * t) + cy
        z = cz
        add_point(matrix, x, y, z)
        if t != 0: add_point(matrix, x, y, z)
        t += TSTEP
    add_edge(matrix, cx, cy, cz, cx + r*math.cos(theta_i), cy + r*math.sin(theta_i), cz)
    add_edge(matrix, cx, cy, cz, cx + r*math.cos(theta_f), cy + r*math.sin(theta_f), cz)

def add_bezier(matrix, x0, y0, x1, y1, x2, y2, x3, y3):
  ax = (3 * x1 + x3 - x0 - 3 * x2)
  bx = (3 * x0 + 3 * x2 - 6 * x1)
  cx = (3 * x1 - 3 * x0)
  dx = x0
  ay = (3 * y1 + y3 - y0 - 3 * y2)
  by = (3 * y0 + 3 * y2 - 6 * y1)
  cy = (3 * y1 - 3 * y0)
  dy = y0
  t = 0
  while t <= 1:
    x = dx + t * (cx + t * (bx + t * ax))
    y = dy + t * (cy + t * (by + t * ay))
    add_point(matrix, x, y)
    if t != 0 and t < 1: add_point(matrix, x, y)
    t += TSTEP
  del matrix[-1]

def add_hermite(matrix, x0, y0, x1, y1, rx0, ry0, rx1, ry1):
  ax = (2 * x0 + rx0 + rx1 - 2 * x1)
  bx = (3 * x1 - 3 * x0 - 2 * rx0 - rx1)
  cx = rx0
  dx = x0
  ay = (2 * y0 + ry0 + ry1 - 2 * y1)
  by = (3 * y1 - 3 * y0 - 2 * ry0 - ry1)
  cy = ry0
  dy = y0
  t = 0
  while t <= 1:
    x = dx + t * (cx + t * (bx + t * ax))
    y = dy + t * (cy + t * (by + t * ay))
    add_point(matrix, x, y)
    if t != 0 and t < 1: add_point(matrix, x, y)
    t += TSTEP
  del matrix[-1]


def draw_lines( matrix, screen, color ):
    if len(matrix) < 2:
        print('Need at least 2 points to draw')
        return

    point = 0
    while point < len(matrix) - 1:
        draw_line( int(matrix[point][0]),
                   int(matrix[point][1]),
                   int(matrix[point+1][0]),
                   int(matrix[point+1][1]),
                   screen, color)    
        point+= 2
        
def add_edge( matrix, x0, y0, z0, x1, y1, z1 ):
    add_point(matrix, x0, y0, z0)
    add_point(matrix, x1, y1, z1)
    
def add_point( matrix, x, y, z=0 ):
    matrix.append( [x, y, z, 1] )


def draw_line( x0, y0, x1, y1, screen, color ):

    #swap points if going right -> left
    if x0 > x1:
        xt = x0
        yt = y0
        x0 = x1
        y0 = y1
        x1 = xt
        y1 = yt

    x = x0
    y = y0
    A = 2 * (y1 - y0)
    B = -2 * (x1 - x0)

    #octants 1 and 8
    if ( abs(x1-x0) >= abs(y1 - y0) ):

        #octant 1
        if A > 0:            
            d = A + B/2

            while x < x1:
                plot(screen, color, x, y)
                if d > 0:
                    y+= 1
                    d+= B
                x+= 1
                d+= A
            #end octant 1 while
            plot(screen, color, x1, y1)
        #end octant 1

        #octant 8
        else:
            d = A - B/2

            while x < x1:
                plot(screen, color, x, y)
                if d < 0:
                    y-= 1
                    d-= B
                x+= 1
                d+= A
            #end octant 8 while
            plot(screen, color, x1, y1)
        #end octant 8
    #end octants 1 and 8

    #octants 2 and 7
    else:
        #octant 2
        if A > 0:
            d = A/2 + B

            while y < y1:
                plot(screen, color, x, y)
                if d < 0:
                    x+= 1
                    d+= A
                y+= 1
                d+= B
            #end octant 2 while
            plot(screen, color, x1, y1)
        #end octant 2

        #octant 7
        else:
            d = A/2 - B;

            while y > y1:
                plot(screen, color, x, y)
                if d > 0:
                    x+= 1
                    d+= A
                y-= 1
                d-= B
            #end octant 7 while
            plot(screen, color, x1, y1)
        #end octant 7
    #end octants 2 and 7
#end draw_line