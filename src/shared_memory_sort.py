import os
from collections import namedtuple
import heapq
import time
from multiprocessing import Process, Pipe
import optparse

""" Merge sort with shared memory

    Reference: http://interactivepython.org/courselib/static/pythonds/SortSearch/TheMergeSort.html
               https://stackoverflow.com/questions/28548414/python-quick-sort-parallel-sort-slower-than-sequential
               http://code.activestate.com/recipes/576755-sorting-big-files-the-python-26-way/
               https://groups.google.com/group/comp.lang.python/msg/484f01f1ea3c832d
"""

Keyed = namedtuple("Keyed", ["key", "obj"])
NUM_OF_PROCCESS = 1


def terminate_proc(p_list):
    """Terminate all the processes in the list
    Args:
        p_list...list
    """    
    for p in p_list:
        if p.is_alive():
            p.terminate()


def merge_lists(left, right):
    """returns a merged and sorted version of the two already-sorted lists.
    Args:
        left...list
        rigt...list
    Reture:
        list
    """
    ret = []
    li = ri = 0
    while li < len(left) and ri < len(right):
        if left[li] <= right[ri]:
            ret.append(left[li])
            li += 1
        else:
            ret.append(right[ri])
            ri += 1
    if li == len(left):
        ret.extend(right[ri:])
    else:
        ret.extend(left[li:])
    return ret


def mergesort(list_of_strings):
    """
    Merge sorting
    Arg:
        list_of_strings...list of strings
    >>> list_s = ['bbb', 'aaa', 'ccc', '111']
    >>> mergesort(list_s)
    ['111', 'aaa', 'bbb', 'ccc']
    """
    if len(list_of_strings) <= 1:
        return list_of_strings
    ind = len(list_of_strings)//2
    return merge_lists(mergesort(list_of_strings[:ind]), mergesort(list_of_strings[ind:]))


def mergeSortParallel(list_of_strings, conn, procNum):
    """Mergesort the left and right sides in parallel.
    Arg:
        list_of_strings...list of strings
        conn
        procNum...........int
    """
    if procNum <= 0 or len(list_of_strings) <= 1:
        conn.send(mergesort(list_of_strings))
        conn.close()
        return

    ind = len(list_of_strings)//2

    #child to communicate the sorted list back to us.
    pconnLeft, cconnLeft = Pipe()
    leftProc = Process(target=mergeSortParallel, args=(list_of_strings[:ind], cconnLeft, procNum - 1))
    pconnRight, cconnRight = Pipe()
    rightProc = Process(target=mergeSortParallel, args=(list_of_strings[ind:], cconnRight, procNum - 1))

    leftProc.start()
    rightProc.start()
    conn.send(merge_lists(pconnLeft.recv(), pconnRight.recv()))
    conn.close()

    #Join the left and right processes.
    leftProc.join()
    rightProc.join()
    terminate_proc([leftProc, rightProc])


def merge(key=None, *iterables):
    """Merge files"""
    if key is None:
        for element in heapq.merge(*iterables):
            yield element
    else:
        keyed_iterables = [(Keyed(key(obj), obj) for obj in iterable)
                            for iterable in iterables]
    for element in heapq.merge(*keyed_iterables):
        yield element.obj


def ext_sort(input, output, key=None, buffer_size=30000, tempdir=None):
    """Split file and peform parallel sort
    Args:
        input.........string
        output........string
        key...........eval
        buffer_size...int in lines
    """
    """
    if tempdirs is None:
        tempdirs = []
    if not tempdirs:
        tempdirs.append(gettempdir())
    """

    chunks = []
    try:

        file = open(input, 'r')
        while True:
            current_chunk = file.readlines(buffer_size)
            print '[*]  Done reading 1 chunk'
            if current_chunk == []:
                break

            # start parallel sorting
            print '[*]  Start sorting'
            pconn, cconn = Pipe()
            p = Process(target=mergeSortParallel, args=(current_chunk, cconn, NUM_OF_PROCCESS))
            p.start()
            current_chunk = pconn.recv()
            p.join()
            terminate_proc([p])
            print '[*]  Chunk sorted'
            output_chunk = open(os.path.join(tempdir, '%06i' % len(chunks)), 'w+b', 100)
            chunks.append(output_chunk)
            output_chunk.writelines(current_chunk)
            output_chunk.flush()
            output_chunk.seek(0)
            print '[*]  Split file', len(chunks)
        with open(output, 'wb', 100) as output_file:
            output_file.writelines(merge(key, *chunks))
    finally:
        for chunk in chunks:
            try:
                chunk.close()
                os.remove(chunk.name)
            except Exception:
                pass


def parse_memory(string):
    """Convert memory to lines
    Args:
        string.........string
    >>> parse_memory('100M')
    1000000
    """
    if string[-1].lower() == 'k':
        return int(string[:-1]) * 1000
    elif string[-1].lower() == 'm':
        return int(string[:-1]) * 1000 * 1000
    elif string[-1].lower() == 'g':
        return int(string[:-1]) * 1000 * 1000 * 1000
    else:
        return int(string)


def main():
    """
    args 0:number of thread args 1: file name args 2: output file
    a line cannot be more than 64KB
    """
    parser = optparse.OptionParser()
    parser.add_option(
        '-b', '--buffer',
        dest='buffer_size',
        type='string', default='3M',
        help='''Size of the line buffer. The file to sort is
            divided into chunks of that many lines. AKA at least one line Default : 3M.'''
    )
    parser.add_option(
        '-k', '--key',
        dest='key',
        help='''Python expression used to compute the key for each
            line, "lambda line:" is prepended.\n
            Example : -k "line[5:10]". By default, the whole line is the key.'''
    )
    parser.add_option(
        '-t', '--tempdir',
        dest='tempdirs',
        type='string', default='',
        help='''Temporary directory to use. You might get performance
            improvements if the temporary directory is not on the same physical
            disk than the input and output directories. You can even try
            providing multiples directories on differents physical disks.
            Use multiple -t options to do that.'''
    )

    options, args = parser.parse_args()

    if options.key:
        options.key = eval('lambda line : (%s)' % options.key)
    NUM_OF_PROCCESS = int(args[0])  # 2^(n+1) - 1 processes will be instantiated.

    # start the timer
    start = time.time()
    # Do merge sorting
    ext_sort(args[1], args[2], options.key, parse_memory(options.buffer_size), options.tempdirs)

    duration = time.time() - start
    print "Duration:", duration


if __name__ == '__main__':
    main()
