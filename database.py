import datetime


class DataBase:
    def __init__(self, filename):
        self.filename = filename
        self.users = None
        self.partners = None
        self.file = None
        if filename == "users.txt":
            self.load()
        else:
            self.load_partner()

    def load(self):
        self.file = open(self.filename, "r")
        self.users = {}

        for line in self.file:
            email, password, name, address, created = line.strip().split(";")
            self.users[email] = [password, name, address, created]

        self.file.close()
    
    def load_partner(self):
        self.file = open(self.filename, "r")
        self.partners = {}

        for line in self.file:
            email, password, name, address, created, limit, food = line.strip().split(";")
            self.partners[email] = [password, name, address, created, limit, food]

        self.file.close()

    def get_user(self, email):
        if email in self.users:
            return self.users[email]
        else:
            return -1

    def get_partner(self, email):
        if email in self.partners:
            return self.partners[email]
        else:
            return -1

    def add_user(self, email, password, name, address):
        if email.strip() not in self.users:
            self.users[email.strip()] = [password.strip(), name.strip(), address.strip(), DataBase.get_date()]
            self.save_user()
            return 1
        else:
            print("Email exists already")
            return -1
            
    def add_partner(self, email, password, name, address, limit, food):
        if email.strip() not in self.partners:
            self.partners[email.strip()] = [password.strip(), name.strip(), address.strip(), DataBase.get_date(), limit.strip(), food]
            self.save_partner()
            return 1
        else:
            print("Email exists already")
            return -1

    def validate(self, email, password):
        if self.get_user(email) != -1:
            return self.users[email][0] == password
        else:
            return False
            
    def validate_partner(self, email, password):
        if self.get_partner(email) != -1:
            return self.partners[email][0] == password
        else:
            return False
            
    def add_food(self, name, cuisine, price, email):
        if eval(self.partners[email][5]) is None:
            self.partners[email][5] = str([[name, cuisine, price]])
        else:
            tempList = eval(self.partners[email][5])
            tempList.append([name, cuisine, price])
            self.partners[email][5] = str(tempList)
        self.update_partner(email)
        
    def match_food(self, name, email):
        tempList = eval(self.partners[email][5])
        for dish in tempList:
            if name in dish:
                return dish
        return [-1, -1, -1]
        
    def update_food(self, oldName, name, cuisine, price, email):
        tempList = eval(self.partners[email][5])
        res = [n for n, c, p in tempList].index(oldName)
        tempList[res][0] = name
        tempList[res][1] = cuisine
        tempList[res][2] = price
        self.partners[email][5] = str(tempList)
        self.update_partner(email)

    def save_user(self):
        with open(self.filename, "w") as f:
            for user in self.users:
                f.write(user + ";" + self.users[user][0] + ";" + self.users[user][1] + ";" + self.users[user][2] + ";" + self.users[user][3] + "\n")

    def match_restaurant(self, name):
        for partner in self.partners:
            if name == self.partners[partner][1]:
                return self.partners[partner][5]
        return -1


    def match_cuisine(self, food, cuisine):
        if cuisine == "all":
            return True
        tempList = eval(food)
        for dish in tempList:
            if dish[1] == cuisine:
                return True

    def limitSet(self, value, email):
        self.partners[email][4] = value
        self.update_partner(email)
    
    def delete_user(self, email):
        with open(self.filename, "r") as f:
            lines = f.readlines()
        with open (self.filename, "w") as f:
            for line in lines:
                if email in line.strip("\n"):
                    continue
                f.write(line)
        
    def update_partner(self, email):
        with open(self.filename, "r") as f:
            lines = f.readlines()
        with open (self.filename, "w") as f:
            for line in lines:
                if email in line.strip("\n"):
                    continue
                f.write(line)
        self.save_partner() 
    
    def update_user(self, email, name, address):
        self.users[email][1] = name
        self.users[email][2] = address
        with open(self.filename, "r") as f:
            lines = f.readlines()
        with open (self.filename, "w") as f:
            for line in lines:
                if email in line.strip("\n"):
                    continue
                f.write(line)
        self.save_user() 
        
    def save_partner(self):
        with open(self.filename, "w") as f:
            for partner in self.partners:
                f.write(partner + ";" + self.partners[partner][0] + ";" + self.partners[partner][1] + ";" + self.partners[partner][2] + ";" + self.partners[partner][3] + ";" + self.partners[partner][4] + ";" + self.partners[partner][5] + "\n")

    @staticmethod
    def get_date():
        return str(datetime.datetime.now()).split(" ")[0]
