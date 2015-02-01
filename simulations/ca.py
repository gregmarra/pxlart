""" Code example from Complexity and Computation, a book about
exploring complexity science with Python.  Available free from

http://greenteapress.com/complexity

Copyright 2011 Allen B. Downey.
Distributed under the GNU General Public License at gnu.org/licenses/gpl.html.
"""

import numpy

class CASimulation(object):
    """A CA is a cellular automaton; the parameters for __init__ are:

    rule:  an integer in the range 0-255 that represents the CA rule
           using Wolfram's encoding.
    n:     the number of rows (timesteps) in the result.
    ratio: the ratio of columns to rows.
    """

    def __init__(self, rule, n):
        """Attributes:
        table:  rule dictionary that maps from triple to next state.
        n:      the number of cells
        array:  the numpy array that contains the data.
        next:   the index of the next empty row.
        """
        self.table = self.make_table(rule)
        self.n = n
        self.array = numpy.zeros(n, dtype=numpy.int8)
        self.next = 0

    def make_table(self, rule):
        """Returns a table for the given CA rule.  The table is a 
        dictionary that maps 3-tuples to binary values.
        """
        table = {}
        for i, bit in enumerate(binary(rule, 8)):
            t = binary(7-i, 3)
            table[t] = bit
        return table

    def start_single(self):
        """Starts with one cell in the middle of the top row."""
        self.array[self.n/2] = 1
        self.next += 1

    def start_random(self):
        """Start with random values in the top row."""
        self.array = numpy.random.random(self.n).round()
        self.next += 1

    def loop(self, steps=1):
        """Executes the given number of time steps."""
        [self.step() for i in xrange(steps)]

    def step(self):
        """Executes one time step by computing the next row of the array."""
        i = self.next
        self.next += 1

        a = self.array
        a_old = numpy.copy(a)

        t = self.table
        for i in xrange(1,self.n-1):
            a[i] = t[tuple(a_old[i-1:i+2])]


    def get_array(self, start=0, end=None):
        """Gets a slice of columns from the CA, with slice indices
        (start, end).  Avoid copying if possible.
        """
        if start==0 and end==None:
            return self.array
        else:
            return self.array[:, start:end]


def binary(n, digits):
    """Returns a tuple of (digits) integers representing the
    integer (n) in binary.  For example, binary(3,3) returns (0, 1, 1)"""
    t = []
    for i in range(digits):
        n, r = divmod(n, 2)
        t.append(r)

    return tuple(reversed(t))
