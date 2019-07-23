from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException

import time
import datetime
import sys

def log_on():
    # Block images (we don't need them), open Chrome and navigate to site
    chrome_options=webdriver.ChromeOptions()
    prefs={"profile.managed_default_content_settings.images":2}
    chrome_options.add_experimental_option("prefs", prefs)
    browser=webdriver.Chrome('/Users/blumski/Desktop/PYNANCE/chromedriver', chrome_options=chrome_options)
    browser.get('https://auth.tdameritrade.com/auth?response_type=code&client_id=MOBI%40AMER.OAUTHAP&redirect_uri=https%3A%2F%2Fsecure.tdameritrade.com%2FauthCafe&cv=production')

    # Login
    login=browser.find_element_by_name('su_username')
    login.send_keys('USERNAME')
    time.sleep(1)
    pword=browser.find_element_by_name('su_password')
    pword.send_keys('PASSWORD')
    submit_button=browser.find_element_by_name('authorize')
    submit_button.click()

    # You may have to answer some security questions after a successful login
    try:
        question=browser.find_element_by_id('ctl00_body_lblQuestion').text
        answer=browser.find_element_by_name('ctl00$body$txtAnswer')
        if question == 'What was the make and model of your first car?':
            answer.send_keys('ANSWER')
        elif question == 'What was the name of your favorite school teacher?':
            answer.send_keys('ANSWER')
        elif question == 'What was your dream job as a child?':
            answer.send_keys('ANSWER')
        elif question == 'What was your favorite TV show as a child?':
            answer.send_keys('ANSWER')    
        elif question == 'What was the name of your best childhood friend?':
            answer.send_keys('ANSWER')    
        elif question == 'What street did you grow up on?':
            answer.send_keys('ANSWER')
        elif question == 'In what city does your father live?':
            answer.send_keys('ANSWER')    
        time.sleep(2)
        browser.find_element_by_name('ctl00$body$btnContinue').send_keys(Keys.RETURN)
    except:
        pass
        
    return browser    

def log_off():
    # Close up shop     
    browser.switch_to.default_content()
    logoff=browser.find_element_by_link_text('Log Off')
    logoff.click()        
    browser.close()
    browser.quit()    

# Used to keep track of runtime
start=datetime.datetime.now()

browser=log_on()

# Our output file (append to it)
csv=open('scottrade.csv', 'a')
#csv.write("ticker,price,expiration,strike,bid,ask,net profit,positive net profit\n")

#tickers
with open("tickers.txt") as f:
    content=f.readlines()
tickers=[x.strip() for x in content]

# start list at ticker entered on command line, if any
if len(sys.argv) == 2:
    tickers=tickers[tickers.index(str(sys.argv[1])):]
    # Our output file (append to it)
    csv=open('scottrade.csv', 'a')
else:
    csv=open('scottrade.csv', 'w')
    csv.write("ticker,price,expiration,strike,bid,ask,net profit,positive net profit\n")
    
# Get the data for each ticker, calculate net profit and write it to our output file
ticker_count = 0
for ticker in tickers:
    num_tries = 0
    ticker_count += 1
    if ticker_count % 100 == 0:
        log_off()
        browser=log_on()
    
    try:
        browser.get('https://trading.scottrade.com/quotesresearch/ScottradeResearch.aspx?symbol=' + ticker)
        frame=browser.find_element_by_tag_name('iframe')
        browser.switch_to.frame(frame)
        options=browser.find_element_by_link_text('Options')
        options.click()
    except:
        time.sleep(90)
        browser.refresh()
        continue
        
    while True:
        try:
            frame=browser.find_element_by_tag_name('iframe')
            browser.switch_to.frame(frame)
            select = Select(browser.find_element_by_id('strike-count'))
            select.select_by_value('0')
            time.sleep(2)
        except:
            pass
        try:
            trs=browser.find_elements_by_class_name('option-row')
            price=browser.find_element_by_class_name('underlying-last-price-row').find_element_by_class_name('bold')
            for tr in trs:
                data=tr.get_attribute('data-details-call')
                parts=data.split(",")
                pr=0
                strike=0
                ask=0
                for p in parts:               
                    key_value=p.split(":")
                    if key_value[0].replace('"', "") == "Name":
                        names=key_value[1].replace('"', "").split(" ")
                        csv.write(names[0] + ",")
                        csv.write(price.text + ",")
                        pr=float(price.text)
                        csv.write(names[1] + " " + names[2] + " " + names[3] + ",")
                        if names[4][0].isalpha():
                            strike=float(names[5])
                            csv.write(names[5] + ",")
                        else:    
                            strike=float(names[4])
                            csv.write(names[4] + ",")
                    elif key_value[0].replace('"', "") == "Bid":
                        csv.write(key_value[1].replace('"', "") + ",")
                    elif key_value[0].replace('"', "") == "Ask":
                        csv.write(key_value[1].replace('"', "") + ",")
                        ask=float(key_value[1].replace('"', ""))
                net_profit = pr - strike - ask
                if net_profit > 0:
                    csv.write(" " + "," + str(net_profit) + ",")
                else:                
                    csv.write(str(net_profit) + "," + " " + ",")        
                csv.write('\n')
            break
        except:
            # a possible exception is a 503 (overloaded server) error that might eventually
            # recover with a refresh. Another possibility is an invalid ticker, in which case
            # we should just move on to the next ticker in the list.
            try:
                need_to_break = False
                divs=browser.find_elements_by_tag_name('div')
                for div in divs:
                    if 'Available' in div.text or 'available' in div.text or 'does not have options' in div.text:
                        need_to_break = True
                        break
                if need_to_break:
                    break                
            except:            
                time.sleep(90)
                browser.refresh()
                continue # try refreshing the screen and continuing with while-loop
     
log_off()
csv.close()

# How long did it take for this program to run?
end=datetime.datetime.now()

print end - start

