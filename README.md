# cb-python-benchmark

A quick Couchbase Python benchmark test app that performs UPSERT and GET of binary documents of various sizes.
The primary intent is to compare performance of the v3.2 release vs the v4.1 release.

## Setup

1. Install Couchbase locally (e.g., using Docker with ports exported or traditional install).
2. Create one bucket using `couchstore` and one using `magma` and the same exact memory and other configuration (e.g. `benchmark-couchstore`, `benchmark-magma`).
3. Install the latest version Python 3 and pip.
4. Use **PyCharm** or something that will allow you to easily switch between Couchbase library versions.
5. `pip` install the appropriate Couchbase SDK (3.2.7 and 4.1.1) then install `numpy` and any other dependencies.
5. The intent is to keep everything the same **except** for the Couchbase library.


## Execution

If using **PyCharm** the included Run Configurations will be helpful.

Execute the [CBUpsert.py](./CBUpsert.py) script first and then the [CBRead.py](./CBRead.py) script.
For consistency, it would be better to run `CBUpsert.py` once first to seed the initial data first and then subsequent operations will all be the same type of operation.

The bucket name is passed as a parameter and there are some constants at the top of each file that can be used to change the number of docs, credentials, etc.

You should run the following combinations for comparison:
- CB 3.2.7 + CouchStore - [upsert-couchstore-cb-3.2.7.out](upsert-couchstore-cb-3.2.7.out) [read-couchstore-cb-3.2.7.out](read-couchstore-cb-3.2.7.out)
- CB 4.1.1 + CouchStore [upsert-couchstore-cb-4.1.1.out](upsert-couchstore-cb-4.1.1.out) [read-couchstore-cb-4.1.1.out](read-couchstore-cb-4.1.1.out)
- CB 3.2.7 + Magma -[upsert-magma-cb-3.2.7.out](upsert-magma-cb-3.2.7.out) [read-magma-cb-3.2.7.out](read-magma-cb-3.2.7.out)
- CB 4.1.1 + Magma - [upsert-magma-cb-4.1.1.out](upsert-magma-cb-4.1.1.out) [read-magma-cb-4.1.1.out](read-magma-cb-4.1.1.out)


## Notes

- It's important to make sure there aren't any other processes running that might consume a lot of memory, disk IO, or CPU.
- For each combination, first run `CBUpsert.py` and then `CBRead.py`
- You will see some deprecation warnings during the Couchbase v4 execution because the location of some Options classes have changed.