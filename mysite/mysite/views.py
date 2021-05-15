import pyrebase
from django.shortcuts import render,redirect
from django.conf import settings
from django.contrib import auth
import webbrowser
import os
from django.http import HttpResponse
from django.core.files.storage import default_storage
from django.contrib import messages
from django.contrib import auth
from .pdf import hello
from django.core.mail import EmailMessage
from django.shortcuts import render, redirect
from django.shortcuts import render
from django.conf import settings
from django.core.files.storage import default_storage
from django.contrib import messages
import pyrebase
import os
from django.contrib import auth
import webbrowser
from django.http import HttpResponse
import datetime

config = {
    'apiKey': "AIzaSyAzYiKb4LWdoUOLfrolU1u5lGl_nHMrcwA",
    'authDomain': "everything-at-tips.firebaseapp.com",
    'projectId': "everything-at-tips",
    'storageBucket': "everything-at-tips.appspot.com",
    'messagingSenderId': "860365369557",
    'appId': "1:860365369557:web:7930fdb7692e5372e3f25c",
    'measurementId': "G-B7NG6FQGCD",
    'databaseURL': "https://everything-at-tips-default-rtdb.firebaseio.com/",
    "serviceAccount": "everything-at-tips-firebase-adminsdk-rs1es-37598fd06c.json"
}
firebase = pyrebase.initialize_app(config)
authe = firebase.auth()
database = firebase.database()
storage = firebase.storage()

def logout(request):
    auth.logout(request)
    return render(request,"login.html")

def home(request):
    return render(request, "home.html")

def student(request):
    usertype = request.session.get("user")
    uid = request.session.get('uid')
    if usertype == "user":
        print("url")
        url = database.child("StudentDetails").child(uid).child("url").get().val()
        print(url)
        fname = database.child("StudentDetails").child(uid).child("Firstname").get().val()

        year = []
        time = []
        dates = []
        month = []
        events = []
        timestamp = []
        name = []
        eml = str(request.session.get("email"))  # eml from session
        email_from = []
        try:
            data_in_database = database.child("Events").child("Data").get()
            todays_date = str(datetime.date.today())
            current_month = int(todays_date[5:7])
            current_day = int(todays_date[8:10])
            current_year = int(todays_date[0:4])
            count = 0

            for item in reversed(data_in_database.each()):
                if item.val()['Email_Fro'] == eml or eml in item.val()['Email_To']:

                    datetime_object = datetime.datetime.strptime(item.val()['Month'], "%b")
                    MonthOfEvent = datetime_object.month

                    if int(item.val()['Year']) < current_year:
                        database.child("Events").child("Data").child(item.key()).remove()
                        continue
                    elif (int(MonthOfEvent) - current_month) < 0:
                        database.child("Events").child("Data").child(item.key()).remove()
                        continue
                    elif (int(MonthOfEvent) - current_month) == 0:
                        if current_day > int(item.val()['Dates']):
                            database.child("Events").child("Data").child(item.key()).remove()
                            continue
                    stamp = item.val()['Time'] + " " + item.val()['Year'] + "-" + item.val()['Month'] + "-" + \
                            item.val()[
                                'Dates']
                    # print(stamp)
                    year.append(item.val()['Year'])
                    time.append(item.val()['Time'])
                    dates.append(item.val()['Dates'])
                    month.append(item.val()['Month'])
                    events.append(item.val()['Event'])
                    name.append(item.val()['Name'])
                    timestamp.append(stamp)
                    count = count + 1
                    # print(item.val()['Dates'])
                    if count > 1:
                        break

            # print(year[-1],time[-1],dates[-1],month[-1])
            # print(email_from)

            combi = zip(year, time, dates, month, events, timestamp, name)
            combi = list(combi)

            # print(combi)

            def get_key(combilist):
                return datetime.datetime.strptime(combilist[5], '%H:%M %Y-%b-%d')

            # print("Before sorting\n", combi)
            sorted(combi, key=get_key)

            x = sorted(combi, key=get_key)
            newlist = []
            # print(x, "dddddddddd\n")
            for item in x:
                # print(item, "\n")
                item2 = list(item)
                del item2[-2]
                newlist.append(tuple(item2))
                # print(item2, "\n")
                item = item2

            # print(x, "dddddddddddd")

            # print(newlist, "dddddddddddd")
            combi = newlist

        except:
            message = "No upcoming events"
            print(message)
            usertype = request.session.get("user")
            return render(request, "student.html", {"message": message,"usertype": usertype, "url": url, "fname": fname})

        usertype = request.session.get("user")
        return render(request, "student.html", {"combi_lis":combi,"usertype": usertype, "url": url, "fname": fname})

    else:
        return render(request, "student.html", {"usertype": usertype})



def login(request):
     return render(request,"login.html")


def signup(request):
    return render(request, "signup.html")

def semester(request):
    usertype = request.session.get("user")
    return render(request, "semester.html",{"usertype":usertype})

def fileupload(request):
    usertype = request.session.get("user")
    print("hey",usertype)
    if request.method=="POST":
        print("hello")
        sem = request.POST.get("sem")
        request.session['sem']=sem
        print(sem)
    else:
        sem = request.session.get('sem')
        print(sem)

    print(sem)
    subject = database.child("Subject").child(sem).get().val()
    list(subject)
    sublis=subject[1:]
    print(sublis)
    request.session['sublis'] = sublis
    usertype = request.session.get("user")
    return render(request, "fileupload.html",{"sublis":sublis,"usertype":usertype})

def display(request):
    usertype = request.session.get("user")
    return render(request, "display.html",{"usertype":usertype})

def Login(request):
    email = request.POST.get("email")
    password = request.POST.get("password")
    print(email)
    print(password)
    try:
      user = firebase.auth().sign_in_with_email_and_password(email, password)
      print("hey")
      session_id = str(user['localId'])
      request.session['uid'] = str(session_id)
      sem = database.child("StudentDetails").child(str(session_id)).child("Semester").get().val()
      request.session['sem'] = str(sem)
      if email == "eat.project.314@gmail.com":
          request.session['user'] = "admin"
      else:
          request.session['user'] = "user"
      request.session["email"] = email
      usertype = request.session['user']
      print(usertype)
    except:
      message = "Invalid Email-id or password"
      return render(request, "login.html", {"message":message,})

    if usertype == "user":
        print("url")
        url = database.child("StudentDetails").child(session_id).child("url").get().val()
        print(url)
        fname = database.child("StudentDetails").child(session_id).child("Firstname").get().val()
        year = []
        time = []
        dates = []
        month = []
        events = []
        timestamp = []
        name = []
        eml = str(request.session.get("email"))  # eml from session
        email_from = []
        try:
            data_in_database = database.child("Events").child("Data").get()
            todays_date = str(datetime.date.today())
            current_month = int(todays_date[5:7])
            current_day = int(todays_date[8:10])
            current_year = int(todays_date[0:4])
            count = 0

            for item in reversed(data_in_database.each()):
                if item.val()['Email_Fro'] == eml or eml in item.val()['Email_To']:

                    datetime_object = datetime.datetime.strptime(item.val()['Month'], "%b")
                    MonthOfEvent = datetime_object.month

                    if int(item.val()['Year']) < current_year:
                        database.child("Events").child("Data").child(item.key()).remove()
                        continue
                    elif (int(MonthOfEvent) - current_month) < 0:
                        database.child("Events").child("Data").child(item.key()).remove()
                        continue
                    elif (int(MonthOfEvent) - current_month) == 0:
                        if current_day > int(item.val()['Dates']):
                            database.child("Events").child("Data").child(item.key()).remove()
                            continue
                    stamp = item.val()['Time'] + " " + item.val()['Year'] + "-" + item.val()['Month'] + "-" + \
                            item.val()[
                                'Dates']
                    # print(stamp)
                    year.append(item.val()['Year'])
                    time.append(item.val()['Time'])
                    dates.append(item.val()['Dates'])
                    month.append(item.val()['Month'])
                    events.append(item.val()['Event'])
                    name.append(item.val()['Name'])
                    timestamp.append(stamp)
                    count = count + 1
                    # print(item.val()['Dates'])
                    if count > 1:
                        break

            # print(year[-1],time[-1],dates[-1],month[-1])
            # print(email_from)

            combi = zip(year, time, dates, month, events, timestamp, name)
            combi = list(combi)

            # print(combi)

            def get_key(combilist):
                return datetime.datetime.strptime(combilist[5], '%H:%M %Y-%b-%d')

            # print("Before sorting\n", combi)
            sorted(combi, key=get_key)

            x = sorted(combi, key=get_key)
            newlist = []
            # print(x, "dddddddddd\n")
            for item in x:
                # print(item, "\n")
                item2 = list(item)
                del item2[-2]
                newlist.append(tuple(item2))
                # print(item2, "\n")
                item = item2

            # print(x, "dddddddddddd")

            # print(newlist, "dddddddddddd")
            combi = newlist

        except:
            message = "No upcoming events"
            print(message)
            usertype = request.session.get("user")
            return render(request, "student.html",
                          {"message": message, "usertype": usertype, "url": url, "fname": fname})

        usertype = request.session.get("user")
        return render(request, "student.html", {"combi_lis": combi, "usertype": usertype, "url": url, "fname": fname})

        #return render(request, "student.html", {"usertype": usertype, "url": url, "fname": fname})

    return render(request, "student.html",{"usertype":usertype})

def Signup(request):
    fname = request.POST.get("firstname")
    lname = request.POST.get("lastname")
    email = request.POST.get("email")
    password = request.POST.get("password")
    phone = request.POST.get("prn")
    semester = request.POST.get("semester")
    department = request.POST.get("department")
    try:
        user = authe.create_user_with_email_and_password(email,password)
        print(user)
        uid = user['localId']
        # uid = user['localId']
        #idtoken = request.session['uid']
        data = {"Firstname": fname, "Lastname": lname, "Email": email, "PhoneNo": phone, "Semester": semester,
                "Department": department}
        print(uid)
        database.child("StudentDetails").child(uid).set(data)
        print(uid)
    except:


        message = "Please try again later!!"
        return render(request, "signup.html",{'message':message})

    message = "Signup successfull!!"
    return render(request, "login.html", {'message':message})


def Filesupload(request):
    subject = request.POST.get("subject")
    newfilename = request.POST.get("filename")
    file = request.FILES['file']
    i = file.name.rindex(".")
    exten = file.name[i:]
    print(i)
    print(exten)
    newname = newfilename + exten
    file_save = default_storage.save(newname, file)
    ref = storage.child("FILES").child(subject + "/" + newname).put("media/" + newname)
    print(ref)
    delete = default_storage.delete(newname)
    #downloadurl = storage.child(file.name).put(file.name).get_url()
    #data = {"Subject":subject,"Filename":newfilename,"Url":downloadurl}
    #database.child("Files").set(data)

    def function():
        try:
            downloadurl = storage.child("FILES").child(subject).child(newname).get_url(None)
            return downloadurl
        except:
            downloadurl= ""
            return downloadurl

    data = {"Subject":subject,"File":newname,"Url":function()}
    database.child("Files").child(subject).child(newfilename).set(data)
    sub = request.session.get('sublis')
    usertype = request.session.get("user")
    message = "File was uploaded successfully!!"
    return render(request, "fileupload.html",{"sublis":sub,"usertype":usertype,"message":message})

def Disp(request):
    if request.method == "POST":
        sub = request.POST.get("sub")
        request.session['sub'] = sub
        print("sub is ",sub)
    else:
        sub = request.session.get('sub')
        print("sub is ", sub)

    try:
        name = list(database.child("Files").child(sub).shallow().get().val())
        print(name)
    except:
        message = "No files present"
        print(message)
        usertype = request.session.get("user")

        return render(request, "display.html", {"message":message,"usertype":usertype})


    url = []
    for i in name:

        a=database.child("Files").child(sub).child(i).child("File").get().val()
        url.append(a)

    print("aaa",name)
    print("bbbb",url)
    #print(name[0])
   # newname=name[0]
    # url = database.child("Files").child(sub).child(newname).child("File").get().val()
    combilis=zip(name,url)
    request.session["fname"] = name
    request.session["furl"] = url

    request.session["filedownsubj"] = sub
    usertype = request.session.get("user")
    return render(request, "display.html", {'combilis': combilis, 's': sub, 'usertype': usertype})


def Downloadf(request):
    ogname = request.POST.get("ogname")
    n=request.POST.get("name")
    name = request.POST.get("subject")
    #name=name+"/"
    print(ogname)
    combine = "FILES/" + str(name) + "/" + str(ogname)
    print(combine)

    storage.child(combine).download(combine,ogname)
    name = request.session.get("fname")
    url = request.session.get("furl")
    combilis=zip(name,url)

    sub = request.session.get("filedownsubj")
    usertype = request.session.get("user")
    message = "File was downloaded successfully!!"
    return render(request, "display.html", {'combilis': combilis, 's': sub, 'usertype': usertype,'message':message})


def Filedelete(request):
    ogname = request.POST.get("ogname")
    n=request.POST.get("name")
    sname = request.POST.get("subject")

    print(ogname)


    database.child("Files").child(sname).child(n).remove()

    path = "FILES/"+sname+"/"+ogname
    storage.child("FILES/").child(sname + "/").delete(path)
    try:
        name = list(database.child("Files").child(sname).shallow().get().val())
        print(name)
    except:
        message = "No files present"
        print(message)
        usertype = request.session.get("user")

        return render(request, "display.html", {"message": message,"usertype":usertype})

    url = []
    for i in name:
        a = database.child("Files").child(sname).child(i).child("File").get().val()
        url.append(a)

    print("aaa", name)
    print("bbbb", url)
    # print(name[0])
    # newname=name[0]
    # url = database.child("Files").child(sub).child(newname).child("File").get().val()
    combilis = zip(name, url)
    request.session["fname"] = name
    request.session["furl"] = url

    request.session["filedownsubj"] = sname
    usertype=request.session.get("user")
    return render(request, "display.html", {'combilis': combilis, 's': sname,'usertype':usertype})




def internship(request):
    import datetime,re
    sub = []
    dat = []
    link = []
    cont = []
    sr_no = []

    todays_date = str(datetime.date.today())
    expire = int(todays_date[5:7])
    i = int(0)
    data_in_database = database.child("Internship").child("info").get()
    for item in data_in_database.each():
        Date2 = item.val()['Date'][5:13]
        Date2 = "".join(re.split("[^a-zA-Z]*", Date2))
        mailmon = Date2
        datetime_object = datetime.datetime.strptime(mailmon, "%b")
        month = datetime_object.month
        if (expire - month) % 12 > 2:
            database.child("Internship").child("info").child(item.key()).remove()
            continue

        sub.append(item.val()['Subject'])
        dat.append(item.val()['Date'])

        cont.append(item.val()['Content'])
        link.append(item.val()['Url'])
        sr_no.append(i)
        i = i + 1

    combi = zip(sub, dat, cont, link, sr_no)
    usertype = request.session.get("user")

    return render(request, 'Internship.html', {'combi_list': combi,"usertype":usertype})




def eventdisplay(request):
    import datetime,re
    year = []
    time = []
    dates = []
    month = []
    events = []
    timestamp = []
    name = []
    eml = str(request.session.get("email"))  # eml from session
    email_from = []
    try:
        data_in_database = database.child("Events").child("Data").get()
        todays_date = str(datetime.date.today())
        current_month = int(todays_date[5:7])
        current_day = int(todays_date[8:10])
        current_year = int(todays_date[0:4])
        count = 0

        for item in reversed(data_in_database.each()):
            if item.val()['Email_Fro'] == eml or eml in item.val()['Email_To']:

                datetime_object = datetime.datetime.strptime(item.val()['Month'], "%b")
                MonthOfEvent = datetime_object.month

                if int(item.val()['Year']) < current_year:
                    database.child("Events").child("Data").child(item.key()).remove()
                    continue
                elif (int(MonthOfEvent) - current_month) < 0:
                    database.child("Events").child("Data").child(item.key()).remove()
                    continue
                elif (int(MonthOfEvent) - current_month) == 0:
                    if current_day > int(item.val()['Dates']):
                        database.child("Events").child("Data").child(item.key()).remove()
                        continue
                stamp = item.val()['Time'] + " " + item.val()['Year'] + "-" + item.val()['Month'] + "-" + item.val()[
                    'Dates']
                # print(stamp)
                year.append(item.val()['Year'])
                time.append(item.val()['Time'])
                dates.append(item.val()['Dates'])
                month.append(item.val()['Month'])
                events.append(item.val()['Event'])
                name.append(item.val()['Name'])
                timestamp.append(stamp)
                count = count + 1
                # print(item.val()['Dates'])
                #if count > 1:
                #     break
        # print(year[-1],time[-1],dates[-1],month[-1])
        # print(email_from)

        combi = zip(year, time, dates, month, events, timestamp, name)
        combi = list(combi)

        print(combi)

        def get_key(combilist):
            return datetime.datetime.strptime(combilist[5], '%H:%M %Y-%b-%d')

        # print("Before sorting\n", combi)
        sorted(combi, key=get_key)

        x = sorted(combi, key=get_key)
        newlist = []
        # print(x, "dddddddddd\n")
        for item in x:
            # print(item, "\n")
            item2 = list(item)
            del item2[-2]
            newlist.append(tuple(item2))
            # print(item2, "\n")
            item = item2

        # print(x, "dddddddddddd")

        # print(newlist, "dddddddddddd")
        combi = newlist

    except:
        message = "No upcoming events"
        print(message)
        usertype = request.session.get("user")
        return render(request, "eventdisplay.html", {"message": message, "usertype": usertype})

    usertype = request.session.get("user")
    print(usertype)
    return render(request, 'eventdisplay.html', {'combi_list': combi, "usertype": usertype})


def eventmain(request):
    usertype = request.session.get("user")
    return render(request,'eventmain.html',{'usertype':usertype})



def profile(request):

    uid = request.session.get('uid')
    a = database.child("StudentDetails").child(uid).get()
    info = [x.val() for x in a.each()]

    name = info[2]+" "+ info[3]
    phoneno =info[4]
    email =info[1]
    sem =info[5]
    dept =info[0]
    if len(info)==7:
        url=info[6]
    else:
        url="https://i.pinimg.com/originals/65/25/a0/6525a08f1df98a2e3a545fe2ace4be47.jpg"
    #print(url)
    data={
        "name": name,
        "phone": phoneno,
        "email": email,
        "semester":sem,
        "department":dept,
        "url":url
    }
    urldata={
        "url":url
    }
    database.child("StudentDetails").child(uid).update(urldata)

    return render(request,"profile.html",data)


def prof_photo_change(request):
   if request.method=='POST':
        uid = request.session.get('uid')
        photo = request.FILES['photo']
        photo.name=uid
        file_save = default_storage.save(photo.name, photo)
        storage.child("profile_pictures/" + photo.name).put("media/" + photo.name)
        try:
            photourl = storage.child("profile_pictures").child(photo.name).get_url(None)
        except:
            photourl = ""
        urldata={
            "url": photourl
        }
        delete = default_storage.delete(photo.name)
        database.child("StudentDetails").child(uid).update(urldata)
        profile(request)
        a = database.child("StudentDetails").child(uid).get()
        info = [x.val() for x in a.each()]
        name = info[2] + " " + info[3]
        phoneno = info[4]
        email = info[1]
        sem = info[5]
        dept = info[0]
        url = info[6]
        data = {
            "name": name,
            "phone": phoneno,
            "email": email,
            "semester": sem,
            "department": dept,
            "url": url
        }

        return render(request,"profile.html",data)
   else:
        message = "Unable to change profile photo. Try again later!!"
        return render(request,'profile.html',{'message':message}) #error page
   #in case of error, do something

def aschedule(request):
    usertype = request.session.get("user")
    return render(request, "aschedule.html",{"usertype":usertype})
def adminschedule(request):
    import smtplib
    import calendar
    from email.mime.multipart import MIMEMultipart
    from email.mime.base import MIMEBase
    from email.mime.text import MIMEText
    from email.utils import formatdate
    from email import encoders
    import os, datetime
    attendees = []
    COMMASPACE = ', '
    # print("0")
    name = str(request.POST.get('title'))
    date = str(request.POST.get('Meetingtime'))
    event_title = str(request.POST.get('details'))
    semester = str(request.POST.get('sem'))
    userlist = ""
    users = (database.child("StudentDetails").shallow().get().val())
    print(semester)
    if semester != "ALL":
        for x in users:
            user = list((database.child("StudentDetails").child(x).get().val()).items())
            print(user)
            user1 = user[1][1]
            sem_no = user[5][1]
            print(user1 + "  hee" + sem_no)
            if str(sem_no) == semester:
                userlist = userlist + "," + user1
                # userlist=userlist+","+str(item.val()['Semester'])
                attendees.append(user1)
            else:
                continue
    elif semester == "ALL":
        for x in users:
            user = list((database.child("StudentDetails").child(x).get().val()).items())
            print(user)
            user1 = user[1][1]
            sem_no = user[5][1]
            print(user1 + "  hee" + sem_no)
            userlist = userlist + "," + user1
            # userlist=userlist+","+str(item.val()['Semester'])
            attendees.append(user1)

        print(attendees)
        # attendees.append(item.val()['Semester'])

    year = date[0:4]
    month = date[5:7]
    dates = date[8:10]
    time = date[11:16]
    hours = int(date[11:13])
    minutes = int(date[14:])
    if (hours - 6) > 9:
        if minutes > 30 and minutes < 40:
            date = date[0:11] + str((int(date[11:13]) - 5)) + ":" + "0" + str((int(date[14:]) - 30))
        elif minutes >= 40:
            date = date[0:11] + str((int(date[11:13]) - 5)) + ":" + str((int(date[14:]) - 30))
        elif minutes < 30:
            date = date[0:11] + str(int(date[11:13]) - 6) + ":" + str(((int(date[14:]) + 30) % 60))
        else:
            date = date[0:11] + str(int(date[11:13]) - 5) + ":" + str((int(date[14:]) - 30)) + "0"
    # to make sure that hour value after subtracting 30 is twodigit

    elif (hours - 6) == 9:
        if minutes > 30 and minutes < 40:
            date = date[0:11] + str((int(date[11:13]) - 5)) + ":" + "0" + str((int(date[14:]) - 30))
        elif minutes >= 40:
            date = date[0:11] + str((int(date[11:13]) - 5)) + ":" + str((int(date[14:]) - 30))

        elif minutes < 30:
            date = date[0:11] + "0" + str(int(date[11:13]) - 6) + ":" + str(((int(date[14:]) + 30) % 60))
        else:
            date = date[0:11] + str(int(date[11:13]) - 5) + ":" + str((int(date[14:]) - 30)) + "0"

    elif (hours - 6) < 9:
        if minutes > 30 and minutes < 40:
            date = date[0:11] + "0" + str((int(date[11:13]) - 5)) + ":" + "0" + str((int(date[14:]) - 30))
        elif minutes >= 40:
            date = date[0:11] + "0" + str((int(date[11:13]) - 5)) + ":" + str((int(date[14:]) - 30))

        elif minutes < 30:
            date = date[0:11] + "0" + str(int(date[11:13]) - 6) + ":" + str(((int(date[14:]) + 30) % 60))
        else:
            date = date[0:11] + "0" + str(int(date[11:13]) - 5) + ":" + str((int(date[14:]) - 30)) + "0"

    # print ("date after calcu is ",date)

    # date=date[0:11]+str(int(date[11:13]+5))+":"+str(int((date[14:16]+30))
    month_text = calendar.month_abbr[int(month)]
    # print(email_to)
    email_fro = "eat.project.314@gmail.com"
    # contact_vol = 9478523695  # contact volunteer
    ##print("1")
    data = {
        "Name": name,
        "Year": year,
        "Month": month_text,
        "Dates": dates,
        "Time": time,
        "Event": event_title,
        "Email_To": userlist,
        "Email_Fro": email_fro,

    }

    database.child("Events").child("Data").push(data)
    # print("2")
    CRLF = "\r\n"
    login = "eat.project.314@gmail.com"
    password = "eateateat"

    organizer = "ORGANIZER;CN=organiser:mailto:eat.project.314" + CRLF + " @gmail.com"
    fro = "Everything At Tips Project"

    ddtstart = datetime.datetime.now()

    # print(date)
    # dt = "2021-03-31T10:33"
    dt = date + ":00"
    # print(dt)

    dt = dt.replace('-', "")
    # print(dt)
    dt = dt.replace(':', "")
    dt = dt + "Z"
    # print(dt)

    dtstart = dt

    dtend2 = (int(dtstart[9:11]) + 2) % 24
    dtend3 = dtstart[0:9] + str(dtend2) + dtstart[11:]

    dtend = dtend3

    desc = name + "  details/notes:" + event_title
    contact = event_title
    description = "Description: " + desc + CRLF

    dtstamp = datetime.datetime.now().strftime("%Y%m%dT%H%M%SZ")
    # print(dtstamp)
    """dtstart = ddtstart.strftime("%Y%m%dT%H%M%SZ")
    dtend = dtend.strftime("%Y%m%dT%H%M%SZ")"""

    desccription = description + CRLF
    attendee = ""
    Name = name
    # print("3")
    for att in attendees:
        attendee += "ATTENDEE;CUTYPE=INDIVIDUAL;ROLE=REQ-    PARTICIPANT;PARTSTAT=ACCEPTED;RSVP=TRUE" + CRLF + " ;CN=" + att + ";X-NUM-GUESTS=0:" + CRLF + " mailto:" + att + CRLF
    ical = "BEGIN:VCALENDAR" + CRLF + "PRODID:TechKnights" + CRLF + "VERSION:2.0" + CRLF + "CALSCALE:GREGORIAN" + CRLF
    ical += "METHOD:REQUEST" + CRLF + "BEGIN:VEVENT" + CRLF + "DTSTART:" + dtstart + CRLF + "DTEND:" + dtend + CRLF + "DTSTAMP:" + dtstamp + CRLF + organizer + CRLF
    ical += "UID:FIXMEUID" + dtstamp + CRLF
    ical += attendee + "CREATED:" + dtstamp + CRLF + description + "LAST-MODIFIED:" + dtstamp + CRLF + "LOCATION: Kolkata/India" + CRLF + "SEQUENCE:0" + CRLF + "STATUS:CONFIRMED" + CRLF
    ical += "SUMMARY:Event: " + Name + CRLF + "TRANSP:OPAQUE" + CRLF + "END:VEVENT" + CRLF + "END:VCALENDAR" + CRLF
    # print("4")
    eml_body = "This is just a email confirmation that your event   " + name + " has been added to your calender with " + " " + " details/notes " + event_title
    eml_body_bin = "This is the email body in binary - two steps"
    msg = MIMEMultipart('mixed')
    msg['Reply-To'] = fro
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = "Event notification " + name + "on " + date
    msg['From'] = fro
    msg['To'] = ",".join(attendees)

    part_email = MIMEText(eml_body, "html")
    part_cal = MIMEText(ical, 'calendar;method=REQUEST')
    # print("5")
    msgAlternative = MIMEMultipart('alternative')
    msg.attach(msgAlternative)

    ical_atch = MIMEBase('application/ics', ' ;name="%s"' % ("invite.ics"))
    ical_atch.set_payload(ical)
    encoders.encode_base64(ical_atch)
    ical_atch.add_header('Content-Disposition', 'attachment; filename="%s"' % ("invite.ics"))

    eml_atch = MIMEText('', 'plain')
    eml_atch.add_header('Content-Transfer-Encoding', "")

    msgAlternative.attach(part_email)
    msgAlternative.attach(part_cal)

    mailServer = smtplib.SMTP('smtp.gmail.com', 587)
    mailServer.ehlo()
    mailServer.starttls()
    mailServer.ehlo()
    mailServer.login(login, password)
    mailServer.sendmail(fro, attendees, msg.as_string())
    mailServer.close()
    usertype = request.session.get("user")

    return render(request, "aschedule.html",{"usertype":usertype})


def sschedule(request):
    usertype = request.session.get("user")
    return render(request, "sschedule.html",{"usertype":usertype})

def studentschedule(request):
    import smtplib
    import calendar
    from email.mime.multipart import MIMEMultipart
    from email.mime.base import MIMEBase
    from email.mime.text import MIMEText
    from email.utils import formatdate
    from email import encoders
    import os, datetime

    COMMASPACE = ', '
    # print("0")
    name = str(request.POST.get('title'))
    date = str(request.POST.get('Meetingtime'))
    event_title = request.POST.get('details')
    # print(date)
    year = date[0:4]
    month = date[5:7]
    dates = date[8:10]
    time = date[11:16]
    hours = int(date[11:13])
    minutes = int(date[14:])
    if (hours - 6) > 9:
        if minutes > 30 and minutes < 40:
            date = date[0:11] + str((int(date[11:13]) - 5)) + ":" + "0" + str((int(date[14:]) - 30))
        elif minutes >= 40:
            date = date[0:11] + str((int(date[11:13]) - 5)) + ":" + str((int(date[14:]) - 30))
        elif minutes < 30:
            date = date[0:11] + str(int(date[11:13]) - 6) + ":" + str(((int(date[14:]) + 30) % 60))
        else:
            date = date[0:11] + str(int(date[11:13]) - 5) + ":" + str((int(date[14:]) - 30)) + "0"
    # to make sure that hour value after subtracting 30 is twodigit

    elif (hours - 6) == 9:
        if minutes > 30 and minutes < 40:
            date = date[0:11] + str((int(date[11:13]) - 5)) + ":" + "0" + str((int(date[14:]) - 30))
        elif minutes >= 40:
            date = date[0:11] + str((int(date[11:13]) - 5)) + ":" + str((int(date[14:]) - 30))

        elif minutes < 30:
            date = date[0:11] + "0" + str(int(date[11:13]) - 6) + ":" + str(((int(date[14:]) + 30) % 60))
        else:
            date = date[0:11] + str(int(date[11:13]) - 5) + ":" + str((int(date[14:]) - 30)) + "0"

    elif (hours - 6) < 9:
        if minutes > 30 and minutes < 40:
            date = date[0:11] + "0" + str((int(date[11:13]) - 5)) + ":" + "0" + str((int(date[14:]) - 30))
        elif minutes >= 40:
            date = date[0:11] + "0" + str((int(date[11:13]) - 5)) + ":" + str((int(date[14:]) - 30))

        elif minutes < 30:
            date = date[0:11] + "0" + str(int(date[11:13]) - 6) + ":" + str(((int(date[14:]) + 30) % 60))
        else:
            date = date[0:11] + "0" + str(int(date[11:13]) - 5) + ":" + str((int(date[14:]) - 30)) + "0"

    # print ("date after calcu is ",date)

    # date=date[0:11]+str(int(date[11:13]+5))+":"+str(int((date[14:16]+30))
    month_text = calendar.month_abbr[int(month)]
    email_to = str(request.session.get("email"))
    # print(email_to)
    email_fro = "eat.project.314@gmail.com"
    contact_vol = 9478523695  # contact volunteer
    ##print("1")
    data = {
        "Name": name,
        "Year": year,
        "Month": month_text,
        "Dates": dates,
        "Time": time,
        "Event": event_title,
        "Email_To": email_to,
        "Email_Fro": email_fro,

    }

    database.child("Events").child("Data").push(data)
    # print("2")
    CRLF = "\r\n"
    login = "eat.project.314@gmail.com"
    password = "eateateat"
    attendees = [email_to]
    organizer = "ORGANIZER;CN=organiser:mailto:eat.project.314" + CRLF + " @gmail.com"
    fro = "Everything At Tips Project"

    ddtstart = datetime.datetime.now()

    # print(date)
    # dt = "2021-03-31T10:33"
    dt = date + ":00"
    # print(dt)

    dt = dt.replace('-', "")
    # print(dt)
    dt = dt.replace(':', "")
    dt = dt + "Z"
    # print(dt)

    dtstart = dt

    dtend2 = (int(dtstart[9:11]) + 2) % 24
    dtend3 = dtstart[0:9] + str(dtend2) + dtstart[11:]

    dtend = dtend3

    desc = name + "  details/notes:" + event_title
    contact = event_title
    description = "Description: " + desc + CRLF

    dtstamp = datetime.datetime.now().strftime("%Y%m%dT%H%M%SZ")
    # print(dtstamp)
    """dtstart = ddtstart.strftime("%Y%m%dT%H%M%SZ")
    dtend = dtend.strftime("%Y%m%dT%H%M%SZ")"""

    desccription = description + CRLF
    attendee = ""
    Name = name
    # print("3")
    for att in attendees:
        attendee += "ATTENDEE;CUTYPE=INDIVIDUAL;ROLE=REQ-    PARTICIPANT;PARTSTAT=ACCEPTED;RSVP=TRUE" + CRLF + " ;CN=" + att + ";X-NUM-GUESTS=0:" + CRLF + " mailto:" + att + CRLF
    ical = "BEGIN:VCALENDAR" + CRLF + "PRODID:TechKnights" + CRLF + "VERSION:2.0" + CRLF + "CALSCALE:GREGORIAN" + CRLF
    ical += "METHOD:REQUEST" + CRLF + "BEGIN:VEVENT" + CRLF + "DTSTART:" + dtstart + CRLF + "DTEND:" + dtend + CRLF + "DTSTAMP:" + dtstamp + CRLF + organizer + CRLF
    ical += "UID:FIXMEUID" + dtstamp + CRLF
    ical += attendee + "CREATED:" + dtstamp + CRLF + description + "LAST-MODIFIED:" + dtstamp + CRLF + "LOCATION: Kolkata/India" + CRLF + "SEQUENCE:0" + CRLF + "STATUS:CONFIRMED" + CRLF
    ical += "SUMMARY:Event: " + Name + CRLF + "TRANSP:OPAQUE" + CRLF + "END:VEVENT" + CRLF + "END:VCALENDAR" + CRLF
    # print("4")
    eml_body = "This is just a email confirmation that your event   " + name + " has been added to your calender with " + " " + " details/notes " + event_title
    eml_body_bin = "This is the email body in binary - two steps"
    msg = MIMEMultipart('mixed')
    msg['Reply-To'] = fro
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = "Event notification " + name + "on " + date
    msg['From'] = fro
    msg['To'] = ",".join(attendees)

    part_email = MIMEText(eml_body, "html")
    part_cal = MIMEText(ical, 'calendar;method=REQUEST')
    # print("5")
    msgAlternative = MIMEMultipart('alternative')
    msg.attach(msgAlternative)

    ical_atch = MIMEBase('application/ics', ' ;name="%s"' % ("invite.ics"))
    ical_atch.set_payload(ical)
    encoders.encode_base64(ical_atch)
    ical_atch.add_header('Content-Disposition', 'attachment; filename="%s"' % ("invite.ics"))

    eml_atch = MIMEText('', 'plain')
    eml_atch.add_header('Content-Transfer-Encoding', "")

    msgAlternative.attach(part_email)
    msgAlternative.attach(part_cal)

    mailServer = smtplib.SMTP('smtp.gmail.com', 587)
    mailServer.ehlo()
    mailServer.starttls()
    mailServer.ehlo()
    mailServer.login(login, password)
    mailServer.sendmail(fro, attendees, msg.as_string())
    mailServer.close()
    # print("6")
    usertype = request.session.get("user")

    return render(request, "sschedule.html",{"usertype":usertype})


#----------------------------------------------

def sell(request):
    if request.method == 'POST':
        file = request.FILES['file']
        name = request.POST.get("name")
        pname = request.POST.get("pname")
        contact = request.POST.get("contactdet")
        price = request.POST.get("price")
        prodDet = request.POST.get("prodData")
        file_save = default_storage.save(file.name, file)
        storage.child("files/" + file.name).put("media/" + file.name)
        email = (list(database.child("StudentDetails").child(
            request.session['uid']).get().val().items()))[1][1]
        user_id = request.session['uid']
        # print("email:", email)
        try:
            downloadurl = storage.child("files").child(file.name).get_url(None)
        except:
            downloadurl = ""

        # print("gibberish: ", downloadurl)

        data = {"name": name, "pname": pname, "contact": contact,
                "price": price, "prodDet": prodDet, "url": downloadurl, "email": email, "user_id": user_id}
        database.child("prod").push(data)
        delete = default_storage.delete(file.name)
        messages.success(request, "Product has been uploaded successfully!!!")
        return render(request, 'Sell.html', {"x": True})
    return render(request, 'Sell.html', {"x": False})


def retProd(request):
    products = (database.child("prod").shallow().get().val())
    pname, price, ID, url = [], [], [], []
    for x in products:
        prod = list((database.child("prod").child(x).get().val()).items())
        # print(x)
        ID.append(x)
        pname.append(prod[3][1])
        price.append(prod[4][1])
        url.append(prod[6][1])

    # print("url   ", url)
    x = zip(ID, pname, price, url)
    return render(request, 'prodList.html', {'y': x})


def prodDet(request, id):
    if request.method == 'POST':
        id1 = request.POST.get("id")
    else:
        id1 = id
    x = list((database.child("prod").child(str(id1)).get().val()).items())
    contact = x[0][1]
    name = x[2][1]
    pname = x[3][1]
    price = x[4][1]
    det = x[5][1]
    url = x[6][1]
    boo = False
    try:
        prods = database.child("cart").child(request.session['uid']).get()
        for prod in prods.each():
            y = prod.val()
            if y["prodid"] == id1:
                boo = True
    except:
        # print("No prod")
        boo = False
    data = {"c": contact, "n": name, "p": pname,
            "pri": price, "d": det, "u": url, "ID": id1, "boo": boo}
    return render(request, "prodDet.html", data)


def addtocart(request):
    if request.method == 'POST':
        id1 = request.POST.get("id")
        # print(id1)
        data = {"prodid": id1}
        uni_key = database.child("cart").child(
            request.session['uid']).push(data)
        pid = uni_key["name"]
        messages.success(request, "Product has been added to the cart")
        x = list((database.child("prod").child(str(id1)).get().val()).items())
        contact = x[0][1]
        name = x[2][1]
        pname = x[3][1]
        price = x[4][1]
        det = x[5][1]
        url = x[6][1]
        boo = True
        data = {"c": contact, "n": name, "p": pname,
                "pri": price, "d": det, "u": url, "ID": id1, "boo": boo, "pid": pid, "x": True}
        return render(request, "prodDet.html", data)


def cart(request):
    pname, price, ID, url, parentID = [], [], [], [], []

    try:
        val = True
        prods = list(database.child("cart").child(
            request.session['uid']).get().val().items())
        for prod in prods:
            x = (prod[1])["prodid"]
            # print("x", x)
            parentID.append(prod[0])
            prod = list((database.child("prod").child(x).get().val()).items())
            # print("prod", prod)
            ID.append(x)
            # print("prodId"+x)
            pname.append(prod[3][1])
            price.append(prod[4][1])
            url.append(prod[6][1])
        price = [int(x) for x in price]
        x = zip(ID, pname, price, url, parentID)
        return render(request, "cart.html", {"x": x, "count": len(ID), "total": sum(price), "val": val})
    except:
        val = False
        return render(request, "cart.html", {"val": val})


def remprod(request):
    if request.method == "POST":
        pid = request.POST.get("id")
        id1 = request.POST.get("child")
        database.child("cart").child(
            request.session['uid']).child(pid).remove()
        diff = request.POST.get("diff")
        if diff == "rem":
            return redirect(prodDet, id1)
        return redirect("cart")


def sendEmailAttach(request):
    pid = request.POST.get("id")
    # print(pid)
    id1 = list(database.child("cart").child(request.session['uid']).child(
        pid).get().val().items())[0][1]
    # print(id1)
    x = list((database.child("prod").child(str(id1)).get().val()).items())
    contact = x[0][1]
    mail = x[1][1]
    name = x[2][1]
    pname = x[3][1]
    price = x[4][1]
    sid = x[7][1]
    seller = list(database.child("StudentDetails").child(sid).get().val().items())
    customer = list(database.child("StudentDetails").child(
        request.session['uid']).get().val().items())
    # print("Seller", seller)
    # print("Customer", customer)
    hello(contact, mail, name, pname, price, seller, customer, id1)
    html_content = "Attached below is the invoice for the product " + \
        pname + "<br>Price: "+price + "<br>Customer details:<br>" + \
        "Name: "+customer[2][1]+" "+customer[3][1] + \
        "<br>ContactNo: "+customer[4][1]
    email = EmailMessage("EAT - Product invoice", html_content,
                         "eat.project.314@gmail.com", [seller[1][1], customer[1][1]])
    email.content_subtype = "html"
    email.attach_file('C:/pro/mysite/invoice.pdf')
    res = email.send()
    database.child("cart").child(request.session['uid']).child(pid).remove()
    database.child("prod").child(id1).remove()
    return redirect("cart")