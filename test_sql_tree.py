import unittest
import sql_request 

class TestSQLTree(unittest.TestCase):

    def test_result(self): 
        self.assertEqual(sql_request.main(["select aaa from GPT", \
                                        "where a = b and c",   \
                                        "order by aaa desc"]), \
                                                                    {'select': ['aaa'], 'from': 'GPT', \
                                                                     'where': {'and': [{'=': ['a', 'b']}, 'c']}, 'order by': [{'aaa': 'desc'}]})
        
        self.assertEqual(sql_request.main(["select aaa,bbb,ccc from GPT", \
                                        "where aaa = r and bbb = c",   \
                                        "order by aaa desc"]),         \
                                                                           {'select' : ['aaa', 'bbb', 'ccc'], 'from' : 'GPT', \
                                                                            'where' : {'and' : [{'=' : ['aaa', 'r']}, {'=' : ['bbb', 'c']}]},\
                                                                             'order by' : [{'aaa' : 'desc'}]})
        

        self.assertEqual(sql_request.main(["select aaa , bbb from GPT", \
                                        "where not(asd = ddd or upper(asd) <> ddd)", \
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

    def test_space_between_brackets(self):
        self.assertEqual(sql_request.skobki("(asd)"), " ( asd ) ")
        self.assertEqual(sql_request.skobki("a = m and (p <> t)"), "a = m and  ( p <> t ) ")
        self.assertEqual(sql_request.skobki("(a = m and ((p <> z or q = c)) and d <> y"), " ( a = m and  (  ( p <> z or q = c )  )  and d <> y")

    def test_preprocessing(self):
        #self.assertEqual(sql_request.processing_str())
        pass




unittest.main()
s = sql_request.main(["select aaa,bbb,ccc from GPT", "where aaa = r and bbb = c", "order by aaa desc"]) 
#print(s)
assert s == {'select': ['aaa', 'bbb', 'ccc'], 'from': 'GPT', 'where': {'and': [{'=': ['aaa', 'r']}, {'=': ['bbb', 'c']}]}, 'order by': [{'aaa': 'desc'}]}