from collections import namedtuple as _namedtuple

Geom = _namedtuple('Geom', ('x', 'y', 'width', 'height'))
_GridName = _namedtuple('_GridName', ('i', 'j'))

class _WinGeomMeta(type):
    def __new__(meta, name, bases, namespace):
        
        def newfn(name, i, j):
            _int = int
            make = Geom._make
            def fn(self):
                x, y = self._xval(i), self._yval(j)
                width, height = self.width, self.height
                return make(_int(x) for x in (x, y, width, height))
            fn.__name__ = name
            return fn
        
        _isinstance = isinstance
        for k,v in namespace.items():
            if _isinstance(v, _GridName):
                namespace[k] = property(newfn(k, *v))
        return super().__new__(meta, name, bases, namespace)

_BORDER_WIDTH = 4

class WinGeom(object, metaclass=_WinGeomMeta):
    center = _GridName(1, 1)
    northwest = _GridName(0, 0)
    north = _GridName(1, 0)
    northeast = _GridName(2, 0)
    west = _GridName(0, 1)
    east = _GridName(2, 1)
    southwest = _GridName(0, 2)
    south = _GridName(1, 2)
    southeast = _GridName(2, 2)

    def __init__(self, screen_geom, width, height, border_width=_BORDER_WIDTH):
        self.border_width = border_width
        self._screen_geom = screen_geom
        self.width = width
        self.height = height

    @classmethod
    def from_width_fraction(cls, screen_geom, width_frac=0.3, aspect_ratio=None, border_width=_BORDER_WIDTH):
        if aspect_ratio is None:
            aspect_ratio = screen_geom.width / screen_geom.height
        width = screen_geom.width * width_frac
        height = width / aspect_ratio
        return cls(screen_geom, width, height, border_width)

    @classmethod
    def from_height_fraction(cls, screen_geom, height_frac=0.5, aspect_ratio=None, border_width=_BORDER_WIDTH):
        if aspect_ratio is None:
            aspect_ratio = screen_geom.width / screen_geom.height
        height = screen_geom.height * height_frac
        width = height * aspect_ratio
        return cls(screen_geom, width, height, border_width)

    def _xval(self, position):
        "pos = 0 on left, 1 on middle, or 2 on right"
        _screen_geom = self._screen_geom
        if position == 0:
            return _screen_geom.x
        elif position == 1:
            mon_ctr_x = _screen_geom.x + (_screen_geom.width // 2)
            return mon_ctr_x - (self.width // 2)
        elif position == 2:
            return _screen_geom.x + _screen_geom.width - self.width - (2 * self.border_width)
        raise ValueError('position must be 0, 1, or 2')

    def _yval(self, position):
        "pos = 0, 1 or 2"
        _screen_geom = self._screen_geom
        if position == 0:
            return _screen_geom.y
        elif position == 1:
            mon_ctr_y = (_screen_geom.y + _screen_geom.height) // 2
            return mon_ctr_y - (self.height // 2)
        elif position == 2:
            return _screen_geom.height - self.height - (2 * self.border_width)
        raise ValueError('position must be 0, 1, or 2')


if __name__ == '__main__':
    mgeom = Geom(0, 0, 1600, 900)
    # x = WinGeom(mgeom, 100, 100)
    dirs = 'northwest north northeast west center east southwest south southeast'.split()
    geoms = [
        WinGeom(mgeom, 100, 100),
        WinGeom.from_width_fraction(mgeom),
        WinGeom.from_height_fraction(mgeom),
    ]
    for wg in geoms:
        print()
        for d in dirs:
            print(d, getattr(wg, d), sep=' -> ')
