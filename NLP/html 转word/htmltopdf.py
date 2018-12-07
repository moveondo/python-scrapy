#!/usr/bin/env python
# -*- coding:utf-8 -*-


import pdfkit

# 有下面3中途径生产pdf


pdfkit.from_url('http://baidu.com', 'out.pdf')

# pdfkit.from_file('test.html', 'out1.pdf')
#
# pdfkit.from_string('Hello!', 'out.pdf')
