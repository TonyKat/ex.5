from elasticsearch import Elasticsearch
from tqdm import tqdm

good_categories = ['Музыка\n', 'Технологии\n', 'Кино\n', 'Авто\n',
                   'Финансы\n', 'Спорт\n', 'Власть\n', 'Общество\n', 'Происшествия\n']


def delete_category(fake_news, fake_category):
    i = 0
    while i < len(fake_category):
        if fake_category[i] not in good_categories:
            fake_category.pop(i)
            fake_news.pop(i)
            continue
        i += 1
    return fake_news, fake_category


def get_news_and_category_from_file():
    with open('file_news_correct.txt', 'r', encoding='utf8') as output_file:
        length_file = len(output_file.readlines())
        output_file.seek(0)
        mas_news = []
        for i in range(0, length_file):
            line = output_file.readline()
            mas_news.append(line)
        output_file.seek(0)
    with open('file_category_correct.txt', 'r', encoding='utf8') as output_file:
        length_file = len(output_file.readlines())
        output_file.seek(0)
        mas_category = []
        for i in range(0, length_file):
            line = output_file.readline()
            mas_category.append(line)
        output_file.seek(0)

    return mas_news, mas_category


es = Elasticsearch()

# удалить индекс (после добавления индексов закомментить)
#es.indices.delete(index='index_1')

# создать индекс (после добавления индексов закомментить)
es.indices.create(index='index_1')

# добавить документ в индекс
news, category = get_news_and_category_from_file()
news, category = delete_category(news, category)

# после добавления индексов закомментить
for i in tqdm(range(len(news))):
    es.index(index='index_1', doc_type='News-Categories', body={'title': news[i], 'category': category[i]})