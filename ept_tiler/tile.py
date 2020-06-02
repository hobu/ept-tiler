import copy
import os
import json



import logging
logger = logging.getLogger('ept_tiler')


class T(object):
    pass

    def __repr__(self):
        return str(self.__dict__)

def tile(args):
    maxx = args.maxx; minx = args.minx
    maxy = args.maxy; miny = args.miny

    dx = float(maxx - minx)
    dy = float(maxy - miny)

    tilesize = args.tilesize
    if not tilesize:
        b = (dx, dy)
        longest = b.index(max(b))
        tilesize = b[longest]/args.divisions

    buffer = args.resolution * 6.0
    if args.buffer:
        buffer = args.buffer

    nx = int((dx / tilesize) + 1)
    ny = int((dy / tilesize) + 1)


    for xi in range(nx):
        for yi in range(ny):
            x0 = (minx) + (xi*tilesize) - buffer
            x1 = (minx) + ((xi + 1) * tilesize) + buffer
            y0 = (miny) + (yi*tilesize) - buffer
            y1 = (miny) + ((yi + 1) * tilesize) + buffer
            t = [x0, y0, 0.0, x1, y1, 0.0]

            d = copy.copy(args.__dict__)
            d['minx+buffer'] = x0-buffer; d['miny+buffer'] = y0-buffer; d['minz+buffer'] = 0.0
            d['maxx-buffer'] = x1+buffer; d['maxy-buffer'] = y1+buffer; d['maxz-buffer'] = 0.0
            d['minx'] = x0; d['miny'] = y0; d['minz'] = 0.0
            d['maxx'] = x1; d['maxy'] = y1; d['maxz'] = 0.0
            d['filename'] = os.path.join(args.path, args.output) + '-%d-%d' % (xi, yi)

            p = json.dumps(args.pipeline) % d
            t = T()

            t.pipeline = p
            t.minx = minx; t.miny = miny;
            t.maxx = maxx; t.maxy = maxy;
            t.xi = xi; t.yi = yi
            t.args = args
            t.filename = d['filename']

            yield t


