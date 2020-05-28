import boto3
import time
import os
import json

import multiprocessing
import subprocess
import string
from pathlib import Path
import logging
logger = logging.getLogger('ept_tiler')



profile = os.environ.get('AWS_PROFILE')
region = os.environ.get('AWS_REGION')

boto3.setup_default_session(region_name=region,
                            profile_name=profile)


class Process(object):

    def __init__(self):
        self.tasks = []

    def put(self, tile):
        self.tasks.append(tile)
    def do(self):
        pass


class SQS(Process):

    def __init__(self, QueueName):
        super(SQS, self).__init__()
        self.resource = boto3.resource('sqs')
        self.sqs = self.resource.get_queue_by_name(QueueName = QueueName)

        self.jobs = []
    def do(self):
        for tile in self.tasks:
            response = self.sqs.send_message(MessageBody = tile.pipeline)
            self.jobs.append(response)

def random_filename(path):
    import random
    import string
    from pathlib import Path
    letters = string.ascii_lowercase
    name = Path(path, ''.join(random.choice(letters) for i in range(10))).with_suffix('.json')
    return name


class Cache(Process):

    def __init__(self, path):
        super(Cache, self).__init__()
        self.path = path

    def do(self):
        cn = Path(self.path) / Path('commands')
        cn = cn.with_suffix('.txt')
        commands = open(cn, 'wb')

        for tile in self.tasks:
            fn = random_filename(self.path)
            with open(fn, 'wb') as o:
                o.write(tile.pipeline.encode('utf-8'))

            command = 'pdal pipeline %s\n' % fn.name
            commands.write(command.encode('utf-8'))



def work(tile):
    command = 'pdal pipeline --stdin'
    args = ['pdal', 'pipeline', '--stdin','--debug', '--pipeline-serialization', 'STDOUT' ]
    p = subprocess.Popen(args, stdin=subprocess.PIPE,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE,
                               encoding='utf8')
    ret = p.communicate(input=tile.pipeline)
    if p.returncode != 0:
        error = ret[1]
        logger.error(error)


class Local(Process):
    def __init__(self, directory ):
        super(Local, self).__init__()


    def do(self):
        count = multiprocessing.cpu_count()
        pool = multiprocessing.Pool(processes=count)
        process = (pool.map(work, self.tasks))

