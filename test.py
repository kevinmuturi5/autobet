from  selenium  import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
import sqlite3
from datetime import datetime
import schedule
import time
import logging

con = sqlite3.connect("db")
c = con.cursor()
logging.basicConfig(filename='app.log', filemode='w', format='%(asctime) - %(name)s - %(levelname)s - %(message)s')
logging.warning('STARTING')
class conn ():
    active = []
    many =[]
    def st(self):
        print('start')
        url ='https://www.sportpesa.co.ke/'
##        options = Options()
##        options.set_headless(True)
##        self.driver = webdriver.Firefox(options=options)
        self.driver = webdriver.Firefox()
        self.driver.get(url)
        print('done')
        self.driver.implicitly_wait(5)
        self.driver.find_element_by_id('username').send_keys("mobileno")
        self.driver.find_element_by_id('password').send_keys("password")
        self.driver.find_element_by_id('password').send_keys(Keys.RETURN)# send enter keys
        self.driver.implicitly_wait(10)
        print("hear")
        self.driver.implicitly_wait(20)
##        self.trans()
##        self.his()
####        self.withd()
    def withdrawal(self,amount):
        self.driver.get("https://www.sportpesa.co.ke/withdraws")
##        self.driver.find_element_by_link_text('withdraw').click()
        self.driver.implicitly_wait(10)
        self.driver.find_element_by_name('amount').click()
        self.driver.find_element_by_name('amount').send_keys(amount)
        self.driver.find_element_by_name('amount').send_keys(Keys.RETURN)
    def transaction(self):
        self.driver.get("https://www.sportpesa.co.ke/transactions")
        self.driver.implicitly_wait(10)
        for i in range(1,16):
            bet_des=self.driver.find_element(By.XPATH, '//div[@class="responsive-table"]/div/div[2]/div['+str(i)+']//div[@class="transaction_description no-shrink ng-binding"]').text
            bet_time =self.driver.find_element(By.XPATH, '//div[@class="responsive-table"]/div/div[2]/div['+str(i)+']//div[@class="transaction_date ng-binding"]').text
            tr_id =self.driver.find_element(By.XPATH, '//div[@class="responsive-table"]/div/div[2]/div['+str(i)+']//div[@class="transaction_id ng-binding"]').text
            amount =self.driver.find_element(By.XPATH, '//div[@class="responsive-table"]/div/div[2]/div['+str(i)+']//div[@class="transaction_amount ng-binding"]').text
            bet_desc = bet_des.split(":")[0]
            tr_id= (tr_id).split(" ")[1]
            print(bet_desc)
            try:
                bet_id = (bet_des).split(":")[1]
            except:
                bet_id=time.time()
            print(tr_id,bet_time,bet_desc,amount,bet_id)
    def history(self):
##        self.driver.find_element(By.XPATH, '//a[@class="bet-history"]').click()
        self.driver.get("https://www.sportpesa.co.ke/bets/history")
        for i in range(1,16):
            self.driver.find_element(By.XPATH, ' //history-bet['+str(i)+']/div').click()
            bet_id=self.driver.find_element(By.XPATH, ' //history-bet['+str(i)+']//div[@class="info"]/span[@class="ng-binding"]').text
            bet_desc=self.driver.find_element(By.XPATH, ' //history-bet['+str(i)+']//div[@class="bet_description no-shrink ng-binding"]').text
            bet_date= self.driver.find_element(By.XPATH, ' //history-bet['+str(i)+']//div[@class="bet_date ng-binding"]').text
            bet_status=self.driver.find_element_by_css_selector('history-bet:nth-of-type('+str(i)+') div.bet_status:nth-child(1)').text
            pos_win=self.driver.find_element(By.XPATH, ' //history-bet['+str(i)+']/div/div[1]/div[6]').text
            bet_amnt=self.driver.find_element(By.XPATH, ' //history-bet['+str(i)+']//div[@class="info"]').text
            self.driver.find_element(By.XPATH, '//history-bet['+str(i)+']/div').click()
            print(bet_status)
            print(bet_amnt)
            bet_amt = (bet_amnt).split(":")[2]
            po_win = (pos_win).split(":")[1]
            bt_id = (bet_id).split(":")[1]

##             bal = (self.driver.find_element_by_id('amount').text).replace("KSH")
            print(bt_id,bet_date,bet_desc,po_win,bet_status,bet_amt)
            self.sv(bt_id,bet_date,bet_desc,po_win,bet_status,bet_amt)

    def sv(self,bt_id,bet_date,bet_desc,po_win,bet_status,bet_amt):
        wo = c.execute('''select bet_time  from his WHERE bet_time =?''', (bet_date,))
        wo = wo.fetchall()
        w = c.execute('''select bet_id from active WHERE bet_id =?''', (bt_id,))
        w = w.fetchall()
##        amount = po_win
##        print("1",wo)
##        c.execute('''INSERT INTO his(ID,bet_time,bet_desc,pos_win,bet_status,bet_amnt)
##                      VALUES(?,?,?,?,?,?)''', (bt_id,bet_date,bet_desc,po_win,bet_status,bet_amt))
##        con.commit()
##        c.execute('''INSERT INTO active(bet_id,bet_amt,amount,bet_desc,bet_date)
##                      VALUES(?,?,?,?,?)''', (bt_id,bet_amt,amount,bet_desc,bet_date))
##        con.commit()
##        wo = c.execute('''select bet_date  from his WHERE bet_date=?''', (bet_date,))
##        wo = wo.fetchall()
##        print(wo)
        if wo == []:
            c.execute('''INSERT INTO his(ID,bet_time,bet_desc,pos_win,bet_status,bet_amnt)
                      VALUES(?,?,?,?,?,?)''', (bt_id,bet_date,bet_desc,po_win,bet_status,bet_amt))
            con.commit()
        elif w == [] and bet_status == 'WON':
            print(po_win,bet_amt)
            po_win = (po_win.replace("KSH","")).replace(",","")
            bet_amt = (bet_amt).replace(",","")
            amount = (int(po_win) - int(bet_amt))*0.3
            print(amount)
            c.execute('''INSERT INTO active(bet_id,bet_amt,amount,bet_desc,bet_date)
                     VALUES(?,?,?,?,?)''', (bt_id,bet_amt,amount,bet_desc,bet_date))
            con.commit()
            logging.info('%s Is being withdrawn ',amount)
##            self.withd(int(amount))

    def main(self):
        self.st()
        schedule.every(1).minute.do(self.his)
        while True:
            try:
                schedule.run_pending()
                time.sleep(1)
            except (IndexError,NoSuchElementException) as a:
                print(a)
                logging.warning('quiting')
                self.driver.quit()
                time.sleep(900)
                self.st()
if  __name__== '__main__':
    new = conn()
    new.main()
