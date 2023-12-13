renovation_costs: float = 191126.1
rental_month: float = 7590
loan_year: int = 5
rental_year = 8
loan_rates: float = 0.03
management_rates = 0.1 * 0.89
maintain_fee_year = 860
management_fee = rental_month * management_rates
occupancy_rate = 0.98
month_sharing_rates = 0.8
# lianjia_profit_sharing_year = 0.074
us_profit_sharing_year_rate = 0.7
total_principal_and_interest = renovation_costs + renovation_costs * loan_rates * loan_year
repay_loan_month = total_principal_and_interest / (loan_year * 12)
maintain_fee_month = maintain_fee_year / 12

rental_increase_rate = 1
while rental_increase_rate <= 1.05:
    rental_month: float = 7590
    init_rental_year = 1
    revenue_sum = []
    while init_rental_year <= rental_year:
        month_sharing = rental_month * month_sharing_rates
        # （出租价格 × 出租率 - 保底）×分成比例 ×12个月

        us_profit_sharing = rental_month * (occupancy_rate - month_sharing_rates) * us_profit_sharing_year_rate
        if init_rental_year <= 5:
            revenue_month = month_sharing - management_fee - maintain_fee_month - repay_loan_month + us_profit_sharing
        else:
            revenue_month = month_sharing - management_fee - maintain_fee_month + us_profit_sharing
        revenue_sum.append(revenue_month * 12)
        print('年涨幅为' + str(int((rental_increase_rate - 1) * 100)) + '%')
        print('第' + str(init_rental_year) + '年月均收益' + str(int(revenue_month)))
        print('第' + str(init_rental_year) + '年总收益' + str(int(revenue_month) * 12))
        print('总计收益' + str(int(sum(revenue_sum))))
        print('总计月均收益' + str(int(sum(revenue_sum) / (init_rental_year * 12))))
        print()
        init_rental_year += 1
        rental_month = rental_month * rental_increase_rate
    rental_increase_rate += 0.01
    print('---------------------------------------------------------------')
