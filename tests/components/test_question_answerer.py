#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_question_answerer
----------------------------------

Tests for `question_answerer` module.
"""
# pylint: disable=locally-disabled,redefined-outer-name
from __future__ import unicode_literals

import pytest
import os

from mmworkbench.components.question_answerer import QuestionAnswerer
from mmworkbench.components._elasticsearch_helpers import create_es_client

ENTITY_TYPE = 'store_name'
KWIK_E_MART_APP_PATH = '../kwik_e_mart'
FOOD_ORDERING_APP_PATH = '../food_ordering'
STORE_DATA_FILE_PATH = os.path.dirname(__file__) + "/../kwik_e_mart/data/stores.json"
DISH_DATA_FILE_PATH = os.path.dirname(__file__) + "/../food_ordering/data/menu_items.json"


@pytest.fixture
def es_client():
    """An Elasticsearch client"""
    return create_es_client()


@pytest.fixture
def answerer(es_client):
    QuestionAnswerer.load_kb(app_name='kwik_e_mart', index_name='store_name',
                             data_file=STORE_DATA_FILE_PATH)
    es_client.indices.flush(index='_all')

    qa = QuestionAnswerer(KWIK_E_MART_APP_PATH)
    return qa


@pytest.fixture
def food_ordering_answerer(resource_loader, es_client):
    QuestionAnswerer.load_kb(app_name='food_ordering', index_name='menu_items',
                             data_file=DISH_DATA_FILE_PATH)
    es_client.indices.flush(index='_all')

    qa = QuestionAnswerer(FOOD_ORDERING_APP_PATH)
    return qa


def test_basic_search(answerer):
    """Test basic search."""

    # retrieve object using ID
    res = answerer.get(index='store_name', id='20')
    assert len(res) > 0

    # simple text query
    res = answerer.get(index='store_name', store_name='peanut')
    assert len(res) > 0

    # simple text query
    res = answerer.get(index='store_name', store_name='Springfield Heights')
    assert len(res) > 0

    # multiple text queries
    res = answerer.get(index='store_name', store_name='peanut', address='peanut st')
    assert len(res) > 0


def test_advanced_search(answerer):
    """Test advanced search."""

    s = answerer.build_search(index='store_name')
    res = s.query(store_name='peanut').execute()
    assert len(res) > 0


def test_partial_match(answerer):
    """Test partial match."""

    # test partial match
    res = answerer.get(index='store_name', store_name='Garden')
    assert len(res) > 0


def test_sort_by_distance(answerer):
    """Test sort by distance."""

    # retrieve object using ID
    res = answerer.get(index='store_name', _sort='location', _sort_type='distance',
                       _sort_location='44.24,-123.12')
    assert len(res) > 0
    assert res[0].get('id') == '19'


def test_basic_search_validation(food_ordering_answerer):
    """Test validation."""

    # index not exist
    with pytest.raises(ValueError):
        res = food_ordering_answerer.get(index='nosuchindex', nosuchfield='novalue')

    # field not exist
    with pytest.raises(ValueError):
        res = food_ordering_answerer.get(index='menu_items', nosuchfield='novalue')

    # invalid field type
    with pytest.raises(ValueError):
        res = food_ordering_answerer.get(index='menu_items', price='novalue')

    # invalid sort type
    with pytest.raises(ValueError):
        res = food_ordering_answerer.get(index='menu_items', _sort='price', _sort_type='distance')

    # invalid sort type
    with pytest.raises(ValueError):
        res = food_ordering_answerer.get(index='menu_items', _sort='location', _sort_type='asc')

    # missing origin
    with pytest.raises(ValueError):
        res = food_ordering_answerer.get(index='menu_items', _sort='location',
                                         _sort_type='distance')


def test_advanced_search_validation(answerer):
    """Tests validation in advanced search."""

    # index not exist
    with pytest.raises(ValueError):
        s = answerer.build_search(index='nosuchindex')
        s.query(fieldnotexist='test')

    # field not exist
    with pytest.raises(ValueError):
        s = answerer.build_search(index='store_name')
        s.query(fieldnotexist='test')

    # invalid field type
    with pytest.raises(ValueError):
        s = answerer.build_search(index='store_name')
        s.query(location='testlocation')

    # range filter can only be specified with number or date fields.
    with pytest.raises(ValueError):
        s = answerer.build_search(index='store_name')
        s.filter(field='phone_number', gt=10)

    # sort field to be number or date type.
    with pytest.raises(ValueError):
        s = answerer.build_search(index='store_name')
        s.sort(field='store_name', sort_type='asc')

    # missing origin
    with pytest.raises(ValueError):
        s = answerer.build_search(index='store_name')
        s.sort(field='location', sort_type='distance')


