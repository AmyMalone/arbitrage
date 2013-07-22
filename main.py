#!/usr/bin/env python

from collections import namedtuple
import sys
import decimal
import re
import math
import copy
from itertools import chain

CURRENCY_NAMES = ['USD', 'AUD', 'EUR']

ExchangeRate = namedtuple('ExchangeRate', 'origin dest rate')

def main():
    # Use 9 decimal places of precision
    decimal.getcontext().prec = 9
    graph = ExchangeGraph(read_exchange_rates('testdata'))

    if len(sys.argv) > 2:
        print('This command only takes 1 or 0 arguments')
        exit(1)
    elif len(sys.argv) == 2:
        cmd = sys.argv[1]
        if cmd == 'list-lonely':
            graph.alone_currency()
        else:
            print('arbitrage graph program')
            print('accepts the following commands:')
            print()
            print('list-lonely: lists the currencies that only have 1 edge')

def read_exchange_rates(filename):
    with open(filename, 'r') as data:
        input_pattern = re.compile('^(.+)\t(.+)\t(.+)$')
        for line in data:
            match = input_pattern.search(line)
            if match is None:
                print('Encountered unexpected line in input file')
                exit(1)
            origin, dest, rate = match.groups()
            rate = math.log(1 / decimal.Decimal(rate))
            yield ExchangeRate(origin, dest, rate)

class ExchangeGraph(object):
    def __init__(self, exchange_rates=[]):
        self.currencies = {}
        self.update_rates(exchange_rates)

    def get_currency(self, name):
        return self.currencies[name]

    def get_routes(self, origin, dest):
        pass

    def update_rates(self, exchange_rates):
        for rate in exchange_rates:
            # Make a currency if it does not already exist
            if not rate.origin in self.currencies:
                self.currencies[rate.origin] = Currency(rate.origin)
            if not rate.dest in self.currencies:
                self.currencies[rate.dest] = Currency(rate.dest)

            # TODO use integer based math to fix floating point issues
            self.currencies[rate.origin].set_rate_to(rate.dest, rate.rate)
            self.currencies[rate.dest].set_rate_to(rate.origin, 1 / rate.rate)

    #added
    def alone_currency(self):
        currency_name_occurences = {}
        currency_edges = map(lambda x: x.edges.keys(), self.currencies.values())

        for currency_name in chain.from_iterable(currency_edges):
            if not currency_name in currency_name_occurences:
                currency_name_occurences[currency_name] = 1
            else:
                currency_name_occurences[currency_name] += 1

        print('Alone Currencies:')
        for name in currency_name_occurences.keys():
            if currency_name_occurences[name] == 1:
                print(name)

class Currency(object):

    def __init__(self, name):
        self.__edges = {}
        self.__name = name

    @property
    def name(self):
        return self.__name

    def set_rate_to(self, currency, rate):
        self.__edges[currency] = rate

    def get_rate_to(self, currency):
        return self.__edges[currency]

    @property
    def edges(self):
        return copy.copy(self.__edges)

if __name__ == '__main__':
    main()
