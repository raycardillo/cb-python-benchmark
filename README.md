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

Notice that there is a [binary](./binary), [json](./json), and [small](./small) variant now.


### Binary Variant

This variant uses **binary** documents (sizes are 60KB, 80KB, 100KB).

Execute the **binary** [CBUpsert.py](./binary/CBUpsert.py) script first and then the **binary** [CBRead.py](./binary/CBRead.py) script.
For consistency, it would be better to run `CBUpsert.py` once first to seed the initial data first and then subsequent operations will all be the same type of operation.

The bucket name is passed as a parameter and there are some constants at the top of each file that can be used to change the number of docs, credentials, etc.

You should run the following combinations for comparison:
- CB 3.2.7 + CouchStore - [bin-upsert-couchstore-cb-3.2.7.out](./binary/bin-upsert-couchstore-cb-3.2.7.out) [bin-read-couchstore-cb-3.2.7.out](./binary/bin-read-couchstore-cb-3.2.7.out)
- CB 4.1.1 + CouchStore [bin-upsert-couchstore-cb-4.1.1.out](./binary/bin-upsert-couchstore-cb-4.1.1.out) [bin-read-couchstore-cb-4.1.1.out](./binary/bin-read-couchstore-cb-4.1.1.out)
- CB 3.2.7 + Magma -[bin-upsert-magma-cb-3.2.7.out](./binary/bin-upsert-magma-cb-3.2.7.out) [bin-read-magma-cb-3.2.7.out](./binary/bin-read-magma-cb-3.2.7.out)
- CB 4.1.1 + Magma - [bin-upsert-magma-cb-4.1.1.out](./binary/bin-upsert-magma-cb-4.1.1.out) [bin-read-magma-cb-4.1.1.out](./binary/bin-read-magma-cb-4.1.1.out)


### JSON Variant

This variant uses **JSON** documents (size are roughly 60KB, 80KB, 100KB).

Execute the **JSON** [CBUpsert.py](./json/CBUpsert.py) script first and then the **JSON** [CBRead.py](./json/CBRead.py) script.
For consistency, it would be better to run `CBUpsert.py` once first to seed the initial data first and then subsequent operations will all be the same type of operation.

The bucket name is passed as a parameter and there are some constants at the top of each file that can be used to change the number of docs, credentials, etc.

You should run the following combinations for comparison:
- CB 3.2.7 + CouchStore - [json-upsert-couchstore-cb-3.2.7.out](./json/json-upsert-couchstore-cb-3.2.7.out) [json-read-couchstore-cb-3.2.7.out](./json/json-read-couchstore-cb-3.2.7.out)
- CB 4.1.1 + CouchStore [json-upsert-couchstore-cb-4.1.1.out](./json/json-upsert-couchstore-cb-4.1.1.out) [json-read-couchstore-cb-4.1.1.out](./json/json-read-couchstore-cb-4.1.1.out)
- CB 3.2.7 + Magma -[json-upsert-magma-cb-3.2.7.out](./json/json-upsert-magma-cb-3.2.7.out) [json-read-magma-cb-3.2.7.out](./json/json-read-magma-cb-3.2.7.out)
- CB 4.1.1 + Magma - [json-upsert-magma-cb-4.1.1.out](./json/json-upsert-magma-cb-4.1.1.out) [json-read-magma-cb-4.1.1.out](./json/json-read-magma-cb-4.1.1.out)


### Small (Binary) Variant

This variant uses **small binary** documents (sizes are 2KB, 4KB, 8KB).

Execute the **small** [CBUpsert.py](./small/CBUpsert.py) script first and then the **small** [CBRead.py](./small/CBRead.py) script.
For consistency, it would be better to run `CBUpsert.py` once first to seed the initial data first and then subsequent operations will all be the same type of operation.

The bucket name is passed as a parameter and there are some constants at the top of each file that can be used to change the number of docs, credentials, etc.

You should run the following combinations for comparison:
- CB 3.2.7 + CouchStore - [sm-upsert-couchstore-cb-3.2.7.out](./small/sm-upsert-couchstore-cb-3.2.7.out) [sm-read-couchstore-cb-3.2.7.out](./small/sm-read-couchstore-cb-3.2.7.out)
- CB 4.1.1 + CouchStore [sm-upsert-couchstore-cb-4.1.1.out](./small/sm-upsert-couchstore-cb-4.1.1.out) [sm-read-couchstore-cb-4.1.1.out](./small/sm-read-couchstore-cb-4.1.1.out)
- CB 3.2.7 + Magma -[sm-upsert-magma-cb-3.2.7.out](./small/sm-upsert-magma-cb-3.2.7.out) [sm-read-magma-cb-3.2.7.out](./small/sm-read-magma-cb-3.2.7.out)
- CB 4.1.1 + Magma - [sm-upsert-magma-cb-4.1.1.out](./small/sm-upsert-magma-cb-4.1.1.out) [sm-read-magma-cb-4.1.1.out](./small/sm-read-magma-cb-4.1.1.out)


## General Notes & Reminders

- It's important to make sure there aren't any other processes running that might consume a lot of memory, disk IO, or CPU.
- Be sure to run `CBUpsert.py` once first to seed the initial data and then subsequent operations will all be the same type of operation.
- For each combination, first run `CBUpsert.py` and then run `CBRead.py`
- You will see some deprecation warnings during the Couchbase v4 execution because the location of some Options classes have changed.