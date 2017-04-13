import os, sys, logging
from argparse import ArgumentParser

class MirrorCheck:

    def __init__(self, should_log=False):
        self.log = logging.getLogger(__name__)
        self.log.disabled = not should_log

    def find_directories(self, path):
        files_and_directories = os.listdir(path)
        return [potential_dir for potential_dir in files_and_directories \
            if os.path.isdir(os.path.join(path, potential_dir))]

    def recursively_find_directories(self, path):
        tree = {}
        for directory in self.find_directories(path):
            absolute_path = os.path.join(path, directory)
            tree[directory] = self.recursively_find_directories(absolute_path)
        return tree 

    def is_reflection(self, tree, other_tree, prefix=None):
        def identical_trees(tree, other_tree, prefix):
            for directory in tree:
                prefixed_directory = (prefix or '') + directory
                identical_trees(tree[directory], other_tree[prefixed_directory], prefix)

        try:
            identical_trees(tree, other_tree, prefix)
            return True
        except KeyError as error:
            self.log.error('%s broke the mirror.' % error)
            return False

    def determine(self, directory_path, other_directory_path, prefix):
        tree = self.recursively_find_directories(directory_path)
        other_tree = self.recursively_find_directories(other_directory_path)
        return self.is_reflection(tree, other_tree, prefix)

def parse_args(args):
    parser = ArgumentParser(prog='dirror.py',
                            description='Ensure that two directories mirror each other.')
    parser.add_argument('source_directory', type=str, help='path to source directory')
    parser.add_argument('test_directory', type=str, help='path to test directory')
    parser.add_argument('prefix', type=str, help='prefix for subddirectories in the test directory')
    return parser.parse_args(args)

if __name__ == '__main__':
    args = parse_args(sys.argv[1:])
    mirror_check = MirrorCheck(should_log=True)
    mirrored = mirror_check.determine(args.source_directory, args.test_directory, args.prefix)
    signal = int(mirrored)
    sys.exit(signal)
