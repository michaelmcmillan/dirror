from unittest import TestCase, main
from dirror import MirrorCheck

class TestFindDirectories(TestCase):

    def test_it_returns_single_subdirectory(self):
        mirror = MirrorCheck()
        path = 'test/fixtures/one-subdirectory'
        directories = mirror.find_directories(path)
        self.assertEqual(directories, ['subdirectory'])

    def test_it_returns_empty_list_if_no_subdirectories(self):
        mirror = MirrorCheck()
        path = 'test/fixtures/no-subdirectory'
        directories = mirror.find_directories(path)
        self.assertEqual(directories, [])

    def test_it_returns_empty_list_if_only_contains_files(self):
        mirror = MirrorCheck()
        path = 'test/fixtures/one-file'
        directories = mirror.find_directories(path)
        self.assertEqual(directories, [])

class TestRecursiveFindDirectories(TestCase):

    def test_it_returns_a_dictionary_of_directory_contents(self):
        mirror = MirrorCheck()
        path = 'test/fixtures/one-subdirectory-within-another-subdirectory'
        directories = mirror.recursively_find_directories(path)
        self.assertEqual(directories, {'subdirectory': {'another-subdirectory': {}}})

    def test_it_returns_an_empty_dictionary_if_no_subdirectories(self):
        mirror = MirrorCheck()
        path = 'test/fixtures/no-subdirectory'
        directories = mirror.recursively_find_directories(path)
        self.assertEqual(directories, {})

    def test_it_returns_a_dictionary_of_multiple_directories(self):
        mirror = MirrorCheck()
        path = 'test/fixtures/two-subdirectories-within-a-subdirectory'
        directories = mirror.recursively_find_directories(path)
        self.assertEqual(directories, {'first-directory': {}, 'second-directory': {}})

class TestCompare(TestCase):

    def test_it_returns_true_if_both_trees_are_empty(self):
        mirror = MirrorCheck()
        first_tree = {}
        second_tree = {}
        reflection = mirror.is_reflection(first_tree, second_tree)
        self.assertTrue(reflection)

    def test_it_returns_false_if_one_tree_has_root_the_other_does_not(self):
        mirror = MirrorCheck()
        first_tree = {'root': {}}
        second_tree = {}
        reflection = mirror.is_reflection(first_tree, second_tree)
        self.assertFalse(reflection)

    def test_it_returns_true_if_prefixed_directory_is_in_the_other_tree(self):
        mirror = MirrorCheck()
        first_tree = {'root': {}}
        second_tree = {'test_root': {}}
        reflection = mirror.is_reflection(first_tree, second_tree, prefix='test_')
        self.assertTrue(reflection)

    def test_it_returns_false_if_leafs_dont_match(self):
        mirror = MirrorCheck()
        first_tree = {'root': {'leaf': {}}}
        second_tree = {'test_root': {'test_liif': {}}}
        reflection = mirror.is_reflection(first_tree, second_tree, prefix='test_')
        self.assertFalse(reflection)

    def test_it_ignores_excluded_directories(self):
        mirror = MirrorCheck()
        first_tree = {'__pycache__': {}}
        second_tree = {}
        reflection = mirror.is_reflection(first_tree, second_tree, prefix='test_', exclusions=['__pycache__'])
        self.assertTrue(reflection)

class TestSystem(TestCase):

    def test_it_returns_true_if_test_has_dir_for_every_src(self):
        mirror = MirrorCheck()
        src_path, test_path = 'test/fixtures/system/src', 'test/fixtures/system/test'
        src_mirrors_test = mirror.determine(src_path, test_path, 'test_', [])
        self.assertTrue(src_mirrors_test)

if __name__ == '__main__':
    main()
