# -*- coding: utf-8 -*-
# Copyright (c) 2023, Silvio Peroni <essepuntato@gmail.com>
#
# Permission to use, copy, modify, and/or distribute this software for any purpose
# with or without fee is hereby granted, provided that the above copyright notice
# and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES WITH
# REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND
# FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT, INDIRECT,
# OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE,
# DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS
# ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS
# SOFTWARE.
import unittest
from os import sep
from pandas import DataFrame
from impl import JournalUploadHandler, CategoryUploadHandler
from impl import JournalQueryHandler, CategoryQueryHandler
from impl import FullQueryEngine
from impl import Journal, Category, Area

# REMEMBER: before launching the tests, please run the Blazegraph instance!

class TestProjectBasic(unittest.TestCase):

    # The paths of the files used in the test should change depending on what you want to use
    # and the folder where they are. Instead, for the graph database, the URL to talk with
    # the SPARQL endpoint must be updated depending on how you launch it - currently, it is
    # specified the URL introduced during the course, which is the one used for a standard
    # launch of the database.
    journal = "data" + sep + "doaj.csv"
    category = "data" + sep + "scimago.json"
    relational = "." + sep + "relational.db"
    graph = "http://127.0.0.1:9999/blazegraph/sparql"
    
    def test_01_JournalUploadHandler(self):
        u = JournalUploadHandler()
        self.assertTrue(u.setDbPathOrUrl(self.graph))
        self.assertEqual(u.getDbPathOrUrl(), self.graph)
        self.assertTrue(u.pushDataToDb(self.journal))

    def test_02_CategoryUploadHandler(self):
        u = CategoryUploadHandler()
        self.assertTrue(u.setDbPathOrUrl(self.relational))
        self.assertEqual(u.getDbPathOrUrl(), self.relational)
        self.assertTrue(u.pushDataToDb(self.category))
    
    def test_03_JournalQueryHandler(self):
        q = JournalQueryHandler()
        self.assertTrue(q.setDbPathOrUrl(self.graph))
        self.assertEqual(q.getDbPathOrUrl(), self.graph)

        self.assertIsInstance(q.getById("just_a_test"), DataFrame)

        self.assertIsInstance(q.getAllJournals(), DataFrame)
        self.assertIsInstance(q.getJournalsWithTitle("just_a_test"), DataFrame)
        self.assertIsInstance(q.getJournalsPublishedBy("just_a_test"), DataFrame)
        self.assertIsInstance(q.getJournalsWithLicense({"just_a_test"}), DataFrame)
        self.assertIsInstance(q.getJournalsWithAPC(), DataFrame)
        self.assertIsInstance(q.getJournalsWithDOAJSeal(), DataFrame)
    
    def test_04_ProcessDataQueryHandler(self):
        q = CategoryQueryHandler()
        self.assertTrue(q.setDbPathOrUrl(self.relational))
        self.assertEqual(q.getDbPathOrUrl(), self.relational)

        self.assertIsInstance(q.getById("just_a_test"), DataFrame)

        self.assertIsInstance(q.getAllCategories(), DataFrame)
        self.assertIsInstance(q.getAllAreas(), DataFrame)
        self.assertIsInstance(q.getCategoriesWithQuartile({"just_a_test"}), DataFrame)
        self.assertIsInstance(q.getCategoriesAssignedToAreas({"just_a_test"}), DataFrame)
        self.assertIsInstance(q.getAreasAssignedToCategories({"just_a_test"}), DataFrame)
        
    def test_05_FullQueryEngine(self):
        jq = JournalQueryHandler()
        jq.setDbPathOrUrl(self.graph)
        cq = CategoryQueryHandler()
        cq.setDbPathOrUrl(self.relational)

        fq = FullQueryEngine()
        self.assertIsInstance(fq.cleanJournalHandlers(), bool)
        self.assertIsInstance(fq.cleanCategoryHandlers(), bool)
        self.assertTrue(fq.addJournalHandler(jq))
        self.assertTrue(fq.addCategoryHandler(cq))

        self.assertEqual(fq.getEntityById("just_a_test"), None)

        r = fq.getAllJournals()
        self.assertIsInstance(r, list)
        for i in r:
            self.assertIsInstance(i, Journal)

        r = fq.getJournalsWithTitle("just_a_test")
        self.assertIsInstance(r, list)
        for i in r:
            self.assertIsInstance(i, Journal)

        r = fq.getJournalsPublishedBy("just_a_test")
        self.assertIsInstance(r, list)
        for i in r:
            self.assertIsInstance(i, Journal)

        r = fq.getJournalsWithLicense({"just_a_test"})
        self.assertIsInstance(r, list)
        for i in r:
            self.assertIsInstance(i, Journal)

        r = fq.getJournalsWithAPC()
        self.assertIsInstance(r, list)
        for i in r:
            self.assertIsInstance(i, Journal)

        r = fq.getJournalsWithDOAJSeal()
        self.assertIsInstance(r, list)
        for i in r:
            self.assertIsInstance(i, Journal)

        r = fq.getAllCategories()
        self.assertIsInstance(r, list)
        for i in r:
            self.assertIsInstance(i, Category)

        r = fq.getAllAreas()
        self.assertIsInstance(r, list)
        for i in r:
            self.assertIsInstance(i, Area)

        r = fq.getCategoriesWithQuartile({"just_a_test"})
        self.assertIsInstance(r, list)
        for i in r:
            self.assertIsInstance(i, Category)

        r = fq.getCategoriesAssignedToAreas({"just_a_test"})
        self.assertIsInstance(r, list)
        for i in r:
            self.assertIsInstance(i, Category)

        r = fq.getAreasAssignedToCategories({"just_a_test"})
        self.assertIsInstance(r, list)
        for i in r:
            self.assertIsInstance(i, Area)

        r = fq.getJournalsInCategoriesWithQuartile({"just_a_test"}, {"just_a_test"})
        self.assertIsInstance(r, list)
        for i in r:
            self.assertIsInstance(i, Journal)

        r = fq.getJournalsInAreasWithLicense({"just_a_test"}, {"just_a_test"})
        self.assertIsInstance(r, list)
        for i in r:
            self.assertIsInstance(i, Journal)

        r = fq.getDiamondJournalsInAreasAndCategoriesWithQuartile({"just_a_test"}, {"just_a_test"}, {"just_a_test"})
        self.assertIsInstance(r, list)
        for i in r:
            self.assertIsInstance(i, Journal) 
