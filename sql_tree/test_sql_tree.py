import unittest
import sql_request 

class TestSQLTree(unittest.TestCase):

    def test_result(self):
        self.assertEqual(sql_request.main(["select aaa from GPT", \
                                           "where b and (c = p or d)"]),  \
                                                                        {'select': 'aaa', 'from': 'GPT', \
                                                                         'where': {'and': ['b', {'or': [{'=': ['c', 'p']}, 'd']}]}})
        
        self.assertEqual(sql_request.main(["select aaa FROM GPT", \
                                            "where b <> (c = p OR d)"]),    {'select': 'aaa', 'from': 'GPT', \
                                                                             'where': {'<>': ['b', {'or': [{'=': ['c', 'p']}, 'd']}]}})

        self.assertEqual(sql_request.main(["select aaa from GPT", \
                                        "where a = b or c",   \
                                        "order BY aaa desc"]), \
                                                                    {'select': 'aaa', 'from': 'GPT', \
                                                                     'where': {'or': [{'=': ['a', 'b']}, 'c']}, 'order by': [{'aaa': 'desc'}]})
        
        self.assertEqual(sql_request.main(["select aaa,bbb,ccc from GPT", \
                                        "WHERE aaa = r and bbb = c",   \
                                        "order by aaa desc"]),         \
                                                                           {'select' : ['aaa', 'bbb', 'ccc'], 'from' : 'GPT', \
                                                                            'where' : {'and' : [{'=' : ['aaa', 'r']}, {'=' : ['bbb', 'c']}]},\
                                                                             'order by' : [{'aaa' : 'desc'}]})
        

        self.assertEqual(sql_request.main(["select aaa , bbb from GPT", \
                                        "where NOT(asd = ddd or upper(asd) <> ddd)", \
                                        "order by aaa asc, bbb desc"]), \
                                                                                            {'select': ['aaa', 'bbb'], 'from': 'GPT',\
                                                                                             'where': {'not': {'or': [{'=': ['asd', 'ddd']}, {'<>': [{'upper': 'asd'}, 'ddd']}]}},\
                                                                                            'order by': [{'aaa': 'asc'}, {'bbb': 'desc'}]})
        

        self.assertEqual(sql_request.main(["select aaa , bbb from GPT", \
                                        "where not(asd = upper(ddd) or asd <> ddd)", \
                                        "order by aaa asc, bbb desc"]), \
                                                                                       {'select': ['aaa', 'bbb'], 'from': 'GPT', \
                                                                                         'where': {'not': {'or': [{'=': ['asd', {'upper': 'ddd'}]}, {'<>': ['asd', 'ddd']}]}},\
                                                                                        'order by': [{'aaa': 'asc'}, {'bbb': 'desc'}]})

        self.assertEqual(sql_request.main(["select aaa , bbb,ccc from GPT", \
                                        "where asd = qwe or ccc = ppp and rrr <> ooo and not(xxx = yyy)", \
                                        "order by aaa asc, bbb desc,ccc desc"]),                           {'select': ['aaa', 'bbb', 'ccc'], 'from': 'GPT', \
                                                                                                            'where': {'or': [{'=': ['asd', 'qwe']}, {'and': [{'and': [{'=': ['ccc', 'ppp']}, {'<>': ['rrr', 'ooo']}]}, {'not': {'=': ['xxx', 'yyy']}}]}]}, \
                                                                                                            'order by': [{'aaa': 'asc'}, {'bbb': 'desc'}, {'ccc': 'desc'}]})

        self.assertEqual(sql_request.main(["select aaa , bbb,ccc from GPT", \
                                        "where not(asd=ddd or upper(asd) <>ddd)"]),   \
                                                                                        {'select': ['aaa', 'bbb', 'ccc'], 'from': 'GPT', \
                                                                                         'where': {'not': {'or': [{'=': ['asd', 'ddd']}, {'<>': [{'upper': 'asd'}, 'ddd']}]}}})


        self.assertEqual(sql_request.main(["select aaa , bbb from GPT", \
                                        "where ((ASD = upper(asd) or asd <> ddd) or not(asd = mmm and qqq <> aaa)) and not(www = xyz or www <> piz)"]),\
                                                                                                                                           {'select': ['aaa', 'bbb'], 'from': 'GPT', \
                                                                                                                                           'where': {'and': [{'or': [{'or': [{'=': ['ASD', {'upper': 'asd'}]}, {'<>': ['asd', 'ddd']}]}, {'not': {'and': [{'=': ['asd', 'mmm']}, {'<>': ['qqq', 'aaa']}]}}]}, {'not': {'or': [{'=': ['www', 'xyz']}, {'<>': ['www', 'piz']}]}}]}} )
        
        self.assertEqual(sql_request.main(["selekt aaa from GPT", \
                                           "where b and (c = p or d)"]), "1 строка введена неверно")
        
        self.assertEqual(sql_request.main(["select aaa from GPT", \
                                           "where b and (c = p or d))"]), "Неверный ввод 2 строки")
        
        self.assertEqual(sql_request.main(["select aaa from GPT", \
                                           "where b and (c = p or d) or"]), "2 строка введена неверно")
        
        self.assertEqual(sql_request.main(["select aaa from GPT", \
                                           "where b and (c = p upper(or) d)"]), "2 строка введена неверно")
        
        self.assertEqual(sql_request.main(["select aaa from GPT", \
                                        "where a = b or c",   \
                                        "order by aaa decs"]),  "3 строка введена неверно")     

# также протестируем вспомогательные функции

    def test_preprocessing(self): # добавляем пробел между = и <>, также проверяем корректность скобочной последовательности
        self.assertEqual(sql_request.processing_str("a=b and c =p")[0], "a = b and c  = p")
        self.assertEqual(sql_request.processing_str("a=b and (c=p")[1], False)
        self.assertEqual(sql_request.processing_str("a=b and (c=p)")[1], True)

    def test_priority(self): # функция, которая ищет применимость and (слева и справа от and должен быть словарь), если есть, то возвращает true
         self.assertEqual(sql_request.priority_and(['a', '=', 'b', 'and', 'c', '<>', 'd']), False)
         self.assertEqual(sql_request.priority_and([{'=' : ['a','b']}, 'and', {'<>' : ['c','d']}]), True)

    def test_delete_brackets(self): #непосредственно удаление ненужных скобок, между которыми заключен словарь. Если нет больше and или or, 
                    #или скобок, то запрос полностью обработан и возвращает False
        self.assertEqual(sql_request.del_skobki(['(', {'=' : ['a','b']}, ')', 'and', {'<>' : ['c','d']}])[0], [{'=' : ['a','b']}, 'and', {'<>' : ['c','d']}])
        self.assertEqual(sql_request.del_skobki([{'<>' : ['c','d']}])[1], False)
        self.assertEqual(sql_request.del_skobki(['(', {'=' : ['a','b']}, ')', 'and', {'<>' : ['c','d']}])[1], True)

    def test_correct_string(self): # если после запятой нет пробела, то добавляем его
        self.assertEqual(sql_request.correct_str("aaa,ccc, fre"), "aaa, ccc, fre")

    def test_space_between_brackets(self): # добавляем пробелы между скобками
        self.assertEqual(sql_request.skobki("(asd)"), " ( asd ) ")
        self.assertEqual(sql_request.skobki("a = m and (p <> t)"), "a = m and  ( p <> t ) ")
        self.assertEqual(sql_request.skobki("(a = m and ((p <> z or q = c)) and d <> y"), " ( a = m and  (  ( p <> z or q = c )  )  and d <> y")






unittest.main()
