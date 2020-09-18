# JetBrains Academy/Python Developer
# Project: To-Do List
# Work on project. Stage 4/4: Bye, completed tasks

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import sessionmaker

from datetime import datetime, timedelta
import calendar

Base = declarative_base()


class Table(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String)
    deadline = Column(Date, default=datetime.today())

    def __repr__(self):
        return f"{self.task}. {self.deadline}"

class Todolist:
    def menu(self) -> None:
        while True:
            print("\n1) Today's tasks\n2) Week's tasks\n3) All tasks\n4) Missed tasks\n5) Add task\n6) Delete task\n0) Exit")
            choice: str = input()
            if choice == '1':
                self.todays_tasks()
            elif choice == '2':
                self.weeks_tasks()
            elif choice == '3':
                self.all_tasks()
            elif choice == '4':
                self.missed_tasks()
            elif choice == '5':
                self.add_task()
            elif choice == '6':
                self.delete_task()
            elif choice == '0':
                print('\nBye!')
                exit()
            else:
                print('Unknown option.')

    def todays_tasks(self) -> None:
        rows = session.query(Table).filter(Table.deadline == datetime.today().date()).all()
        print('\nToday:', datetime.today().day, datetime.today().strftime('%b'))
        if not rows:
            print('Nothing to do!')
        else:
            for i, item in enumerate(rows):
                print(f'{i + 1}. {item.task}')

    def weeks_tasks(self) -> None:
        for i in range(7):
            today = datetime.today()
            today += timedelta(days=i)
            rows = session.query(Table).filter(Table.deadline == today.date()).all()
            print(calendar.day_name[today.weekday()], today.day, today.strftime('%b'), ':')
            if not rows:
                print('Nothing to do!\n')
            else:
                for i, item in enumerate(rows):
                    print(f'{i + 1}. {item.task}')
                print()

    def all_tasks(self) -> None:
        rows = session.query(Table).order_by(Table.deadline).all()
        print('\nAll tasks:')
        if not rows:
            print('Nothing to do!')
        else:
            for i, item in enumerate(rows):
               print(f"{i + 1}. {item.task}. {item.deadline.day} {item.deadline.strftime('%b')}")

    def missed_tasks(self) -> None:
        rows = session.query(Table).filter(Table.deadline < datetime.today().date()).order_by(Table.deadline).all()
        print('\nMissed tasks:')
        if not rows:
            print('Nothing to do!')
        else:
            for i, item in enumerate(rows):
               print(f"{i + 1}. {item.task}. {item.deadline.day} {item.deadline.strftime('%b')}")

    def add_task(self) -> None:
        print('Enter task')
        new_row = input()
        print('Enter deadline')
        new_date = input()
        new_date = datetime.strptime(new_date, "%Y-%m-%d")
        session.add(Table(task=new_row, deadline=new_date))
        session.commit()
        print('The task has been added!')

    def delete_task(self) -> None:
        rows = session.query(Table).filter(Table.deadline <= datetime.today().date()).order_by(Table.deadline).all()
        if not rows:
            print('Nothing is missed!')
        else:
            print('Choose the number of the task you want to delete:')
            for i, item in enumerate(rows):
                print(f"{i + 1}. {item.task}. {item.deadline.day} {item.deadline.strftime('%b')}")
            row_to_del = int(input())
            try:
                session.delete(rows[row_to_del - 1])
                session.commit()
            except IndexError:
                print('Wrong row number!')

if __name__ == "__main__":
    engine = create_engine('sqlite:///todo.db?check_same_thread=False')
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    Todolist().menu()
