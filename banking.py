import sqlite3
from sqlite3 import Error
from random import sample


class Banking:
    def __init__(self):
        self.database = r"card.s3db"
        self.conn = create_connection(self.database)

    def menu(self) -> None:
        while True:
            print('1. Create an account\n2. Log into account\n0. Exit')
            choice: str = input()
            if choice == '1':
                self.create_account()
            elif choice == '2':
                self.login()
            elif choice == '0':
                print('Bye!')
                exit()
            else:
                print('Unknown option!')

    def sub_menu(self, card: str) -> None:
        while True:
            print('1. Balance\n2. Add income\n3. Do transfer\n4. Close account\n5. Log out\n0. Exit')
            choice = input()
            if choice == '1':
                balance = select_balance(self.conn, card)
                print(f"\nBalance: {balance[0]}\n")
            elif choice == '2':
                self.income(card)
            elif choice == '3':
                self.transfer(card)
            elif choice == '4':
                self.delete(card)
            elif choice == '5':
                print('You have successfully logged out!\n')
                return
            elif choice == '0':
                print('Bye!')
                exit()
            else:
                print('Unknown option!')

    @staticmethod
    def luhn_method(card_number:str) -> str:
        card_number = [int(x) for x in card_number]
        card_number[::2] = [x * 2 for x in card_number[::2]]
        for i, x in enumerate(card_number):
                if card_number[i] > 9:
                    card_number[i] = card_number[i] - 9
        last_digit = str((sum(card_number) * 9) % 10) # we've got the checksum
        return last_digit

    @staticmethod
    def generate_numbers() -> tuple:
        random_card_number = '400000' + ''.join((str(x) for x in sample(range(10), 9)))
        random_pin = ''.join((str(x) for x in sample(range(10), 4)))
        yield random_card_number + Banking.luhn_method(random_card_number), random_pin

    def create_account(self) -> None:
        card_number, card_pin = next(self.generate_numbers())
        data = (card_number, card_pin)
        insert_data(self.conn, data)
        print('\nYour card has been created')
        print(f'Your card number:\n{card_number}')
        print(f'Your card PIN:\n{card_pin}\n')

    def login(self) -> None:
        card: str = input('Enter your card number:\n')
        pin: str = input('Enter your PIN:\n')
        with self.conn:
            try:
                pin_card = select_pin(self.conn, card)
                if pin_card[0] == pin:
                    print('You have successfully logged in!\n')
                    self.sub_menu(card)
                else:
                    print('Wrong card number or PIN\n')
            except TypeError:
                print('Wrong card number or PIN\n')

    def income(self, card) -> None:
        amount: int = int(input('Enter income:\n'))
        with self.conn:
            update_balance(self.conn, card, amount)
            print('Income was added!')

    def transfer(self, card) -> None:
        card_recipient: str = input('Enter card number:\n')
        card_to_check = list(card_recipient)
        del card_to_check[-1]
        card_to_check = "".join(card_to_check) + self.luhn_method(card_to_check)
        if card_to_check == card_recipient:
            with self.conn:
                if select_card(self.conn, card_recipient)[0]:
                    print(select_card(self.conn, card_recipient)[0])
                    amount: int = int(input('Enter how much money you want to transfer:\n'))
                    balance = select_balance(self.conn, card)[0]
                    if amount <= balance:
                        balance -= amount
                        update_balance(self.conn, card_recipient, amount)
                        decrease_balance(self.conn, card, balance)
                        print('Success!')
                    else:
                        print('Not enough money!')
                else:
                    print('Such a card does not exist.')
        else:
            print('Probably you made a mistake in the card number. Please try again!')

    def delete(self, card) -> None:
        with self.conn:
            delete_card(self.conn, card)
            print('The account has been closed!!')


def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
    return conn


def create_table(conn, create_table_sql):
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)


def insert_data(conn, data):
    sql = ''' INSERT INTO card(number, pin)
              VALUES(?, ?) '''
    cur = conn.cursor()
    cur.execute(sql, data)
    conn.commit()


def select_pin(conn, card):
    cur = conn.cursor()
    cur.execute("SELECT pin FROM card WHERE number=?", (card, ))
    return cur.fetchone()


def select_balance(conn, card):
    cur = conn.cursor()
    cur.execute("SELECT balance FROM card WHERE number=:card", {"card": card})
    return cur.fetchone()


def update_balance(conn, card, amount):
    cur = conn.cursor()
    current_balance = select_balance(conn, card)
    cur.execute("UPDATE card SET balance=:amount WHERE number=:card ", {"amount": amount + current_balance[0], "card": card})
    conn.commit()


def decrease_balance(conn, card, amount):
    cur = conn.cursor()
    cur.execute("UPDATE card SET balance=:amount WHERE number=:card ", {"amount": amount, "card": card})
    conn.commit()


def select_card(conn, card):
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM card WHERE number=:card", {"card": card})
    return cur.fetchone()


def delete_card(conn, card):
    cur = conn.cursor()
    cur.execute("DELETE FROM card WHERE number=:card", {"card": card})
    conn.commit()


def main():
    database = r"card.s3db"
    sql_create_card_table = """ CREATE TABLE IF NOT EXISTS card (
                                        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                                        number TEXT,
                                        pin TEXT,
                                        balance INTEGER default 0
                                    ); """

    # create a database connection
    conn = create_connection(database)

    if conn is not None:
        # create card table
        create_table(conn, sql_create_card_table)
    else:
        print("Error! cannot create the database connection.")


if __name__ == '__main__':
    main()

Banking().menu()
