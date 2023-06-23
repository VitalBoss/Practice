import sys

def priority_and(s): # функция, которая на верхнем уровне выражения ищет and, если есть, то возвращает true
    close = 0
    open = 0
    c = False
    for i in range(len(s)):
        if (abs(close - open) == 0) and (s[i] == 'and'):
            c = True
        if s[i] == ')':
            close += 1
        if s[i] == '(':
            open += 1
    return c

def check(s):  #если после открывающейся скобки идем закрывающаяся, то запомним их индексы, чтобы потом удалить их
                #также если скобок или логический операций and, or в выражении нет, то возвращаем false, что означает, что запрос полностью обработан
    c = False
    mas = []
    ex = False
    for ind,elem in enumerate(s):
        if elem == '(':
            c = True
            ex = True
            i = ind
        if elem == ')':
            ex = True
            if c:
                mas.append(i)
                mas.append(ind)
                c = False
        if elem == 'and' or elem == 'or':
            ex = True
    return mas, ex


def del_skobki(s): #удаление скобок, находящихся на одном нижнем уровне
    mas, ex = check(s)
    #print(mas)
    new_mas = []
    for i in range(len(s)):
        if not(i in mas):
            new_mas.append(s[i])

    #new_mas = ''.join(new_mas)
    return new_mas, ex       

def correct_str(mas): #если после запятой нет пробела, то добавляем его
    ans = ''
    c = False
    for elem in mas:
        for s in elem:
            if c:
                ans = ans + " "
                c = False
            if s == ',':
                c = True 
            ans = ans + s
        ans = ans + " "
    return ans

def skobki(s): # слева и справа от скобки добавляем пробел, чтобы удобней было обрабатывать массив
    ans = ''
    for symb in s:
        if symb == '(' or symb == ')':
            ans = ans + ' ' + symb + ' '
        else:
            ans = ans + symb
    return ans
                

query_necessary = ['selekt', 'from']
query_not_necessary = ['where', 'order by']
oper = ['=', '<>',  'upper']
bool_oper = ['not', 'or', 'and']
sort = ['asc', 'desc']

s = '(aaa == rty or sss = bbb) and rrr <> k'
s = skobki(s)
s = s.split()
s, c  = del_skobki(s)
print(s)
print(c)

print("Введите запрос, после написания всех строчек дважды нажмите enter")
mas_str = []
while s != '':
    s = input()
    mas_str.append(s)

mas_str = mas_str[:len(mas_str)-1] #последней элемент - это пустая строка, уберем его

#если в первой строке нет хотя бы одного обязательного символа, то выход
if (query_necessary[0] == mas_str[0].lower().split()[0]) and (query_necessary[0] == mas_str[-2].lower().split()[-2]):
    print(mas_str[0].lower().split()[0], mas_str[-2].lower().split()[-2])
    print("Неверный ввод")
    sys.exit()

query = {
    'select' : []
}

flag = True
# разделяю слова пробелами, если слова разделены еще запятой, значит делим их запятой. Если одно слово, то все хорошо
#первое и предпоследнее слово фиксировано, между ними может быть, что угодно
for elem in mas_str[0].split():
    if elem.lower() != 'select' and elem.lower() != 'from' and flag:
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

    if elem.lower() == 'from':
        flag = False
    if not(flag):
        query['from'] = elem


#рассмотрим строчки с необязательными запросами
#Алгоритм таков: если более одной строчки в запросе то начинаем разбор строчек(2 и 3) поочередно
#если в строчке первый символ where, то пробегаемся по всей строчке в следующем порядке: сначала группируем выражение,
#разделенное знаками = или <>, или upper. Затем в порядке приоритетности обрабатываем логические выражения. Not обрабатывается,
#если следующий символ откр. скобка, а потом словарик или если сразу словарик. and и or обрабатываются, если слева и справа 
#расположены словарики, причем сначала обрабатывается and, а потом or, далее убираем лишние скобки и итерация возобнавляется

#обработка order by очень простая: начиная с 1 элемента в массиве обрабатывем пары 1 и 2, 2 и 3 и т.д., но сначала идет обработка запятой
if len(mas_str) > 1:
    mas_str = mas_str[1:]
    for s in mas_str:
        s = skobki(s)
        st = s.split()
        if st[0] == 'where':
            query['where'] = {}
            st.pop(0)
            s1 = []
            #print("st = ", st)
            cnt = 0
            for idx in range(len(st)):
                if cnt > 0:
                    cnt -= 1
                elif st[idx] == 'upper':
                    s1.append({st[idx+4] : [{'upper' : st[idx+2]}, st[idx+5]]})
                    cnt = 5
                elif  st[idx] != 'not' and st[idx] != '=' and st[idx] != '<>' and st[idx] != 'and' and st[idx] != 'or' and st[idx] != ')' and st[idx] != '(' and ((idx+2) <= len(st)):
                    if (idx+2) <= (len(st)-1):
                        s1.append({st[idx+1]: [st[idx], st[idx+2]]})
                        cnt = 2
                    else:
                        s1.append(st[idx])
                else:
                    s1.append(st[idx])
            #print("s1 = ", s1)
            bool_skob = []
            c = True
            cnt = 0
            p = 'and'
            while c:
                if priority_and(s1):
                    p = 'and'
                else:
                    p = 'or'
                #print("s1=",s1)
                #print("bool_skob=",bool_skob)
                for idx in range(len(s1)):    
                #print(type(s1[idx]),(idx+2) <= len(s1) )
                        if cnt > 0:
                            cnt -= 1
                        elif s1[idx] == 'not' and s1[idx+1] == '(' and type(s1[idx+2])==dict and s1[idx+3] == ')' and (idx+3) <= (len(s1)-1):
                            bool_skob.append({'not' : s1[idx+2]})
                            cnt = 3
                        elif s1[idx] == 'not' and type(s1[idx+1]) == dict:
                            bool_skob.append({'not' : s1[idx+1]})
                            cnt = 1
                        elif type(s1[idx]) == dict  and ((idx+2) <= len(s1)-1):
                            if type(s1[idx+1])==str and type(s1[idx+2]) == dict:
                                if s1[idx+1] == p:
                                    bool_skob.append({s1[idx+1] : [s1[idx], s1[idx+2]]})
                                    cnt = 2
                                else:
                                    bool_skob.append(s1[idx])
                                    bool_skob.append(s1[idx+1])
                                    cnt = 1
                            else:
                                bool_skob.append(s1[idx])
                        elif s1[idx] == 'upper':
                            bool_skob.append({'upper' : s1[idx+2]})
                            cnt = 3
                        else:
                            bool_skob.append(s1[idx])
                s1 = bool_skob
                bool_skob = []
                #print("bool_skob = ",s1)
                s1, c = del_skobki(s1)
                #print("s1=",s1)
                #print('c = ', c)
                bool_skob = []
            query['where'] = s1[0]
                
                    
        s = st
        if s[0] == 'order' and s[1] == 'by': #
            query['order by'] = []
            s = correct_str(s)
            s = s.split()
            s = s[2:]
            length = len(s)
            for i in range(0, length, 2):
                query['order by'].append({s[i] : s[i+1]})
                

print("query = ", query)


#select aaa, bbb,ccc from GPT
#where aaa = r and bbb = c
# order by aaa desc
     
#where ((asd = ddd or asd <> ddd) or not(asd = mmm and qqq <> aaa)) and not(www = xyz or www <> piz)
#where not(asd = ddd or upper(asd) <> ddd)
#where asd = qwe or ccc = ppp and rrr <> ooo and not(xxx = yyy)

#order by aaa asc,bbb desc
#order by aaa asc, bbb desc, ccc desc