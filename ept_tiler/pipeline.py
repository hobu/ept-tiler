

import sys
import io
import json
from .tile import tile
from .layer import Layer
from .proqueue import Local, SQS


import logging
logger = logging.getLogger('ept_tiler')


def get_writer_data(json):
    for s in json:
        try:
            t = s['type'].split('.')[0]
            if t == 'writers':
                try:
                    return s
                except KeyError:
                    return None

        except KeyError:
            pass


def update_tags(args):
    writer = get_writer_data(args.pipeline)

    tags = args.tags

    writer['user_data'] = tags['user_data']

    return writer


def read_json(filename, stdin=False):
    if stdin:
        buffer = sys.stdin.buffer
    else:
        buffer = open(filename, 'rb')

    stream = io.TextIOWrapper(buffer, encoding='utf-8')

    pipe = stream.read()
    pipe = json.loads(pipe)
    return pipe

def pipeline(args):
    # read pipeline substitute

    args.pipeline = read_json(args.pipeline, args.stdin)


    if args.tags:
        args.tags = read_json(args.tags)
        update_tags(args)

    layer = None
    if args.features:
        layer = Layer(args)


    queue = None
    if args.target_type == 'local':
        queue = Local(args.target)
    else:
        queue = SQS(args.target)



    tiles = tile(args)

    count = 0
    for t in tiles:

        if count == args.limit and count != 0:
            break

        if layer:
            layer.add(t)
        queue.put(t)

        logger.debug(t.pipeline)

        count += 1

    queue.do()
    import pdb;pdb.set_trace()





