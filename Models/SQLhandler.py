import sqlite3
import re
from Models.Logging import log
import const
import string

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

class SQLHandler(object):

    def __init__(self):
        self.conn = sqlite3.connect(const.DB)
        self.conn.row_factory = dict_factory
        self.c = self.conn.cursor()


    def __specchars(self, lists):
        """

        :param lists: lista wartosci z naszego dicta.
        :return: lists
        """
        for item_wth_quote in range(len(lists)): #dostaje index i element z listy
            if "'" in lists[item_wth_quote]: #jak wykryje ' znak to podmien replacem
                lists[item_wth_quote] = string.replace(lists[item_wth_quote], u"'", u"''")
            if '"' in lists[item_wth_quote]:#jak wykryje " znak to podmien replacem
                lists[item_wth_quote] = string.replace(lists[item_wth_quote], u'"', u'""')
        return lists

    def insert(self, table_name, data):
        """

        :param table_name: nazwa tabeli
        :type table_name: str
        :param data: dane zapisane w dict lub liscie
        :type data: dict or list
        :return: zwraca nam ostatni id wrzucony do bazy danych
        :rtype: str
        """
        log.debug("Start of INSERT class... ")
        if isinstance(data, list):
            log.debug("Start of SQL INSERT query that transform list of dict into tuple class...")
            sql = u"INSERT INTO {} ({}) VALUES ({})".format(table_name, u",".join(key for key in data[0].keys()),
                                                            u", ".join(u"?".format(v) for v in data[0].values()))
            log.debug("Start of anti injection sql method...")
            regex = r"\s*INSERT.*"
            matches = re.match(regex, sql, re.MULTILINE | re.IGNORECASE)
            if not matches:
                raise Exception('Pytanie do bazy nie jest wlasciwe: {}'.format(sql))
            listaprzebojow = []  # lista do zapisu tuple
            zmienna_val2 = None
            log.debug("start of validating and transforming list of dict to tuple...")
            for item_index in data:  # robisz fora do danych i go iterujesz
                tuple_wyc = tuple(item_index.values())
                zmienna_valid = len(tuple_wyc)
                self.validateSQL(zmienna_valid, zmienna_val2)
                zmienna_val2 = zmienna_valid
                listaprzebojow.append(tuple_wyc)  # dodajesz do listy przerobionego tupla ziterowanego forem wyzej
            log.debug("Inserting data into database...")
            log.debug(sql)
            self.c.executemany(sql, listaprzebojow)
            self.conn.commit()
            log.debug("Success!")
            return True
        else:
            log.debug("Start of SQL INSERT query for dict types...")
            sql = u"INSERT INTO {} ({}) VALUES ({})".format(table_name, u", ".join(key for key in data.keys()),
                                                            u", ".join(u'"{}"'.format(v) for v in data.values()))
            log.debug("Start of anti injection sql method...")
            regex = r"\s*INSERT.*"
            matches = re.match(regex, sql, re.MULTILINE | re.IGNORECASE)
            if not matches:
                raise Exception('Pytanie do bazy nie jest wlasciwe: {}'.format(sql))
            log.debug("Inserting data into database...")
            log.debug(sql)
            self.c.execute(sql)
            self.conn.commit()
            log.debug("Success!")
            return self.c.lastrowid

    def update(self, table_name, dane, where):
        """

        :param table_name: nazwa tabeli
        :type table_name: str
        :param dane: dane zapisane w dict
        :type dane: dict
        :param where: jest warunkiem wykonywania naszego update
        :type where: str
        """
        log.debug("Start of SQL UPDATE query...")
        sql = u"UPDATE {} SET {} WHERE {}".format(table_name, u", ".join(
            u"{} = '{}'".format(key, values) for key, values in dane.iteritems()), where)
        log.debug("Updating data in database...")
        self.c.execute(sql)
        self.conn.commit()
        log.debug("Success!")

    def delete(self, table_name, where):
        """

        :param table_name: nazwa tabeli
        :type table_name: str
        :param where: jest warunkiem wykonywania naszego delete
        :type where: str
        :return:
        """
        log.debug("Start of SQL DELETE query...")
        sql = 'DELETE from {} WHERE {}'.format(table_name, where)
        log.debug("Deleting data from database...")
        self.c.execute(sql)
        self.conn.commit()
        log.debug("Success!")

    def select(self, sql):
        """
        :param sql: typ danych wejsciowych
        :type sql: str
        :rtype tuple
        :return:
        """

        log.debug("Start of anti injection sql method...")
        regex = r"\s*SELECT.*"
        matches = re.match(regex, sql, re.MULTILINE | re.IGNORECASE)
        if not matches:
            raise Exception('Pytanie do bazy nie jest wlasciwe: {}'.format(sql))
        log.debug("Selecting data from database...")
        self.c.execute(sql)
        self.conn.commit()
        log.debug("Success!")
        return self.c.fetchall()

    def validateSQL(self, zmienna_valid, zmienna_val2):
        if zmienna_valid <> zmienna_val2 and zmienna_val2 is not None:
            log.error('Item number in data is not the same as number of expected items')
            raise ValueError("Item number in data is not the same as number of expected items")


