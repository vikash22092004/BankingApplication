import socket
from flask import Flask, send_file, render_template, request, redirect



app = Flask(__name__)
host = socket.gethostname()
port = 5000

client_socket = socket.socket()
client_socket.connect((host, port))


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template("index.html")

@app.route('/openAccount',methods=['GET', 'POST'])
def openAccount():
    return render_template("openacc.html")


@app.route('/openAccount1',methods=['GET', 'POST'])
def openAccount1():
    message = "1"
    client_socket.send(message.encode())
    n = request.form['name']
    ac = request.form['accno']
    db = request.form['dob']
    add = request.form['address']
    cn= request.form['contact']
    ob = request.form['balance']
    pin = request.form['pin']
    data = f"{n},{ac},{db},{add},{cn},{ob},{pin}"
    try:
        client_socket.send(data.encode())
        return render_template("openacc.html",outval = "Account Created Successfully")
    except:
        return render_template("error.html")
    

@app.route('/deposit', methods=['GET', 'POST'])
def deposit():
    return render_template("depo.html")

@app.route('/deposit1', methods=['GET', 'POST'])
def deposit1():
    if request.method == 'POST':
        message = "2"
        client_socket.send(message.encode())
        ac = request.form['accno']
        pin = request.form['pin']
        amount = request.form['amount']
        data = f"{amount},{ac},{pin}"
        try:
            client_socket.send(data.encode())
            response = client_socket.recv(1024).decode()
            fresponse = "Amount Deposited Succesfully"
            return render_template("depo.html",fresponse=fresponse,updatedbalance = response)  
        except:
            return render_template("error.html")

@app.route('/withdraw', methods=['GET', 'POST'])
def withdraw():
    return render_template("withd.html")


@app.route('/withdraw1', methods=['GET', 'POST'])
def withdraw1():
    message = "3"
    client_socket.send(message.encode())
    ac = request.form['accno']
    pin = request.form['pin']
    amount = request.form['amount']
    data = f"{amount},{ac},{pin}"
    try:
        client_socket.send(data.encode())
        response = client_socket.recv(1024).decode()
        return render_template("withd.html",updatedbalance = response)  
    except:
        return render_template("error.html")

@app.route('/checkbalance', methods=['GET', 'POST'])
def balance():
    return render_template("balance.html")
 
@app.route('/balance1', methods=['GET', 'POST'])
def balance1():
    message = "4"
    client_socket.send(message.encode())
    ac = request.form['accno']
    pin = request.form['pin']
    data = f"{ac},{pin}"
    try:
        client_socket.send(data.encode())
        response = client_socket.recv(1024).decode()
        return render_template("balance.html",balance = response)  
    except:
        return render_template("error.html")    
@app.route('/Details', methods=['GET', 'POST'])
def details():
    return render_template("Details.html")

@app.route('/details1', methods=['GET', 'POST'])
def details1():
    message = "5"
    client_socket.send(message.encode())
    ac = request.form['accno']
    pin = request.form['pin']
    data = f"{ac},{pin}"
    try:
        client_socket.send(data.encode())
        response = client_socket.recv(1024).decode()
        return render_template("Details.html",response = response)  
    except:
        return render_template("error.html")  



    
@app.route('/transfer',methods=['GET','POST'])
def transfer():
    return render_template("transfer.html")

@app.route('/transfer1',methods=['GET','POST'])
def transfer1():
    message="6"
    client_socket.send(message.encode())
    ac = request.form['accno']
    transferac = request.form['baccno']
    pin = request.form['pin']
    amnt = request.form['amount']
    data = f"{ac},{transferac},{pin},{amnt}"
    try:
        client_socket.send(data.encode())
        response = client_socket.recv(1024).decode()
        return render_template("transfer.html",response = response)  
    except:
        return render_template("error.html")


@app.route('/deleteAccount', methods=['GET', 'POST'])
def deleteAccount():
    return render_template("delacc.html")

@app.route('/DeleteAccount1', methods=['GET', 'POST'])
def deleteAccount1():
    message = "7"
    client_socket.send(message.encode())
    ac = request.form['accno']
    pin = request.form['pin']
    data = f"{ac},{pin}"
    try:
        client_socket.send(data.encode())
        response = client_socket.recv(1024).decode()
        return render_template("delacc.html",delout = response)  
    except:
        return render_template("error.html")  

    # print("Connected to bank server")
    # print("Do You want to: 1 - Open an Account, 2 - Deposit Amount, 3 - Withdraw Amount, 4 - Check Balance, 5 - Display Customer Details, 6 - Close an Account, 7 - Exit")

    # while True:
    #     message = input("Enter your choice: ").strip().lower()

    #     if message == '7':
    #         client_socket.send(str('Exit').encode())
    #         break

    #     client_socket.send(message.encode())
        
    #     if message == '1': 
    #         n = input("Enter the Name: ")
    #         ac = input("Enter the Account No: ")
    #         db = input("Enter the Date of Birth: ")
    #         add = input("Enter the Address: ")
    #         cn = input("Enter your Contact No: ")
    #         ob = input("Enter the Opening balance: ")
    #         data = f"{n},{ac},{db},{add},{cn},{ob}"
    #         client_socket.send(data.encode())
        
    #     elif message == '2':  
    #         amount = input("Enter the amount you want to deposit: ")
    #         ac = input("Enter the Account No: ")
    #         pin = input("Enter the PIN: ")
    #         data = f"{amount},{ac},{pin}"
    #         client_socket.send(data.encode())
    #         response = client_socket.recv(1024).decode()
    #         print("Deposit Successful. Updated Balance:", response)  
            
    #     elif message == '3':  
    #         amount = input("Enter the amount you want to withdraw: ")
    #         ac = input("Enter the Account No: ")
    #         pin = input("Enter the PIN: ")
    #         data = f"{amount},{ac},{pin}"
    #         client_socket.send(data.encode())
    #         response = client_socket.recv(1024).decode()
    #         print("Withdrawal Successful. Updated Balance:", response)  
            
    #     elif message == '4':  
    #         ac = input("Enter the Account No: ")
    #         pin = input("Enter the PIN: ")
    #         data = f"{ac},{pin}"
    #         client_socket.send(data.encode())
    #         response = client_socket.recv(1024).decode()
    #         print("Current Balance:", response) 
        
    #     elif message == '5':  
    #         ac = input("Enter the Account No: ")
    #         client_socket.send(ac.encode())
    #         response = client_socket.recv(1024).decode()
    #         print("Customer Details:")
    #         print(response) 
        
    #     elif message == '6':  
    #         ac = input("Enter the Account No to close: ")
    #         client_socket.send(ac.encode())
    #         print("Account Closed Successfully.")
        
    #     else:
    #         data = client_socket.recv(1024).decode()
    #         print("Server Response:", data)


if __name__ == '__main__':
    try:
        app.run(debug=True)
    except:
        pass