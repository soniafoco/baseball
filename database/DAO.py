from database.DB_connect import DBConnect
from model.team import Team


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def getAllYears():


        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """ select distinct(t.year)
                    from teams t
                    where t.year>=1980
                    order by t.year desc"""

        cursor.execute(query)

        for row in cursor:
            result.append(row["year"])

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getSquadreAnno(year):

        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """ select t.*, sum(s.salary) as salary
                    from salaries s, teams t, appearances a 
                    where s.`year` = %s and t.`year` = %s and a.`year` = %s
                    and t.ID = a.teamID and s.playerID = a.playerID 
                    group by t.teamCode 
                    order by t.teamCode asc"""

        cursor.execute(query, (year, year, year,))

        for row in cursor:
            result.append(Team(**row))

        cursor.close()
        conn.close()
        return result




