# python-avalanche
avalance debt calculator in python

## Instructions

```bash
git clone https://github.com/skaramicke/python-avalanche.git
cd python-avalanche
python3 -m venv env
source env/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
cp example.data.yaml data.yaml
vim data.yaml # edit to your liking
python main.py
```

## Sample data file, with comments
```yaml
settings:
    # Some banks round the interest due
    round_interests: True 
    # Date of first event, useful for long term use
    first_payment: 2020-06-28
    # The total amount you can spend on debts each month
    amount: 100

debts:
    - name: Car loan # Name
      debt: 1000 # Starting amount
      interest: 4.00 # Year on year interest
    - name: Mortgage
      debt: 10000
      interest: 2.89
    - name: Student loans
      debt: 25000
      interest: 2.8
```