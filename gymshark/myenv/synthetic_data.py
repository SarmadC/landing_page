from faker import Faker
import pandas as pd
from random import randint

fake = Faker()

def input_data(x):
    df = pd.DataFrame()
    for i in range(0, x):
        df.loc[i, 'id'] = randint(1,1000)
        df.loc[i, 'name'] = fake.name()
        df.loc[i, 'email'] = fake.email()
        df.loc[i, 'phone_number'] = fake.phone_number()
        df.loc[i, 'birthdate'] = fake.date_of_birth()
        df.loc[i,'address'] = fake.address()

    return df

df = input_data(1000)

synthetic_customer_data = df.to_csv('synthetic_customer.csv')