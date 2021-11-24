from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium import webdriver


driver = webdriver.Edge ()
driver.get("https://finance.yahoo.com/quote/BTC-EUR/history/")
#assert "Python" in driver.title
try:
    table = driver.find_element(By.ID, "mrt\-node\-Col1\-1\-HistoricalDataTable")
except:
    print >> sys.stderr, "failed on finding table by ID"
    sys.exit(1)
try:
    table = table.find_element(By.TAG_NAME, "tbody")
except:
    print >> sys.stderr, "failed on finding table by TAG_NAME"
    sys.exit(1)

try:
    lines = table.find_elements(By.TAG_NAME, "tr")
except:
    print >> sys.stderr, "failed on finding lines by TAG_NAME"
    sys.exit(1)
#print (len (lines))

file  = open("eur_btc_rates.csv", "w")
line_to_write = ["Date", "BTC Closing Value"]
file.write("Date, BTC Closing Value\n")
for i in range(0,10):
    line_to_write = []
    
    try:
        coluns_from_line = lines[i].find_elements(By.TAG_NAME, "td")
    except:
        print >> sys.stderr, "failed on finding coluns_from_line by TAG_NAME"
        sys.exit(1)
        
    try:
        coluns_from_line_data = lines[i].find_elements(By.TAG_NAME, "span")
    except:
        print >> sys.stderr, "failed on finding coluns_from_line_data by TAG_NAME"
        sys.exit(1)
    
    #this part is needed because a line from the table once showed up withou data (except date) 
    try:
        reactid_date = int (coluns_from_line[0].get_attribute("data-reactid"))+1
    except:
        print >> sys.stderr, "failed on getting reactid_date from data-reactid"
        sys.exit(1)
        
    try:
        reactid_close = int (coluns_from_line[4].get_attribute("data-reactid"))+1
    except:
        print >> sys.stderr, "failed on getting reactid_date from data-reactid"
        sys.exit(1)
        
    for item in coluns_from_line_data:
        if int(item.get_attribute("data-reactid")) == reactid_date or \
            int(item.get_attribute("data-reactid")) == reactid_close:
            line_to_write.append(item.text)
    if (len(coluns_from_line)==1): #no close data from that day
        line_to_write.append("no data")
    file.write (line_to_write[0].replace(",", '') + ", "+ line_to_write[1].replace(",", '') + "\n")
#assert "No results found." not in driver.page_source
driver.close()
file.close()