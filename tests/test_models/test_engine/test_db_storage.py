#!/usr/bin/python3
"""
Contains the TestDBStorageDocs and TestDBStorage classes
"""

from datetime import datetime
import inspect
import models
from models.engine import db_storage
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
import json
import os
import pep8
import unittest
DBStorage = db_storage.DBStorage
classes = {"Amenity": Amenity, "City": City, "Place": Place,
           "Review": Review, "State": State, "User": User}


class TestDBStorageDocs(unittest.TestCase):
    """Tests to check the documentation and style of DBStorage class"""
    @classmethod
    def setUpClass(cls):
        """Set up for the doc tests"""
        cls.dbs_f = inspect.getmembers(DBStorage, inspect.isfunction)

    def test_pep8_conformance_db_storage(self):
        """Test that models/engine/db_storage.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['models/engine/db_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_conformance_test_db_storage(self):
        """Test tests/test_models/test_db_storage.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['tests/test_models/test_engine/\
test_db_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_db_storage_module_docstring(self):
        """Test for the db_storage.py module docstring"""
        self.assertIsNot(db_storage.__doc__, None,
                         "db_storage.py needs a docstring")
        self.assertTrue(len(db_storage.__doc__) >= 1,
                        "db_storage.py needs a docstring")

    def test_db_storage_class_docstring(self):
        """Test for the DBStorage class docstring"""
        self.assertIsNot(DBStorage.__doc__, None,
                         "DBStorage class needs a docstring")
        self.assertTrue(len(DBStorage.__doc__) >= 1,
                        "DBStorage class needs a docstring")

    def test_dbs_func_docstrings(self):
        """Test for the presence of docstrings in DBStorage methods"""
        for func in self.dbs_f:
            self.assertIsNot(func[1].__doc__, None,
                             "{:s} method needs a docstring".format(func[0]))
            self.assertTrue(len(func[1].__doc__) >= 1,
                            "{:s} method needs a docstring".format(func[0]))


class TestDBStorage(unittest.TestCase):
    """Test the FileStorage class"""
    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_all_returns_dict(self):
        """Test that all returns a dictionaty"""
        self.assertIs(type(models.storage.all()), dict)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_all_no_class(self):
        """Test that all returns all rows when no class is passed"""
        stateData = {"name": "America"}
        newState = State(**stateData)
        models.storage.new(newState)
        models.storage.save()

        session = models.storage.DBStorage__session

        allObjects = session.query(State).all()

        self.assertTrue(len(allObjects) > 0)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_new(self):
        """test that new adds an object to the database"""
        stateData = {"name": "Pretoria"}
        newState = State(**stateData)
        models.storage.new(newState)

        session = models.storage.DBStorage__session

        retrieveState = session.query(State).filter_by(id.newState.id)first()
        self.assertEqual(retrieveState.id, newState.id)
        self.assertEqual(retrieveState.name, newState.name)
        self.assertIsNotNone(retrieveState)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_save(self):
        """Test that save properly saves objects to database"""
        stateData = {"name": "Capetown"}
        newState = State(**stateData)
        models.storage.new(newState)
        models.storage.save()

        session = models.storage.DBStorage__session

        retrieveState = session.query(State).filter_by(id.newState.id)first()

        self.assertEqual(retrieveState.id, newState.id)
        self.assertEqual(retrieveState.name, newState.name)
        self.assertIsNone(retrieveState)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_get(self):
        """Test method for getting a db storage instance"""
        storage = models.storage

        stateData = {"name": "Dubai"}
        stateInstance = State(**stateData)
        storage.new(stateInstance)
        storage.save()

        retrieveState = storage.get(State, stateInstance, id)

        self.assertEqual(stateInstance, retrieveState)

        f_stateId = storage.get(State, 'fakeId')
        self.assertEqual(f_stateId, None)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_count(self):
        """Test method for getting an instance of a db storage"""
        storage = models.storage
        storage.reload()
        stateData = {"name": "Maputo"}
        stateInstance = State(**stateData)
        storage.new(stateInstance)

        cityData = {"name": "Mauritious", "stateId": stateInstance.id}

        cityInstance = city(**cityData)

        storage.new(cityInstance)

        storage.save()

        stateOcur = storage.count(State)
        self.asserEqual(stateOcur, len(storage.all(State)))

        all_stateOcur = storage.count()
        self.assertEqual(all_stateOcur, len(storage.all()))
