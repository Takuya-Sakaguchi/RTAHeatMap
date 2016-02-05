from DataGeneration import DataGenerator
from DataGeneration import DatabaseHandler
from DataGeneration import MapLocation
from DataGeneration import MapboxAPIWrapper
import unittest
from mock import Mock, patch


class test_DataGenerator(unittest.TestCase):

    # __init__ tests
    def test_constructor_sets_stops_array_to_empty_list(self):
        generator = DataGenerator()
        self.assertEqual([], generator.stops)

    def test_constructor_sets_handler_to_simple_handler(self):
        generator = DataGenerator()
        self.assertIsInstance(generator.handler, DatabaseHandler)

    def test_constructor_sets_wrapper_instance_variable(self):
        generator = DataGenerator()
        self.assertIsInstance(generator.wrapper, MapboxAPIWrapper)

    # initialize tests
    @patch('DataGeneration.DataGenerator.get_database_handler')
    def test_DataGenerator_exists(self,
                                  mock_get_db):
        generator = DataGenerator()
        self.assertIsInstance(generator, DataGenerator)

    @patch('DataGeneration.DatabaseHandler.get_all_stops')
    @patch('DataGeneration.DataGenerator.get_database_handler')
    def test_start_initializes_database(self,
                                        mock_get_db,
                                        mock_get_all_stops):
        generator = DataGenerator()
        mock_get_db.return_value = DatabaseHandler(full=False)
        generator.initialize()
        mock_get_db.assert_called_once_with()

    @patch('DataGeneration.DatabaseHandler.get_all_stops')
    @patch('DataGeneration.DataGenerator.get_database_handler')
    def test_start_pulls_all_stops(self,
                                   mock_get_db,
                                   mock_get_all_stops):
        generator = DataGenerator()
        mock_get_db.return_value = DatabaseHandler(full=False)
        generator.initialize()
        mock_get_all_stops.assert_called_once_with()

    # get_database_handler tests
    def test_get_database_handler_returns_DatabaseHandler(self):
        generator = DataGenerator()
        self.assertIsInstance(generator.get_database_handler(), DatabaseHandler)

    # get_api_wrapper tests
    @patch('DataGeneration.MapboxAPIWrapper.load_api_key_from_file')
    def test_get_api_wrapper_returns_MapboxAPIWrapper(self,
                                                      mock_get_key):
        generator = DataGenerator()
        self.assertIsInstance(generator.get_api_wrapper(), MapboxAPIWrapper)

    @patch('DataGeneration.MapboxAPIWrapper.load_api_key_from_file')
    def test_get_api_wrapper_pulls_api_key(self,
                                           mock_get_key):
        generator = DataGenerator()
        generator.get_api_wrapper()
        mock_get_key.assert_called_once_with('api_key.txt')

    # begin tests
    @patch('DataGeneration.DatabaseHandler.get_address_without_route')
    def test_begin_calls_handler_get_next_address(self,
                                                  mock_get_address):
        generator = DataGenerator()
        generator.begin()
        mock_get_address.assert_called_once_with()
