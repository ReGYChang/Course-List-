from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup as bs
import tkinter as tk
import tkinter.messagebox
import sqlite3

    
def class_selected(): 
    global WeekTemp    
    global HourTemp

    conn = sqlite3.connect('FinalprojectDB_python.db ')
    c = conn.cursor()
    c.execute("INSERT INTO class_info (CourseNo,CourseTittle,CourseCredits,CourseTime) \
                  VALUES ({}, '{}', {}, '{}')".format(CourseNo,CourseTittle,CourseCredits,CourseTime))
    conn.commit()
    conn.close()
    print("加入database")

    view()


def week_time(Timetemp):
    if(Timetemp[0] == 'Mon'):
        Timetemp[0] = '1'
    if(Timetemp[0] == 'Tue'):
        Timetemp[0] = '2'
    if(Timetemp[0] == 'Wed'):
        Timetemp[0] = '3'
    if(Timetemp[0] == 'Thu'):
        Timetemp[0] = '4'
    if(Timetemp[0] == 'Fri'):
        Timetemp[0] = '5'
    temp = Timetemp[0]
    return temp


def message(arg):
    global mes
    global CourseNo
    global CourseTittle
    global CourseCredits
    global CourseTime
    global WeekTemp
    global HourTemp

    if(arg == 1):
        WeekTemp = week_time(CourseTime.split())
        HourTemp = CourseTime.split()[1]
        print(CourseTittle+CourseTime)
        print(WeekTemp)
        mes.set('課程:'+ CourseNo + CourseTittle +'\n學分數:'+ CourseCredits+'\n時段:'+ CourseTime)
        a = '要將下列課程加選嗎?\n' + mes.get() + ':10~'+str(int(HourTemp)+int(CourseCredits))+':00'
        if (tk.messagebox.askquestion(title='message',message=a) == 'yes'):
            print('gggggg')
            class_selected()
    else:
        tk.messagebox.showwarning(title='錯誤',message='沒這門課!!!')


def search():
    global num
    global CourseNo
    global CourseTittle
    global CourseCredits
    global CourseTime
    driver = webdriver.Chrome('C:/Users/User/Desktop/chromedriver.exe')
    driver.get('https://www.is.cgu.edu.tw/portal/DesktopDefault.aspx?tabindex=1&tabid=61')
    search  = driver.find_element_by_id('_ctl1_courseID')
    search.send_keys(num.get())
    search.send_keys(Keys.RETURN)  
    sp = bs(driver.page_source, 'lxml')
    test = sp.select('#_ctl2_message')
    
    if(test[0].text == "沒有符合查詢規則的課程, 請修改規則後重新查詢."):
        driver.close()
        message(0)        
    else:
        table = sp.select('#_ctl2_myGrid')
        tr = table[0].select("tr")
        td = tr[1].select("td")
        CourseNo = td[2].text.replace("\r\n","").replace("\n","")
        CourseTittle = td[5].text[1:].replace("\n\xa0 \n\xa0 \n\n","").split()[0]
        CourseCredits = td[7].text.replace('\n\xa0\n',"").replace('\n',"")
        CourseTime = td[8].text.split(':')[0].replace('\n',"")
        driver.close()          
        message(1)   
    

def delete_DB():
    
    conn = sqlite3.connect('FinalprojectDB_python.db ')

    c = conn.cursor()

    c.execute("DELETE *from class_info ")

    conn.commit()
    conn.close()

def init_classsheet():
    conn = sqlite3.connect('FinalprojectDB_python.db ')

    c = conn.cursor()

    init_class_info = c.execute("SELECT *from class_info ")

    for each_class in init_class_info:
        week_local = week_time(each_class[3].split())
        hour_local = each_class[3].split()[1]
        if int(hour_local) <12 :
            if each_class[2]=='3':
                list1[int(week_local)-1][int(hour_local)-8].set(list1[int(week_local)-1][int(hour_local)-8].get()+CourseNo+' '+CourseTittle+' '+CourseCredits+'\n')
                list1[int(week_local)-1][int(hour_local)-7].set(list1[int(week_local)-1][int(hour_local)-7].get()+CourseNo+' '+CourseTittle+' '+CourseCredits+'\n')
                list1[int(week_local)-1][int(hour_local)-6].set(list1[int(week_local)-1][int(hour_local)-6].get()+CourseNo+' '+CourseTittle+' '+CourseCredits+'\n')

            else:
                list1[int(week_local)-1][int(hour_local)-8].set(list1[int(week_local)-1][int(hour_local)-8].get()+CourseNo+' '+CourseTittle+' '+CourseCredits+'\n')
                list1[int(week_local)-1][int(hour_local)-7].set(list1[int(week_local)-1][int(hour_local)-7].get()+CourseNo+' '+CourseTittle+' '+CourseCredits+'\n')
        else:
            if CourseCredits=='3':
                list1[int(week_local)-1][int(hour_local)-9].set(list1[int(week_local)-1][int(hour_local)-9].get()+CourseNo+' '+CourseTittle+' '+CourseCredits+'\n')
                list1[int(week_local)-1][int(hour_local)-8].set(list1[int(week_local)-1][int(hour_local)-8].get()+CourseNo+' '+CourseTittle+' '+CourseCredits+'\n')
                list1[int(week_local)-1][int(hour_local)-7].set(list1[int(week_local)-1][int(hour_local)-7].get()+CourseNo+' '+CourseTittle+' '+CourseCredits+'\n')
            else:
                list1[int(week_local)-1][int(hour_local)-9].set(list1[int(week_local)-1][int(hour_local)-9].get()+CourseNo+' '+CourseTittle+' '+CourseCredits+'\n')
                list1[int(week_local)-1][int(hour_local)-8].set(list1[int(week_local)-1][int(hour_local)-8].get()+CourseNo+' '+CourseTittle+' '+CourseCredits+'\n')

    conn.close()

def view():
    global list1
    global CourseNo
    global CourseTittle
    global CourseCredits
    global CourseTime
    global WeekTemp
    global HourTemp
    print(CourseNo+CourseTittle)
    print(CourseCredits)
    print(CourseTime)
    print(WeekTemp)
    print(HourTemp)

    if int(HourTemp) <12 :
        if CourseCredits=='3':
            list1[int(WeekTemp)-1][int(HourTemp)-8].set(list1[int(WeekTemp)-1][int(HourTemp)-8].get()+CourseNo+' '+CourseTittle+' '+CourseCredits+'\n')
            list1[int(WeekTemp)-1][int(HourTemp)-7].set(list1[int(WeekTemp)-1][int(HourTemp)-7].get()+CourseNo+' '+CourseTittle+' '+CourseCredits+'\n')
            list1[int(WeekTemp)-1][int(HourTemp)-6].set(list1[int(WeekTemp)-1][int(HourTemp)-6].get()+CourseNo+' '+CourseTittle+' '+CourseCredits+'\n')

        else:
            list1[int(WeekTemp)-1][int(HourTemp)-8].set(list1[int(WeekTemp)-1][int(HourTemp)-8].get()+CourseNo+' '+CourseTittle+' '+CourseCredits+'\n')
            list1[int(WeekTemp)-1][int(HourTemp)-7].set(list1[int(WeekTemp)-1][int(HourTemp)-7].get()+CourseNo+' '+CourseTittle+' '+CourseCredits+'\n')
    else:
        if CourseCredits=='3':
            list1[int(WeekTemp)-1][int(HourTemp)-9].set(list1[int(WeekTemp)-1][int(HourTemp)-9].get()+CourseNo+' '+CourseTittle+' '+CourseCredits+'\n')
            list1[int(WeekTemp)-1][int(HourTemp)-8].set(list1[int(WeekTemp)-1][int(HourTemp)-8].get()+CourseNo+' '+CourseTittle+' '+CourseCredits+'\n')
            list1[int(WeekTemp)-1][int(HourTemp)-7].set(list1[int(WeekTemp)-1][int(HourTemp)-7].get()+CourseNo+' '+CourseTittle+' '+CourseCredits+'\n')
        else:
            list1[int(WeekTemp)-1][int(HourTemp)-9].set(list1[int(WeekTemp)-1][int(HourTemp)-9].get()+CourseNo+' '+CourseTittle+' '+CourseCredits+'\n')
            list1[int(WeekTemp)-1][int(HourTemp)-8].set(list1[int(WeekTemp)-1][int(HourTemp)-8].get()+CourseNo+' '+CourseTittle+' '+CourseCredits+'\n')

    CourseNo=""
    CourseTittle=""
    CourseCredits=""
    CourseTime=""
    WeekTemp=""
    HourTemp=""


    
    
win = tk.Tk()
win.geometry("1000x740")
win.title("預選課表")
Timetemp = ''
num = tk.StringVar()
mes = tk.StringVar()

bt11=tk.StringVar()
bt12=tk.StringVar()
bt13=tk.StringVar()
bt14=tk.StringVar()
bt15=tk.StringVar()
bt16=tk.StringVar()
bt17=tk.StringVar()
bt18=tk.StringVar()
bt19=tk.StringVar()
bt110=tk.StringVar()
bt111=tk.StringVar()
bt112=tk.StringVar()

bt21=tk.StringVar()
bt22=tk.StringVar()
bt23=tk.StringVar()
bt24=tk.StringVar()
bt25=tk.StringVar()
bt26=tk.StringVar()
bt27=tk.StringVar()
bt28=tk.StringVar()
bt29=tk.StringVar()
bt210=tk.StringVar()
bt211=tk.StringVar()
bt212=tk.StringVar()

bt31=tk.StringVar()
bt32=tk.StringVar()
bt33=tk.StringVar()
bt34=tk.StringVar()
bt35=tk.StringVar()
bt36=tk.StringVar()
bt37=tk.StringVar()
bt38=tk.StringVar()
bt39=tk.StringVar()
bt310=tk.StringVar()
bt311=tk.StringVar()
bt312=tk.StringVar()

bt41=tk.StringVar()
bt42=tk.StringVar()
bt43=tk.StringVar()
bt44=tk.StringVar()
bt45=tk.StringVar()
bt46=tk.StringVar()
bt47=tk.StringVar()
bt48=tk.StringVar()
bt49=tk.StringVar()
bt410=tk.StringVar()
bt411=tk.StringVar()
bt412=tk.StringVar()

bt51=tk.StringVar()
bt52=tk.StringVar()
bt53=tk.StringVar()
bt54=tk.StringVar()
bt55=tk.StringVar()
bt56=tk.StringVar()
bt57=tk.StringVar()
bt58=tk.StringVar()
bt59=tk.StringVar()
bt510=tk.StringVar()
bt511=tk.StringVar()
bt512=tk.StringVar()

list1=[[bt11,bt12,bt13,bt14,bt15,bt16,bt17,bt18,bt19,bt110,bt111,bt112],
       [bt21,bt22,bt23,bt24,bt25,bt26,bt27,bt28,bt29,bt210,bt211,bt212],
       [bt31,bt32,bt33,bt34,bt35,bt36,bt37,bt38,bt39,bt310,bt311,bt312],
       [bt41,bt42,bt43,bt44,bt45,bt46,bt47,bt48,bt49,bt410,bt411,bt412],
       [bt51,bt52,bt53,bt54,bt55,bt56,bt57,bt58,bt59,bt510,bt511,bt512]]

frame1 = tk.Frame(win)
frame1.pack()

label1 = tk.Label(frame1,text="時段\星期",width=10,height=1,font=("Helvetica",15,"bold"),bg="lime green")
label1.grid(row=0, column=0)
label1 = tk.Label(frame1,text="08:10~09:00",width=10,height=2,font=("Helvetica",15,"bold"),bg="lime green")
label1.grid(row=1, column=0)
label1 = tk.Label(frame1,text="09:10~10:00",width=10,height=2,font=("Helvetica",15,"bold"),bg="lime green")
label1.grid(row=2, column=0)
label1 = tk.Label(frame1,text="10:10~11:00",width=10,height=2,font=("Helvetica",15,"bold"),bg="lime green")
label1.grid(row=3, column=0)
label1 = tk.Label(frame1,text="11:10~12:00",width=10,height=2,font=("Helvetica",15,"bold"),bg="lime green")
label1.grid(row=4, column=0)

label1 = tk.Label(frame1,text="星期一",width=13,height=1,font=("Helvetica",14,"bold"),bg="lime green")
label1.grid(row=0, column=1)
label1 = tk.Label(frame1,text="星期二",width=13,height=1,font=("Helvetica",14,"bold"),bg="lime green")
label1.grid(row=0, column=2)
label1 = tk.Label(frame1,text="星期三",width=13,height=1,font=("Helvetica",14,"bold"),bg="lime green")
label1.grid(row=0, column=3)
label1 = tk.Label(frame1,text="星期四",width=13,height=1,font=("Helvetica",14,"bold"),bg="lime green")
label1.grid(row=0, column=4)
label1 = tk.Label(frame1,text="星期五",width=13,height=1,font=("Helvetica",14,"bold"),bg="lime green")
label1.grid(row=0, column=5)


button11 = tk.Button(frame1,textvariable=bt11,width=23,height=3)
button11.grid(column=1,row=1)
button12 = tk.Button(frame1,textvariable=bt12,width=23,height=3)
button12.grid(column=1, row=2)
button13 = tk.Button(frame1,textvariable=bt13, width=23,height=3)
button13.grid(column=1, row=3)
button14 = tk.Button(frame1,textvariable=bt14, width=23,height=3)
button14.grid(column=1, row=4)


button21 = tk.Button(frame1,textvariable=bt21, width=23,height=3)
button21.grid(column=2,row=1)
button22 = tk.Button(frame1,textvariable=bt22, width=23,height=3)
button22.grid(column=2, row=2)
button23 = tk.Button(frame1,textvariable=bt23, width=23,height=3)
button23.grid(column=2, row=3)
button24 = tk.Button(frame1,textvariable=bt24, width=23,height=3)
button24.grid(column=2, row=4)


button31 = tk.Button(frame1,textvariable=bt31, width=23,height=3)
button31.grid(column=3,row=1)
button32 = tk.Button(frame1,textvariable=bt32, width=23,height=3)
button32.grid(column=3, row=2)
button33 = tk.Button(frame1,textvariable=bt33, width=23,height=3)
button33.grid(column=3, row=3)
button34 = tk.Button(frame1,textvariable=bt34, width=23,height=3)
button34.grid(column=3, row=4)


button41 = tk.Button(frame1,textvariable=bt41, width=23,height=3)
button41.grid(column=4,row=1)
button42 = tk.Button(frame1,textvariable=bt42, width=23,height=3)
button42.grid(column=4, row=2)
button43 = tk.Button(frame1,textvariable=bt43, width=23,height=3)
button43.grid(column=4, row=3)
button44 = tk.Button(frame1,textvariable=bt44, width=23,height=3)
button44.grid(column=4, row=4)


button51 = tk.Button(frame1,textvariable=bt51, width=23,height=3)
button51.grid(column=5,row=1)
button52 = tk.Button(frame1,textvariable=bt52, width=23,height=3)
button52.grid(column=5, row=2)
button53 = tk.Button(frame1,textvariable=bt53, width=23,height=3)
button53.grid(column=5, row=3)
button54 = tk.Button(frame1,textvariable=bt54, width=23,height=3)
button54.grid(column=5, row=4)



frame2 = tk.Frame(win)
frame2.pack(pady=3)

label1 = tk.Label(frame2,text="13:10~14:00",width=10,height=2,font=("Helvetica",15,"bold"),bg="lime green")
label1.grid(row=0, column=0)
label1 = tk.Label(frame2,text="14:10~15:00",width=10,height=2,font=("Helvetica",15,"bold"),bg="lime green")
label1.grid(row=1, column=0)
label1 = tk.Label(frame2,text="15:10~16:00",width=10,height=2,font=("Helvetica",15,"bold"),bg="lime green")
label1.grid(row=2, column=0)
label1 = tk.Label(frame2,text="16:10~17:00",width=10,height=2,font=("Helvetica",15,"bold"),bg="lime green")
label1.grid(row=3, column=0)
label1 = tk.Label(frame2,text="17:10~18:00",width=10,height=2,font=("Helvetica",15,"bold"),bg="lime green")
label1.grid(row=4, column=0)
label1 = tk.Label(frame2,text="18:10~19:00",width=10,height=2,font=("Helvetica",15,"bold"),bg="lime green")
label1.grid(row=5, column=0)
label1 = tk.Label(frame2,text="19:10~20:00",width=10,height=2,font=("Helvetica",15,"bold"),bg="lime green")
label1.grid(row=6, column=0)
label1 = tk.Label(frame2,text="20:10~21:00",width=10,height=2,font=("Helvetica",15,"bold"),bg="lime green")
label1.grid(row=7, column=0)

button15 = tk.Button(frame2,textvariable=bt15, width=23,height=3)
button15.grid(column=1, row=0)
button16 = tk.Button(frame2,textvariable=bt16, width=23,height=3)
button16.grid(column=1, row=1)
button17 = tk.Button(frame2,textvariable=bt17, width=23,height=3)
button17.grid(column=1, row=2)
button18 = tk.Button(frame2,textvariable=bt18, width=23,height=3)
button18.grid(column=1, row=3)
button19 = tk.Button(frame2,textvariable=bt19, width=23,height=3)
button19.grid(column=1, row=4)
button110 = tk.Button(frame2,textvariable=bt110, width=23,height=3)
button110.grid(column=1, row=5)
button111 = tk.Button(frame2,textvariable=bt111, width=23,height=3)
button111.grid(column=1, row=6)
button112 = tk.Button(frame2,textvariable=bt112, width=23,height=3)
button112.grid(column=1, row=7)


button25 = tk.Button(frame2,textvariable=bt25, width=23,height=3)
button25.grid(column=2, row=0)
button26 = tk.Button(frame2,textvariable=bt26, width=23,height=3)
button26.grid(column=2, row=1)
button27 = tk.Button(frame2,textvariable=bt27, width=23,height=3)
button27.grid(column=2, row=2)
button28 = tk.Button(frame2,textvariable=bt28, width=23,height=3)
button28.grid(column=2, row=3)
button29 = tk.Button(frame2,textvariable=bt29, width=23,height=3)
button29.grid(column=2, row=4)
button210 = tk.Button(frame2,textvariable=bt210, width=23,height=3)
button210.grid(column=2, row=5)
button211 = tk.Button(frame2,textvariable=bt211, width=23,height=3)
button211.grid(column=2, row=6)
button212 = tk.Button(frame2,textvariable=bt212, width=23,height=3)
button212.grid(column=2, row=7)


button35 = tk.Button(frame2,textvariable=bt35, width=23,height=3)
button35.grid(column=3, row=0)
button36 = tk.Button(frame2,textvariable=bt36, width=23,height=3)
button36.grid(column=3, row=1)
button37 = tk.Button(frame2,textvariable=bt37, width=23,height=3)
button37.grid(column=3, row=2)
button38 = tk.Button(frame2,textvariable=bt38, width=23,height=3)
button38.grid(column=3, row=3)
button39 = tk.Button(frame2,textvariable=bt39, width=23,height=3)
button39.grid(column=3, row=4)
button310 = tk.Button(frame2,textvariable=bt310, width=23,height=3)
button310.grid(column=3, row=5)
button311 = tk.Button(frame2,textvariable=bt311, width=23,height=3)
button311.grid(column=3, row=6)
button312 = tk.Button(frame2,textvariable=bt312, width=23,height=3)
button312.grid(column=3, row=7)


button45 = tk.Button(frame2,textvariable=bt45, width=23,height=3)
button45.grid(column=4, row=0)
button46 = tk.Button(frame2,textvariable=bt46, width=23,height=3)
button46.grid(column=4, row=1)
button47 = tk.Button(frame2,textvariable=bt47, width=23,height=3)
button47.grid(column=4, row=2)
button48 = tk.Button(frame2,textvariable=bt48, width=23,height=3)
button48.grid(column=4, row=3)
button49 = tk.Button(frame2,textvariable=bt49, width=23,height=3)
button49.grid(column=4, row=4)
button410 = tk.Button(frame2,textvariable=bt410, width=23,height=3)
button410.grid(column=4, row=5)
button411 = tk.Button(frame2,textvariable=bt411, width=23,height=3)
button411.grid(column=4, row=6)
button412 = tk.Button(frame2,textvariable=bt412, width=23,height=3)
button412.grid(column=4, row=7)


button55 = tk.Button(frame2,textvariable=bt55, width=23,height=3)
button55.grid(column=5, row=0)
button56 = tk.Button(frame2,textvariable=bt56, width=23,height=3)
button56.grid(column=5, row=1)
button57 = tk.Button(frame2,textvariable=bt57, width=23,height=3)
button57.grid(column=5, row=2)
button58 = tk.Button(frame2,textvariable=bt58, width=23,height=3)
button58.grid(column=5, row=3)
button59 = tk.Button(frame2,textvariable=bt59, width=23,height=3)
button59.grid(column=5, row=4)
button510 = tk.Button(frame2,textvariable=bt510, width=23,height=3)
button510.grid(column=5, row=5)
button511 = tk.Button(frame2,textvariable=bt511, width=23,height=3)
button511.grid(column=5, row=6)
button512 = tk.Button(frame2,textvariable=bt512, width=23,height=3)
button512.grid(column=5, row=7)


frame3 = tk.Frame(win)
frame3.pack()
label1 = tk.Label(frame3,text="開課序號:")
label1.grid(row=0, column=0)
entry = tk.Entry(frame3, textvariable=num)
entry.grid(row=0, column=1)     
button00 = tk.Button(frame3, text="選擇課程", width=10,height=1,command=search)
button00.grid(row=0, column=2, padx=10)
button000 = tk.Button(frame3, text="清除課表", width=10,height=1,command=view)
button000.grid(row=0, column=3)
#button0000 = tk.Button(frame3, text="清除課表", width=10,height=1,command=view)
#button0000.grid(row=0, column=4, padx=10)
#view()
#label2 = tk.Label(frame3,textvariable=warnning,font="bold",fg="red",width=15)
#label2.grid(row=0, column=4)


win.mainloop()
"""list2 = [[button11,button12,button13,button14,button15,button16,
          button17,button18,button19,button110,button111,button112],
         [button21,button22,button23,button24,button25,button26,
          button27,button28,button29,button210,button211,button212],
         [button31,button32,button33,button34,button35,button36,
          button37,button38,button39,button310,button311,button312],
         [button41,button42,button43,button44,button45,button46,
          button47,button48,button49,button410,button411,button412],
         [button51,button52,button53,button54,button55,button56,
          button57,button58,button59,button510,button511,button512]]"""
#,columnspan=2
# padx=20,


