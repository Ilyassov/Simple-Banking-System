import random
import sqlite3


class BankCard:
    def __init__(self, client_id):
        self.id = client_id
        number = str(client_id)
        number = "400000" + "0" * (9 - len(number)) + number
        number = number + generate_checksum(number)
        self.number = number
        self.pin = str(random.randint(0, 9999))
        self.pin = "0" * (4 - len(self.pin)) + self.pin
        self.balance = 0

    def get_number(self):
        return self.number

    def get_pin(self):
        return self.pin

    def get_info(self):
        return self.id, self.number, self.pin, self.balance


def generate_checksum(generated_id):
    generated_id = [int(number) for number in generated_id]
    for i in range(0, len(generated_id), 2):
        generated_id[i] *= 2
    ans = 0
    for i in range(len(generated_id)):
        if generated_id[i] > 9:
            generated_id[i] -= 9
        ans += generated_id[i]
    return '0' if ans % 10 == 0 else str(10 - ans % 10)


class CardBase:
    def __init__(self):
        random.seed()

    @staticmethod
    def generate_account(cur, conn):
        while True:
            cur.execute('SELECT id FROM card;')
            id_list = cur.fetchall()
            generated_id = random.randint(0, 999999999)
            if (generated_id, ) not in id_list:
                break
        new_card = BankCard(generated_id)
        cur.execute(f'INSERT INTO card VALUES {new_card.get_info()};')
        print("Your card has been created")
        print("Your card number:")
        print(new_card.get_number())
        print("Your card PIN:")
        print(new_card.get_pin())
        conn.commit()

    @staticmethod
    def check_card_and_pin(cur, card_number, pin):
        if len(card_number) != 16:
            return False
        elif card_number[:6] != "400000":
            return False
        else:
            cur.execute(f'''SELECT number, pin FROM card
                            WHERE number = "{card_number}" AND pin = "{pin}";''')
            return cur.fetchall() != []

    @staticmethod
    def get_balance(cur, card_number):
        cur.execute(f'''SELECT balance FROM card WHERE number = "{card_number}";''')
        return cur.fetchall()[0][0]

    @staticmethod
    def update_balance(cur, conn, number, income):
        cur.execute(f'''UPDATE card SET balance = balance + {income}
        where number = "{number}";''')
        conn.commit()

    @staticmethod
    def check_card(cur, card_number):
        cur.execute(f'''SELECT number FROM card
                        WHERE number = "{card_number}";''')
        return cur.fetchall() != []

    @staticmethod
    def delete_account(cur, conn, number):
        cur.execute(f'delete from card where number = "{number}"')
        conn.commit()


class Program:
    def __init__(self, conn, cur):
        self.card_base = CardBase()
        self.state = "main"
        self.number = None
        self.conn = conn
        self.cur = cur

    def log_in(self, card_number, pin):
        if self.card_base.check_card_and_pin(self.cur, card_number, pin):
            self.state = "logged"
            self.number = card_number
            print("You have successfully logged in!")
        else:
            self.state = "main"
            print("Wrong card number or PIN!")

    def print_menu(self):
        if self.state == "logged":
            print("1. Balance\n2. Add income\n3. Do transfer\n4. Close account\n5. Log out\n0. Exit")
        else:
            print("1. Create an account\n2. Log into account\n0. Exit")

    def log_out(self):
        self.state = "main"
        self.number = None
        print("You have successfully logged out!")

    def proceed_main_menu(self, user_input):
        if user_input not in ["1", "2", "0"]:
            print("Wrong user input!")
        elif user_input == "1":
            self.card_base.generate_account(self.cur, self.conn)
        elif user_input == "2":
            card_number = input("Enter your card number:\n")
            pin = input("Enter your PIN:\n")
            self.log_in(card_number, pin)
        else:
            self.close()

    def proceed_logged_account(self, user_input):
        if user_input not in ["1", "2", "3", "4", "5", "0"]:
            print("Wrong user input!")
        elif user_input == "1":
            print("Balance:", self.card_base.get_balance(self.cur, self.number))
        elif user_input == "2":
            user_input = input("Enter income:\n")
            if not user_input.isdecimal():
                print("Wrong income value!")
            else:
                self.card_base.update_balance(self.cur, self.conn, self.number, user_input)
                print("Income was added!")
        elif user_input == "3":
            print("Transfer")
            user_input = input("Enter card number:\n")
            if not user_input.isdecimal() or len(user_input) != 16 or generate_checksum(user_input[:15]) != user_input[-1]:
                print("Probably you made a mistake in the card number. Please try again!")
            else:
                number = user_input
                if not self.card_base.check_card(self.cur, number):
                    print("Such a card does not exist.")
                else:
                    user_input = input("Enter how much money you want to transfer:\n")
                    if not user_input.isdecimal():
                        print("Wrong money transfer value!")
                    else:
                        money = int(user_input)
                        if self.card_base.get_balance(self.cur, self.number) >= money:
                            self.card_base.update_balance(self.cur, self.conn, number, money)
                            self.card_base.update_balance(self.cur, self.conn, self.number, -money)
                            print("Success!")
                        else:
                            print("Not enough money!")
        elif user_input == "4":
            self.card_base.delete_account(self.cur, self.conn, self.number)
            self.number = None
            self.state = "main"
            print("The account has been closed!")
        elif user_input == "5":
            self.log_out()
        else:
            self.close()

    def proceed_user_input(self, user_input):
        if self.state == "main":
            self.proceed_main_menu(user_input)
        elif self.state == "logged":
            self.proceed_logged_account(user_input)
        else:
            self.close()

    def start(self):
        while True:
            self.print_menu()
            self.proceed_user_input(input())
            if self.state == "off":
                break

    def close(self):
        self.state = "off"
        print("Bye!")


if __name__ == "__main__":
    _connect = sqlite3.connect('card.s3db')
    _cursor = _connect.cursor()
    _cursor.execute('''CREATE TABLE IF NOT EXISTS
                        card(
                            id INTEGER,
                            number TEXT,
                            pin TEXT,
                            balance INTEGER DEFAULT 0
                        );''')
    _connect.commit()
    program = Program(_connect, _cursor)
    program.start()
