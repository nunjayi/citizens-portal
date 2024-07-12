#backend/sedd.py

import random
from faker import Faker
from datetime import datetime
from app import app, db
from models import Citizen, Ministry, CivilServant, Project, Budget, Expenditure, Tender

fake = Faker()

def create_citizens(n=40):
    citizens = []
    for _ in range(n):
        citizen = Citizen(name=fake.name(), _password_hash=fake.password())
        db.session.add(citizen)
        citizens.append(citizen)
    db.session.commit()
    return citizens

def create_ministries(n=10):
    ministries = []
    for _ in range(n):
        ministry = Ministry(name=fake.company(), amount=round(random.uniform(10000, 1000000), 2))
        db.session.add(ministry)
        ministries.append(ministry)
    db.session.commit()
    return ministries

def create_budgets(n=20):
    budgets = []
    for _ in range(n):
        budget = Budget(amount=round(random.uniform(10000, 1000000), 2))
        db.session.add(budget)
        budgets.append(budget)
    db.session.commit()
    return budgets

def create_civil_servants(citizens, ministries, n=50):
    civil_servants = []
    for _ in range(n):
        civil_servant = CivilServant(
            user_id=random.choice(citizens).id,
            ministry_id=random.choice(ministries).id,
            role=fake.job(),
            salary=round(random.uniform(30000, 120000), 2),
            allowance=round(random.uniform(1000, 10000), 2)
        )
        db.session.add(civil_servant)
        civil_servants.append(civil_servant)
    db.session.commit()
    return civil_servants

def create_projects(ministries, budgets, n=10):
    projects = []
    statuses = ['Planning', 'In Progress', 'Complete'] 

    for _ in range(n):
        ministry = random.choice(ministries)
        budget = random.choice(budgets)
        status = random.choice(statuses)
        start_date = fake.date_time_between(start_date='-1y', end_date='now')
        
        if status == 'Complete':
            end_date = datetime.now()
        else:
            end_date = None
        
        project = Project(
            ministry_id=ministry.id,
            name=fake.company(),
            description=fake.text(),
            start_date=start_date,
            end_date=end_date,
            status=status,
            budget_id=budget.id
        )
        db.session.add(project)
        projects.append(project)
    
    db.session.commit()
    return projects

def create_expenditures(budgets, n=100):
    expenditures = []
    for _ in range(n):
        expenditure = Expenditure(
            budget_id=random.choice(budgets).id,
            item=fake.word(),
            amount=round(random.uniform(10, 10000), 2)
        )
        db.session.add(expenditure)
        expenditures.append(expenditure)
    db.session.commit()
    return expenditures

def create_tenders(civil_servants, expenditures, n=50):
    tenders = []
    for _ in range(n):
        tender = Tender(
            user_id=random.choice(civil_servants).user_id,
            expenditure_id=random.choice(expenditures).id,
            description=fake.sentence(),
            cost=round(random.uniform(1000, 100000), 2)
        )
        db.session.add(tender)
        tenders.append(tender)
    db.session.commit()
    return tenders

if __name__ == '__main__':
    with app.app_context():
        print('Starting seeding...')
        db.create_all()
        
        citizens = create_citizens()
        ministries = create_ministries()
        budgets = create_budgets()
        civil_servants = create_civil_servants(citizens, ministries)
        projects = create_projects(ministries, budgets)
        expenditures = create_expenditures(budgets)
        tenders = create_tenders(civil_servants, expenditures)
        
        print("Fake data has been generated and added to the database.")
