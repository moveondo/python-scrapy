#!/usr/bin/env python
# -*- coding:utf-8 -*-


import pdfkit

# 有下面3中途径生产pdf
# config = pdfkit.configuration(wkhtmltopdf='/usr/local/bin/wkhtmltopdf')


pdfkit.from_url('http://google.com', 'out.pdf')

# pdfkit.from_file('test.html', 'out.pdf')
#
# pdfkit.from_string('Hello!', 'out.pdf')
