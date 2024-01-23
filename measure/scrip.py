import pandas as pd
import argparse
import os

def expand_data(df, target_rows):
    current_rows = len(df)
    if current_rows >= target_rows:
        return df, 0

    # 计算需要添加的总行数
    rows_to_add = target_rows - current_rows

    # 遍历数据框，均匀插入新行
    new_rows = []
    for i in range(1, current_rows):
        # 计算在这对行之间需要插入的新行数
        rows_to_insert = round(i * rows_to_add / (current_rows - 1))

        # 在前一对行之间已插入的行数
        rows_already_inserted = len(new_rows)

        # 计算差值，生成新行
        row_diff = (df.iloc[i] - df.iloc[i-1]) / (rows_to_insert - rows_already_inserted + 1)
        for _ in range(rows_to_insert - rows_already_inserted):
            new_row = df.iloc[i-1] + row_diff * (_ + 1)
            new_row = new_row.round(2)  # 保留两位小数
            new_rows.append(new_row)

    # 使用pandas.concat方法添加新行
    df = pd.concat([df, pd.DataFrame(new_rows)], ignore_index=True)
    return df.sort_values(by=df.columns[0]), rows_to_add

def main(args):
    # 读取CSV文件
    df = pd.read_csv(args.input, header=None)

    # 按第一列升序排列
    df.sort_values(by=df.columns[0], inplace=True)

    # 识别所有重复行（排除第一次出现）
    duplicated_rows = df[df.duplicated(subset=df.columns[0], keep='first')]

    # 打印被移除的行和被移除行的数量
    print("Removed rows:")
    print(duplicated_rows)
    print(f"A total of {len(duplicated_rows)} rows were removed.")

    # 仅保留基于第一列的重复行的第一次出现
    df.drop_duplicates(subset=df.columns[0], keep='first', inplace=True)

    # 如果数据不足128条，扩充到129条
    df, rows_added = expand_data(df, 129)

    # 打印扩充了多少行
    print(f"Expanded by {rows_added} rows.")

    # 将结果保存到新的CSV文件
    df.to_csv(args.output, header=False, index=False)
    os.remove(args.input)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Remove all but the first occurrence of duplicate rows in a CSV file based on the first column and expand the data to 129 rows if there are less than 128 rows using linear interpolation, rounding off to 2 decimal places.')
    parser.add_argument('--input', '-i', type=str, required=True, help='Path to the input CSV file')
    parser.add_argument('--output', '-o', type=str, required=True, help='Path to the output CSV file')

    args = parser.parse_args()
    main(args)

