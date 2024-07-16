import sqlite3

db = sqlite3.connect('cars.db')

cursor = db.cursor()

async def start_db():
    cursor.execute('''
CREATE TABLE IF NOT EXISTS cars(
                   seller TEXT,
                   model TEXT,
                   horsepower TEXT,
                   car_number TEXT,
                   date TEXT,
                   is_new TEXT,
                   photo TEXT
)
''')
async def add_to_db(seller,model,horsepower,car_number,date,is_new,photo):
    cursor.execute('''
INSERT INTO cars(
                   seller,model,horsepower,car_number,date,is_new,photo
)
                   VALUES(?,?,?,?,?,?,?)
''',(seller,model,horsepower,car_number,date,is_new,photo))
    db.commit()

async def show_cars():
    cursor.execute('SELECT *FROM cars')
    cars = cursor.fetchall()
    return cars
print()