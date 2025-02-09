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


# Supposing that all the classes developed for the project
# are contained in the file 'impl.py', then:

# 1) Importing all the classes for handling the relational database
from impl import CategoryUploadHandler, CategoryQueryHandler

# 2) Importing all the classes for handling graph database
from impl import JournalUploadHandler, JournalQueryHandler

# 3) Importing the class for dealing with mashup queries
from impl import FullQueryEngine

# Once all the classes are imported, first create the relational
# database using the related source data
rel_path = "relational.db"
cat = CategoryUploadHandler()
cat.setDbPathOrUrl(rel_path)
cat.pushDataToDb("data/scimago.json")
# Please remember that one could, in principle, push one or more files
# calling the method one or more times (even calling the method twice
# specifying the same file!)

# Then, create the graph database (remember first to run the
# Blazegraph instance) using the related source data
grp_endpoint = "http://127.0.0.1:9999/blazegraph/sparql"
jou = JournalUploadHandler()
jou.setDbPathOrUrl(grp_endpoint)
jou.pushDataToDb("data/doaj.csv")
# Please remember that one could, in principle, push one or more files
# calling the method one or more times (even calling the method twice
# specifying the same file!)

# In the next passage, create the query handlers for both
# the databases, using the related classes
cat_qh = CategoryQueryHandler()
cat_qh.setDbPathOrUrl(rel_path)

jou_qh = JournalQueryHandler()
jou_qh.setDbPathOrUrl(grp_endpoint)

# Finally, create a advanced mashup object for asking
# about data
que = FullQueryEngine()
que.addCategoryHandler(cat_qh)
que.addJournalHandler(jou_qh)

result_q1 = que.getAllJournals()
result_q2 = que.getJournalsInCategoriesWithQuartile({"Artificial Intelligence", "Oncology"}, {"Q1"})
result_q3 = que.getEntityById("Artificial Intelligence")
result_q4 = que.getEntityById("2532-8816")
# etc...