from flask import Flask, render_template, Response, redirect, request, session, abort, url_for

import cv2
import shutil
import PIL.Image
from PIL import Image
from datetime import date
import datetime
from flask_mail import Mail, Message
import hashlib
import imagehash
import mysql.connector
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  charset="utf8",
  database="product_bc"

)

#from store import *


app = Flask(__name__)
app.secret_key = 'abcdef'
##email
mail_settings = {
    "MAIL_SERVER": 'smtp.gmail.com',
    "MAIL_PORT": 465,
    "MAIL_USE_TLS": False,
    "MAIL_USE_SSL": True,
    "MAIL_USERNAME": "rnd1024.64@gmail.com",
    "MAIL_PASSWORD": "RnDtrichy2018"
}

app.config.update(mail_settings)
mail = Mail(app)
#######

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    msg=""
    act = request.args.get('act')
    if request.method=='POST':
        uname=request.form['uname']
        pwd=request.form['pass']
        cursor = mydb.cursor()
        cursor.execute('SELECT * FROM pr_manufacture WHERE uname = %s AND pass = %s', (uname, pwd))
        account = cursor.fetchone()
        if account:
            session['username'] = uname
            return redirect(url_for('product'))
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'
    
        
        
    return render_template('index.html',msg=msg,act=act)

@app.route('/login_admin', methods=['GET', 'POST'])
def login_admin():
    msg=""
    act = request.args.get('act')
    if request.method=='POST':
        uname=request.form['uname']
        pwd=request.form['pass']
        cursor = mydb.cursor()
        cursor.execute('SELECT * FROM sc_admin WHERE username = %s AND password = %s', (uname, pwd))
        account = cursor.fetchone()
        if account:
            session['username'] = uname
            return redirect(url_for('admin_home'))
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'
    
        
        
    return render_template('login_admin.html',msg=msg,act=act)

@app.route('/admin_home', methods=['GET', 'POST'])
def admin_home():
    msg=""
    if 'username' in session:
        uname = session['username']
    
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM sc_blockchain")
    data = mycursor.fetchall()
       
    
    return render_template('admin_home.html', data=data)

@app.route('/product', methods=['GET', 'POST'])
def product():
    msg=""
    if 'username' in session:
        uname = session['username']
    
    #mycursor = mydb.cursor()
    #mycursor.execute("SELECT * FROM sc_blockchain")
    #data = mycursor.fetchall()
    cursor = mydb.cursor()
    cursor.execute('SELECT * FROM pr_category')
    catt = cursor.fetchall()
    if request.method=='POST':
        cat=request.form['category']
        prd=request.form['product']
        price=request.form['price']
        description=request.form['description']
        location=request.form['location']
        mdate=request.form['mdate']
        
        
        mycursor = mydb.cursor()
        mycursor.execute("SELECT max(id)+1 FROM pr_product")
        maxid = mycursor.fetchone()[0]
        if maxid is None:
            maxid=1
        
        numStr = str(maxid)
        numStr = numStr.zfill(4)
        now = datetime.datetime.now()
        rdate=now.strftime("%d-%m-%Y")
        my=now.strftime("%y%m")
        pcode=my+numStr

        
        sql = "INSERT INTO pr_product(id,category,product,company,price,description,location,mdate,pcode,rdate) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        val = (maxid,cat,prd,uname,price,description,location,mdate,pcode,rdate)
        cursor.execute(sql, val)
        mydb.commit()            
        print(cursor.rowcount, "Added Success")
        result="sucess"
        ##BC##
        sdata="PID:"+str(maxid)+",Product:"+prd+",Company:"+uname+",Manufacture:"+mdate+",RegDate:"+rdate
        result = hashlib.md5(sdata.encode())
        key=result.hexdigest()

        mycursor1 = mydb.cursor()
        mycursor1.execute("SELECT max(id)+1 FROM pr_blockchain")
        maxid1 = mycursor1.fetchone()[0]
        if maxid1 is None:
            maxid1=1
            pkey="00000000000000000000000000000000"
        else:
            mid=maxid-1
            cursor.execute('SELECT * FROM pr_blockchain where id=%s',(mid, ))
            pp = cursor.fetchone()
            pkey=pp[3]
        sql2 = "INSERT INTO pr_blockchain(id,block_id,pre_hash,hash_value,sdata) VALUES (%s, %s, %s, %s, %s)"
        val2 = (maxid1,maxid,pkey,key,sdata)
        cursor.execute(sql2, val2)
        mydb.commit()   
        ####
        
        if cursor.rowcount==1:
            msg="success"
            return redirect(url_for('man_home',msg=msg))
        else:
            msg="fail"
            return redirect(url_for('man_home',msg=msg))
            #msg='Already Exist'

    
    return render_template('product.html',catt=catt)

@app.route('/view_user', methods=['GET', 'POST'])
def view_user():
    msg=""
    act=""
    if 'username' in session:
        uname = session['username']
    
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM sc_user")
    data = mycursor.fetchall()
       
    
    if request.method=='GET':
        act = request.args.get('act')
        id1 = request.args.get('id')
        if act=="yes":
            cursor1 = mydb.cursor()
            cursor1.execute('SELECT * FROM sc_user WHERE id = %s', (id1, ))
            account1 = cursor1.fetchone()
            email=account1[5]
            prk=account1[8]
            pbk=account1[7]
            usid=account1[6]
            message="User:"+usid+", Public Key:"+pbk+", Private Key:"+prk
            print(message)
            ##send mail
            print(email)
            with app.app_context():
                msg = Message(subject="Smart Contract", sender=app.config.get("MAIL_USERNAME"),recipients=[email], body=message)
                mail.send(msg)
            
            ##BC########################    
        
            cursor = mydb.cursor()
            cursor.execute('update sc_user set status=1 WHERE id = %s', (id1,))
            mydb.commit()
            act='no'
            return redirect(url_for('view_user')) 
        else:
            cursor = mydb.cursor()
            cursor.execute('update sc_user set status=0 WHERE id = %s', (id1,))
            mydb.commit()
            
            #return redirect(url_for('view_user')) 
        
    return render_template('view_user.html', data=data)

@app.route('/login_cus', methods=['GET', 'POST'])
def login_cus():
    msg=""
    act=""
    
        
    if request.method=='POST':
        uname=request.form['uname']
        pwd=request.form['pass']
        cursor = mydb.cursor()
        cursor.execute('SELECT * FROM sc_customer WHERE uname = %s AND pass = %s', (uname, pwd))
        account = cursor.fetchone()
        if account:
            session['username'] = uname
            return redirect(url_for('cus_home'))
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'
    return render_template('login_cus.html',msg=msg,act=act)


@app.route('/login_shop', methods=['GET', 'POST'])
def login_shop():
    msg=""
    act = request.args.get('act')
    if request.method=='POST':
        uname=request.form['uname']
        pwd=request.form['pass']
        cursor = mydb.cursor()
        cursor.execute('SELECT * FROM sc_shop WHERE uname = %s AND pass = %s', (uname, pwd))
        account = cursor.fetchone()
        if account:
            session['username'] = uname
            return redirect(url_for('shop_home'))
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'
    return render_template('login_shop.html',msg=msg,act=act)


@app.route('/login_sup', methods=['GET', 'POST'])
def login_sup():
    msg=""
    act = request.args.get('act')
    if request.method=='POST':
        uname=request.form['uname']
        pwd=request.form['pass']
        cursor = mydb.cursor()
        cursor.execute('SELECT * FROM sc_supplier WHERE uname = %s AND pass = %s', (uname, pwd))
        account = cursor.fetchone()
        if account:
            session['username'] = uname
            return redirect(url_for('sup_home'))
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'
    return render_template('login_sup.html',msg=msg,act=act)


@app.route('/register', methods=['GET', 'POST'])
def register():
    msg=""
    if request.method=='POST':
        name=request.form['name']
        address=request.form['address']
        mobile=request.form['mobile']
        email=request.form['email']
        uname=request.form['uname']
        pass1=request.form['pass']
        rdate=date.today()
        print(rdate)
        cursor = mydb.cursor()

        cursor.execute('SELECT * FROM sc_company')
        result = cursor.fetchall()
        j=0
        for i in result:
            print(i[0])
            j+=1
        id2=j+1
        
        rd=str(rdate).split("-")
        rdd=rd[2]+"-"+rd[1]+"-"+rd[0]
        sql = "INSERT INTO sc_company(id,name,address,mobile,email,uname,pass,rdate) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        val = (id2,name,address,mobile,email,uname,pass1,rdd)
        cursor.execute(sql, val)
        mydb.commit()            
        print(cursor.rowcount, "Registered Success")
        result="sucess"
        
        if cursor.rowcount==1:
            return redirect(url_for('login',act='1'))
        else:
            return redirect(url_for('login',act='2'))
            #msg='Already Exist'  
    return render_template('register.html',msg=msg)


@app.route('/reg_shop', methods=['GET', 'POST'])
def reg_shop():
    msg=""
    if request.method=='POST':
        name=request.form['name']
        address=request.form['address']
        mobile=request.form['mobile']
        email=request.form['email']
        uname=request.form['uname']
        pass1=request.form['pass']
        rdate=date.today()
        print(rdate)
        cursor = mydb.cursor()

        cursor.execute('SELECT * FROM sc_shop')
        result = cursor.fetchall()
        j=0
        for i in result:
            print(i[0])
            j+=1
        id2=j+1
        rd=str(rdate).split("-")
        rdd=rd[2]+"-"+rd[1]+"-"+rd[0]
        sql = "INSERT INTO sc_shop(id,name,address,mobile,email,uname,pass,rdate) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        val = (id2,name,address,mobile,email,uname,pass1,rdd)
        cursor.execute(sql, val)
        mydb.commit()            
        print(cursor.rowcount, "Registered Success")
        result="sucess"
        if cursor.rowcount==1:
            return redirect(url_for('login_shop',act='1'))
        else:
            return redirect(url_for('login_shop',act='2'))
            #msg='Already Exist' 
    return render_template('reg_shop.html',msg=msg)
    
@app.route('/reg_cus', methods=['GET', 'POST'])
def reg_cus():
    msg=""
    if request.method=='POST':
        name=request.form['name']
        address=request.form['address']
        mobile=request.form['mobile']
        email=request.form['email']
        uname=request.form['uname']
        pass1=request.form['pass']
        rdate=date.today()
        print(rdate)
        cursor = mydb.cursor()

        cursor.execute('SELECT * FROM sc_customer')
        result = cursor.fetchall()
        j=0
        for i in result:
            print(i[0])
            j+=1
        id2=j+1
        rd=str(rdate).split("-")
        rdd=rd[2]+"-"+rd[1]+"-"+rd[0]
        sql = "INSERT INTO sc_customer(id,name,address,mobile,email,uname,pass,rdate) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        val = (id2,name,address,mobile,email,uname,pass1,rdd)
        cursor.execute(sql, val)
        mydb.commit()            
        print(cursor.rowcount, "Registered Success")
        result="sucess"
        if cursor.rowcount==1:
            return redirect(url_for('login_cus',act='1'))
        else:
            return redirect(url_for('login_cus',act='2'))
            #msg='Already Exist' 
    return render_template('reg_cus.html',msg=msg)

@app.route('/reg_sup', methods=['GET', 'POST'])
def reg_sup():
    msg=""
    if request.method=='POST':
        name=request.form['name']
        address=request.form['address']
        mobile=request.form['mobile']
        email=request.form['email']
        uname=request.form['uname']
        pass1=request.form['pass']
        rdate=date.today()
        print(rdate)
        cursor = mydb.cursor()

        cursor.execute('SELECT * FROM pr_supplier')
        result = cursor.fetchall()
        j=0
        for i in result:
            print(i[0])
            j+=1
        id2=j+1
        rd=str(rdate).split("-")
        rdd=rd[2]+"-"+rd[1]+"-"+rd[0]
        sql = "INSERT INTO pr_supplier(id,owner,name,mobile,email,city,uname,pass,rdate) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        val = (id2,name,address,mobile,email,uname,pass1,rdd)
        cursor.execute(sql, val)
        mydb.commit()            
        print(cursor.rowcount, "Registered Success")
        result="sucess"
        if cursor.rowcount==1:
            return redirect(url_for('login_sup',act='1'))
        else:
            return redirect(url_for('login_sup',act='2'))
            #msg='Already Exist' 
    return render_template('reg_sup.html',msg=msg)

@app.route('/man_cat', methods=['GET', 'POST'])
def man_cat():
    msg=""
    if request.method=='POST':
        category=request.form['category']

        mycursor = mydb.cursor()
        mycursor.execute("SELECT max(id)+1 FROM sc_category")
        maxid = mycursor.fetchone()[0]
        if maxid is None:
            maxid=1
        cursor = mydb.cursor()
        sql = "INSERT INTO sc_category(id,category) VALUES (%s, %s)"
        val = (maxid,category)
        cursor.execute(sql, val)
        mydb.commit()
        msg="Added Success"
        return redirect(url_for('man_cat',msg=msg))
            
    return render_template('man_cat.html',msg=msg)

@app.route('/man_transfer', methods=['GET', 'POST'])
def man_transfer():
    if 'username' in session:
        uname = session['username']
    msg=""
    pid=""
    if request.method=='GET':
        pid = request.args.get('pid')
    if request.method=='POST':
        pid = request.form['pid']
        ttype=request.form['ttype']
        transport=request.form['transport']
        location=request.form['location']
        tdate=request.form['tdate']
        rd=str(tdate).split("-")
        rdd=rd[2]+"-"+rd[1]+"-"+rd[0]
        cursor = mydb.cursor()
        cursor.execute('update sc_product set ttype=%s,transport=%s,tlocation=%s,tdate=%s,status=1 where id=%s',(ttype,transport,location,rdd,pid))
        mydb.commit()

        ##BC##
        sdata="PID:"+pid+",Company:"+uname+",Transport:"+transport+",Location:"+location+",Date:"+tdate
        result = hashlib.md5(sdata.encode())
        key=result.hexdigest()

        mycursor1 = mydb.cursor()
        mycursor1.execute("SELECT max(id)+1 FROM sc_blockchain")
        maxid1 = mycursor1.fetchone()[0]
        if maxid1 is None:
            maxid1=1
            pkey="00000000000000000000000000000000"
        else:
            mid=int(pid)-1
            cursor.execute('SELECT * FROM sc_blockchain where id=%s',(mid, ))
            pp = cursor.fetchone()
            pkey=pp[3]
        sql2 = "INSERT INTO sc_blockchain(id,block_id,pre_hash,hash_value,sdata) VALUES (%s, %s, %s, %s, %s)"
        val2 = (maxid1,pid,pkey,key,sdata)
        cursor.execute(sql2, val2)
        mydb.commit()   
        ####
        msg="Added Success"
        return redirect(url_for('man_transview',msg=msg))
    
    return render_template('man_transfer.html',pid=pid,msg=msg)

@app.route('/man_transview', methods=['GET', 'POST'])
def man_transview():
    if 'username' in session:
        uname = session['username']
    cursor = mydb.cursor()
    cursor.execute('SELECT * FROM sc_product where status=1 and company=%s',(uname, ))
    data = cursor.fetchall()
    return render_template('man_transview.html',data=data)

@app.route('/sup_home', methods=['GET', 'POST'])
def sup_home():
    msg=""
    if 'username' in session:
        uname = session['username']
    cursor = mydb.cursor()
    cursor.execute('SELECT * FROM sc_product where supplier=%s && status = 2',(uname, ))
    data = cursor.fetchall()
    return render_template('sup_home.html',data=data)

@app.route('/sup_trans', methods=['GET', 'POST'])
def sup_trans():
    msg=""
    if 'username' in session:
        uname = session['username']
    cursor = mydb.cursor()
    cursor.execute('SELECT * FROM sc_shop')
    data = cursor.fetchall()

    pid=""
    if request.method=='GET':
        pid = request.args.get('pid')
    if request.method=='POST':
        pid = request.form['pid']
        shop=request.form['shop']
        ttype=request.form['ttype']
        transport=request.form['transport']
        location=request.form['location']
        tdate=request.form['sdate']
        rd=str(tdate).split("-")
        rdd=rd[2]+"-"+rd[1]+"-"+rd[0]
        cursor = mydb.cursor()
        cursor.execute('update sc_product set retailer=%s,ttype=%s,transport=%s,tlocation=%s,sdate=%s,status=3 where id=%s',(shop,ttype,transport,location,rdd,pid))
        mydb.commit()

        ##BC##
        sdata="PID:"+pid+",Supplier:"+uname+",Retailer:"+shop+",Transport:"+transport+",Location:"+location+",Date:"+tdate
        result = hashlib.md5(sdata.encode())
        key=result.hexdigest()

        mycursor1 = mydb.cursor()
        mycursor1.execute("SELECT max(id)+1 FROM sc_blockchain")
        maxid1 = mycursor1.fetchone()[0]
        if maxid1 is None:
            maxid1=1
            pkey="00000000000000000000000000000000"
        else:
            mid=int(pid)-1
            cursor.execute('SELECT * FROM sc_blockchain where id=%s',(mid, ))
            pp = cursor.fetchone()
            pkey=pp[3]
        sql2 = "INSERT INTO sc_blockchain(id,block_id,pre_hash,hash_value,sdata) VALUES (%s, %s, %s, %s, %s)"
        val2 = (maxid1,pid,pkey,key,sdata)
        cursor.execute(sql2, val2)
        mydb.commit()   
        ####
        msg="Added Success"
        return redirect(url_for('sup_shopview',msg=msg))
    return render_template('sup_trans.html',data=data,pid=pid)

@app.route('/sup_shopview', methods=['GET', 'POST'])
def sup_shopview():
    msg=""
    if 'username' in session:
        uname = session['username']
    cursor = mydb.cursor()
    cursor.execute('SELECT * FROM sc_product where supplier=%s && status = 3',(uname, ))
    data = cursor.fetchall()
    return render_template('sup_shopview.html',data=data)

@app.route('/shop_home', methods=['GET', 'POST'])
def shop_home():
    msg=""
    if 'username' in session:
        uname = session['username']
    cursor = mydb.cursor()
    cursor.execute('SELECT * FROM sc_product where retailer=%s && status = 3',(uname, ))
    data = cursor.fetchall()
    return render_template('shop_home.html',data=data)

@app.route('/shop_sale', methods=['GET', 'POST'])
def shop_sale():
    msg=""
    if 'username' in session:
        uname = session['username']
    cursor = mydb.cursor()
    cursor.execute('SELECT * FROM sc_customer')
    data = cursor.fetchall()

    pid=""
    if request.method=='GET':
        pid = request.args.get('pid')
    if request.method=='POST':
        pid = request.form['pid']
        customer=request.form['customer']
        
        tdate=request.form['sdate']
        rd=str(tdate).split("-")
        rdd=rd[2]+"-"+rd[1]+"-"+rd[0]
        cursor = mydb.cursor()
        cursor.execute('update sc_product set customer=%s,sdate=%s,status=4 where id=%s',(customer,rdd,pid))
        mydb.commit()

        ##BC##
        sdata="PID:"+pid+",Retailer:"+uname+",Customer:"+customer+",Date:"+tdate
        result = hashlib.md5(sdata.encode())
        key=result.hexdigest()

        mycursor1 = mydb.cursor()
        mycursor1.execute("SELECT max(id)+1 FROM sc_blockchain")
        maxid1 = mycursor1.fetchone()[0]
        if maxid1 is None:
            maxid1=1
            pkey="00000000000000000000000000000000"
        else:
            mid=int(pid)-1
            cursor.execute('SELECT * FROM sc_blockchain where id=%s',(mid, ))
            pp = cursor.fetchone()
            pkey=pp[3]
        sql2 = "INSERT INTO sc_blockchain(id,block_id,pre_hash,hash_value,sdata) VALUES (%s, %s, %s, %s, %s)"
        val2 = (maxid1,pid,pkey,key,sdata)
        cursor.execute(sql2, val2)
        mydb.commit()   
        ####
        msg="Added Success"
        return redirect(url_for('shop_saleview',msg=msg))
    return render_template('shop_sale.html',data=data,pid=pid)

@app.route('/shop_saleview', methods=['GET', 'POST'])
def shop_saleview():
    msg=""
    if 'username' in session:
        uname = session['username']
    cursor = mydb.cursor()
    cursor.execute('SELECT * FROM sc_product where retailer=%s && status = 4',(uname, ))
    data = cursor.fetchall()
    return render_template('shop_saleview.html',data=data)

@app.route('/cus_home', methods=['GET', 'POST'])
def cus_home():
    msg=""
    pid=""
    act=""
    prdid=""
    if 'username' in session:
        uname = session['username']
    cursor = mydb.cursor()
    cursor.execute('SELECT * FROM sc_product where customer=%s && status = 4',(uname, ))
    data = cursor.fetchall()
    if request.method=='GET':
        act = request.args.get('act')
        pid=request.args.get('pid')
        if act=="get":
            cursor1 = mydb.cursor()
            cursor1.execute('SELECT * FROM sc_product where id=%s',(pid, ))
            data1 = cursor1.fetchone()
            prdid = data1[11]
        
        
    return render_template('cus_home.html',data=data,act=act,pid=pid,prdid=prdid)

@app.route('/cus_verify', methods=['GET', 'POST'])
def cus_verify():
    msg=""
    pid=""
    prdid=""
    key=""
    act=""
    data=""
    delta=""
    days=""
    if 'username' in session:
        uname = session['username']
    if request.method=='GET':
        pid = request.args.get('pid')
        
        cursor = mydb.cursor()
        cursor.execute('SELECT * FROM sc_product WHERE id = %s', (pid, ))
        account = cursor.fetchone()
        prdid=account[11]
        print(prdid)
    if request.method=='POST':
        key=request.form['key']
        pid=request.form['pid']
        prdid=request.form['prdid']
        act="yes"
        
        if prdid==key:
            cursor1 = mydb.cursor()    
            cursor1.execute('SELECT * FROM sc_blockchain WHERE block_id = %s order by id', (pid, ))
            data = cursor1.fetchall()
            dd=data[0][4]
            dd2=dd.split(',')
            dd3=dd2[4].split(':')
            #print(dd3[1])
            #print(dd3[1])
            dd4=dd3[1]
            dd5=dd4.split('-')
            yr=dd5[0]
            mon=dd5[1]
            dy=dd5[2]

            now = datetime.datetime.now()
            yr1=now.strftime("%Y")
            mon1=now.strftime("%m")
            da1=now.strftime("%d")
            
            f_date = date(int(yr1), int(mon1), int(da1))
            l_date = date(int(yr), int(mon), int(dy))
            #f_date = date(yr1, mon1, da1)
            #l_date = date(yr, mon, dy)
            delta = l_date - f_date
            print(delta.days)
            days=delta.days
            msg="success" 
        else:
            msg="Invalid Key!" 
    return render_template('cus_verify.html',msg=msg, prdid=prdid, data=data, days=days, act=act, pid=pid)


@app.route('/man_home', methods=['GET', 'POST'])
def man_home():
    msg=""
    maxid=0
    maxid1=0
    mid=0
    if 'username' in session:
        uname = session['username']
    
    if request.method=='GET':
        msg = request.args.get('msg')
    cursor = mydb.cursor()
    cursor.execute('SELECT * FROM sc_category')
    catt = cursor.fetchall()


    if request.method=='POST':
        cat=request.form['category']
        prd=request.form['product']
        price=request.form['price']
        psize=request.form['psize']
        kg=request.form['kg']
        description=request.form['description']
        location=request.form['location']
        mdate=request.form['mdate']
        edate=request.form['edate']
        
        

        
        mycursor = mydb.cursor()
        mycursor.execute("SELECT max(id)+1 FROM sc_product")
        maxid = mycursor.fetchone()[0]
        if maxid is None:
            maxid=1
        
        numStr = str(maxid)
        numStr = numStr.zfill(4)
        now = datetime.datetime.now()
        rdate=now.strftime("%d-%m-%Y")
        my=now.strftime("%y%m")
        pcode=my+numStr

        
        sql = "INSERT INTO sc_product(id,category,product,company,price,psize,kg,description,location,mdate,edate,pcode,rdate) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        val = (maxid,cat,prd,uname,price,psize,kg,description,location,mdate,edate,pcode,rdate)
        cursor.execute(sql, val)
        mydb.commit()            
        print(cursor.rowcount, "Added Success")
        result="sucess"
        ##BC##
        sdata="PID:"+str(maxid)+",Product:"+prd+",Company:"+uname+",Manufacture:"+mdate+",Expire:"+edate+",RegDate:"+rdate
        result = hashlib.md5(sdata.encode())
        key=result.hexdigest()

        mycursor1 = mydb.cursor()
        mycursor1.execute("SELECT max(id)+1 FROM sc_blockchain")
        maxid1 = mycursor1.fetchone()[0]
        if maxid1 is None:
            maxid1=1
            pkey="00000000000000000000000000000000"
        else:
            mid=maxid-1
            cursor.execute('SELECT * FROM sc_blockchain where id=%s',(mid, ))
            pp = cursor.fetchone()
            pkey=pp[3]
        sql2 = "INSERT INTO sc_blockchain(id,block_id,pre_hash,hash_value,sdata) VALUES (%s, %s, %s, %s, %s)"
        val2 = (maxid1,maxid,pkey,key,sdata)
        cursor.execute(sql2, val2)
        mydb.commit()   
        ####
        
        if cursor.rowcount==1:
            msg="success"
            return redirect(url_for('man_home',msg=msg))
        else:
            msg="fail"
            return redirect(url_for('man_home',msg=msg))
            #msg='Already Exist'
    '''if request.method=='POST':
        product=request.form['product']
        price=request.form['price']
        store.addprod(product,price)'''
    return render_template('man_home.html',catt=catt, msg=msg)

@app.route('/man_viewprd', methods=['GET', 'POST'])
def man_viewprd():
    msg=""
    if 'username' in session:
        uname = session['username']
    
    if request.method=='GET':
        msg = request.args.get('msg')
    cursor = mydb.cursor()
    cursor.execute('SELECT * FROM sc_category')
    catt = cursor.fetchall()
    if request.method=='POST':
        cat=request.form['category']
        mycursor = mydb.cursor()
        mycursor.execute("SELECT * FROM sc_product where company=%s && category = %s",(uname, cat, ))
        data = mycursor.fetchall()
        return render_template('man_viewprd.html',catt=catt,data=data)
    
    return render_template('man_viewprd.html',catt=catt, msg=msg)

@app.route('/man_sup', methods=['GET', 'POST'])
def man_sup():
    if 'username' in session:
        uname = session['username']
    msg=""
    pid=""
    print(uname)
    cursor = mydb.cursor()
    cursor.execute('SELECT * FROM sc_supplier')
    data = cursor.fetchall()
    
    if request.method=='GET':
        pid = request.args.get('pid')
    if request.method=='POST':
        pid = request.form['pid']
        supplier = request.form['supplier']
        ttype=request.form['ttype']
        transport=request.form['transport']
        location=request.form['location']
        sdate=request.form['sdate']
        rd=str(sdate).split("-")
        rdd=rd[2]+"-"+rd[1]+"-"+rd[0]
        cursor = mydb.cursor()
        cursor.execute('update sc_product set supplier=%s,ttype=%s,transport=%s,tlocation=%s,sdate=%s,status=2 where id=%s',(supplier,ttype,transport,location,rdd,pid))
        mydb.commit()

        ##BC##
        sdata="PID:"+str(pid)+",Company:"+uname+",Supplier:"+supplier+",Transport:"+transport+",Location:"+location+",Date:"+sdate
        result = hashlib.md5(sdata.encode())
        key=result.hexdigest()

        mycursor1 = mydb.cursor()
        mycursor1.execute("SELECT max(id)+1 FROM sc_blockchain")
        maxid1 = mycursor1.fetchone()[0]
        if maxid1 is None:
            maxid1=1
            pkey="00000000000000000000000000000000"
        else:
            mid=int(pid)-1
            cursor.execute('SELECT * FROM sc_blockchain where id=%s',(mid, ))
            pp = cursor.fetchone()
            pkey=pp[3]
        sql2 = "INSERT INTO sc_blockchain(id,block_id,pre_hash,hash_value,sdata) VALUES (%s, %s, %s, %s, %s)"
        val2 = (maxid1,pid,pkey,key,sdata)
        cursor.execute(sql2, val2)
        mydb.commit()   
        ####
        msg="Added Success"
        return redirect(url_for('man_supply',msg=msg))
    
    return render_template('man_sup.html',pid=pid,msg=msg,data=data)


@app.route('/man_supply', methods=['GET', 'POST'])
def man_supply():
    msg=""
    if 'username' in session:
        uname = session['username']
    
    if request.method=='GET':
        msg = request.args.get('msg')
    cursor = mydb.cursor()
    cursor.execute('SELECT * FROM sc_product where company=%s && status = 2',(uname, ))
    data = cursor.fetchall()
    
    
    return render_template('man_supply.html',data=data, msg=msg)

@app.route('/login_user', methods=['GET', 'POST'])
def login_user():
    msg=""
    act = request.args.get('act')
    if request.method=='POST':
        uname=request.form['uname']
        pwd=request.form['pass']
        cursor = mydb.cursor()
        cursor.execute('SELECT * FROM sc_user WHERE uname = %s AND pbkey = %s', (uname, pwd))
        account = cursor.fetchone()
        if account:
            session['username'] = uname
            return redirect(url_for('user'))
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'
    return render_template('login_user.html',msg=msg,act=act)

@app.route('/user_reg', methods=['GET', 'POST'])
def user_reg():
    msg=""
    if request.method=='POST':
        utype=request.form['utype']
        name=request.form['name']
        address=request.form['address']
        mobile=request.form['mobile']
        email=request.form['email']
        
        
        rdate=date.today()
        print(rdate)
        cursor = mydb.cursor()

        mycursor = mydb.cursor()
        mycursor.execute("SELECT max(id)+1 FROM sc_user")
        maxid = mycursor.fetchone()[0]
        if maxid is None:
            maxid=1
        now = datetime.datetime.now()
        rdate=now.strftime("%d-%m-%Y")

        uname="U"+str(maxid)
        result = hashlib.md5(uname.encode())
        key=result.hexdigest()
        pbkey=key[0:8]
        prkey=key[8:16]
        
        sql = "INSERT INTO sc_user(id,utype,name,address,mobile,email,uname,pbkey,prkey,status,rdate) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        val = (maxid,utype,name,address,mobile,email,uname,pbkey,prkey,'0',rdate)
        cursor.execute(sql, val)
        mydb.commit()            
        print(cursor.rowcount, "Registered Success")
        msg="sucess"
        
        
    return render_template('user_reg.html', msg=msg)

@app.route('/user', methods=['GET', 'POST'])
def user():
    msg=""
    act=""
    data=""
    pid=""
    if request.method=='GET':
        act = request.args.get('act')
        data = request.args.get('data')
        pid = request.args.get('pid')
    if request.method=='POST':
        pid=request.form['pid']
        act="yes"
        cursor = mydb.cursor()
        cursor.execute('SELECT * FROM sc_blockchain WHERE block_id = %s order by id limit 0,1', (pid, ))
        account = cursor.fetchone()
        dd=account[4]
        dd2=dd.split(',')
        data=dd2[0]+","+dd2[1]+","+dd2[2]
        return redirect(url_for('user', act=act, pid=pid, data=data))
    return render_template('user.html', msg=msg, act=act, data=data, pid=pid)

@app.route('/view_block', methods=['GET', 'POST'])
def view_block():
    msg=""
    pid=""
    act=""
    data=""
    delta=""
    days=""
    if 'username' in session:
        uname = session['username']
    cursor = mydb.cursor()
    cursor.execute('SELECT * FROM sc_user WHERE uname = %s', (uname, ))
    account = cursor.fetchone()
    prkey=account[8]
    if request.method=='GET':
        pid = request.args.get('pid')
    if request.method=='POST':
        prk=request.form['prk']
        pid=request.form['pid']
        act="yes"
        
        if prk==prkey:
            cursor1 = mydb.cursor()    
            cursor1.execute('SELECT * FROM sc_blockchain WHERE block_id = %s order by id', (pid, ))
            data = cursor1.fetchall()
            dd=data[0][4]
            dd2=dd.split(',')
            dd3=dd2[4].split(':')
            #print(dd3[1])
            #print(dd3[1])
            dd4=dd3[1]
            dd5=dd4.split('-')
            yr=dd5[0]
            mon=dd5[1]
            dy=dd5[2]

            now = datetime.datetime.now()
            yr1=now.strftime("%Y")
            mon1=now.strftime("%m")
            da1=now.strftime("%d")
            
            f_date = date(int(yr1), int(mon1), int(da1))
            l_date = date(int(yr), int(mon), int(dy))
            #f_date = date(yr1, mon1, da1)
            #l_date = date(yr, mon, dy)
            delta = l_date - f_date
            print(delta.days)
            days=delta.days
            msg="success" 
        else:
            msg="Invalid Key!" 
    return render_template('view_block.html',msg=msg, prkey=prkey, data=data, days=days, act=act, pid=pid)


@app.route('/logout')
def logout():
    # remove the username from the session if it is there
    session.pop('username', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
