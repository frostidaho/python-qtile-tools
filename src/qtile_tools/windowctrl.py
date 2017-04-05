from collections import namedtuple as _namedtuple


Geom = _namedtuple('Geom', ('x', 'y', 'width', 'height'))
_GridName = _namedtuple('_GridName', ('i', 'j'))
_BORDER_WIDTH = 4


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


class WinGeom(object, metaclass=_WinGeomMeta):
    center    = _GridName(1, 1)
    northwest = _GridName(0, 0)
    north     = _GridName(1, 0)
    northeast = _GridName(2, 0)
    west      = _GridName(0, 1)
    east      = _GridName(2, 1)
    southwest = _GridName(0, 2)
    south     = _GridName(1, 2)
    southeast = _GridName(2, 2)

    def __init__(self, container_geom, width, height, border_width=_BORDER_WIDTH):
        self.border_width = border_width
        self._container_geom = container_geom
        self.width = width
        self.height = height

    @classmethod
    def from_width_fraction(cls, container_geom, width_frac=0.3, aspect_ratio=None, border_width=_BORDER_WIDTH):
        if aspect_ratio is None:
            aspect_ratio = container_geom.width / container_geom.height
        width = container_geom.width * width_frac
        height = width / aspect_ratio
        return cls(container_geom, width, height, border_width)

    @classmethod
    def from_height_fraction(cls, container_geom, height_frac=0.5, aspect_ratio=None, border_width=_BORDER_WIDTH):
        if aspect_ratio is None:
            aspect_ratio = container_geom.width / container_geom.height
        height = container_geom.height * height_frac
        width = height * aspect_ratio
        return cls(container_geom, width, height, border_width)

    def _xval(self, position):
        "pos = 0 on left, 1 on middle, or 2 on right"
        _container_geom = self._container_geom
        if position == 0:
            return _container_geom.x
        elif position == 1:
            mon_ctr_x = _container_geom.x + (_container_geom.width // 2)
            return mon_ctr_x - (self.width // 2)
        elif position == 2:
            return _container_geom.x + _container_geom.width - self.width - (2 * self.border_width)
        raise ValueError('position must be 0, 1, or 2')

    def _yval(self, position):
        "pos = 0, 1 or 2"
        _container_geom = self._container_geom
        if position == 0:
            return _container_geom.y
        elif position == 1:
            mon_ctr_y = (_container_geom.y + _container_geom.height) // 2
            return mon_ctr_y - (self.height // 2)
        elif position == 2:
            return _container_geom.height - self.height - (2 * self.border_width)
        raise ValueError('position must be 0, 1, or 2')


if __name__ == '__main__':
    mgeom = Geom(0, 0, 1600, 900)
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
