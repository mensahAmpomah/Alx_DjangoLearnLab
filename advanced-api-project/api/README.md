### Filtering
- /books/?author=John%20Doe
- /books/?publication_year=2023
- /books/?title=Python%20Guide&publication_year=2022

### Searching
- /books/?search=python
- /books/?search=Mark%20Twain

### Ordering
- /books/?ordering=title
- /books/?ordering=-publication_year  # descending

Multiple features can be combined in one request:
- /books/?search=django&ordering=-publication_year