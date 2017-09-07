import os
import unittest

from monni.games.loading import Servers


class LoadTests(unittest.TestCase):

    def test_return_value_error_when_nonexistent_game(self):
        load = Servers()
        a = load.add_server('localhost', 27000, 'asd')
        self.assertEqual(ValueError, a)

    def test_default_server(self):

        def call_function(server):
            return None

        load = Servers()
        load.call_when_server_created = call_function
        load.file = 'test_server_file'
        load.servers()

        server_list_file = open(load.file, 'r')
        server_list = eval(server_list_file.read())
        server_list_file.close()

        self.assertEqual(server_list.pop()[0], '151.80.41.55')

    def test_write_server_in_file(self):

        def call_function(server):
            return None

        load = Servers()
        load.file = 'test_server_file'
        load.call_when_server_created = call_function
        load.servers()
        a = load.add_new_server('localhost', 27000, 'urbanterror')
        server_list_file = open(load.file, 'r')
        server_list = eval(server_list_file.read())
        server_list_file.close()
        os.remove(load.file)
        self.assertEqual(server_list.pop()[0], 'localhost')


if __name__ == '__main__':
    unittest.main()