#ept-tiler command

from .pipeline import pipeline


import logging
import sys

logger = logging.getLogger('ept_tiler')

# create console handler and set level to debug
ch = logging.StreamHandler(stream=sys.stderr)

# create formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# add formatter to ch
ch.setFormatter(formatter)

# add ch to logger
logger.addHandler(ch)
logger.setLevel(logging.DEBUG)



def main():
    import argparse

    parser = argparse.ArgumentParser(description="EPT Tiler")
    parser.add_argument("url", type=str, help="EPT Endpoint URL")
    parser.add_argument("-p", "--pipeline", type=str, help="Pipeline filename to execute")
    parser.add_argument("-s", "--stdin", action="store_true", help="Read PDAL pipeline from STDIN")
    parser.add_argument("--target-type", choices=['sqs','local'], default='local', help="Where to run the jobs")
    parser.add_argument("-t", "--target", type=str, help="Queue to place jobs")
    parser.add_argument("-g", "--tags", type=str, help="Filename to use for 'user_data'")
    parser.add_argument("-o", "--output", type=str , default='something', help="Output filename")
    parser.add_argument("-f", "--features", type=str , default=None, help="Save tile boundaries as filename")
    parser.add_argument("--path", type=str , default='tiles/', help="Output path directory")
    parser.add_argument("-l","--limit", type=int, help="Only run 'limit' tiles")

    tilesplit = parser.add_mutually_exclusive_group()
    tilesplit.add_argument("-e", "--tilesize", type=float, default= None, help="Tile edge size")
    tilesplit.add_argument("-d", "--divisions", type=int, default=6, help="Number of tiles to split domain ")

    group = parser.add_mutually_exclusive_group()
    group.add_argument("-v", "--verbose", action="store_true")
    group.add_argument("-q", "--quiet", action="store_true")

    options = parser.add_argument_group('Pipeline options')
    options.add_argument("-r", "--resolution", default=5.0, type=float, help="EPT resolution")
    options.add_argument("-b", "--bbox",
                         type=float,
                         nargs=6,
                         metavar = ('minx','miny','minz','maxx','maxy','maxz'),
                         default = None,
                         help="EPT query limit")
    options.add_argument("-m", "--buffer", type=float, default= None, help="Tile boundary metatile buffer. Defaults to 10x resolution size")
    args = parser.parse_args()


    if args.bbox:
        args.minx = args.bbox[0]
        args.miny = args.bbox[1]
        args.minz = args.bbox[2]
        args.maxx = args.bbox[3]
        args.maxy = args.bbox[4]
        args.maxz = args.bbox[5]

    args.tile_id = 'tiles/empty.tif'

    p = pipeline(args)





