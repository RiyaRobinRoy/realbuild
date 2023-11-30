from django.shortcuts import render
from tkinter import E
from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.core.files.storage import FileSystemStorage
import webbrowser
from django.contrib.auth import logout
from django.shortcuts import redirect
import mysql.connector as MySQLdb

# database connection
db = MySQLdb.connect(
    host='localhost',
    user='root',
    password='',
    database='realbuild')
c = db.cursor()

# Create your views here.
def index(request):
    return render(request,'index.html')

# Login_Form
def loginpg(request):
    msg = ""
    if(request.POST):
        email = request.POST.get("txtEmail")
        pwd = request.POST.get("txtPassword")
        s = "select count(*) from tbllogin where username='"+email+"'"
        c.execute(s)
        i = c.fetchone()
        if(i[0] > 0):
            s = "select * from tbllogin where username='"+email+"'"
            c.execute(s)
            i = c.fetchone()
            if(i[1] == pwd):
                request.session['email'] = email
                if(i[3] == "1"):
                    if(i[2] == "admin"):
                        return HttpResponseRedirect("/adminhome")
                    elif(i[2] == "contractor"):
                        return HttpResponseRedirect("/contractorhome")
                    elif(i[2] == "customer"):
                        return HttpResponseRedirect("/customerhome")
                else:
                    msg = "You are not authenticated to login"
            else:
                msg = "Incorrect password"
        else:
            msg = "User doesnt exist"
    return render(request, "loginpg.html", {"msg": msg})

def logout_view(request):
    logout(request)
    return redirect('index')

# ADMIN
def adminhome(request):
    return render(request,"adminhome.html")

def admincontractors(request):
    s = "select * from tblcontractor where cEmail in(select username from tbllogin where status='0')"
    c.execute(s)
    data = c.fetchall()
    print("*"*300)
    print(data)
    print("*"*300)
    s = "select * from tblcontractor where cEmail in(select username from tbllogin where status='1')"
    c.execute(s)
    data1 = c.fetchall()
    return render(request,"admincontractor.html",{"data": data,"data1": data1})

def admincustomers(request):
    s = "select * from tblcustomer where cEmail in(select username from tbllogin where status='1')"
    c.execute(s)
    data = c.fetchall()
    print("*"*300)
    print(data)
    print("*"*300)
    return render(request,"admincustomers.html",{"data": data})

def adminapproveuser(request):
    email = request.GET.get("id")
    status = request.GET.get("status")
    url = request.GET.get("url")
    if status == '1':
        s = "update tbllogin set status='"+status+"' where username='"+email+"'"
        c.execute(s)
        db.commit()
        c.execute("select utype from tbllogin where username='"+email+"'")
        k = c.fetchone()

        if(k[0] == 'contractor'):
            n = "Select cContact from tblcontractor where cEmail='"+email+"'"
            c.execute(n)
            d = c.fetchone()
            contact = d[0]
            msg = "Your registeration is approved"

        if(k[0] == 'customer'):
            n = "Select cContact from tblcustomer where cEmail='"+email+"'"
            c.execute(n)
            d = c.fetchone()
            contact = d[0]
            msg = "Your registeration is approved"
    elif status == '-1':
        # Delete user
        s = "delete from tbllogin where username='" + email + "'"
        c.execute(s)
        s = "delete from tblcontractor where cEmail='" + email + "'"
        c.execute(s)
        db.commit()

        # Optionally, you can add more cleanup or confirmation logic here

        msg = "User deleted successfully"

    return HttpResponseRedirect(url)

def viewfeedback(request):

    data = ""
    c.execute("select feedback.*,tblcustomer.* from feedback join tblcustomer on feedback.uid=tblcustomer.cEmail")
    data = c.fetchall()
    print(data)
    return render(request, "adminviewfeedback.html", {"data": data})

# CUSTOMER

# Customer Registration Form
def customerreg(request):
    msg = ""
    if(request.POST):
        name = request.POST.get("txtName")
        address = request.POST.get("txtAddress")
        contact = request.POST.get("txtContact")
        email = request.POST.get("txtEmail")
        pwd = request.POST.get("txtPassword")
        s = "select count(*) from tbllogin where username='"+str(email)+"'"
        c.execute(s)
        i = c.fetchone()
        if(i[0] > 0):
            msg = "User already registered"
        else:
            s = "insert into tblcustomer(cName,cAddress,cContact,cEmail) values('"+str(
                name)+"','"+str(address)+"','"+str(contact)+"','"+str(email)+"')"
            print(s)
            try:
                c.execute(s)
                db.commit()
            except:
                msg = "Sorry registration error"
            else:
                s = "insert into tbllogin (username,password,utype,status) values('"+str(
                    email)+"','"+str(pwd)+"','customer','1')"
                try:
                    c.execute(s)
                    db.commit()
                except:
                    msg = "Sorry login error"
                else:
                    msg = "Registration successfull"
    return render(request,'customerreg.html',{"msg": msg})

def customerhome(request):
    email = request.session["email"]
    s = "select * from tblcustomer where cEmail='"+email+"'"
    c.execute(s)
    data = c.fetchall()
    if request.POST:
        name = request.POST.get("txtName")
        address = request.POST.get("txtAddress")
        contact = request.POST.get("txtContact")
        email = request.POST.get("txtEmail")
        e = "update tblcustomer set cName='"+str(name)+"',cAddress='"+str(
            address)+"',cContact='"+str(contact)+"' where cEmail='"+str(email)+"'"
        c.execute(e)
        db.commit()
        return HttpResponseRedirect("/customerhome")
    return render(request, "customerhome.html", {"data": data})

def customerreq(request):

    email = request.session["email"]
    msg = ""
    if(request.POST):
        bed = request.POST["txtBed"]
        bath = request.POST["txtBath"]
        attached = request.POST["txtAttached"]
        car = request.POST["txtCar"]
        kitchen = request.POST["txtKitchen"]
        sitout = request.POST["txtSitout"]
        work = request.POST["txtWork"]
        floor = request.POST["txtFloor"]
        sqft = request.POST["txtSqft"]
        other = request.POST["txtOther"]
        s = "insert into tblrequirement(cEmail,bedroom,bathroom,attached,carporch,kitchen,sitout,workarea,floor,sqft,other,reqDate,reqStatus) values('"+email + \
            "','"+bed+"','"+bath+"','"+attached+"','"+car+"','"+kitchen+"','"+sitout+"','" + \
            work+"','"+floor+"','"+sqft+"','"+other + \
            "',(select sysdate()),'requested')"
        try:
            c.execute(s)
            db.commit()
        except:
            msg = "Sorry some error occured"
        else:
            msg = "Requirement submitted"
    s = "Select * from tblrequirement where cEmail='"+email+"' \
          and tblrequirement.reqStatus='requested'"
    c.execute(s)
    data = c.fetchall()

    email = request.session["email"]
    s1 = "Select * from tblrequirement where cEmail='"+email+"' and tblrequirement.reqStatus='uploaded'"
    c.execute(s1)
    data1 = c.fetchall()
    return render(request, 'customerreq.html',{"msg": msg, "data": data, "data1": data1})

def assigncontractor(request):
    msg = ""
    data = ""

    if(request.POST):
        msg = ""
        reqid = request.GET.get('reqid')
        aid = request.POST.get('cid')
        m = "insert into tblallocation(requid,cid,status) values('" +str(reqid)+"','"+str(aid)+"','assigned')"
        c.execute(m)
        db.commit()
        print("assign query", m)

        msg = "Assigned successfuly"
    n = "select * from tblcontractor,tbllogin where tbllogin.status='1' and tblcontractor.cEmail=tbllogin.username "
    c.execute(n)
    data1 = c.fetchall()
    print(data1)
    data = showcontractor()
    return render(request, "assigncontractor.html", {"data": data, "msg": msg, "data1": data1})

def showcontractor():

    data = ""
    c.execute(
        "select * from tblcontractor where cEmail in(select username from tbllogin where status='1')")

    data = c.fetchall()
    return data

def plandetails(request):
    msg = ""
    email = request.session["email"]
    rid = request.GET.get("id")
    # s = "select tblrequirement.reqId,tblcontractor.cName,tblplan.sqft,tblplan.cost,tblplan.planStatus,tblplan.planId,tblplan.plan from tblrequirement,tblplan,tblcontractor where tblcontractor.cEmail=tblplan.cEmail and tblplan.reqId=tblrequirement.reqId and tblplan.reqId='" + \
    #     str(rid)+"' and tblrequirement.cEmail='"+str(email)+"'"
    # c.execute(s)
    # data = c.fetchall()
    s = "SELECT * FROM tblplan WHERE reqId IN (SELECT reqId FROM tblrequirement WHERE cEmail IN(SELECT cEmail FROM tblcustomer WHERE cEmail='"+email+"'))"
    c.execute(s)
    data = c.fetchall()
    s1 = "SELECT * FROM tblcontractor WHERE cEmail IN(SELECT cEmail FROM tblplan where reqId IN(SELECT reqId FROM tblrequirement WHERE cEmail='"+email+"'))"
    c.execute(s1)
    data1 = c.fetchall()
    return render(request,"customerplan.html",{"data":data, "data1":data1})

def payment(request):
    msg = ""
    email=request.session["email"]
    s = "SELECT * FROM tblplan WHERE reqId IN (SELECT reqId FROM tblrequirement WHERE cEmail='"+str(email)+"' AND feesstatus='pending')"
    c.execute(s)
    data = c.fetchall()
    feesstatus = request.GET.get("feesstatus")
    planId = request.GET.get("planId")
    url = request.GET.get("url")
    print("the plan")
    print(planId)
    if(request.POST):
        card = request.POST.get("card")
        exp = request.POST.get("exp")
        cvv = request.POST.get("cvv")
        amt = request.POST.get("amt")
        s = "UPDATE tblplan SET feesstatus='success' WHERE planId='"+str(planId)+"'"    
        msg = "Thank you for paying Rs. '"+str(amt)+"'"
        print(msg)
        c.execute(s)
        db.commit()    
    return HttpResponseRedirect(url)
    # return render(request,"payment.html",{"data":data,"msg":msg})

def editreq(request):
    reqid = request.GET.get("reqid")
    s1 = "Select * from tblrequirement where reqId='"+reqid+"'"
    c.execute(s1)
    data = c.fetchall()
    if request.POST:
        t1 = request.POST.get("t1")
        t2 = request.POST.get("t2")
        t3 = request.POST.get("t3")
        t4 = request.POST.get("t4")
        t5 = request.POST.get("t5")
        t6 = request.POST.get("t6")
        t7 = request.POST.get("t7")
        t8 = request.POST.get("t8")
        t9 = request.POST.get("t9")
        t10 = request.POST.get("t10")
        e = "update tblrequirement set bedroom='"+str(t1)+"',bathroom='"+str(t2)+"',attached='"+str(t3)+"',carporch='"+str(t4)+"',kitchen='"+str(
            t5)+"',sitout='"+str(t6)+"',workarea='"+str(t7)+"',floor='"+str(t8)+"',sqft='"+str(t9)+"',other='"+str(t10)+"'  where reqid='"+str(reqid)+"'"
        c.execute(e)
        db.commit()
        return HttpResponseRedirect("/customerreq")

    return render(request, "editreq.html", {"data": data})

def customerplanapprove(request):

    pid = request.GET.get("id")
    fees = request.GET.get("fees")
    rid = request.GET.get("rid")

    request.session["pid"] = pid
    request.session["fees"] = fees
    request.session["rid"] = rid

    status = request.GET.get("status")
    url = request.GET.get("url")
    rid = request.GET.get("rid")
    s = "update tblplan set planStatus='"+status + \
        "',feesstatus='paid' where planId='"+pid+"'"
    try:
        c.execute(s)
        db.commit()
    except:
        pass
    else:
        if(status == "approved"):
            status1 = "rejected"
        elif(status == "rejected"):
            status1 = "approved"
        s = "update tblplan set planStatus='"+status1 + \
            "' where reqId='"+rid+"' and planId<>'"+pid+"'"
        try:
            c.execute(s)
            db.commit()
        except:
            pass
        else:
            if(status == "approved"):
                status = "plan approved"
                s = "update tblrequirement set reqStatus='"+status+"' where reqId='"+rid+"'"
                try:
                    c.execute(s)
                    db.commit()
                    url = 'first'
                except:
                    pass
                else:
                    url = 'first'
                    return HttpResponseRedirect("/"+url+"?id="+pid)

            else:
                return HttpResponseRedirect("/"+url)

def feedback(request):
    msg = ""
    uid = request.session['email']
    if(request.POST):
        msg = ""

        desc = request.POST.get('feed')
        m = "INSERT INTO `feedback`(`feedback`,`uid`)VALUES('" +str(desc)+"','"+str(uid)+"')"
        c.execute(m)
        db.commit()
        print(m)
        msg = "Message Added"

    return render(request, "customerfeedback.html", {"msg": msg})

#   CONTRACTOR

# Contractor Registration Form
def contractorreg(request):
    msg = ""
    if(request.POST):
        name = request.POST.get("txtName")
        address = request.POST.get("txtAddress")
        contact = request.POST.get("txtContact")
        email = request.POST.get("txtEmail")
        pwd = request.POST.get("txtPassword")

        img = request.FILES["txtFile"]
        fs = FileSystemStorage()
        filename = fs.save(img.name, img)
        uploaded_file_url = fs.url(filename)

        s = "select count(*) from tbllogin where username='"+str(email)+"'"
        c.execute(s)
        i = c.fetchone()
        if(i[0] > 0):
            msg = "User already registered"
        else:
            s = "insert into tblcontractor(cName,cAddress,cContact,cEmail,cPhoto) values('"+str(name)+"','"+str(
                address)+"','"+str(contact)+"','"+str(email)+"','"+str(uploaded_file_url)+"')"
            try:
                c.execute(s)
                db.commit()
            except:
                msg = "Sorry registration error"
            else:
                s = "insert into tbllogin (username,password,utype,status) values('"+str(
                    email)+"','"+str(pwd)+"','contractor','0')"
                try:
                    c.execute(s)
                    db.commit()
                except:
                    msg = "Sorry login error"
                else:
                    msg = "Registration successfull"
    return render(request,'contractorreg.html',{"msg": msg})

# Contractor Home
def contractorhome(request):
    email = request.session["email"]
    s = "select * from tblcontractor where cEmail='"+email+"'"
    c.execute(s)
    data = c.fetchall()
    return render(request,'contractorhome.html',{"data":data})

def contractorplan(request):
    email=request.session["email"]
    fee = request.GET.get("feesstatus")
    msg=""
    s= "select tblrequirement.*,tblcustomer.cName from tblcustomer,tblrequirement,tblallocation,tblcontractor where tblrequirement.cEmail=tblcustomer.cEmail and tblallocation.status='assigned' and tblallocation.cid='"+email+"' and tblallocation.cid=tblcontractor.cEmail and tblallocation.requid=tblrequirement.reqId and tblrequirement.reqStatus='requested'"
    c.execute(s)
    data1 = c.fetchall()
    a = "SELECT tblrequirement.*, tblcustomer.cName FROM tblcustomer, tblrequirement, tblplan, tblcontractor WHERE tblrequirement.cEmail = tblcustomer.cEmail  AND tblplan.feesstatus = 'pending'  AND tblplan.cEmail = '"+email+"'  AND tblplan.cEmail = tblcontractor.cEmail  AND tblplan.reqId = tblrequirement.reqId  AND tblrequirement.reqStatus = 'uploaded'"
    c.execute(a)
    data2 = c.fetchall()
    b = "SELECT tblrequirement.*, tblcustomer.cName FROM tblcustomer, tblrequirement, tblplan, tblcontractor WHERE tblrequirement.cEmail = tblcustomer.cEmail  AND tblplan.feesstatus = 'completed'  AND tblplan.cEmail = '"+email+"'  AND tblplan.cEmail = tblcontractor.cEmail  AND tblplan.reqId = tblrequirement.reqId  AND tblrequirement.reqStatus = 'uploaded'"
    c.execute(b)
    data3 = c.fetchall()
    return render(request,'contractorplan.html',{ "msg": msg, "data1": data1,"data2":data2,"data3":data3})

def contractoraddplan(request):

    msg = ""
    email = request.session["email"]
    rid = request.GET.get("id")
    e = "SELECT * from tblcustomer where cEmail in (SELECT cEmail from tblrequirement where reqId='"+rid+"')"
    c.execute(e)
    data = c.fetchall()
    if(request.POST):
        img = request.FILES["txtFile"]
        fs = FileSystemStorage()
        filename = fs.save(img.name, img)
        uploaded_file_url = fs.url(filename)
        sqft = request.POST["txtSqft"]
        cost = request.POST["txtCost"]
        fees = int(sqft)*2
        s = "insert into tblplan (cEmail,reqId,plan,sqft,cost,planStatus,fees,feesstatus) values('"+email +"','"+rid+"','"+uploaded_file_url+"','"+sqft +"', \
            '"+cost+"','submitted','"+str(fees)+"','pending')"
        try:
            c.execute(s)
            db.commit()
        except:
            msg = "Sorry some error occured"
        else:
            s = "update tblrequirement set reqStatus='uploaded' where reqId='"+rid+"'"
            try:
                c.execute(s)
                db.commit()
            except:
                msg = "Sorry error"
            else:
                msg = "Plan added"
    return render(request, "contractoraddplan.html", {"msg": msg,"data":data})
