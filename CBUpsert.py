import argparse
import random
import sys
import threading
import time
from datetime import timedelta
from importlib.metadata import version

from couchbase.auth import PasswordAuthenticator
from couchbase.cluster import Cluster, ClusterOptions
from couchbase.collection import InsertOptions
from couchbase.options import LockMode
from couchbase.transcoder import RawBinaryTranscoder

# Static benchmark config parameters
username = 'Administrator'
password = 'P@ssw0rd'
NUM_DOCS = 15000
NUM_DOCS_STR = str(NUM_DOCS)

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


class UpsertThread(threading.Thread):
    def __init__(self, thread_id, name, doc_size):
        threading.Thread.__init__(self)
        self.thread_id = thread_id
        self.name = name
        self.doc_size = doc_size

    def run(self):
        print("Starting {name} ({size}) thread".format(name=self.name, size=self.doc_size))
        sys.stdout.flush()

        key_prefix = 'doc_{name}_'.format(name=self.name)

        thread_start = time.perf_counter_ns()
        upsert_docs(self.doc_size, key_prefix)
        thread_end = time.perf_counter_ns()

        thread_total = thread_end - thread_start
        print("\nCompleted {name} thread after {time_ns}ns = {time_s}s\n"
              .format(name=self.name, time_ns=thread_total, time_s=thread_total / 1000000000))
        sys.stdout.flush()


transcoder = RawBinaryTranscoder()

# Connect options - authentication
auth = PasswordAuthenticator(
    username,
    password,
)

# Get a reference to our cluster
# NOTE: For TLS/SSL connection use 'couchbases://<your-ip-address>' instead
cluster = Cluster('couchbase://localhost', ClusterOptions(auth, lockmode=LockMode.WAIT))

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


# Function to create random binary data
def rand_binary(p):
    value = bytearray(random.getrandbits(8) for _ in range(p))
    return value


def upsert_docs(doc_size, key_prefix):
    long_suffix = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
    doc_size_str = str(doc_size)

    for i in range(NUM_DOCS):
        data = rand_binary(doc_size)
        p_done = (i / NUM_DOCS) * 100
        istr = str(i)
        if i % 1000 == 0:
            print(str(p_done) + '% done with ' + doc_size_str + ' docs. ' +
                  istr + ' docs inserted of ' + NUM_DOCS_STR + ' total')
        cb_coll.upsert(key_prefix + istr + long_suffix, data, InsertOptions(transcoder=transcoder))


# Create new threads
thread1 = UpsertThread(1, "60k", 60000)
thread2 = UpsertThread(2, "80k", 80000)
thread3 = UpsertThread(3, "100k", 100000)

started = time.perf_counter_ns()
print("Threads Started @ {time_ns}ns = {time_s.02f}s\n".format(time_ns=started, time_s=started / 1000000000))

# Start new Threads
thread1.start()
thread2.start()
thread3.start()

# Wait for Threads to complete
thread1.join()
thread2.join()
thread3.join()

completed = time.perf_counter_ns()
print("\nThreads Completed @ {time_ns}ns = {time_s.02f}s".format(time_ns=completed, time_s=completed / 1000000000))

total = completed - started
print("\nTotal Time @ {time_ns}ns = {time_s.02f}s\n".format(time_ns=total, time_s=total / 1000000000))
