
import os, requests, time, urllib.request, json
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import asyncio


PATH = "Companies/"
ENDPOINTS = ["https://finance.yahoo.com/quote/",
             "https://www.investopedia.com/articles/investing/053116/10-largest-holdings-sp-500-aaplamznfb.asp"]
HEADERS = ['Date', 'Open', 'High', 'Low', 'Close', 'Adj_Close', 'Vol']
NAMES=['MSFT', 'XOM', 'JNJ', 'GE', 'FB', 'AMZN', 'BRK-B', 'T', 'WFC']
URLS=['https://finance.yahoo.com/quote/MSFT/history?p=MSFT', 'https://finance.yahoo.com/quote/XOM/history?p=XOM', 'https://finance.yahoo.com/quote/JNJ/history?p=JNJ', 'https://finance.yahoo.com/quote/GE/history?p=GE', 'https://finance.yahoo.com/quote/FB/history?p=FB', 'https://finance.yahoo.com/quote/AMZN/history?p=AMZN', 'https://finance.yahoo.com/quote/BRK-B/history?p=BRK-B', 'https://finance.yahoo.com/quote/T/history?p=T', 'https://finance.yahoo.com/quote/WFC/history?p=WFC']
