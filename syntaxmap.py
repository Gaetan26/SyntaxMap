import sqlite3
import re


DATABASE = "databases/keywords.db"
def sql_read(request:str, arguments=[]) -> object | list | None:
    connected = False
    try:
        conn = sqlite3.connect(DATABASE)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        connected = True
    
        request = cursor.execute(request, arguments)
        fetch = cursor.fetchall()

        if fetch is not None:
            if len(fetch) == 1:
                return fetch[0]
            return fetch
        return []

    except Exception as err:
        raise(err)
    
    finally:
        if connected:
            cursor.close()
            conn.close()


class SyntaxMap:
    def __init__(self, codes:str):
        self.codes = codes
        self.codes = (self.codes).lower()    
    
    def find(self) -> dict:
        return self.evaluate()
    
    def words_decomposer(self) -> list:        
        pattern = r"[a-z]+"
        matchs = re.findall(pattern=pattern, string=self.codes, flags=re.I)
        
        if matchs is not None:
            return matchs
        return []

    def evaluate(self) -> dict:
        languages = sql_read(request="SELECT * FROM languages") 
        keywords = sql_read(request="SELECT * FROM keywords")
        file_words = self.words_decomposer()
        sum_weight = int()
        scores = dict()

        for word in file_words:
            word = sql_read("SELECT weight FROM keywords WHERE keyword=? LIMIT 0,1",[word])
            if len(word) != 0:
                sum_weight += word['weight']

        for language in languages:
            scores[language['name']] = 0
            for word in file_words:
                for keyword in keywords:
                    if (word == keyword['keyword']) and (language['id'] == keyword['language_id']):
                        scores[language['name']] += keyword['weight']

            scores[language['name']] /= sum_weight
            scores[language['name']] = round(scores[language['name']], 2)
        
        return scores