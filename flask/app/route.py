#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import os
from flask import render_template, request, redirect, url_for, session, abort
from app import app
#from flask.elasticsearch_main import es
from elasticsearch_main import es

LOG = logging.getLogger('access')


@app.route('/', methods=['GET', 'POST'])
def index():
    LOG.info('Access: %s, %s, %s' % (request.remote_addr, request.args, request.form))

    results = []
    query = ''

    for k_form, v_form in request.form.items():

        # сделать запрос
        text = []
        text.append(v_form)
        search_query = es.search(index='index_1', doc_type='News-Categories', q=text[0])

        query = text[0]

        # вывести результат
        result = search_query.get('hits').get('hits')
        source = []
        for i in range(len(result)):
            source.append(result[i].get('_source'))


        for i in range(len(source)):
            results.append('Title : %s. Category : %s' % (source[i].get('title'), source[i].get('category')))

    return render_template('index.html', results=results, query=query)


