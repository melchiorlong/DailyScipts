import pandas as pd
import concurrent.futures
import os
import openpyxl


def save_to_excel(date, data, output_dir):
    """将单个日期的数据保存为Excel文件"""
    output_file = os.path.join(output_dir, f'{date}.csv')
    data.to_csv(output_file, index=False)
    print(f"保存完毕: {output_file}")


def process_chunk(chunk, date_column, data_dict):
    """将数据块按日期分组并存储在字典中"""
    for date, group in chunk.groupby(date_column):
        if date in data_dict:
            data_dict[date] = pd.concat([data_dict[date], group])
        else:
            data_dict[date] = group


def main(input_file, date_column, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    chunksize = 100000  # 每次读取的行数
    data_dict = {}

    # 逐行读取CSV文件
    for chunk in pd.read_csv(input_file, chunksize=chunksize, parse_dates=[date_column]):
        process_chunk(chunk, date_column, data_dict)

    # 使用ThreadPoolExecutor来并行保存Excel文件
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []
        for date, data in data_dict.items():
            futures.append(executor.submit(save_to_excel, date, data, output_dir))

        # 等待所有线程完成
        concurrent.futures.wait(futures)


if __name__ == "__main__":
    input_file = 'data.csv'
    date_column = 'datetime'  # 替换为你的日期时间列名
    output_dir = '/Users/tianlong/PycharmProjects/DailyScipts/DailyTest/TemporaryScript/res'

    main(input_file, date_column, output_dir)
