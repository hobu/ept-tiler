import boto3
import time
import os
import json

import multiprocessing
import subprocess


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

