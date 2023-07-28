#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup

def get_books():
  all_books = os.listdir('./books')
  # remove non-epub files
  for book in all_books:
    if not book.endswith('.epub'):
      all_books.remove(book)
  return all_books

def get_book_content(book: str) -> str:
  content = ''
  try:
    book_ref = epub.read_epub('./books/' + book)
    for item in book_ref.get_items():
      if item.get_type() == ebooklib.ITEM_DOCUMENT:
        content += item.get_content().decode('utf-8')
  except Exception as e:
    print(e)
    return ''
  return content.lower()

def remove_punctuation(content: str) -> str:
  punc = '''!()[]{-};:'"–\,<>./?@#$%’^&*_~=+*/'''
  for ele in punc:
    content = content.replace(ele, ' ')
  return content


def parse_book(content: str) -> str:
  soup = BeautifulSoup(content, 'html.parser')
  data = remove_punctuation(soup.get_text())
  return data

def has_number(s: str) -> bool:
  # check if string has a number
  for char in s:
    if char.isdigit():
      return True
  return False

def parse_words(content: str) -> list:
  lst = content.split()

  # remove words with number
  lst = [word for word in lst if not has_number(word)]
  # remove words with length < 3
  lst = [word for word in lst if len(word) > 2]
  # remove words with non-ascii characters
  lst = [word for word in lst if word.isascii()]

  return lst

class T:
  def __init__(self, word: str, count: int):
    self.word = word
    self.count = count

if __name__ == '__main__':
  dct = dict()
  all_books = get_books()
  for book in all_books:
    source = get_book_content(book)
    source = parse_book(source)
    data = parse_words(source)
    for word in data:
      dct[word] = dct.get(word, 0) + 1
  lst = []
  for key, value in dct.items():
    lst.append(T(key, value))
  lst.sort(key=lambda x: x.count, reverse=True)
  with open('result.txt', 'w') as f:
    for t in lst:
      if t.count < 3:
        break
      # export to txt
      f.write(t.word + '\n')
