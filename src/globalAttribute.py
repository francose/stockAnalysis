
import aiohttp
import asyncio
import os, requests, time, urllib.request, json
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from typing import Callable, List, Any
import six
from abc import ABCMeta


PATH = "Companies/"
ENDPOINTS = ["https://finance.yahoo.com/quote/",
             "https://www.investopedia.com/articles/investing/053116/10-largest-holdings-sp-500-aaplamznfb.asp"]
HEADERS = ['Date', 'Open', 'High', 'Low', 'Close', 'Adj_Close', 'Vol']
