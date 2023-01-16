import argparse
import random
import time
from datetime import timedelta
from importlib.metadata import version
import numpy as np

from couchbase.auth import PasswordAuthenticator
from couchbase.cluster import Cluster, ClusterOptions
from couchbase.collection import GetOptions
from couchbase.transcoder import RawBinaryTranscoder

# Static benchmark config parameters
username = 'Administrator'
password = 'P@ssw0rd'
NUM_DOCS = 2000
MAX_DOCS_INDEX = NUM_DOCS-1
NUM_READ_BATCHES = 2

# Initialize parser
parser = argparse.ArgumentParser()

# Adding optional argument
parser.add_argument('bucket_name', help="Couchbase bucket name to use")

# Read arguments from command line
args = parser.parse_args()

bucket_name = args.bucket_name

# Print the run configuration
print("Running with:\n  couchbase version = {version}\n  bucket = {bucket}\n"
      .format(version=version('couchbase'), bucket=bucket_name))

transcoder = RawBinaryTranscoder()

# Connect options - authentication
auth = PasswordAuthenticator(
    username,
    password,
)

# Get a reference to our cluster
# NOTE: For TLS/SSL connection use 'couchbases://<your-ip-address>' instead
cluster = Cluster('couchbase://localhost', ClusterOptions(auth))

# Wait until the cluster is ready for use.
try:
    cluster.wait_until_ready(timedelta(seconds=5))
    print("wait_until_ready completed successfully\n")
except AttributeError:
    print("wait_until_ready is not available - sleeping instead\n")
    time.sleep(5)

# get a reference to our bucket
cb = cluster.bucket(bucket_name)

# Get a reference to the default collection, required for older Couchbase server versions
cb_coll = cb.default_collection()

long_suffix = "aaaaa"


def read_mixed_docs():
    start_read = time.perf_counter_ns()
    all_times = []

    get_options = GetOptions(transcoder=transcoder)

    for i in range(10000):
        key = 'bdoc_2k_{:}{:}'.format(random.randint(0, MAX_DOCS_INDEX), long_suffix)

        start_get = time.perf_counter_ns()
        res = cb_coll.get(key, get_options)
        end_get = time.perf_counter_ns()

        all_times.append(end_get - start_get)

        for j in range(10):
            key = 'bdoc_4k_{:}{:}'.format(random.randint(0, MAX_DOCS_INDEX), long_suffix)

            start_get = time.perf_counter_ns()
            res = cb_coll.get(key, get_options)
            end_get = time.perf_counter_ns()

            all_times.append(end_get - start_get)

        for j in range(2):
            key = 'bdoc_8k_{:}{:}'.format(random.randint(0, MAX_DOCS_INDEX), long_suffix)

            start_get = time.perf_counter_ns()
            res = cb_coll.get(key, get_options)
            end_get = time.perf_counter_ns()

            all_times.append(end_get - start_get)

    end_read = time.perf_counter_ns()

    total_read = end_read - start_read
    print("Total Read Batch Time @ {:}ns = {:.02f}s".format(total_read, total_read / 1000000000))

    all_times.sort()
    np_array = np.array(all_times)
    print("size: {:}".format(np.size(np_array)))
    print("avg:  {:.02f}ns".format(np.average(np_array)))
    print("min:  {:.02f}ns".format(np_array.min()))
    print("max:  {:.02f}ns".format(np_array.max()))
    print("p50:  {:.02f}ns".format(np.percentile(np_array, 50)))
    print("p95:  {:.02f}ns".format(np.percentile(np_array, 95)))
    print("p99:  {:.02f}ns".format(np.percentile(np_array, 99)))
    print("p999: {:.02f}ns".format(all_times[int(len(all_times) * 0.999)]))


started = time.perf_counter_ns()
print("Reads Started @ {time_ns}ns = {time_s:.02f}s".format(time_ns=started, time_s=started / 1000000000))

for x in range(NUM_READ_BATCHES):
    print("\nRead Batch ({:}) ...".format(x))
    read_mixed_docs()

completed = time.perf_counter_ns()
print("\nReads Completed @ {time_ns}ns = {time_s:.02f}s".format(time_ns=completed, time_s=completed / 1000000000))

total = completed - started
print("\nTotal Time @ {time_ns}ns = {time_s:.02f}s\n".format(time_ns=total, time_s=total / 1000000000))
