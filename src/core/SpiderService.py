from selenium import webdriver
from models.entities import Job
from selenium.webdriver.common.by import By
import time
import xlwt


class SpiderService:
    __page_url__ = 'https://search.51job.com/list/180200%252c010000%252c020000%252c030200%252c040000,000000,0000,00,9,99,+,2,{}.html?lang=c&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&ord_field=0&dibiaoid=0&line=&welfare='

    def getPageURL(self, pageIndex: int) -> str:
        return self.__page_url__.format(pageIndex)

    def Crawling(self, pageAmount: int, timeout: int = 15) -> list[Job]:
        driver = webdriver.Chrome()
        allJobList = []
        jobNumber = 0
        page = 1
        driver.get(__first_page_url__)
        while (page < 301):
            time.sleep(timeout)
            onePageJobInfoList = []
            # try:
            print(
                "----------------------------正在爬取第{}页数据--------------------------------".format(page))
            list = driver.find_elements(By.CSS_SELECTOR, '.j_joblist .e')
            for item in list:
                title = item.find_element(By.CSS_SELECTOR, 'a .t span').text
                salary = item.find_element(
                    By.CSS_SELECTOR, 'a > p.info > span.sal').text
                information = item.find_element(
                    By.CSS_SELECTOR, 'a > p.info > span.d.at').text.replace(' ', '').split('|')
                if len(information) == 3:
                    jobPlace = information[0]
                    jobExperience = information[1]
                    education = information[2]
                    company = item.find_element(
                        By.CSS_SELECTOR, 'div.er > a').text
                    jobType = item.find_element(
                        By.CSS_SELECTOR, 'div.er > p.int.at').text
                    print(title, salary, jobPlace, jobExperience,
                          education, company, jobType)
                    onePageJobInfoList.append(
                        [title, salary, jobPlace, jobExperience, education, company, jobType])
                    allJobList.append(
                        [title, salary, jobPlace, jobExperience, education, company, jobType])
                else:
                    continue
            # 将一页数据写入excel
            for row in range(jobNumber, jobNumber+len(onePageJobInfoList)):
                data = allJobList[row]
                for col in range(0, 7):
                    worksheet.write(row + 1, col, data[col])
            jobNumber += len(onePageJobInfoList)
            workbook.save('51job.xls')  # 保存
            print('当前数据量:', jobNumber)
            print(
                "----------------------------第{}页数据保存成功!--------------------------------".format(page))
            driver.find_element(
                By.CSS_SELECTOR, 'div.j_page > div > div > div > ul > li.next > a').click()  # 点击下一页
            page += 1
