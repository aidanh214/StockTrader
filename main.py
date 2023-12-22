import sqlite3

# AlphaVantage API Key:
# W2RO7B9H5RESE4N1


class SpendingData:
    def __init__(self):
        self.transactions = {}

    def add_transaction(self, trans_date, value, note):
        if (trans_date, note) in self.transactions:
            self.transactions[trans_date, note][2] += value
        else:
            self.transactions[trans_date, note] = [trans_date, note, value]

    def remove_transaction(self, trans_date, note):
        if (trans_date, note) in self.transactions:
            del self.transactions[trans_date, note]
        else:
            raise ValueError("No transaction to delete.")

    def modify_transaction(self, date, note, new_value):
        if (date, note) in self.transactions:
            self.transactions[date, note] = [date, note, new_value]
        else:
            raise ValueError("No transaction to modify.")

    def save_data(self, filename):
        spend_string = ""
        for spend in self.transactions:
            spend_list = self.transactions[spend]
            spend_string += ("('"+str(spend_list[0])+"', '"+str(spend_list[1])+"', "+str(spend_list[2])+"),"+" ")
        spend_string = spend_string.removesuffix(", ")
        con = sqlite3.connect(filename)
        cur = con.cursor()
        try:
            cur.execute("DELETE FROM spending")
            cur.execute("""INSERT INTO spending (date, note, value) VALUES"""+spend_string)
        except sqlite3.OperationalError:
            cur.execute("CREATE TABLE spending(date, note, value)")
            cur.execute("DELETE FROM spending")
            cur.execute("""INSERT INTO spending (date, note, value) VALUES """ + spend_string)
        con.commit()

    def load_data(self, filename):
        con = sqlite3.connect(filename)
        cur = con.cursor()
        spends = cur.execute("SELECT date, note, value FROM spending ORDER BY date")
        for row in spends:
            date = row[0]
            note = row[1]
            value = int(row[2])
            self.transactions[date, note] = [date, note, value]


class InvestmentData:
    def __init__(self):
        self.portfolio = {}

    def add_asset(self, asset_type, number_of_asset, note=""):
        if (asset_type, note) in self.portfolio:
            self.portfolio[asset_type, note] += number_of_asset
        else:
            self.portfolio[asset_type, note] = number_of_asset

    def get_asset_value(self, asset_type, note=""):
        asset_value = self.portfolio[asset_type, note]
        return asset_value

    def save_data(self, filename):
        sql_string = ""
        for asset in self.portfolio:
            sql_string += "("
            sql_string += "'" + asset[0] + "', "
            sql_string += "'" + asset[1] + "', "
            sql_string += "'" + str(self.portfolio[asset]) + "'"
            sql_string += "),"
        sql_string = sql_string.removesuffix(",")
        con = sqlite3.connect(filename)
        cur = con.cursor()
        try:
            cur.execute("DELETE FROM assets")
            cur.execute("""INSERT INTO assets VALUES """ + sql_string)
        except sqlite3.OperationalError:
            cur.execute("CREATE TABLE assets(type, note, amount)")
            cur.execute("DELETE FROM assets")
            cur.execute("""INSERT INTO assets VALUES """ + sql_string)
        con.commit()

    def load_data(self, filename):
        con = sqlite3.connect(filename)
        cur = con.cursor()
        assets = cur.execute("SELECT type, note, amount FROM assets ORDER BY type")
        for row in assets:
            self.portfolio[row[0],row[1]] = int(row[2])


if __name__ == "__main__":
    pass
