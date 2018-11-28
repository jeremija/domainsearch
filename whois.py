#!/usr/bin/env python3
import argparse
import itertools
import socket
import sys

HOST='whois.crsnic.net'
PORT=43


class WhoIs:
    def __init__(self, server, port):
        self.server = server
        self.port = port

    def lookup(self, domain):
        """Looks up the domain. Returns true if domain is registered,
        false otherwise"""
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((self.server, self.port))
        sock.send(("%s\r\n" % domain).encode("utf-8"))

        value = self._recv(sock)
        if 'No match for' in value:
            return False
        return True

    def _recv(self, sock):
        buff = b""
        while True:
            data = sock.recv(1024)
            if len(data) == 0:
                break
            buff += data
        return buff.decode("utf-8")


alphabet = tuple('abcdefghijklmnopqrstuvwxyz')
numbers = tuple('0123456789')
alphanumeric = alphabet + numbers
vowels = tuple('aeiou')
consonants = tuple(c for c in alphabet if c not in vowels)

class Wildcard:
    def __init__(self, wildcard):
        self.wildcard = wildcard

    @property
    def values(self):
        wildcards = []
        letters = []

        for c in self.wildcard:
            if c == 'A':
                wildcards.append(alphabet)
                letters.append('_')
            elif c == 'C':
                wildcards.append(consonants)
                letters.append('_')
            elif c == 'V':
                wildcards.append(vowels)
                letters.append('_')
            elif c == '*':
                wildcards.append(alphanumeric)
                letters.append('_')
            elif c == '#':
                wildcards.append(numbers)
                letters.append('_')
            else:
                letters.append(c)

        if len(wildcards) == 0:
            yield self.wildcard
            raise StopIteration()

        product = itertools.product(*wildcards)

        for p in product:
            word = ''
            i = -1
            for l in letters:
                if l == '_':
                    i += 1
                    word += p[i]
                else:
                    word += l
            yield word


def parse_args(argv):
    parser = argparse.ArgumentParser()

    parser.add_argument('--host', default=HOST,
                        help='of the WhoIs lookup server')
    parser.add_argument('--port', default=PORT, type=int,
                        help='Port of the WhoIs lookup server')
    parser.add_argument('-n', '--dry-run', default=False, action='store_true',
                        help='Only print the permutations')
    parser.add_argument('-o', '--only', default=False, action='store_true',
                        help='Print only available')
    parser.add_argument('--progress', default=False, action='store_true',
                        help='Show progress')
    parser.add_argument('domain',
                        help='Domain to look up')

    return parser.parse_args(argv)


def main(argv):
    args = parse_args(argv)
    host = args.host
    port = args.port

    whois = WhoIs(host, port)
    wildcard = Wildcard(args.domain)

    for i, domain in enumerate(wildcard.values):
        count = i + 1
        if count % 100 == 0:
            print('Count', count, file=sys.stderr)

        if args.dry_run:
            print(domain)
            continue

        registered  = whois.lookup(domain)
        if not registered:
            print('✓', domain)
        elif not args.only:
            print('- ', domain)


if __name__ == '__main__':
    main(sys.argv[1:])
