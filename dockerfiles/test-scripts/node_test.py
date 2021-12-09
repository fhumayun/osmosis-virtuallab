#!/usr/bin/env python3

import os
import requests
import time
from functools import partial
from multiprocessing import Pool


def request(hostname, iters, wait):
    """
    Make the requests to the nodes to see if they are active
    ----------
    Parameters
    ----------
    hostname : str
        The nodes names
    iters: int
        Amount of iterations to make
    wait: int
        Seconds to wait between iterations

    Returns
    -------
    list
        a list of the information receive from the requests
    """
    print('Running requests on %s' %hostname)
    results = []
    # sending get request and saving the response as response object
    for i in range(iters):
        print('Running iters on %s' %hostname)
        time.sleep(wait)
        try:
            r = requests.get('http://%s:9091/Info' %hostname, timeout=5)
            results.append(r.status_code)
        except requests.exceptions.ConnectionError as e:
            results.append(e)
        except requests.exceptions.RequestException as e:
            print(e)

    return results

# get the nodes from the environment variable NODES
nodes = os.environ.get('NODES').split(';')

p = partial(request, iters=6, wait=2)

# Run parallel process to make the requests to the nodes
with Pool(len(nodes)) as pool:
    print("Testing nodes")
    node_data = pool.map(p,nodes, 1)

working_nodes = []

# Acceptance Criteria
pass_threshold = 0.9

for node in node_data:
    # Counts the amount of good requests that were made
    pass_request = node.count(200)
    if pass_request > (len(node)*pass_threshold):
        working_nodes.append(node)


# Creates the file with the results, 1 for passed and 0 for failed
result_file = open('node_result.txt', 'w')

if len(working_nodes) == len(nodes):
    result_file.write('SUCCEEDED')
else:
    result_file.write('FAILED')

result_file.close()
