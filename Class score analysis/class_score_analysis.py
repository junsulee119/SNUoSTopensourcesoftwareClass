# -*- coding: utf-8 -*-
"""
Created on Mon Sep 23 18:51:50 2024

@author: junsu
"""

def read_data(filename):
    f = open(filename, 'r')
    f_list = f.read().split('\n')
    f_list.remove(f_list[0])  # 첫 번째 줄 제거
    data = [[int(x) for x in line.split(',')] for line in f_list if line]  # 쉼표로 분리하여 정수 리스트로 변환
    return data


def calc_weighted_average(data_2d, weight):
    average = []  # 각 행의 가중평균을 저장할 리스트
    weight_sum = sum(weight)  # 가중치의 합을 계산
    
    for row in data_2d:  # data_2d의 각 행에 대해 반복
        weighted_sum = 0
        for i in range(len(row)):
            weighted_sum += row[i] * weight[i]  # 각 점수에 가중치를 곱한 값을 더함
        average.append(weighted_sum / weight_sum)  # 가중합을 가중치의 합으로 나눔
    
    return average


def analyze_data(data_1d):
    mean = sum(data_1d) / len(data_1d)
    var = sum([(val - mean) ** 2 for val in data_1d]) / len(data_1d)
    median = 0
    sorted_data = sorted(data_1d)
    n = len(sorted_data)
    
    if n % 2 == 0:
        median = (sorted_data[n // 2 - 1] + sorted_data[n // 2]) / 2
    else:
        median = sorted_data[n // 2]
    
    return mean, var, median, min(data_1d), max(data_1d)


if __name__ == '__main__':
    data = read_data('data/class_score_en.csv')
    if data and len(data[0]) == 2: # Check 'data' is valid
        average = calc_weighted_average(data, [40/125, 60/100])

        # Write the analysis report as a markdown file
        with open('class_score_analysis.md', 'w') as report:
            report.write('### Individual Score\n\n')
            report.write('| Midterm | Final | Average |\n')
            report.write('| ------- | ----- | ----- |\n')
            for ((m_score, f_score), a_score) in zip(data, average):
                report.write(f'| {m_score} | {f_score} | {a_score:.3f} |\n')
            report.write('\n\n\n')

            report.write('### Examination Analysis\n')
            data_columns = {
                'Midterm': [m_score for m_score, _ in data],
                'Final'  : [f_score for _, f_score in data],
                'Average': average }
            for name, column in data_columns.items():
                mean, var, median, min_, max_ = analyze_data(column)
                report.write(f'* {name}\n')
                report.write(f'  * Mean: **{mean:.3f}**\n')
                report.write(f'  * Variance: {var:.3f}\n')
                report.write(f'  * Median: **{median:.3f}**\n')
                report.write(f'  * Min/Max: ({min_:.3f}, {max_:.3f})\n')