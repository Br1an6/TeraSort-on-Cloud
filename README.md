# TeraSort-on-Cloud
TeraSort on Hadoop/Spark, Shared-Memory: Parallel external sort

### To run shared memory sort
`python shared_memory_sort.py number_of_proccess input_file_name output_file_name -b block_szie -k key -t temp_path`

e.g. `python shared_memory_sort.py 3 input output -b 55M -k "line[0:10]" -t /mnt`

| Args   | Value                  |
|:------:| ---------------------- |
| 0      | number of threads      |
| 1      | input file             |
| 2      | output file            |
| -b     | block size e.g. 50M 16G|
| -k     | key                    |
| -t     | temporary file path    |

We assume each line is 100 bytes. Generate your data with the gensort tool [Sortbenchmark](http://sortbenchmark.org).
Each line should be no more than 64KB. Modify the code if needed.

---


### To generate data:
`./gensort -a num_of_records filename`

e.g. 1TB `./gensort -a 10000000000 testfile`

### To verify sorted data:
`./valsort outputFileName`

###### For more information: [Please read](https://github.com/Br1an6/TeraSort-on-Cloud/blob/master/readme.txt).

License
-------

This software is licensed under the MIT license
© 2017 TeraSort on Cloud contributors [Br1an6](https://github.com/Br1an6) &  [Sh4rel](https://github.com/Sh4rel)
