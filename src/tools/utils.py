import datetime
from langchain.tools import tool

@tool
def get_current_datetime() -> datetime.datetime:
	"""Узнать текущую дату и время"""
	return datetime.datetime.now()