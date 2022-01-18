from selenium import webdriver
from collections import Counter
from pandas import *

options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument("--disable-gpu")
options.add_experimental_option('excludeSwitches', ['enable-logging'])
options.add_argument('--log-level=3')

driver = webdriver.Chrome('/HDD1/mvpservereight/minhyeok/chromedriver/chromedriver', options=options)
driver.implicitly_wait(5)

driver.get(url="https://paperswithcode.com/area/computer-vision")

total_list = []

cnt = 1
field_list = []

while True:
    try:
        field = driver.find_element_by_xpath('/html/body/div[3]/div/div[2]/div[{}]/div/h2'.format(cnt)).text
        cnt += 3

        field_list.append(field)

    except:
        break

driver.close()

for field_name in field_list:
    print(field_name)
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument("--disable-gpu")
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.add_argument('--log-level=3')

    driver = webdriver.Chrome('/HDD1/mvpservereight/minhyeok/chromedriver/chromedriver', options=options)
    driver.maximize_window()
    driver.implicitly_wait(5)

    driver.get(url="https://paperswithcode.com/area/computer-vision/{}".format(field_name.lower().replace(' ', '-')))

    cnt = 1

    while True:
        try:
            small_field_name = driver.find_element_by_xpath('/html/body/div[3]/div[2]/div[{}]/div[{}]/a/div/h1'.format((cnt - 1) // 5 + 1, (cnt - 1) % 5 + 1)).text
            print(small_field_name)
            driver.find_element_by_xpath('/html/body/div[3]/div[2]/div[{}]/div[{}]/a'.format((cnt - 1) // 5 + 1, (cnt - 1) % 5 + 1)).send_keys("\n")
            cnt += 1

            try:
                driver.find_element_by_xpath('//*[@id="benchmarks"]/div[2]/div[1]/a').send_keys("\n")
            except:
                pass

            table_cnt = 1

            year_list = []

            while True:
                try:
                    driver.find_element_by_xpath('//*[@id="benchmarksTable"]/tbody/tr[{}]/td[6]/div/a'.format(table_cnt)).send_keys("\n")
                    table_cnt += 1

                    leaderboard_item_cnt = 1
                    leaderboard_cnt = 1

                    while True:
                        try:
                            leaderboard_item = driver.find_element_by_xpath('//*[@id="leaderboard"]/div[3]/table/thead/tr/th[{}]'.format(leaderboard_item_cnt)).text
                            if leaderboard_item == 'Year':
                                target_leaderboard_cnt = leaderboard_item_cnt
                                break

                            leaderboard_item_cnt += 1

                        except:
                            break

                    while True:
                        try:
                            year = driver.find_element_by_xpath('//*[@id="leaderboard"]/div[3]/table/tbody/tr[{}]/td[{}]/div'.format(leaderboard_cnt, target_leaderboard_cnt)).text
                            leaderboard_cnt += 1
                            
                            year_list.append(year)

                        except:
                            break
                    
                    driver.back()

                except:
                    break
            
            year_result = Counter(year_list)
            print(year_result)

            total_list.append((field_name, small_field_name, year_result))
        
        except:
            break

        driver.back()
    driver.close()

year_sort_dic = {}

for item_result in total_list:
    years = item_result[2]

    for year in years:
        year_sort_dic[year] = []

for item_result in total_list:
    big_name = item_result[0]
    small_name = item_result[1]
    years = item_result[2]

    for year in years:
        year_sort_dic[year].append((big_name, small_name, years[year]))

for year in list(year_sort_dic.keys()):
    year_sort_dic[year].sort(key = lambda object : object[2], reverse = True)

f = open("./result.txt", 'w')

for year in sorted(list(year_sort_dic.keys()), reverse = True):
    f.write('## ' + year + '\n\n')
    
    Task_buffeer = []

    Task = []
    Field = []
    num_paper = []

    for i in range(len(year_sort_dic[year])):
        if year_sort_dic[year][i][1] not in Task_buffeer:
            Task_buffeer.append(year_sort_dic[year][i][1])
            Task.append("[{}](https://paperswithcode.com/task/{})".format(year_sort_dic[year][i][1], year_sort_dic[year][i][1].lower().replace(' ', '-')))
            Field.append(year_sort_dic[year][i][0])
            num_paper.append(year_sort_dic[year][i][2])

    raw_data = {'Task': Task,
                'Field': Field,
                'Number of Papers': num_paper,
                }

    data = DataFrame(raw_data)
    new_buffer = data.to_markdown()

    f.write(new_buffer + '\n\n')
f.close()
