import sys
import time

query_necessary = ['selekt', 'from']
query_not_necessary = ['where', 'group by', 'order by', 'having', 'join']
command = ['=', '<>', 'in']
agg = ['count', 'upper', 'max', 'min', 'sum', 'avg']

s = 'asd'

mas_str = []
while s != '':
    s = input()
    s = s.lower()
    mas_str.append(s)

#если в первой строке нет хотя бы одного обязательного символа, то выход
if not(query_necessary[0] in mas_str[0]) and not(query_necessary[1] in mas_str[0]):
    print("Неверный ввод")
    sys.exit()

query = {
    'select' : []
}


flag = True
# разделяю слова пробелами, если слова заделены еще запятой, значит делим их запятой. Если одно слово, то все хорошо
for elem in mas_str[0].split():
    if elem != 'select' and elem != 'from' and flag:
        el = elem
        c = True
        if ',' in el:
            if el[-1] == ',':
                el = el[:len(el)-2]
            else:
                el = el.split(sep = ',')
                c = False
                for i in el:
                    query['select'].append(i)
        if c:
            query['select'].append(elem)

    if elem == 'from':
        flag = False
    if not(flag):
        query['from'] = elem

#рассмотрим строчки с необязательными запросами (не доделал пока)
if len(mas_str > 1):
    mas_str = mas_str[1:]
    for s in mas_str:
        for elem in s.split():
            if elem == 'where':
                query['where'] = {}
                
            if elem == 'group by':
                pass
            if elem == 'order by':
                pass
            if elem == 'having':
                pass
            if elem == 'join':
                pass



print(query)


#select asd from gpt