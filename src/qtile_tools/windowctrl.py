from collections import namedtuple as _namedtuple


Geom = _namedtuple('Geom', ('x', 'y', 'width', 'height'))
_BORDER_WIDTH = 4

_positions = {
    'northwest': (0, 0),
    'north': (1, 0),
    'northeast': (2, 0),
    'west': (0, 1),
    'center': (1, 1),
    'east': (2, 1),
    'southwest': (0, 2),
    'south': (1, 2),
    'southeast': (2, 2),
}

class _MoveGeomMeta(type):
    def __new__(meta, name, bases, namespace):
        factory = namespace['_factory']
        positions = namespace['_positions']
        for k,v in positions.items():
            # namespace[k] = property(factory(k, v))
            namespace[k] = factory(k, v)
        namespace['_factory'] = staticmethod(factory)
        return super().__new__(meta, name, bases, namespace)


class MoveGeom(object, metaclass=_MoveGeomMeta):
    _positions = _positions
    def _factory(key, value):
        name = key
        i, j = value
        _int = int
        make = Geom._make
        def fn(self):
            x, y = self._xval(i), self._yval(j)
            width, height = self.width, self.height
            return make(_int(x) for x in (x, y, width, height))
        fn.__name__ = name
        return property(fn)

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
        "pos = 0 on top, 1 in the middle, or 2 on bottom"
        _container_geom = self._container_geom
        if position == 0:
            return _container_geom.y
        elif position == 1:
            mon_ctr_y = (_container_geom.y + _container_geom.height) // 2
            return mon_ctr_y - (self.height // 2)
        elif position == 2:
            return _container_geom.height - self.height - (2 * self.border_width)
        raise ValueError('position must be 0, 1, or 2')


def _float_move(window, geometry, above=True):
    STACKMODE_ABOVE = 0
    window.floating = True
    window.tweak_float(
        x=geometry.x,
        y=geometry.y,
        w=geometry.width,
        h=geometry.height,
    )
    if above:
        window.window.configure(stackmode=STACKMODE_ABOVE)
    return window



class MoveWindow(metaclass=_MoveGeomMeta):
    _positions = _positions
    def _factory(name, value):
        float_move = _float_move
        def fn(self, above=True):
            geom = getattr(self.move_geom, name)
            win = self.window
            return float_move(win, geom, above)
        fn.__name__ = name
        return fn

    def __init__(self, window, *, width_frac=None, height_frac=None,
                 aspect_ratio=None, border_width=_BORDER_WIDTH):
        if width_frac and height_frac:
            raise ValueError('Only give either width_frac or height_frac')
        grp = window.group
        screen = grp.screen or grp.qtile.currentScreen
        screen = Geom(screen.x, screen.y, screen.width, screen.height)
        if width_frac:
            move_geom = MoveGeom.from_width_fraction(
                container_geom=screen,
                width_frac=width_frac,
                aspect_ratio=aspect_ratio,
                border_width=border_width,
            )
        else:
            move_geom = MoveGeom.from_height_fraction(
                container_geom=screen,
                height_frac=height_frac,
                aspect_ratio=aspect_ratio,
                border_width=border_width,
            )
        self.move_geom = move_geom
        self.window = window


if __name__ == '__main__':
    mgeom = Geom(0, 0, 1600, 900)
    dirs = 'northwest north northeast west center east southwest south southeast'.split()
    geoms = [
        MoveGeom(mgeom, 100, 100),
        MoveGeom.from_width_fraction(mgeom),
        MoveGeom.from_height_fraction(mgeom),
    ]
    for wg in geoms:
        print()
        for d in dirs:
            print(d, getattr(wg, d), sep=' -> ')


    class FakeWindow:
        class group:
            screen = Geom(0, 0, 1600, 900)

        def tweak_float(self, *args, **kwargs):
            print('tweak_float', args, kwargs, sep=' -> ')

        class window:
            @staticmethod
            def configure(*args, **kwargs):
                print('window.configure', args, kwargs, sep=' -> ')

    fakewin = FakeWindow()
    x=MoveWindow(fakewin, width_frac=0.3)
    print(x.center())

