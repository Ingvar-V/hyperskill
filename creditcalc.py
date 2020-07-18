import math
import argparse

parser = argparse.ArgumentParser(description="Credit calculator")
parser.add_argument("--type", choices=['annuity', 'diff'], help="a type of payment")
parser.add_argument("--payment", type=int, dest="payment", help="monthly payment")
parser.add_argument("--principal", type=int, dest="principal")
parser.add_argument("--periods", type=int, dest="periods")
parser.add_argument("--interest", type=float, dest="interest")
args = parser.parse_args()
diff_payment_sum = 0
if args.type == 'diff':
    if not args.principal or not args.periods or not args.interest:
        print("Incorrect parameters.")
    else:
        for m in range (1, args.periods + 1):
            diff_payment = args.principal / args.periods + args.interest / (12 * 100) * (args.principal - args.principal * (m - 1) / args.periods)
            diff_payment = math.ceil(diff_payment)
            print("Month {}: paid out {}".format(m, diff_payment))
            diff_payment_sum +=  diff_payment
        overpaiment = diff_payment_sum - args.principal
        print()
        print("Overpayment = {}".format(overpaiment))
if args.type == 'annuity':
    if args.interest:
        nominal_interest_rate = args.interest / (12 * 100)
        if not args.periods:
            periods_cnt = math.log(args.payment / (args.payment - nominal_interest_rate * args.principal), 1 + nominal_interest_rate)
            periods_cnt = math.ceil(periods_cnt)
            year_cnt = periods_cnt // 12
            month_cnt = periods_cnt % 12
            overpaiment = args.payment * periods_cnt - args.principal
            if year_cnt == 0:
                print('You need {} months to repay this credit!'.format(month_cnt))
            elif month_cnt == 0:
                print('You need {} years to repay this credit!'.format(year_cnt))
            else:
                print('You need {} years and {} months to repay this credit!'.format(year_cnt, month_cnt))
            print('Overpaiment = {}'.format(overpaiment))
        if not args.payment:
            monthly_payment = args.principal * (nominal_interest_rate * math.pow(1 + nominal_interest_rate, args.periods)) / (math.pow(1 + nominal_interest_rate, args.periods) - 1)
            monthly_payment = math.ceil(monthly_payment)
            overpaiment = monthly_payment * args.periods - args.principal
            print('Your annuity payment = {}!'.format(monthly_payment))
            print('Overpaiment = {}'.format(overpaiment))
        if not args.principal:
            principal = args.payment / ((nominal_interest_rate * (math.pow(1 + nominal_interest_rate, args.periods))) / (math.pow(1 + nominal_interest_rate, args.periods) - 1))
            principal = math.floor(principal)
            overpaiment = args.payment * args.periods - principal
            print('Your credit principal = {}!'.format(principal))
            print('Overpaiment = {}'.format(overpaiment))
    else:
        print("Incorrect parameters.")
