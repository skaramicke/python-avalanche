#!env/bin/python3

from matplotlib import pyplot
import datetime as dt
import yaml


class Debt:
    name: str = ''
    starting_amount: float = 0.0
    amount: float = 0.0
    interest: float = 0.0
    paid_amount: float = 0.0
    paid_interest: float = 0.0

    def __init__(self, name: str, amount: float, interest: float):
        self.name = name
        self.starting_amount = amount
        self.amount = amount
        self.interest = interest

    def get_interest_amount(self) -> float:
        return self.amount / 100 * self.interest / 12

    def get_paid_total(self) -> float:
        return self.paid_amount + self.paid_interest

    def monthly_pay(self, amount) -> float:
        amoritization = amount - self.get_interest_amount()
        if amoritization < 0:
            # print('%s. %.2f is not enough' % (self, amount))
            return amount
        interest_amount = self.get_interest_amount()

        self.paid_interest += self.get_interest_amount()
        if amoritization > self.amount:
            amoritization -= self.amount
            self.paid_amount += self.amount
            self.amount = 0
            # print('%s. %.2f in. Finished. Remaining: %.2f' % (self, amount, amoritization))
            return amoritization

        self.paid_amount += amoritization
        self.amount -= amoritization
        # print('%s. %.2f in. Paid %.2f interest and amoritized %.2f' % (self, amount, interest_amount, amoritization))
        return 0

    def __str__(self) -> str:
        return '%s: %.2f, %.2f%% (paid %.2f and %.2f)' % (self.name, self.starting_amount, self.interest, self.paid_amount, self.paid_interest)


def read_data() -> ([Debt], []):
    settings = []
    debts = []
    with open('data.yaml') as file:
        sections = yaml.load(file, Loader=yaml.FullLoader)
        settings = sections['settings']
        debts = []
        for d in sections['debts']:
            debt = Debt(d['name'], d['debt'], d['interest'])
            debts.append(debt)

    return settings, debts


def process():
    settings, debts = read_data()
    print('Starting process on', settings['first_payment'])

    # order debts by mode
    debts = sorted(debts, key=lambda i: i.interest, reverse=True)

    datasets = {}

    interests = 0
    for debt in debts:
        datasets[debt.name] = []
        interest = debt.get_interest_amount()
        if 'round_interests' in settings and settings['round_interests']:
            interest = round(interest)
        interests += interest

    payment = settings['amount'] - interests

    if payment < 0:
        print('Monthly amount is too low. At least', interests, ' is required.')
    else:
        remainder = 0
        months = 0
        for debt in debts:
            starting_interest = debt.get_interest_amount()
            payment += starting_interest
            dataset = []
            while debt.amount > 0:
                months += 1
                remainder = debt.monthly_pay(payment + remainder)
                for d in debts:
                    datasets[d.name].append(d.amount)

            payment += round(starting_interest)

        sum_paid_amount = 0
        sum_paid_interest = 0
        for debt in debts:
            sum_paid_amount += debt.paid_amount
            sum_paid_interest += debt.paid_interest
            print(debt)

        start_date = settings['first_payment']
        end_date = start_date + dt.timedelta(weeks=months*4)

        print('By %s you will have paid %.2f in debt and %.2f in interest over a period of %d months' % (
            end_date,
            sum_paid_amount,
            sum_paid_interest,
            months
        ))

        for name in datasets:
            pyplot.plot(datasets[name])
        pyplot.savefig('graph.pdf')


if __name__ == "__main__":
    process()
