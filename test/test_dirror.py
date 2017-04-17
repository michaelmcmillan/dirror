from unittest import TestCase, main, skip
from subprocess import check_output
from dirror import Dirror, Sweeper

class TestFindDirectories(TestCase):

    def test_it_returns_single_subdirectory(self):
        sweeper = Sweeper()
        path = 'test/fixtures/one-subdirectory'
        directories = sweeper.find_directories(path)
        self.assertEqual(directories, ['subdirectory'])

    def test_it_returns_empty_list_if_no_subdirectories(self):
        sweeper = Sweeper()
        path = 'test/fixtures/no-subdirectory'
        directories = sweeper.find_directories(path)
        self.assertEqual(directories, [])

    def test_it_returns_empty_list_if_only_contains_files(self):
        sweeper = Sweeper()
        path = 'test/fixtures/one-file'
        directories = sweeper.find_directories(path)
        self.assertEqual(directories, [])

class TestRecursiveFindDirectories(TestCase):

    def test_it_returns_a_dictionary_of_directory_contents(self):
        sweeper = Sweeper()
        path = 'test/fixtures/one-subdirectory-within-another-subdirectory'
        directories = sweeper.recursively_find_directories(path)
        self.assertEqual(directories, {'subdirectory': {'another-subdirectory': {}}})

    def test_it_returns_an_empty_dictionary_if_no_subdirectories(self):
        sweeper = Sweeper()
        path = 'test/fixtures/no-subdirectory'
        directories = sweeper.recursively_find_directories(path)
        self.assertEqual(directories, {})

    def test_it_returns_a_dictionary_of_multiple_directories(self):
        sweeper = Sweeper()
        path = 'test/fixtures/two-subdirectories-within-a-subdirectory'
        directories = sweeper.recursively_find_directories(path)
        self.assertEqual(directories, {'first-directory': {}, 'second-directory': {}})

class TestCompare(TestCase):

    def test_it_returns_empty_list_if_both_trees_are_empty(self):
        dirror = Dirror()
        first_tree = {}
        second_tree = {}
        shards = dirror.find_shards(first_tree, second_tree, [])
        self.assertEqual(shards, [])

    def test_it_returns_shard_if_one_tree_has_root_the_other_does_not(self):
        dirror = Dirror()
        first_tree = {'root': {}}
        second_tree = {}
        shards = dirror.find_shards(first_tree, second_tree, [])
        self.assertEqual(shards, ['root'])

    def test_it_returns_empty_list_if_prefixed_directory_is_in_the_other_tree(self):
        dirror = Dirror(prefix='test_')
        first_tree = {'root': {}}
        second_tree = {'test_root': {}}
        shards = dirror.find_shards(first_tree, second_tree, [])
        self.assertEqual(shards, [])
    
    def test_it_returns_empty_list_if_appendixed_directory_is_in_the_other_tree(self):
        dirror = Dirror(appendix='_test')
        first_tree = {'root': {}}
        second_tree = {'root_test': {}}
        shards = dirror.find_shards(first_tree, second_tree, [])
        self.assertEqual(shards, [])

    def test_it_returns_shard_if_leafs_dont_match(self):
        dirror = Dirror()
        first_tree = {'root': {'leaf': {}}}
        second_tree = {'root': {'liif': {}}}
        shards = dirror.find_shards(first_tree, second_tree, [])
        self.assertEqual(shards, ['leaf'])

    def test_it_ignores_excluded_directories(self):
        dirror = Dirror(exclusions=['__pycache__'])
        first_tree = {'__pycache__': {}}
        second_tree = {}
        shards = dirror.find_shards(first_tree, second_tree, [])
        self.assertEqual(shards, [])

class TestSystem(TestCase):

    def test_it_exits_silently_if_no_shards_found(self):
        flags = ('test/fixtures/system/src', 'test/fixtures/system/test', 'test_', '__pycache__')
        command = 'python3 dirror.py %s' % ' '.join(flags)
        output = check_output(command, shell=True)
        self.assertEqual(output, b'')

if __name__ == '__main__':
    main()
