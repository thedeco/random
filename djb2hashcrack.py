#!/usr/bin/env python

import argparse
import os

def djb2(base, word):
    ''' Hash a word using the djb2 algorithm with the specified base. '''
    hash = base
    for c in word:
        hash = ((hash << 5) + hash + ord(c)) & (0xffffffff)
    return hash


def auto_int(string):
    ''' argparse type conversion for ints. Allows base 10 and base 16 '''
    try:
        return int(string, 0)
    except ValueError as e:
        raise argparse.ArgumentTypeError('Cannot parse int: {0}'.format(e))


def filepath(string):
    ''' argparse type conversion for file paths '''
    path = string
    if not os.path.isabs(path):
        path = os.path.abspath(path)
    if not os.path.isfile(path):
        raise argparse.ArgumentTypeError('Cannot find file: {0}'.format(string))
    return path


def main():
    parser = argparse.ArgumentParser(description='Brute force a djb2 hash from a wordlist')
    parser.add_argument('-w', '--wordlist',
                        type=filepath,
                        required=True,
                        help='A wordlist to crack with')
    parser.add_argument('-b', '--base',
                        type=auto_int,
                        default=0,
                        help='The base value at which the hash should start each iteration')

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-d', '--hash',
                       type=auto_int,
                       help='Specify a single hash to crack')
    group.add_argument('-l', '--hash-list',
                       type=filepath,
                       help='Specify a list of hashes to crack')

    args = parser.parse_args()

    # Extract hash items
    if args.hash:
        hashes = [args.hash]
    else:
        with open(args.hash_list) as f:
            hashes = [int(line, 0) for line in f.readlines()]

    print 'DJB2 Base: {0}'.format(args.base)
    print 'Using Wordlist: {0}'.format(args.wordlist)

    n_hashes = len(hashes)
    if n_hashes == 1: print 'Cracking 1 hash...'
    else: print 'Cracking {0} hashes...'.format(n_hashes)

    n_cracked = 0
    with open(args.wordlist) as wordlist:
        for word in wordlist:
            word = word.strip()
            attempt = djb2(args.base, word)
            for h in hashes:
                if attempt == h:
                    n_cracked += 1
                    hashes.remove(h)
                    print '[+] Hash Cracked ({0}/{1}): {2}:{3}'.format(n_cracked, n_hashes, h, word)

    print ''
    print 'Cracked {0}/{1} hashes'.format(n_cracked, n_hashes)
                    

if __name__ == '__main__':
    main()
