#!/usr/bin/env python3
import os, sys, logging
from argparse import ArgumentParser

class Sweeper:
    '''Recursively generates tree from directory structure.'''

    @staticmethod
    def find_directories(path):
        files_and_directories = os.listdir(path)
        return [potential_dir for potential_dir in files_and_directories \
            if os.path.isdir(os.path.join(path, potential_dir))]

    @staticmethod
    def recursively_find_directories(path):
        tree = {}
        for directory in Sweeper.find_directories(path):
            absolute_path = os.path.join(path, directory)
            tree[directory] = Sweeper.recursively_find_directories(absolute_path)
        return tree 

class Dirror:
    '''Finds asymmetries between directory trees.'''

    def __init__(self, prefix=None, appendix=None, exclusions=None):
        self.prefix = prefix or ''
        self.appendix = appendix or ''
        self.exclusions = exclusions or []

    def find_shards(self, tree, other_tree, shards):
        for directory in (tree.keys() - self.exclusions):
            test_directory = self.prefix + directory + self.appendix

            try:
                self.find_shards(tree[directory], other_tree[test_directory], shards)
            except KeyError as error:
                shard = str(error)[1:-1]
                shards.append(shard)
        return shards

    def determine(self, directory_path, other_directory_path):
        tree = Sweeper.recursively_find_directories(directory_path)
        other_tree = Sweeper.recursively_find_directories(other_directory_path)
        return self.find_shards(tree, other_tree, [])

class CommandLine:
    '''Interfaces Dirror with the command line.'''

    NAME = 'dirror.py'
    DESCRIPTION = 'Ensure that two directories mirror each other.'
    ARGUMENTS = (
        {'flag': 'source_directory', 'type': str, 'help': 'path to source directory'},
        {'flag': 'test_directory', 'type': str, 'help': 'path to test directory'},
        {'flag': '-prefix', 'type': str, 'help': 'prefix for subddirectories in the test directory'},
        {'flag': '-exclude', 'type': lambda paths: [path for path in paths.split(',')], 'help': 'comma delimited list of exlcuded directory names'}
    )

    def __init__(self, raw_arguments):
        self.raw_arguments = raw_arguments[1:]

    def parse_arguments(self):
        parser = ArgumentParser(prog=self.NAME, description=self.DESCRIPTION)
        for argument in self.ARGUMENTS:
            parser.add_argument(argument['flag'], type=argument['type'], help=argument['help'])
        return parser.parse_args(self.raw_arguments)

if __name__ == '__main__':
    arguments = CommandLine(sys.argv).parse_arguments()
    dirror = Dirror(prefix=arguments.prefix, exclusions=arguments.exclude)

    shards = dirror.determine(arguments.source_directory, arguments.test_directory)
    for shard in shards:
        logging.getLogger('dirror').error('%s broke the mirror.' % shard)

    sys.exit(1 if any(shards) else 0)
