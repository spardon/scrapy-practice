#!/usr/bin/env python
# -*- coding:utf-8 -*-
import logging

try:
    from local_config import *  # NOQA
except Exception, e:
    logging.info(e)
