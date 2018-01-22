from collections import namedtuple
from functools import partial
from itertools import chain
from math import sin, cos, tan, radians
from time import time
from tkinter import Tk, Canvas, mainloop
from typing import Union, Tuple, Optional


class V(namedtuple('V', 'x y z w')):
    __slots__ = ()

    def __add__(self, v: 'V') -> 'V':
        return V(self.x + v.x, self.y + v.y, self.z + v.z, self.w + v.w)

    def __sub__(self, v: 'V') -> 'V':
        return V(self.x - v.x, self.y - v.y, self.y - v.z, self.w - v.w)

    def __mul__(self, m: Union['V', 'M']) -> 'V':
        if isinstance(m, V):
            return V(self.x * m.x, self.y * m.y, self.z * m.z, self.w * m.w)
        elif isinstance(m, M):
            return vm(self, m)


class M(namedtuple('M', 'a0 a1 a2 a3 '
                        'b0 b1 b2 b3 '
                        'c0 c1 c2 c3 '
                        'd0 d1 d2 d3')):
    __slots__ = ()

    def __mul__(self, m: Union[V, 'M']) -> Union[V, 'M']:
        if isinstance(m, V):
            return vm(m, self)
        return mm(self, m)

    def __str__(self) -> str:
        return ('M(a0=%f, a1=%f, a2=%f, a3=%f,\n'
                '  b0=%f, b1=%f, b2=%f, b3=%f,\n'
                '  c0=%f, c1=%f, c2=%f, c3=%f,\n'
                '  d0=%f, d1=%f, d2=%f, d3=%f)' % self)

    def __repr__(self):
        return str(self)


def vm(v: V, m: M) -> V:
    """Multiplies vector v with matrix m and returns a new vector."""
    return V(
        v.x * m.a0 + v.y * m.a1 + v.z * m.a2 + v.w * m.a3,
        v.x * m.b0 + v.y * m.b1 + v.z * m.b2 + v.w * m.b3,
        v.x * m.c0 + v.y * m.c1 + v.z * m.c2 + v.w * m.c3,
        v.x * m.d0 + v.y * m.d1 + v.z * m.d2 + v.w * m.d3)


def mm(m1: M, m2: M) -> M:
    """Multiplies 2 matrices and returns a new matrix."""
    return M(
        m1.a0 * m2.a0 + m1.a1 * m2.b0 + m1.a2 * m2.c0 + m1.a3 * m2.d0,
        m1.a0 * m2.a1 + m1.a1 * m2.b1 + m1.a2 * m2.c1 + m1.a3 * m2.d1,
        m1.a0 * m2.a2 + m1.a1 * m2.b2 + m1.a2 * m2.c2 + m1.a3 * m2.d2,
        m1.a0 * m2.a3 + m1.a1 * m2.b3 + m1.a2 * m2.c3 + m1.a3 * m2.d3,

        m1.b0 * m2.a0 + m1.b1 * m2.b0 + m1.b2 * m2.c0 + m1.b3 * m2.d0,
        m1.b0 * m2.a1 + m1.b1 * m2.b1 + m1.b2 * m2.c1 + m1.b3 * m2.d1,
        m1.b0 * m2.a2 + m1.b1 * m2.b2 + m1.b2 * m2.c2 + m1.b3 * m2.d2,
        m1.b0 * m2.a3 + m1.b1 * m2.b3 + m1.b2 * m2.c3 + m1.b3 * m2.d3,

        m1.c0 * m2.a0 + m1.c1 * m2.b0 + m1.c2 * m2.c0 + m1.c3 * m2.d0,
        m1.c0 * m2.a1 + m1.c1 * m2.b1 + m1.c2 * m2.c1 + m1.c3 * m2.d1,
        m1.c0 * m2.a2 + m1.c1 * m2.b2 + m1.c2 * m2.c2 + m1.c3 * m2.d2,
        m1.c0 * m2.a3 + m1.c1 * m2.b3 + m1.c2 * m2.c3 + m1.c3 * m2.d3,

        m1.d0 * m2.a0 + m1.d1 * m2.b0 + m1.d2 * m2.c0 + m1.d3 * m2.d0,
        m1.d0 * m2.a1 + m1.d1 * m2.b1 + m1.d2 * m2.c1 + m1.d3 * m2.d1,
        m1.d0 * m2.a2 + m1.d1 * m2.b2 + m1.d2 * m2.c2 + m1.d3 * m2.d2,
        m1.d0 * m2.a3 + m1.d1 * m2.b3 + m1.d2 * m2.c3 + m1.d3 * m2.d3)


def scale_m(x=1.0, y=1.0, z=1.0) -> M:
    """Returns a scaling matrix with the specified magnitudes."""
    return M(x, 0.0, 0.0, 0.0,
             0.0, y, 0.0, 0.0,
             0.0, 0.0, z, 0.0,
             0.0, 0.0, 0.0, 1.0)


def trans_m(v: V) -> M:
    """Returns a translation matrix along to the specified vector."""
    return M(1.0, 0.0, 0.0, v.x,
             0.0, 1.0, 0.0, v.y,
             0.0, 0.0, 1.0, v.z,
             0.0, 0.0, 0.0, 1.0)


def rot_x(a: float) -> M:
    """Returns a rotation matrix on the x-axis, with the specified angle in
    radians."""
    return M(1.0, 0.0, 0.0, 0.0,
             0.0, cos(a), -sin(a), 0.0,
             0.0, sin(a), cos(a), 0.0,
             0.0, 0.0, 0.0, 1.0)


def rot_y(a: float) -> M:
    """Returns a rotation matrix on the y-axis, with the specified angle in
    radians."""
    return M(cos(a), 0.0, sin(a), 0.0,
             0.0, 1.0, 0.0, 0.0,
             -sin(a), 0.0, cos(a), 0.0,
             0.0, 0.0, 0.0, 1.0)


def rot_z(a: float) -> M:
    """Returns a rotation matrix on the z-axis, with the specified angle in
    radians."""
    return M(cos(a), -sin(a), 0.0, 0.0,
             sin(a), cos(a), 0.0, 0.0,
             0.0, 0.0, 1.0, 0.0,
             0.0, 0.0, 0.0, 1.0)


class Model(object):
    def __init__(self, *polygons: Tuple[V, ...], color: Optional[str]=None) -> None:
        self.polygons = polygons
        self.color = color

    def __mul__(self, m: M) -> 'Model':
        """Applies the specified transformation matrix to the model and returns
        a new model instance.
        """
        return Model(*tuple(tuple(v * m for v in pol) for pol in self.polygons),
                     color=self.color)


class Projector(object):
    def __init__(self, resolution, angle_of_view=60) -> None:
        """Instantiates a perspective projector located at the origin, facing
        the negative z-axis, with the specified angle of view in degrees.

        The specified resolution is that of the (square) screen (e.g. 800 or
        1024).
        """
        self.aov = radians(angle_of_view)
        self.size = resolution
        self.plane = tan(self.aov / 2.0)  # half the width of projection plane
        self.scale = resolution / (self.plane * 2)

    def project(self, v: V) -> (int, int):
        """Given a vertex, computes its (x, y) pixel projection on the
        projection plane, normalizes to NDC space, converts to raster space and
        returns the screen pixel coordinates.
        """
        return (int(((v.x / -v.z) + self.plane) * self.scale),
                int(((v.y / -v.z) + self.plane) * self.scale))


def render(canvas: Canvas, proj: Projector, model: Model) -> None:
    for pol in model.polygons:
        canvas.create_line(*chain.from_iterable(proj.project(v) for v in pol),
                           fill=model.color)


CUBE = partial(
    Model,
    # upper plane:
    (V(.5, .5, .5, 1), V(-.5, .5, .5, 1), V(-.5, -.5, .5, 1),
     V(.5, -.5, .5, 1), V(.5, .5, .5, 1)),
    # bottom plane:
    (V(.5, .5, -.5, 1), V(-.5, .5, -.5, 1), V(-.5, -.5, -.5, 1),
     V(.5, -.5, -.5, 1), V(.5, .5, -.5, 1)),
    # connecting rods:
    (V(.5, .5, .5, 1), V(.5, .5, -.5, 1)),
    (V(-.5, .5, .5, 1), V(-.5, .5, -.5, 1)),
    (V(-.5, -.5, .5, 1), V(-.5, -.5, -.5, 1)),
    (V(.5, -.5, .5, 1), V(.5, -.5, -.5, 1))
)


if __name__ == '__main__':
    projector = Projector(400, angle_of_view=52)
    model1 = CUBE(color='red')
    model2 = CUBE(color='blue') * scale_m(.2, .2, .2)
    speed = 20   # rotation in degrees/second

    screen = Tk()
    screen.winfo_toplevel().title('Perspective Projection')
    screen.lift()
    screen.attributes('-topmost', True)
    screen.after_idle(screen.attributes, '-topmost', False)
    w = Canvas(screen, width=projector.size, height=projector.size)
    w.pack()

    def frame(prev_tick, prev_angle):
        w.delete(*w.find_all())
        now = time()
        angle = (prev_angle + (now - prev_tick) * speed) % 360

        a = radians(angle)
        render(w, projector, model1 *
               rot_x(a) * rot_y(a) * rot_z(a) * trans_m(V(0, 0, -2, 1)))
        render(w, projector, model2 *
               rot_x(-a) * rot_y(-a) * rot_z(-a) * trans_m(V(0, 0, -2, 1)))

        screen.after(50, frame, now, angle)

    screen.after_idle(frame, time(), 0)
    mainloop()
