from flask import Flask
from flask import Flask, render_template, Response, redirect, request, session, abort, url_for
from datetime import datetime
from datetime import date
import datetime
import random
from random import seed
from random import randint
#import cv2
#import numpy as np
import os
import time
import shutil
import hashlib
import json
#import imagehash
#import PIL.Image
#from PIL import Image
#from PIL import ImageTk
import urllib.request
import urllib.parse
from urllib.request import urlopen
import webbrowser
import mysql.connector
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  charset="utf8",
  database="medical_product"

)

#from store import *


app = Flask(__name__)
app.secret_key = 'abcdef'


@app.route('/', methods=['GET', 'POST'])
def index():
    msg=""
    act=""
    show=""
    expiry_st=""
    ms1=""
    ms2=""
    ms3=""
    soldate=""
    reto=""
    data2=[]
    data3=[]
    mdata=[]
    sdata=[]
    rdata=[]
    pdata=[]

    pdata1=[]
    pdata11=[]
    scnt=0
    company=""
    supplier=""
    shop=""
    sact=""
    pid=0
    pcode=""
    if request.method=='POST':
        pcode=request.form['pcode']
        show="yes"

        #pp=pcode.split("P")
        #pcode2=pp[0]
        
        cursor = mydb.cursor()
            
        cursor.execute("SELECT count(*) FROM pr_productcode where product_code=%s",(pcode, ))
        cnt = cursor.fetchone()[0]
        if cnt>0:
            act="1"
            cursor.execute("SELECT * FROM pr_productcode where product_code=%s",(pcode, ))
            dd = cursor.fetchone()
            pid=dd[1]
            company=dd[2]
            suplier=dd[5]
            shop=dd[6]
            sale_st=dd[7]

            ####check expiry
            now = datetime.datetime.now()
            rdate=now.strftime("%d-%m-%Y")
            rdd1=rdate.split('-')
            cursor.execute("SELECT * FROM pr_product where id=%s",(pid,))
            dd4 = cursor.fetchone()
            edd=dd4[14]
            edd1=edd.split("-")
            ey=int(edd1[0])
            em=int(edd1[1])
            ed=int(edd1[2])

            ry=int(rdd1[2])
            rm=int(rdd1[1])
            rd=int(rdd1[0])
            
            from datetime import date

            date1 = date(ey, em, ed)
            date2 = date(ry, rm, rd)

            if date1 < date2:
                expiry_st="1"
            else:
                expiry_st="2"
            
            print(expiry_st)
            ############
            if sale_st==1:
                soldate=dd[8]
                reto=dd[5]
                act="4"
            else:
                if expiry_st=="2":
                    cursor.execute('SELECT * FROM pr_blockchain where block_id=%s && ptype=%s',(pid, 'PID'))
                    data2 = cursor.fetchall()

                    cursor.execute("SELECT * FROM pr_productcode  where pid=%s && shop!='' group by shop",(pid,))
                    pdata1 = cursor.fetchall()

                    for p11 in pdata1:
                        dt=[]
                        cursor.execute("SELECT * FROM pr_productcode  where pid=%s && shop=%s && sale=0",(pid,p11[6]))
                        p21 = cursor.fetchall()
                        x=0
                       
                        for p22 in p21:
                            
                            x+=1
                        if x>0:
                            dt.append(p11[6])
                            dt.append(str(x))
                            
                            cursor.execute("SELECT * FROM pr_shop  where uname=%s",(p11[6],))
                            p23 = cursor.fetchone()

                            dt.append(p23[3])
                            dt.append(p23[4])
                            dt.append(p23[6])
                            pdata11.append(dt)

                    ####Find Manufacture###
                    #code=int(pp[1])
                    ms1="1"
                    cursor.execute("SELECT * FROM pr_manufacture where uname=%s",(company, ))
                    mdata = cursor.fetchone()

                    cursor.execute("SELECT * FROM pr_product where id=%s",(pid, ))
                    pdata = cursor.fetchone()

                    ####Find Distributor###
                    cursor.execute("SELECT count(*) FROM pr_send where pid=%s",(pid,))
                    cn41 = cursor.fetchone()[0]
                    if cn41>0:
                        ms2="1"
                        supplier=""
                        cursor.execute("SELECT * FROM pr_send where pid=%s",(pid,))
                        dd41 = cursor.fetchall()
                        for dd42 in dd41:
                            supplier=dd42[8]
                    
                        cursor.execute("SELECT * FROM pr_supplier where uname=%s",(supplier, ))
                        sdata = cursor.fetchone()
                    else:
                        ms2="2"
                        print("none")
                   
                        
                    
                        
                    ####Find Retailer###
                    if shop=="":
                        ms3="2"
                        print("none")
                    else:
                        ms3="1"
                        

                        cursor.execute("SELECT * FROM pr_shop where uname=%s",(shop, ))
                        rdata = cursor.fetchone()
                    
                    ####SOLD##
                    cursor.execute("SELECT count(*) FROM pr_sale where pcode=%s",(pcode, ))
                    scnt = cursor.fetchone()[0]
                    if scnt>0:
                        sact="1"
                    else:
                        sact=""
                    ######
                else:
                    act="3"

            
        else:
            act="2"


        
        '''cursor.execute("SELECT count(*) FROM pr_product where pcode=%s",(pcode2, ))
        cnt = cursor.fetchone()[0]
        if cnt>0:
            act="1"
            cursor.execute("SELECT * FROM pr_product where pcode=%s",(pcode2, ))
            dd = cursor.fetchone()
            pid=dd[0]
            company=dd[3]
            cursor.execute('SELECT * FROM pr_blockchain where block_id=%s && ptype=%s',(pid, 'PID'))
            data2 = cursor.fetchall()
            #for ss in data:
            #    ss1=ss[4].split(",")
            #    data1.append()
            cursor.execute("SELECT * FROM pr_shop")
            data3 = cursor.fetchall()
            ####Find Manufacture###
            code=int(pp[1])
            ms1="1"
            cursor.execute("SELECT * FROM pr_manufacture where uname=%s",(company, ))
            mdata = cursor.fetchone()

            cursor.execute("SELECT * FROM pr_product where id=%s",(pid, ))
            pdata = cursor.fetchone()
            
            ####Find Distributor###
            cursor.execute("SELECT count(*) FROM pr_send where pid=%s && prd1<=%s && prd2>=%s",(pid, code,code))
            dss1 = cursor.fetchone()[0]
            if dss1>0:
                ms2="1"
                cursor.execute("SELECT * FROM pr_send where pid=%s && prd1<=%s && prd2>=%s",(pid, code,code))
                dss2 = cursor.fetchone()
                supplier=dss2[8]

                cursor.execute("SELECT * FROM pr_supplier where uname=%s",(supplier, ))
                sdata = cursor.fetchone()
            else:
                ms2="2"
                print("none")
            ####Find Retailer###
            cursor.execute("SELECT count(*) FROM pr_send2 where pid=%s && prd1<=%s && prd2>=%s",(pid, code,code))
            dss2 = cursor.fetchone()[0]
            if dss2>0:
                ms3="1"
                cursor.execute("SELECT * FROM pr_send2 where pid=%s && prd1<=%s && prd2>=%s",(pid, code,code))
                dss2 = cursor.fetchone()
                shop=dss2[12]

                cursor.execute("SELECT * FROM pr_shop where uname=%s",(shop, ))
                rdata = cursor.fetchone()
            else:
                ms3="2"
                print("none")
            ####SOLD##
            cursor.execute("SELECT count(*) FROM pr_sale where pcode=%s",(pcode, ))
            scnt = cursor.fetchone()[0]
            if scnt>0:
                sact="1"
            else:
                sact=""
            ######
            
        
        else:
            act="2"'''
        
        
    return render_template('index.html',ms1=ms1,ms2=ms2,ms3=ms3,act=act,msg=msg,show=show,data2=data2,data3=data3,sact=sact,soldate=soldate,reto=reto,pdata11=pdata11,mdata=mdata,sdata=sdata,rdata=rdata,pdata=pdata,pcode=pcode)

@app.route('/login', methods=['GET', 'POST'])
def login():
    msg=""
    act = request.args.get('act')
    if request.method=='POST':
        uname=request.form['uname']
        pwd=request.form['pass']
        cursor = mydb.cursor()
        cursor.execute('SELECT * FROM pr_manufacture WHERE uname = %s AND pass = %s AND status=1', (uname, pwd))
        account = cursor.fetchone()
        if account:
            ff1=open("log.txt","w")
            ff1.write(uname)
            ff1.close()
            session['username'] = uname
            return redirect(url_for('product'))
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password! or Not Approved'
            return redirect(url_for('mess'))
        
        
    return render_template('index.html',msg=msg,act=act)

@app.route('/login_admin', methods=['GET', 'POST'])
def login_admin():
    msg=""
    act = request.args.get('act')
    if request.method=='POST':
        uname=request.form['uname']
        pwd=request.form['pass']
        cursor = mydb.cursor()
        cursor.execute('SELECT * FROM pr_admin WHERE username = %s AND password = %s', (uname, pwd))
        account = cursor.fetchone()
        if account:
            ff1=open("log.txt","w")
            ff1.write(uname)
            ff1.close()
            session['username'] = uname
            return redirect(url_for('admin'))
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'
    
        
        
    return render_template('index.html',msg=msg,act=act)


@app.route('/admin', methods=['GET', 'POST'])
def admin():
    msg=""
    act = request.args.get('act')

    cursor = mydb.cursor()
    cursor.execute('SELECT * FROM pr_manufacture')
    data = cursor.fetchall()

    if act=="ok":
        mid = request.args.get('mid')
        cursor.execute('update pr_manufacture set status=1 where id=%s',(mid,))
        mydb.commit()
        return redirect(url_for('admin'))
       

    return render_template('admin.html',msg=msg,act=act,data=data)

@app.route('/index_dist', methods=['GET', 'POST'])
def index_dist():
    msg=""
    act = request.args.get('act')
    if request.method=='POST':
        uname=request.form['uname']
        pwd=request.form['pass']
        cursor = mydb.cursor()
        cursor.execute('SELECT * FROM pr_supplier WHERE uname = %s AND pass = %s', (uname, pwd))
        account = cursor.fetchone()
        if account:
            ff1=open("log2.txt","w")
            ff1.write(uname)
            ff1.close()
            session['username'] = uname
            return redirect(url_for('dist_home'))
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'

    return render_template('index_dist.html',msg=msg,act=act)

@app.route('/index_shop', methods=['GET', 'POST'])
def index_shop():
    msg=""
    act = request.args.get('act')
    if request.method=='POST':
        uname=request.form['uname']
        pwd=request.form['pass']
        cursor = mydb.cursor()
        cursor.execute('SELECT * FROM pr_shop WHERE uname = %s AND pass = %s AND status=1', (uname, pwd))
        account = cursor.fetchone()
        if account:
            ff1=open("log3.txt","w")
            ff1.write(uname)
            ff1.close()
            session['username'] = uname
            return redirect(url_for('shop_home'))
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'

    return render_template('index_shop.html',msg=msg,act=act)



#Blockchain
class Blockchain:
    def __init__(self):
        self.current_transactions = []
        self.chain = []
        self.nodes = set()

        # Create the genesis block
        self.new_block(previous_hash='1', proof=100)

    def register_node(self, address):
        """
        Add a new node to the list of nodes

        :param address: Address of node. Eg. 'http://192.168.0.5:5000'
        """

        parsed_url = urlparse(address)
        if parsed_url.netloc:
            self.nodes.add(parsed_url.netloc)
        elif parsed_url.path:
            # Accepts an URL without scheme like '192.168.0.5:5000'.
            self.nodes.add(parsed_url.path)
        else:
            raise ValueError('Invalid URL')


    def valid_chain(self, chain):
        """
        Determine if a given blockchain is valid

        :param chain: A blockchain
        :return: True if valid, False if not
        """

        last_block = chain[0]
        current_index = 1

        while current_index < len(chain):
            block = chain[current_index]
            print(f'{last_block}')
            print(f'{block}')
            print("\n-----------\n")
            # Check that the hash of the block is correct
            last_block_hash = self.hash(last_block)
            if block['previous_hash'] != last_block_hash:
                return False

            # Check that the Proof of Work is correct
            if not self.valid_proof(last_block['proof'], block['proof'], last_block_hash):
                return False

            last_block = block
            current_index += 1

        return True

    def resolve_conflicts(self):
        """
        This is our consensus algorithm, it resolves conflicts
        by replacing our chain with the longest one in the network.

        :return: True if our chain was replaced, False if not
        """

        neighbours = self.nodes
        new_chain = None

        # We're only looking for chains longer than ours
        max_length = len(self.chain)

        # Grab and verify the chains from all the nodes in our network
        for node in neighbours:
            response = requests.get(f'http://{node}/chain')

            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']

                # Check if the length is longer and the chain is valid
                if length > max_length and self.valid_chain(chain):
                    max_length = length
                    new_chain = chain

        # Replace our chain if we discovered a new, valid chain longer than ours
        if new_chain:
            self.chain = new_chain
            return True

        return False

    def new_block(self, proof, previous_hash):
        """
        Create a new Block in the Blockchain

        :param proof: The proof given by the Proof of Work algorithm
        :param previous_hash: Hash of previous Block
        :return: New Block
        """

        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.current_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1]),
        }

        # Reset the current list of transactions
        self.current_transactions = []

        self.chain.append(block)
        return block

    def new_transaction(self, sender, recipient, amount):
        """
        Creates a new transaction to go into the next mined Block

        :param sender: Address of the Sender
        :param recipient: Address of the Recipient
        :param amount: Amount
        :return: The index of the Block that will hold this transaction
        """
        self.current_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount,
        })

        return self.last_block['index'] + 1

    @property
    def last_block(self):
        return self.chain[-1]

    @staticmethod
    def hash(block):
        """
        Creates a SHA-256 hash of a Block

        :param block: Block
        """

        # We must make sure that the Dictionary is Ordered, or we'll have inconsistent hashes
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    def proof_of_work(self, last_block):
        """
        Simple Proof of Work Algorithm:

         - Find a number p' such that hash(pp') contains leading 4 zeroes
         - Where p is the previous proof, and p' is the new proof
         
        :param last_block: <dict> last Block
        :return: <int>
        """

        last_proof = last_block['proof']
        last_hash = self.hash(last_block)

        proof = 0
        while self.valid_proof(last_proof, proof, last_hash) is False:
            proof += 1

        return proof

    @staticmethod
    def valid_proof(last_proof, proof, last_hash):
        """
        Validates the Proof

        :param last_proof: <int> Previous Proof
        :param proof: <int> Current Proof
        :param last_hash: <str> The hash of the Previous Block
        :return: <bool> True if correct, False if not.

        """

        guess = f'{last_proof}{proof}{last_hash}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"

def mine():
    # We run the proof of work algorithm to get the next proof...
    last_block = blockchain.last_block
    proof = blockchain.proof_of_work(last_block)

    # We must receive a reward for finding the proof.
    # The sender is "0" to signify that this node has mined a new coin.
    blockchain.new_transaction(
        sender="0",
        recipient=node_identifier,
        amount=1,
    )

    # Forge the new Block by adding it to the chain
    previous_hash = blockchain.hash(last_block)
    block = blockchain.new_block(proof, previous_hash)

    response = {
        'message': "New Block Forged",
        'index': block['index'],
        'transactions': block['transactions'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash'],
    }
    return jsonify(response), 200


def new_transaction():
    values = request.get_json()

    # Check that the required fields are in the POST'ed data
    required = ['sender', 'recipient', 'amount']
    if not all(k in values for k in required):
        return 'Missing values', 400

    # Create a new Transaction
    index = blockchain.new_transaction(values['sender'], values['recipient'], values['amount'])

    response = {'message': f'Transaction will be added to Block {index}'}
    return jsonify(response), 201

def full_chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain),
    }
    return jsonify(response), 200



def register_nodes():
    values = request.get_json()

    nodes = values.get('nodes')
    if nodes is None:
        return "Error: Please supply a valid list of nodes", 400

    for node in nodes:
        blockchain.register_node(node)

    response = {
        'message': 'New nodes have been added',
        'total_nodes': list(blockchain.nodes),
    }
    return jsonify(response), 201

def consensus():
    replaced = blockchain.resolve_conflicts()

    if replaced:
        response = {
            'message': 'Our chain was replaced',
            'new_chain': blockchain.chain
        }
    else:
        response = {
            'message': 'Our chain is authoritative',
            'chain': blockchain.chain
        }

    return jsonify(response), 200

def productchain(uid,uname,bcdata,utype):
    ############

    now = datetime.datetime.now()
    yr=now.strftime("%Y")
    mon=now.strftime("%m")
    rdate=now.strftime("%d-%m-%Y")
    rtime=now.strftime("%H:%M:%S")
    
    ff=open("static/key.txt","r")
    k=ff.read()
    ff.close()
    
    #bcdata="CID:"+uname+",Time:"+val1+",Unit:"+val2
    dtime=rdate+","+rtime

    #ky=uname
    #obj=AESCipher(ky)

    
    #benc=obj.encrypt(bcdata)
    #benc1=benc.decode("utf-8")

    ff1=open("static/js/d1.txt","r")
    bc1=ff1.read()
    ff1.close()
    
    px=""
    if k=="1":
        px=""
        result = hashlib.md5(bcdata.encode())
        key=result.hexdigest()
        print(key)
        v=k+"##"+key+"##"+bcdata+"##"+dtime

        ff1=open("static/js/d1.txt","w")
        ff1.write(v)
        ff1.close()
        
        dictionary = {
            "ID": "1",
            "Pre-hash": "00000000000000000000000000000000",
            "Hash": key,
            "utype": utype,
            "Date/Time": dtime
        }

        k1=int(k)
        k2=k1+1
        k3=str(k2)
        ff1=open("static/key.txt","w")
        ff1.write(k3)
        ff1.close()

        ff1=open("static/prehash.txt","w")
        ff1.write(key)
        ff1.close()
        
    else:
        px=","
        pre_k=""
        k1=int(k)
        k2=k1-1
        k4=str(k2)

        ff1=open("static/prehash.txt","r")
        pre_hash=ff1.read()
        ff1.close()
        
        g1=bc1.split("#|")
        for g2 in g1:
            g3=g2.split("##")
            if k4==g3[0]:
                pre_k=g3[1]
                break

        
        result = hashlib.md5(bcdata.encode())
        key=result.hexdigest()
        

        v="#|"+k+"##"+key+"##"+bcdata+"##"+dtime

        k3=str(k2)
        ff1=open("static/key.txt","w")
        ff1.write(k3)
        ff1.close()

        ff1=open("static/js/d1.txt","a")
        ff1.write(v)
        ff1.close()

        
        
        dictionary = {
            "ID": k,
            "Pre-hash": pre_hash,
            "Hash": key,
            "utype:": utype,
            "Date/Time": dtime
        }
        k21=int(k)+1
        k3=str(k21)
        ff1=open("static/key.txt","w")
        ff1.write(k3)
        ff1.close()

        ff1=open("static/prehash.txt","w")
        ff1.write(key)
        ff1.close()

    m=""
    if k=="1":
        m="w"
    else:
        m="a"
    # Serializing json
    
    json_object = json.dumps(dictionary, indent=4)
     
    # Writing to sample.json
    with open("static/productchain.json", m) as outfile:
        outfile.write(json_object)
    ##########





@app.route('/reg', methods=['GET', 'POST'])
def reg():
    msg=""
    now = datetime.datetime.now()
    rdate=now.strftime("%d-%m-%Y")
    mycursor = mydb.cursor()
    
    if request.method=='POST':
        name=request.form['name']
        mobile=request.form['mobile']
        email=request.form['email']
        address=request.form['address']
        uname=request.form['uname']
        pass1=request.form['pass']

        mycursor.execute("SELECT count(*) FROM pr_manufacture where uname=%s",("uname",))
        cnt = mycursor.fetchone()[0]

        if cnt==0:
            mycursor.execute("SELECT max(id)+1 FROM pr_manufacture")
            maxid = mycursor.fetchone()[0]
            if maxid is None:
                maxid=1
            sql = "INSERT INTO pr_manufacture(id,name,mobile,email,address,uname,pass) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            val = (maxid,name,mobile,email,address,uname,pass1)
            mycursor.execute(sql, val)
            mydb.commit()

            bcdata="ID: "+str(maxid)+", Manufacturer ID:"+uname+", Manufacturer Name:"+name+", Location:"+address            
            productchain(str(maxid),uname,bcdata,'MC')
            msg="success"
        else:
            msg="fail"
        
    
    return render_template('index.html',msg=msg)


@app.route('/complaint', methods=['GET', 'POST'])
def complaint():
    msg=""
    act = request.args.get('act')
    pcode = request.args.get('pcode')

    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM pr_productcode where product_code=%s",(pcode,))
    pdd = mycursor.fetchone()
    company=pdd[2]
    pid=pdd[1]

    mycursor.execute("SELECT * FROM pr_product where id=%s",(pid,))
    pdd1 = mycursor.fetchone()
    product=pdd1[2]
        
    now = datetime.datetime.now()
    rdate=now.strftime("%d-%m-%Y")
        
    if request.method=='POST':
        name=request.form['name']
        email=request.form['email']
        message=request.form['message']
      

        mycursor = mydb.cursor()
        mycursor.execute("SELECT max(id)+1 FROM pr_complaint")
        maxid = mycursor.fetchone()[0]
        if maxid is None:
            maxid=1
        sql = "INSERT INTO pr_complaint(id,company,pid,pcode,name,email,message,rdate,product) VALUES (%s, %s, %s, %s, %s,%s,%s,%s,%s)"
        val = (maxid,company,pid,pcode,name,email,message,rdate,product)
        mycursor.execute(sql, val)
        mydb.commit()            
        return redirect(url_for('complaint',pcode=pcode,act='1'))

    return render_template('complaint.html',act=act,pcode=pcode)


@app.route('/message', methods=['GET', 'POST'])
def message():
    
    return render_template('message.html')

@app.route('/mess', methods=['GET', 'POST'])
def mess():
    
    return render_template('mess.html')

@app.route('/code1', methods=['GET', 'POST'])
def code1():
    pid = request.args.get('pid')
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM pr_productcode where pid=%s",(pid,))
    data = mycursor.fetchall()

        
    return render_template('code1.html',data=data)


@app.route('/code2', methods=['GET', 'POST'])
def code2():
    pid = request.args.get('pid')
    k1 = request.args.get('k1')
    k2 = request.args.get('k2')
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM pr_productcode where pid=%s && pcount between %s and %s",(pid,k1,k2))
    data = mycursor.fetchall()

        
    return render_template('code2.html',data=data)

@app.route('/view_comp', methods=['GET', 'POST'])
def view_comp():
    msg=""
    uname=""
    if 'username' in session:
        uname = session['username']
    print(uname)
    cursor = mydb.cursor()
    ff1=open("log.txt","r")
    company=ff1.read()
    ff1.close()

    
    
    cursor.execute('SELECT * FROM pr_complaint where company=%s order by id desc',(company, ))
    data = cursor.fetchall()

    return render_template('view_comp.html',data=data)


@app.route('/product', methods=['GET', 'POST'])
def product():
    msg=""
    uname=""
    if 'username' in session:
        uname = session['username']
    print(uname)
    cursor = mydb.cursor()
    ff1=open("log.txt","r")
    company=ff1.read()
    ff1.close()

    cursor.execute('SELECT count(*) FROM pr_product where company=%s',(company, ))
    cnpr = cursor.fetchone()[0]
    
    cursor.execute('SELECT * FROM pr_product where company=%s order by id desc',(company, ))
    data = cursor.fetchall()
    
    cursor.execute('SELECT * FROM pr_category')
    catt = cursor.fetchall()
    if request.method=='POST':
        cat=request.form['category']
        prd=request.form['product']
        price=request.form['price']
        description=request.form['description']
        location=request.form['location']
        mdate=request.form['mdate']
        edate=request.form['edate']
        num_piece=request.form['num_piece']

        num_start="1"
        plen=len(num_piece)
        numStr1 = num_start.zfill(plen)
        numStr2 = num_piece.zfill(plen)
        
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

        xn=randint(1000, 9999)
        pcode="K"+numStr
        code1=pcode+"P"+numStr1
        code2=pcode+"P"+numStr2

        i=1
        nmm=int(num_piece)
        while i<=nmm:
            
            mycursor.execute("SELECT max(id)+1 FROM pr_productcode")
            maxid2 = mycursor.fetchone()[0]
            if maxid2 is None:
                maxid2=1

            xn1=randint(100, 999)
            xn2=randint(1, 9)
            kycode="K"+str(xn2)+str(maxid)+"0"+str(maxid2)+str(xn1)
            
            sql = "INSERT INTO pr_productcode(id,pid,company,product_code,pcount) VALUES (%s, %s, %s, %s,%s)"
            val = (maxid2,maxid,company,kycode,i)
            cursor.execute(sql, val)
            mydb.commit()     
            
            i+=1
        

        
        sql = "INSERT INTO pr_product(id,category,product,company,price,description,location,mdate,edate,tdate,pcode,rdate,num_piece,code1,code2) VALUES (%s,%s,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        val = (maxid,cat,prd,company,price,description,location,mdate,edate,edate,pcode,rdate,num_piece,code1,code2)
        cursor.execute(sql, val)
        mydb.commit()            
        print(cursor.rowcount, "Added Success")
        result="success"

        bcdata="PID:"+str(maxid)+", Product:"+prd+", Company:"+company+", Manufacture:"+mdate+",Expiry Date:"+edate+", KYP Code:"+code1+" to "+code2
        productchain(str(maxid),uname,bcdata,'PC')
        ##BC##
        '''sdata="PID:"+str(maxid)+", Product:"+prd+", Company:"+company+", Manufacture:"+mdate+",KYP Code:"+code1+" to "+code2+", RegDate:"+rdate
        result = hashlib.md5(sdata.encode())
        key=result.hexdigest()

        mycursor1 = mydb.cursor()
        mycursor1.execute("SELECT max(id)+1 FROM pr_blockchain")
        maxid1 = mycursor1.fetchone()[0]
        if maxid1 is None:
            maxid1=1
            pkey="00000000000000000000000000000000"
        else:
            mid=maxid1-1
            cursor.execute('SELECT * FROM pr_blockchain where id=%s',(mid, ))
            pp = cursor.fetchone()
            pkey=pp[3]
        sql2 = "INSERT INTO pr_blockchain(id,block_id,pre_hash,hash_value,sdata,ptype) VALUES (%s, %s, %s, %s, %s,%s)"
        val2 = (maxid1,maxid,pkey,key,sdata,'PID')
        cursor.execute(sql2, val2)
        mydb.commit()  ''' 
        ####
        
        if cursor.rowcount==1:
            msg="success"
            return redirect(url_for('product',msg=msg))
        else:
            msg="fail"
            return redirect(url_for('product',msg=msg))
            #msg='Already Exist'

    
    return render_template('product.html',catt=catt,data=data,cnpr=cnpr)


@app.route('/dist', methods=['GET', 'POST'])
def dist():
    msg=""
    email=""
    mess=""
    owner=""
    st=""
    if 'username' in session:
        owner = session['username']
    ff1=open("log.txt","r")
    company=ff1.read()
    ff1.close()
    cursor = mydb.cursor()
    
    cursor.execute('SELECT * FROM pr_supplier where owner=%s order by id desc',(company, ))
    data = cursor.fetchall()

    cursor.execute('SELECT * FROM pr_send where company=%s',(company,))
    data2 = cursor.fetchall()

    now = datetime.datetime.now()
    rdate=now.strftime("%d-%m-%Y")
        
    if request.method=='POST':
        name=request.form['name']
        city=request.form['city']
        mobile=request.form['mobile']
        email=request.form['email']
        uname=request.form['uname']
        pass1=request.form['pass']
        name2=request.form['name2']
        gst_number=request.form['gst_number']
        

        cursor.execute('SELECT * FROM pr_supplier')
        result = cursor.fetchall()
        j=0
        for i in result:
            print(i[0])
            j+=1
        id2=j+1

        cursor.execute("SELECT count(*) FROM pr_supplier where uname=%s",(uname,))
        cnt = cursor.fetchone()[0]

        if cnt==0:
            cursor.execute("SELECT max(id)+1 FROM pr_supplier")
            maxid = cursor.fetchone()[0]
            if maxid is None:
                maxid=1
            #rd=str(rdate).split("-")
            #rdd=rd[2]+"-"+rd[1]+"-"+rd[0]
            sql = "INSERT INTO pr_supplier(id,owner,name,mobile,email,city,uname,pass,rdate,name2,gst_number) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            val = (maxid,company,name,mobile,email,city,uname,pass1,rdate,name2,gst_number)
            cursor.execute(sql, val)
            mydb.commit()
            st="1"
            link="http://localhost:5000/index_dist"
            mess="Dear "+name+", Distributed Account created, Username:"+uname+", Password"+pass1+", Link:"+link
            msg="success"
            ##BC##
            bcdata="DID:"+str(maxid)+", Distributor:"+name+", Company:"+company+", Mobile:"+mobile+", City:"+city+", RegDate:"+rdate
            productchain(str(maxid),uname,bcdata,'PC')
            
            msg="success"
            '''mycursor1 = mydb.cursor()
            mycursor1.execute("SELECT max(id)+1 FROM pr_blockchain")
            maxid1 = mycursor1.fetchone()[0]
            if maxid1 is None:
                maxid1=1
                pkey="00000000000000000000000000000000"
            else:
                mid=maxid1-1
                cursor.execute('SELECT * FROM pr_blockchain where id=%s',(mid, ))
                pp = cursor.fetchone()
                pkey=pp[3]
            sql2 = "INSERT INTO pr_blockchain(id,block_id,pre_hash,hash_value,sdata,ptype) VALUES (%s, %s, %s, %s, %s,%s)"
            val2 = (maxid1,maxid,pkey,key,sdata,'DID')
            cursor.execute(sql2, val2)
            mydb.commit()   
            ####
            link="http://localhost:5000/index_dist"
            message="Dear "+name+", Distributed Account created, Username:"+uname+", Password"+pass1+", Link:"+link
            url="http://iotcloud.co.in/testmail/sendmail.php?email="+email+"&message="+message
            webbrowser.open_new(url)
                
            if cursor.rowcount==1:
                return redirect(url_for('dist',act='1'))
            else:
                return redirect(url_for('dist',act='2'))
                #msg='Already Exist' '''

        else:
            msg="fail"
    return render_template('dist.html',msg=msg,data=data,data2=data2,email=email,mess=mess,st=st)




@app.route('/view_prd', methods=['GET', 'POST'])
def view_prd():
    msg=""
    act=""
    uname=""
    if 'username' in session:
        uname = session['username']
    print(uname)
    ff1=open("log.txt","r")
    company=ff1.read()
    ff1.close()
    
    now = datetime.datetime.now()
    rdate=now.strftime("%d-%m-%Y")
    
    cursor = mydb.cursor()

    cursor.execute('SELECT * FROM pr_supplier where owner=%s',(company, ))
    catt = cursor.fetchall()
    # where status=0
    cursor.execute('SELECT * FROM pr_product where company=%s',(company, ))
    data = cursor.fetchall()

    '''if request.method=='POST':
        prd_from=request.form['prd_from']
        prd_to=request.form['prd_to']
        supplier=request.form['supplier']
        p1=int(prd_from)
        p2=int(prd_to)
        #cursor.execute("SELECT count(*) FROM pr_product where id=%s && status=0",(prd_from, ))
        #cnt = cursor.fetchone()[0]
        #cursor.execute("SELECT count(*) FROM pr_product where id=%s && status=0",(prd_to, ))
        #cnt2 = cursor.fetchone()[0]
        if cnt>0 and cnt2>0 and p1<=p2:
            i=p1

            
            cursor.execute("SELECT max(id)+1 FROM pr_send")
            maxid2 = cursor.fetchone()[0]
            if maxid2 is None:
                maxid2=1
            sql3 = "INSERT INTO pr_send(id,prd_from,prd_to,supplier,rdate) VALUES (%s, %s, %s, %s, %s)"
            val3 = (maxid2,prd_from,prd_to,supplier,rdate)
            cursor.execute(sql3, val3)
                
                    
            while i<=p2:
                cursor.execute('update pr_product set supplier=%s,status=1 WHERE id = %s', (supplier, i))
                mydb.commit()
                ##BC##
                sdata="PID:"+str(i)+", Distribute to:"+supplier+", RegDate:"+rdate
                result = hashlib.md5(sdata.encode())
                key=result.hexdigest()

                mycursor1 = mydb.cursor()
                mycursor1.execute("SELECT max(id)+1 FROM pr_blockchain")
                maxid1 = mycursor1.fetchone()[0]
                if maxid1 is None:
                    maxid1=1
                    pkey="00000000000000000000000000000000"
                else:
                    mid=maxid1-1
                    cursor.execute('SELECT * FROM pr_blockchain where id=%s',(mid, ))
                    pp = cursor.fetchone()
                    pkey=pp[3]
                sql2 = "INSERT INTO pr_blockchain(id,block_id,pre_hash,hash_value,sdata,ptype) VALUES (%s, %s, %s, %s, %s,%s)"
                val2 = (maxid1,i,pkey,key,sdata,'PID')
                cursor.execute(sql2, val2)
                mydb.commit()   
                ####
                i+=1
            act="1"
            msg="Distributed Success"
            return redirect(url_for('view_prd'))
            
        else:
            act="2"
            msg="Product ID not available!"'''

    return render_template('view_prd.html',data=data,catt=catt,act=act,msg=msg)

@app.route('/prd_send', methods=['GET', 'POST'])
def prd_send():
    msg=""
    act=""
    uname=""
    if 'username' in session:
        uname = session['username']
    print(uname)
    ff1=open("log.txt","r")
    company=ff1.read()
    ff1.close()

    pid = request.args.get('pid')
    
    now = datetime.datetime.now()
    rdate=now.strftime("%d-%m-%Y")
    
    cursor = mydb.cursor()

    cursor.execute('SELECT * FROM pr_supplier where owner=%s',(company, ))
    catt = cursor.fetchall()
    # where status=0
    cursor.execute('SELECT * FROM pr_product where id=%s',(pid, ))
    dd1 = cursor.fetchone()
    tot=dd1[21]
    pcode=dd1[9]
    tot1=str(tot)

    if request.method=='POST':
        num_prd=request.form['num_prd']
        supp=request.form['supplier']
        pid=request.form['pid']

        num=int(num_prd)
        cursor.execute('SELECT sum(num_prd) FROM pr_send where pid=%s',(pid, ))
        sn1 = cursor.fetchone()[0]
        if sn1 is None:
            sn1=0
        bal=tot-sn1

        
        
        
        if bal>=num:

            num_start=sn1+1
            num_end=sn1+num
            num_s=str(num_start)
            num_e=str(num_end)
            plen=len(tot1)
            numStr1 = num_s.zfill(plen)
            numStr2 = num_e.zfill(plen)
            code1=pcode+"P"+numStr1
            code2=pcode+"P"+numStr2

            balance=tot-num_end
            
            cursor.execute("SELECT max(id)+1 FROM pr_send")
            maxid2 = cursor.fetchone()[0]
            if maxid2 is None:
                maxid2=1
            sql3 = "INSERT INTO pr_send(id,pid,num_prd,prd_from,prd_to,prd1,prd2,company,supplier,rdate) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            val3 = (maxid2,pid,num_prd,code1,code2,num_start,num_end,company,supp,rdate)
            cursor.execute(sql3, val3)
            mydb.commit()
                    
            
            cursor.execute('update pr_product set distribute=%s,balance=%s WHERE id = %s', (num_end,balance, pid))
            mydb.commit()

            cursor.execute('update pr_productcode set supplier=%s WHERE pid = %s && pcount between %s and %s', (supp, pid, num_start, num_end))
            mydb.commit()

            bcdata="PID:"+pid+", Distribute to:"+supp+", Company:"+company+", Pcode:"+num_s+" to "+num_e+", RegDate:"+rdate
            productchain(str(maxid2),uname,bcdata,'PC')
            ##BC##
            '''sdata="PID:"+pid+", Distribute to:"+supp+", Company:"+company+", Pcode:"+num_s+" to "+num_e+", RegDate:"+rdate
            result = hashlib.md5(sdata.encode())
            key=result.hexdigest()

            mycursor1 = mydb.cursor()
            mycursor1.execute("SELECT max(id)+1 FROM pr_blockchain")
            maxid1 = mycursor1.fetchone()[0]
            if maxid1 is None:
                maxid1=1
                pkey="00000000000000000000000000000000"
            else:
                mid=maxid1-1
                cursor.execute('SELECT * FROM pr_blockchain where id=%s',(mid, ))
                pp = cursor.fetchone()
                pkey=pp[3]
            sql2 = "INSERT INTO pr_blockchain(id,block_id,pre_hash,hash_value,sdata,ptype) VALUES (%s, %s, %s, %s, %s,%s)"
            val2 = (maxid1,pid,pkey,key,sdata,'PID')
            cursor.execute(sql2, val2)
            mydb.commit() '''  
            ####
                
            act="1"
            msg="Distributed Success"
            return redirect(url_for('view_prd'))
            
        else:
            act="2"
            msg="Product not available!"

    return render_template('prd_send.html',catt=catt,act=act,msg=msg,pid=pid)

@app.route('/view_req', methods=['GET', 'POST'])
def view_req():
    ff1=open("log.txt","r")
    company=ff1.read()
    ff1.close()
    data=[]
    
    cursor = mydb.cursor()

    #cursor.execute('SELECT * FROM pr_supplier where owner=%s',(company, ))
    #dd1 = cursor.fetchone()
    #company=dd1[1]

    cursor.execute('SELECT * FROM pr_request where company=%s',(company, ))
    data1 = cursor.fetchall()
    for ss in data1:
        data3=[]
        cursor.execute('SELECT * FROM pr_product where id=%s',(ss[1], ))
        dd2 = cursor.fetchone()
        data3.append(ss[1])
        data3.append(dd2[2])
        data3.append(dd2[5])
        data3.append(ss[2])
        data3.append(ss[3])
        data.append(data3)

    return render_template('view_req.html',data=data)

@app.route('/dist_home', methods=['GET', 'POST'])
def dist_home():
    msg=""
    #supplier=""
    #if 'username' in session:
    #    supplier = session['username']

    ff1=open("log2.txt","r")
    supplier=ff1.read()
    ff1.close()
    
    cursor = mydb.cursor()
    
    cursor.execute('SELECT * FROM pr_shop where distributor=%s',(supplier, ))
    data = cursor.fetchall()

    cursor.execute('SELECT * FROM pr_supplier where uname=%s',(supplier, ))
    data1 = cursor.fetchone()
    company=data1[1]

    #cursor.execute('SELECT * FROM pr_send')
    #data2 = cursor.fetchall()

    now = datetime.datetime.now()
    rdate=now.strftime("%d-%m-%Y")
        
    if request.method=='POST':
        name=request.form['name']
        city=request.form['city']
        mobile=request.form['mobile']
        email=request.form['email']
        uname=request.form['uname']
        pass1=request.form['pass']
        name2=request.form['name2']
        

        
        cursor.execute("SELECT max(id)+1 FROM pr_shop")
        maxid = cursor.fetchone()[0]
        if maxid is None:
            maxid=1
        
        sql = "INSERT INTO pr_shop(id,owner,distributor,name,mobile,email,city,uname,pass,name2) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        val = (maxid,company,supplier,name,mobile,email,city,uname,pass1,name2)
        cursor.execute(sql, val)
        mydb.commit()            
        print(cursor.rowcount, "Registered Success")
        result="sucess"

        bcdata="RID:"+str(maxid)+", Retailer:"+name+", Distributor:"+supplier+", Company:"+company+", City:"+city+", RegDate:"+rdate
        productchain(str(maxid),uname,bcdata,'PC')
        ##BC##
        '''sdata="RID:"+str(maxid)+", Retailer:"+name+", Distributor:"+supplier+", Company:"+company+", City:"+city+", RegDate:"+rdate
        result = hashlib.md5(sdata.encode())
        key=result.hexdigest()

        mycursor1 = mydb.cursor()
        mycursor1.execute("SELECT max(id)+1 FROM pr_blockchain")
        maxid1 = mycursor1.fetchone()[0]
        if maxid1 is None:
            maxid1=1
            pkey="00000000000000000000000000000000"
        else:
            mid=maxid1-1
            cursor.execute('SELECT * FROM pr_blockchain where id=%s',(mid, ))
            pp = cursor.fetchone()
            pkey=pp[3]
        sql2 = "INSERT INTO pr_blockchain(id,block_id,pre_hash,hash_value,sdata,ptype) VALUES (%s, %s, %s, %s, %s,%s)"
        val2 = (maxid1,maxid,pkey,key,sdata,'RID')
        cursor.execute(sql2, val2)
        mydb.commit()'''   
        ####
        link="http://localhost:5000/index_shop"
        message="Dear "+name+", Retailer Account created, Username:"+uname+", Password"+pass1+", Link:"+link
        url="http://iotcloud.co.in/testmail/testmail1.php?email="+email+"&message="+message+"&subject=Retailer"
        webbrowser.open_new(url)
            
        if cursor.rowcount==1:
            return redirect(url_for('dist_home',act='1'))
        else:
            return redirect(url_for('dist_home',act='2'))
            #msg='Already Exist' 
    return render_template('dist_home.html',msg=msg,data=data,data1=data1)

@app.route('/dist_online', methods=['GET', 'POST'])
def dist_online():
    msg=""
    act=request.args.get("act")
    #supplier=""
    #if 'username' in session:
    #    supplier = session['username']

    ff1=open("log2.txt","r")
    supplier=ff1.read()
    ff1.close()
    
    cursor = mydb.cursor()
    
    cursor.execute('SELECT * FROM pr_online_sale where supplier=%s',(supplier, ))
    data = cursor.fetchall()

    cursor.execute('SELECT * FROM pr_supplier where uname=%s',(supplier, ))
    data1 = cursor.fetchone()
    company=data1[1]

    if act=="yes":
        rid=request.args.get("rid")
        cursor.execute("update pr_online_sale set status=1 where id=%s",(rid,))
        mydb.commit()
        msg="ok"

    return render_template('dist_online.html',msg=msg,act=act,data=data,data1=data1)

@app.route('/comp_online', methods=['GET', 'POST'])
def comp_online():
    msg=""
    data1=[]
    act=request.args.get("act")
    #supplier=""
    #if 'username' in session:
    #    supplier = session['username']

    ff1=open("log.txt","r")
    company=ff1.read()
    ff1.close()
    
    cursor = mydb.cursor()
    
    cursor.execute('SELECT * FROM pr_online_sale where company=%s',(company, ))
    data = cursor.fetchall()


    if act=="yes":
        rid=request.args.get("rid")
        cursor.execute("update pr_online_sale set status=2 where id=%s",(rid,))
        mydb.commit()
        msg="ok"

    return render_template('comp_online.html',msg=msg,act=act,data=data,data1=data1)


@app.route('/shop_req', methods=['GET', 'POST'])
def shop_req():
    msg=""
    act=""
    sid=""
    supplier=""
    if 'username' in session:
        supplier = session['username']

    ff1=open("log.txt","r")
    company=ff1.read()
    ff1.close()
    cursor = mydb.cursor()

    ###Retailer approval
    cursor.execute('SELECT * FROM pr_shop where owner=%s', (company, ))
    data = cursor.fetchall()

    cursor.execute('SELECT * FROM pr_supplier where uname=%s',(supplier, ))
    data1 = cursor.fetchone()

    if request.method=='GET':
        sid = request.args.get('sid')
        if sid is None:
            print("sid")
        else:
            cursor.execute('update pr_shop set status=1 WHERE id = %s', (sid, ))
            mydb.commit()
            return redirect(url_for('shop_req',act='1'))

    return render_template('shop_req.html',msg=msg,data=data,data1=data1,act=act)

@app.route('/dist_prd', methods=['GET', 'POST'])
def dist_prd():
    msg=""
    act=""
    #uname=""
    #if 'username' in session:
    #    uname = session['username']
    #print(uname)
    ff1=open("log2.txt","r")
    supplier=ff1.read()
    ff1.close()
    
    now = datetime.datetime.now()
    rdate=now.strftime("%d-%m-%Y")
    
    cursor = mydb.cursor()

    cursor.execute('SELECT * FROM pr_supplier where uname=%s',(supplier, ))
    dd1 = cursor.fetchone()
    company=dd1[1]

    cursor.execute('SELECT * FROM pr_shop where status=1')
    catt = cursor.fetchall()
    
    cursor.execute('SELECT * FROM pr_product where company=%s',(company, ))
    data = cursor.fetchall()

    if request.method=='POST':
        prd_from=request.form['prd_from']
        prd_to=request.form['prd_to']
        shop=request.form['shop']
        p1=int(prd_from)
        p2=int(prd_to)
        cursor.execute("SELECT count(*) FROM pr_product where id=%s && supplier=%s && status=1",(prd_from, uname ))
        cnt = cursor.fetchone()[0]
        cursor.execute("SELECT count(*) FROM pr_product where id=%s && supplier=%s && status=1",(prd_to, uname))
        cnt2 = cursor.fetchone()[0]
        if cnt>0 and cnt2>0 and p1<=p2:
            i=p1

            
            cursor.execute("SELECT max(id)+1 FROM pr_send2")
            maxid2 = cursor.fetchone()[0]
            if maxid2 is None:
                maxid2=1
            sql3 = "INSERT INTO pr_send(id,prd_from,prd_to,supplier,shop,rdate) VALUES (%s, %s, %s, %s, %s, %s)"
            val3 = (maxid2,prd_from,prd_to,supplier,shop,rdate)
            cursor.execute(sql3, val3)
                
                    
            while i<=p2:
                cursor.execute('update pr_product set shop=%s,status=1 WHERE id = %s', (shop, i))
                mydb.commit()

                bcdata="PID:"+str(i)+", Retailer:"+shop+", RegDate:"+rdate
                productchain(str(maxid2),shop,bcdata,'PC')
            
                ##BC##
                '''sdata="PID:"+str(i)+", Retailer:"+shop+", RegDate:"+rdate
                result = hashlib.md5(sdata.encode())
                key=result.hexdigest()

                mycursor1 = mydb.cursor()
                mycursor1.execute("SELECT max(id)+1 FROM pr_blockchain")
                maxid1 = mycursor1.fetchone()[0]
                if maxid1 is None:
                    maxid1=1
                    pkey="00000000000000000000000000000000"
                else:
                    mid=maxid1-1
                    cursor.execute('SELECT * FROM pr_blockchain where id=%s',(mid, ))
                    pp = cursor.fetchone()
                    pkey=pp[3]
                sql2 = "INSERT INTO pr_blockchain(id,block_id,pre_hash,hash_value,sdata,ptype) VALUES (%s, %s, %s, %s, %s,%s)"
                val2 = (maxid1,i,pkey,key,sdata,'PID')
                cursor.execute(sql2, val2)
                mydb.commit()'''   
                ####
                i+=1
            act="1"
            msg="Distributed Success"
            return redirect(url_for('view_prd'))
            
        else:
            act="2"
            msg="Product ID not available!"

    return render_template('dist_prd.html',data=data,catt=catt,act=act,msg=msg)

@app.route('/dist_send', methods=['GET', 'POST'])
def dist_send():
    ff1=open("log2.txt","r")
    supplier=ff1.read()
    ff1.close()
    
    now = datetime.datetime.now()
    rdate=now.strftime("%d-%m-%Y")

    cursor = mydb.cursor()

    cursor.execute('SELECT * FROM pr_supplier where uname=%s',(supplier, ))
    dd1 = cursor.fetchone()
    company=dd1[1]
    
    pid = request.args.get('pid')
    if request.method=='POST':
        num_prd=request.form['num_prd']
        pid=request.form['pid']

        cursor.execute("SELECT max(id)+1 FROM pr_request")
        maxid2 = cursor.fetchone()[0]
        if maxid2 is None:
            maxid2=1
        sql3 = "INSERT INTO pr_request(id,pid,num_prd,supplier,company,rdate) VALUES (%s, %s, %s, %s, %s, %s)"
        val3 = (maxid2,pid,num_prd,supplier,company,rdate)
        cursor.execute(sql3, val3)
            
                
        
        #cursor.execute('update pr_product set supplier=%s,status=1 WHERE id = %s', (supplier, i))
        #mydb.commit()
        ##BC##
        bcdata="PID:"+pid+",Distributor:"+supplier+", Request to "+company+", Required Products:"+num_prd+", RegDate:"+rdate
        productchain(str(maxid2),supplier,bcdata,'PC')
            
        '''sdata="PID:"+pid+",Distributor:"+supplier+", Request to "+company+", Required Products:"+num_prd+", RegDate:"+rdate
        result = hashlib.md5(sdata.encode())
        key=result.hexdigest()

        mycursor1 = mydb.cursor()
        mycursor1.execute("SELECT max(id)+1 FROM pr_blockchain")
        maxid1 = mycursor1.fetchone()[0]
        if maxid1 is None:
            maxid1=1
            pkey="00000000000000000000000000000000"
        else:
            mid=maxid1-1
            cursor.execute('SELECT * FROM pr_blockchain where id=%s',(mid, ))
            pp = cursor.fetchone()
            pkey=pp[3]
        sql2 = "INSERT INTO pr_blockchain(id,block_id,pre_hash,hash_value,sdata,ptype) VALUES (%s, %s, %s, %s, %s,%s)"
        val2 = (maxid1,pid,pkey,key,sdata,'Req')
        cursor.execute(sql2, val2)
        mydb.commit()'''   
        ####
            
        act="1"
        msg="Distributed Success"
        return redirect(url_for('dist_sent'))
    
    return render_template('dist_send.html',pid=pid)
    
@app.route('/dist_sent', methods=['GET', 'POST'])
def dist_sent():
    ff1=open("log2.txt","r")
    supplier=ff1.read()
    ff1.close()
    data=[]
    
    cursor = mydb.cursor()

    cursor.execute('SELECT * FROM pr_supplier where uname=%s',(supplier, ))
    dd1 = cursor.fetchone()
    company=dd1[1]

    cursor.execute('SELECT * FROM pr_request where supplier=%s',(supplier, ))
    data1 = cursor.fetchall()
    for ss in data1:
        data3=[]
        cursor.execute('SELECT * FROM pr_product where id=%s',(ss[1], ))
        dd2 = cursor.fetchone()
        data3.append(ss[1])
        data3.append(dd2[2])
        data3.append(dd2[5])
        data3.append(ss[2])
        data3.append(ss[5])
        data.append(data3)
    
    return render_template('dist_sent.html',data=data)

@app.route('/dist_view', methods=['GET', 'POST'])
def dist_view():
    ff1=open("log2.txt","r")
    supplier=ff1.read()
    ff1.close()
    data=[]
    
    cursor = mydb.cursor()

    cursor.execute('SELECT * FROM pr_supplier where uname=%s',(supplier, ))
    dd1 = cursor.fetchone()
    company=dd1[1]

    cursor.execute('SELECT * FROM pr_send where supplier=%s',(supplier, ))
    data1 = cursor.fetchall()
    
    for ss in data1:
        data3=[]
        cursor.execute('SELECT * FROM pr_product where id=%s',(ss[1], ))
        dd2 = cursor.fetchone()
        data3.append(ss[1])
        data3.append(dd2[2])
        data3.append(dd2[5])
        data3.append(dd2[4])
        data3.append(ss[2])
        data3.append(ss[3])
        data3.append(ss[4])
        data3.append(ss[10])
        data3.append(ss[11])
        data3.append(ss[0])
        
        data3.append(ss[5])
        data3.append(ss[6])
        
        data.append(data3)
    
    return render_template('dist_view.html',data=data)

@app.route('/dist_sendprd', methods=['GET', 'POST'])
def dist_sendprd():
    st=""
    msg=""
    ff1=open("log2.txt","r")
    supplier=ff1.read()
    ff1.close()
    data=[]
    data3=[]
    expiry_st=""
    cursor = mydb.cursor()

    cursor.execute('SELECT * FROM pr_supplier where uname=%s',(supplier, ))
    dd1 = cursor.fetchone()
    company=dd1[1]

    pid = request.args.get('pid')
    rid = request.args.get('rid')
    
    now = datetime.datetime.now()
    rdate=now.strftime("%d-%m-%Y")

    rdd1=rdate.split('-')
    ####check expiry    
    cursor.execute("SELECT * FROM pr_product where id=%s",(pid,))
    dd4 = cursor.fetchone()
    edd=dd4[14]
    edd1=edd.split("-")
    ey=int(edd1[0])
    em=int(edd1[1])
    ed=int(edd1[2])

    ry=int(rdd1[2])
    rm=int(rdd1[1])
    rd=int(rdd1[0])
    
    from datetime import date

    date1 = date(ey, em, ed)
    date2 = date(ry, rm, rd)

    if date1 < date2:
        expiry_st="1"
    else:
        expiry_st="2"

    print(expiry_st)
    ############
    
    cursor.execute('SELECT * FROM pr_shop where distributor=%s && status=1',(supplier, ))
    catt = cursor.fetchall()
    # where status=0
    
    cursor.execute('SELECT * FROM pr_send where id=%s',(rid, ))
    sg1 = cursor.fetchone()
    tot=sg1[2]
    stnum=sg1[5]
    ednum=sg1[6]
    

    cursor.execute('SELECT * FROM pr_product where id=%s',(pid, ))
    dd2 = cursor.fetchone()
    pcode=dd2[9]
    print(pcode)
    tot1=str(tot)

    if request.method=='POST':
        st="1"
        if expiry_st=="2":
            num_prd=request.form['num_prd']
            shopp=request.form['shopp']
            pid=request.form['pid']

            num=int(num_prd)
            cursor.execute('SELECT sum(num_prd) FROM pr_send2 where rid=%s',(rid, ))
            sn1 = cursor.fetchone()[0]
            if sn1 is None:
                sn1=0
            
            bal=tot-sn1

            
            
            
            if bal>=num:

                sn2=stnum+sn1

                num_start=sn2
                num_end=sn2+(num-1)
                num_s=str(num_start)
                num_e=str(num_end)
                plen=len(tot1)
                numStr1 = num_s.zfill(plen)
                numStr2 = num_e.zfill(plen)
                code1=pcode+"P"+numStr1
                code2=pcode+"P"+numStr2

                num3=sn1+num
                balance=tot-num3
                cursor.execute('update pr_send set distribute=%s,balance=%s WHERE id = %s ', (num3, balance, rid))
                mydb.commit()

                cursor.execute('update pr_productcode set shop=%s WHERE pid = %s && pcount between %s and %s', (shopp, pid, num_start, num_end,))
                mydb.commit()
                
                cursor.execute("SELECT max(id)+1 FROM pr_send2")
                maxid2 = cursor.fetchone()[0]
                if maxid2 is None:
                    maxid2=1
                sql3 = "INSERT INTO pr_send2(id,pid,num_prd,prd_from,prd_to,prd1,prd2,company,supplier,shop,rdate,rid) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                val3 = (maxid2,pid,num_prd,code1,code2,num_start,num_end,company,supplier,shopp,rdate,rid)
                cursor.execute(sql3, val3)
                mydb.commit()
                        
                
                
                ##BC##
                bcdata="PID:"+pid+", Distribute to:"+shopp+", Supplier:"+supplier+", Company:"+company+", Pcode:"+num_s+" to "+num_e+", RegDate:"+rdate
                productchain(str(maxid2),supplier,bcdata,'PC')
                
                '''sdata="PID:"+pid+", Distribute to:"+shopp+", Supplier:"+supplier+", Company:"+company+", Pcode:"+num_s+" to "+num_e+", RegDate:"+rdate
                result = hashlib.md5(sdata.encode())
                key=result.hexdigest()

                mycursor1 = mydb.cursor()
                mycursor1.execute("SELECT max(id)+1 FROM pr_blockchain")
                maxid1 = mycursor1.fetchone()[0]
                if maxid1 is None:
                    maxid1=1
                    pkey="00000000000000000000000000000000"
                else:
                    mid=maxid1-1
                    mycursor1.execute('SELECT * FROM pr_blockchain where id=%s',(mid, ))
                    pp = mycursor1.fetchone()
                    pkey=pp[3]
                sql2 = "INSERT INTO pr_blockchain(id,block_id,pre_hash,hash_value,sdata,ptype) VALUES (%s, %s, %s, %s, %s,%s)"
                val2 = (maxid1,pid,pkey,key,sdata,'PID')
                mycursor1.execute(sql2, val2)
                mydb.commit()   '''
                ####
                    
                act="1"
                msg="Distributed Success"
                return redirect(url_for('dist_view'))
                
            else:
                act="2"
                msg="Product not available!"

        else:
            
            msg="Product has Expired!!"
    
    return render_template('dist_sendprd.html',msg=msg,expiry_st=expiry_st,catt=catt,pid=pid,rid=rid,st=st)

@app.route('/dist_req', methods=['GET', 'POST'])
def dist_req():
    ff1=open("log2.txt","r")
    supplier=ff1.read()
    ff1.close()
    data=[]
    
    cursor = mydb.cursor()

    cursor.execute('SELECT * FROM pr_supplier where uname=%s',(supplier, ))
    dd1 = cursor.fetchone()
    company=dd1[1]

    cursor.execute('SELECT * FROM pr_request2 where supplier=%s',(supplier, ))
    data1 = cursor.fetchall()
    for ss in data1:
        data3=[]
        cursor.execute('SELECT * FROM pr_product where id=%s',(ss[1], ))
        dd2 = cursor.fetchone()
        data3.append(ss[1])
        data3.append(dd2[2])
        data3.append(dd2[5])
        data3.append(ss[2])
        data3.append(ss[6])
        data3.append(ss[3])
        data.append(data3)
    
    return render_template('dist_req.html',data=data)

@app.route('/dist_deliver', methods=['GET', 'POST'])
def dist_deliver():
    ff1=open("log2.txt","r")
    supplier=ff1.read()
    ff1.close()
    data=[]
    
    cursor = mydb.cursor()

    cursor.execute('SELECT * FROM pr_supplier where uname=%s',(supplier, ))
    dd1 = cursor.fetchone()
    company=dd1[1]

    cursor.execute('SELECT * FROM pr_send2 where supplier=%s',(supplier, ))
    data1 = cursor.fetchall()
    for ss in data1:
        data3=[]
        cursor.execute('SELECT * FROM pr_product where id=%s',(ss[1], ))
        dd2 = cursor.fetchone()
        data3.append(ss[1])
        data3.append(ss[3])
        data3.append(ss[4])
        data3.append(ss[2])
        data3.append(ss[9])
        data3.append(ss[12])
        data.append(data3)
    
    return render_template('dist_deliver.html',data=data)

@app.route('/shop_home', methods=['GET', 'POST'])
def shop_home():
    msg=""
    #supplier=""
    #if 'username' in session:
    #    supplier = session['username']

    ff1=open("log3.txt","r")
    shop=ff1.read()
    ff1.close()
    
    cursor = mydb.cursor()
    
    cursor.execute('SELECT * FROM pr_shop where uname=%s',(shop, ))
    data1 = cursor.fetchone()
    company=data1[1]
    supplier=data1[2]

    cursor.execute('SELECT * FROM pr_supplier where uname=%s',(supplier, ))
    data = cursor.fetchone()
    cursor.execute('SELECT * FROM pr_manufacture where uname=%s',(company, ))
    data2 = cursor.fetchone()
    

    now = datetime.datetime.now()
    rdate=now.strftime("%d-%m-%Y")
        
    return render_template('shop_home.html',msg=msg,data=data,data1=data1,data2=data2)

@app.route('/shop_distprd', methods=['GET', 'POST'])
def shop_distprd():
    msg=""
    #supplier=""
    #if 'username' in session:
    #    supplier = session['username']

    ff1=open("log3.txt","r")
    shop=ff1.read()
    ff1.close()
    data4=[]
    
    cursor = mydb.cursor()
    
    cursor.execute('SELECT * FROM pr_shop where uname=%s',(shop, ))
    data1 = cursor.fetchone()
    company=data1[1]
    supplier=data1[2]

    cursor.execute('SELECT * FROM pr_supplier where uname=%s',(supplier, ))
    data = cursor.fetchone()
    cursor.execute('SELECT * FROM pr_manufacture where uname=%s',(company, ))
    data2 = cursor.fetchone()
    
    cursor.execute('SELECT * FROM pr_send where supplier=%s',(supplier, ))
    data3 = cursor.fetchall()
    for ss in data3:
        dat=[]
        pid=ss[1]
        cursor.execute('SELECT * FROM pr_product where id=%s',(pid, ))
        dd2 = cursor.fetchone()
        dat.append(ss[1])
        dat.append(dd2[2])
        dat.append(dd2[5])
        dat.append(dd2[4])
        dat.append(ss[2])
        dat.append(ss[3])
        dat.append(ss[4])
        dat.append(ss[5])
        dat.append(ss[6])
        dat.append(ss[10])
        dat.append(ss[11])
        data4.append(dat)
        
    
    
    now = datetime.datetime.now()
    rdate=now.strftime("%d-%m-%Y")
        
    return render_template('shop_distprd.html',msg=msg,data=data,data1=data1,data2=data2,data4=data4)

@app.route('/shop_send', methods=['GET', 'POST'])
def shop_send():
    msg=""
    #supplier=""
    #if 'username' in session:
    #    supplier = session['username']

    ff1=open("log3.txt","r")
    shop=ff1.read()
    ff1.close()
    data4=[]
    dat=[]
    cursor = mydb.cursor()
    
    cursor.execute('SELECT * FROM pr_shop where uname=%s',(shop, ))
    data1 = cursor.fetchone()
    company=data1[1]
    supplier=data1[2]

    cursor.execute('SELECT * FROM pr_supplier where uname=%s',(supplier, ))
    data = cursor.fetchone()
    cursor.execute('SELECT * FROM pr_manufacture where uname=%s',(company, ))
    data2 = cursor.fetchone()
    
    
    
    now = datetime.datetime.now()
    rdate=now.strftime("%d-%m-%Y")
    pid = request.args.get('pid')
    if request.method=='POST':
        num_prd=request.form['num_prd']
        pid=request.form['pid']

        cursor.execute("SELECT max(id)+1 FROM pr_request2")
        maxid2 = cursor.fetchone()[0]
        if maxid2 is None:
            maxid2=1
        sql3 = "INSERT INTO pr_request2(id,pid,num_prd,shop,supplier,company,rdate) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        val3 = (maxid2,pid,num_prd,shop,supplier,company,rdate)
        cursor.execute(sql3, val3)
            
                
        
        #cursor.execute('update pr_product set supplier=%s,status=1 WHERE id = %s', (supplier, i))
        #mydb.commit()
        ##BC##
        bcdata="PID:"+pid+",:Retailer"+shop+", Request to "+supplier+", Required Products:"+num_prd+", RegDate:"+rdate
        productchain(str(maxid2),shop,bcdata,'PC')
        ''''sdata="PID:"+pid+",:Retailer"+shop+", Request to "+supplier+", Required Products:"+num_prd+", RegDate:"+rdate
        result = hashlib.md5(sdata.encode())
        key=result.hexdigest()

        mycursor1 = mydb.cursor()
        mycursor1.execute("SELECT max(id)+1 FROM pr_blockchain")
        maxid1 = mycursor1.fetchone()[0]
        if maxid1 is None:
            maxid1=1
            pkey="00000000000000000000000000000000"
        else:
            mid=maxid1-1
            cursor.execute('SELECT * FROM pr_blockchain where id=%s',(mid, ))
            pp = cursor.fetchone()
            pkey=pp[3]
        sql2 = "INSERT INTO pr_blockchain(id,block_id,pre_hash,hash_value,sdata,ptype) VALUES (%s, %s, %s, %s, %s,%s)"
        val2 = (maxid1,pid,pkey,key,sdata,'Req2')
        cursor.execute(sql2, val2)
        mydb.commit()   
        ####'''
            
        act="1"
        msg="Request Sent"
        return redirect(url_for('shop_sent'))
        
    return render_template('shop_send.html',msg=msg,data=data,data1=data1,data2=data2,pid=pid)

@app.route('/shop_sent', methods=['GET', 'POST'])
def shop_sent():
    msg=""
    #supplier=""
    #if 'username' in session:
    #    supplier = session['username']

    ff1=open("log3.txt","r")
    shop=ff1.read()
    ff1.close()
    
    cursor = mydb.cursor()
    
    cursor.execute('SELECT * FROM pr_shop where uname=%s',(shop, ))
    data1 = cursor.fetchone()
    company=data1[1]
    supplier=data1[2]

    
    data=[]

    cursor.execute('SELECT * FROM pr_request2 where shop=%s',(shop, ))
    data11 = cursor.fetchall()
    for ss in data11:
        data3=[]
        cursor.execute('SELECT * FROM pr_product where id=%s',(ss[1], ))
        dd2 = cursor.fetchone()
        data3.append(ss[1])
        data3.append(dd2[2])
        data3.append(dd2[5])
        data3.append(ss[2])
        data3.append(ss[6])
        data.append(data3)
        
    return render_template('shop_sent.html',msg=msg,data=data,data1=data1)

@app.route('/shop_product', methods=['GET', 'POST'])
def shop_product():
    msg=""
    #supplier=""
    #if 'username' in session:
    #    supplier = session['username']

    ff1=open("log3.txt","r")
    shop=ff1.read()
    ff1.close()
    
    cursor = mydb.cursor()
    
    cursor.execute('SELECT * FROM pr_shop where uname=%s',(shop, ))
    data1 = cursor.fetchone()
    company=data1[1]
    supplier=data1[2]

    
    data=[]

    cursor.execute('SELECT * FROM pr_send2 where supplier=%s',(supplier, ))
    data11 = cursor.fetchall()
    for ss in data11:
        data3=[]
        cursor.execute('SELECT * FROM pr_product where id=%s',(ss[1], ))
        dd2 = cursor.fetchone()
        data3.append(ss[1])
        data3.append(ss[3])
        data3.append(ss[4])
        data3.append(ss[2])
        data3.append(ss[9])
        data3.append(ss[12])
        data3.append(ss[0])
        data.append(data3)
        
    return render_template('shop_product.html',msg=msg,data=data,data1=data1)

@app.route('/shop_sale', methods=['GET', 'POST'])
def shop_sale():
    msg=""
    act=""
    kid=""
    st=""
    expiry_st=""
    #supplier=""
    #if 'username' in session:
    #    supplier = session['username']

    ff1=open("log3.txt","r")
    shop=ff1.read()
    ff1.close()

    now = datetime.datetime.now()
    rdate=now.strftime("%d-%m-%Y")
    pid = request.args.get('pid')
    rid = request.args.get('rid')
    
    cursor = mydb.cursor()
    
    cursor.execute('SELECT * FROM pr_shop where uname=%s',(shop, ))
    data1 = cursor.fetchone()
    company=data1[1]
    supplier=data1[2]

    
    data=[]

    cursor.execute('SELECT * FROM pr_product where id=%s',(pid, ))
    data2 = cursor.fetchone()
    pcode=data2[9]
    tot=data2[21]
    tot1=str(tot)
    plen=len(tot1)

    

    cursor.execute('SELECT * FROM pr_send2 where id=%s',(rid, ))
    data11 = cursor.fetchone()

    p1=data11[5]
    p2=data11[6]
    print(p1)
    print(" ")
    print(p2)

    cursor.execute('SELECT * FROM pr_productcode where pid=%s && pcount between %s and %s',(pid, p1,p2))
    data22 = cursor.fetchall()


    
    i=p1
    s="0"
    while i<p2:
        dat=[]

        num_start=i
        num_s=str(num_start)
        numStr1 = num_s.zfill(plen)
        code1=pcode+"P"+numStr1

        cursor.execute('SELECT count(*) FROM pr_sale where pcode=%s',(code1, ))
        dt = cursor.fetchone()[0]
        if dt>0:
            s="1"
        else:
            s="0"
            
        dat.append(i)
        dat.append(code1)
        dat.append(s)
        data.append(dat)
        i+=1

    #######
    
    if request.method=='GET':
        act=request.args.get('act')
        kid=request.args.get('kid')
        pcode2=request.args.get('pcode2')
        if act=="1":

            ####check expiry
            pid=request.args.get('pid')
            now = datetime.datetime.now()
            rdate=now.strftime("%d-%m-%Y")
            rdd1=rdate.split('-')
            cursor.execute("SELECT * FROM pr_product where id=%s",(pid,))
            dd4 = cursor.fetchone()
            edd=dd4[14]
            edd1=edd.split("-")
            ey=int(edd1[0])
            em=int(edd1[1])
            ed=int(edd1[2])

            ry=int(rdd1[2])
            rm=int(rdd1[1])
            rd=int(rdd1[0])
            
            from datetime import date

            date1 = date(ey, em, ed)
            date2 = date(ry, rm, rd)

            if date1 < date2:
                expiry_st="1"
            else:
                expiry_st="2"
            
            print(expiry_st)
            ############
            if expiry_st=="2":
                st="2"
                cursor.execute("SELECT max(id)+1 FROM pr_sale")
                maxid2 = cursor.fetchone()[0]
                if maxid2 is None:
                    maxid2=1
                sql3 = "INSERT INTO pr_sale(id,shop,pid,rid,kid,pcode,rdate) VALUES (%s, %s, %s, %s, %s, %s, %s)"
                val3 = (maxid2,shop,pid,rid,kid,pcode2,rdate)
                cursor.execute(sql3, val3)
                
                    
                cursor.execute('update pr_productcode set sale=1,sale_date=%s WHERE pid = %s && product_code=%s', (rdate,pid, pcode2))
                mydb.commit()
                
                #cursor.execute('update pr_send2 set supplier=%s,status=1 WHERE id = %s', (supplier, i))
                #mydb.commit()
                ##BC##
                bcdata="PID:"+pid+",:Retailer"+shop+", Product:"+pcode2+", RegDate:"+rdate
                productchain(str(maxid2),shop,bcdata,'PC')
                
                '''sdata="PID:"+pid+",:Retailer"+shop+", Product:"+pcode2+", RegDate:"+rdate
                result = hashlib.md5(sdata.encode())
                key=result.hexdigest()

                mycursor1 = mydb.cursor()
                mycursor1.execute("SELECT max(id)+1 FROM pr_blockchain")
                maxid1 = mycursor1.fetchone()[0]
                if maxid1 is None:
                    maxid1=1
                    pkey="00000000000000000000000000000000"
                else:
                    mid=maxid1-1
                    cursor.execute('SELECT * FROM pr_blockchain where id=%s',(mid, ))
                    pp = cursor.fetchone()
                    pkey=pp[3]
                sql2 = "INSERT INTO pr_blockchain(id,block_id,pre_hash,hash_value,sdata,ptype) VALUES (%s, %s, %s, %s, %s,%s)"
                val2 = (maxid1,pid,pkey,key,sdata,'Sale')
                cursor.execute(sql2, val2)
                mydb.commit()  ''' 
                ####
                    
                act="1"
                msg="Request Sent"
                return redirect(url_for('shop_sale',pid=pid,rid=rid))
            else:
                st="1"
            
        
    return render_template('shop_sale.html',msg=msg,data=data,data1=data1,data2=data2,pid=pid,rid=rid,data22=data22,st=st)

@app.route('/shop_sold', methods=['GET', 'POST'])
def shop_sold():
    msg=""
    act=""
    kid=""
    #supplier=""
    #if 'username' in session:
    #    supplier = session['username']

    ff1=open("log3.txt","r")
    shop=ff1.read()
    ff1.close()

    now = datetime.datetime.now()
    rdate=now.strftime("%d-%m-%Y")
    
    cursor = mydb.cursor()
    
    cursor.execute('SELECT * FROM pr_shop where uname=%s',(shop, ))
    data1 = cursor.fetchone()
    company=data1[1]
    supplier=data1[2]

    
    

    cursor.execute('SELECT * FROM pr_sale where shop=%s',(shop, ))
    data = cursor.fetchall()

    return render_template('shop_sold.html',msg=msg,data=data,data1=data1)

@app.route('/shop_online_req', methods=['GET', 'POST'])
def shop_online_req():
    msg=""
    act=""
    kid=""
    s1=""
    #supplier=""
    #if 'username' in session:
    #    supplier = session['username']

    ff1=open("log3.txt","r")
    shop=ff1.read()
    ff1.close()

    now = datetime.datetime.now()
    rdate=now.strftime("%d-%m-%Y")
    
    cursor = mydb.cursor()
    
    cursor.execute('SELECT * FROM pr_shop where uname=%s',(shop, ))
    data1 = cursor.fetchone()
    company=data1[1]
    supplier=data1[2]

    if request.method=='POST':
        web_url=request.form['web_url']
        cursor.execute("SELECT max(id)+1 FROM pr_online_sale")
        maxid = cursor.fetchone()[0]
        if maxid is None:
            maxid=1
        sql2 = "INSERT INTO pr_online_sale(id,shop,web_url,status,rdate,supplier,company) VALUES (%s, %s, %s, %s, %s,%s,%s)"
        val2 = (maxid,shop,web_url,'0',rdate,supplier,company)
        cursor.execute(sql2, val2)
        mydb.commit()
        msg="ok"

    cursor.execute('SELECT count(*) FROM pr_online_sale where shop=%s',(shop, ))
    cnt = cursor.fetchone()[0]
    if cnt>0:
        s1="1"

    cursor.execute('SELECT * FROM pr_online_sale where shop=%s',(shop, ))
    data = cursor.fetchall()
    

    return render_template('shop_online_req.html',msg=msg,data=data,data1=data1,s1=s1)

@app.route('/change1', methods=['GET', 'POST'])
def change1():
    msg=""
    cursor = mydb.cursor()
    if request.method=='POST':
        pid=request.form['pid']
        edate=request.form['edate']

        cursor.execute("update pr_product set edate=%s where id=%s",(edate,pid))
        mydb.commit()
        msg="ok"

    return render_template('change1.html',msg=msg)

@app.route('/logout')
def logout():
    # remove the username from the session if it is there
    session.pop('username', None)
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True,host='0.0.0.0', port=5000)
