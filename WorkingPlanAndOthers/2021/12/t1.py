l1 = [1,2,3,7]

def get_day_rev_expr_list(day_list: list) -> list:
    day_rev_expr_list: list = list()
    for day_index in day_list:
        day_rev_expr_list.append(
            f"nvl(sum(day{day_index}_ads_rev), 0.0) as day{day_index}_ads_rev,"
        )
        day_rev_expr_list.append(
            f"nvl(sum(day{day_index}_iap_rev), 0.0) as day{day_index}_iap_rev,"
        )
    return day_rev_expr_list



def get_day_item_list(day_list: list) -> list:
    day_item_list: list = list()
    for day_index in day_list:
        day_item_list.append(
            f"nvl(day{day_index}_ads_rev, 0.0) as day{day_index}_ads_rev, \n "
            f"nvl(day{day_index}_iap_rev, 0.0) as day{day_index}_iap_rev,"
        )
    return day_item_list

# res = get_day_rev_expr_list(l1)
res = get_day_item_list(l1)
for i in res:
    print(i)