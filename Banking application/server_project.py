import mysql.connector
import socket
import threading as td

host = socket.gethostname()
port = 5000

server_socket = socket.socket()
server_socket.bind((host, port))

server_socket.listen(1)

def handle_open_account(server_socket):
    mydb = mysql.connector.connect(host='localhost', user='root', password='Vikash04', database='bank_management')
    data = server_socket.recv(1024).decode()
    n, ac, db, add, cn, ob, p = data.split(',')
    data1 = (n, ac, db, add, cn, ob, p)
    data2 = (n, ac, ob, p)
    sql1 = 'INSERT INTO account VALUES (%s, %s, %s, %s, %s, %s, %s)'
    sql2 = 'INSERT INTO amount VALUES (%s, %s, %s, %s)'
    x = mydb.cursor()
    try:
        x.execute(sql1, data1)
    except Exception as e :
        print(e)
        server_socket.send("error pk".encode())
    server_socket.send("Account created successfully".encode())
    x.execute(sql2, data2)
    mydb.commit()
    mydb.close()
    print("Data Entered successfully")

def handle_deposit_amount(server_socket):
    mydb = mysql.connector.connect(host='localhost', user='root', password='Vikash04', database='bank_management')
    amount_info = server_socket.recv(1024).decode()
    amount, ac, p = amount_info.split(',')
    a = 'SELECT balance FROM amount WHERE AccNo = %s AND Pin = %s'
    data = (ac, p)
    x = mydb.cursor()
    x.execute(a, data)
    result = x.fetchone()
    updated_balance = result[0] + int(amount)
    sql = 'UPDATE amount SET balance = %s WHERE AccNo = %s'
    d = (updated_balance, ac)
    x.execute(sql, d)
    mydb.commit()
    server_socket.send(str(updated_balance).encode())  
    mydb.close()

def handle_withdraw_amount(server_socket):
    mydb = mysql.connector.connect(host='localhost', user='root', password='Vikash04', database='bank_management')
    amount_info = server_socket.recv(1024).decode()
    amount, ac, p = amount_info.split(',')
    a = 'SELECT balance FROM amount WHERE AccNo = %s AND Pin = %s'
    data = (ac,p)
    x = mydb.cursor()
    x.execute(a, data)
    result = x.fetchone()
    updated_balance = result[0] - int(amount)
    sql = 'UPDATE amount SET balance = %s WHERE AccNo = %s'
    d = (updated_balance, ac)
    x.execute(sql, d)
    mydb.commit()
    server_socket.send(str(updated_balance).encode())  
    mydb.close()


def handle_check_balance(server_socket):
    mydb = mysql.connector.connect(host='localhost', user='root', password='Vikash04', database='bank_management')
    data = server_socket.recv(1024).decode()

    ac,p = data.split(',')
    data = (ac,p)
    a = 'SELECT balance FROM amount WHERE AccNo = %s AND Pin = %s'
    x = mydb.cursor()
    x.execute(a, data)
    result = x.fetchone()

    if result:
        server_socket.send(str(result[0]).encode())
    else:
        print("Invalid account number")
        server_socket.send("Invalid account number or pin".encode())
    mydb.close()

def handle_display_details(server_socket):
    mydb = mysql.connector.connect(host='localhost', user='root', password='Vikash04', database='bank_management')
    data = server_socket.recv(1024).decode()
    ac,p = data.split(',')
    data = (ac,p)
    a = 'SELECT Name,AccNo,Balance FROM amount WHERE AccNo = %s AND Pin = %s'
    x = mydb.cursor()
    x.execute(a, data)
    result = x.fetchone()
    print(result)
    if result:
        formatted_details = f"Name: {result[0]}, Account No: {result[1]}, Balance: {result[2]}"
        print(formatted_details)
        server_socket.send(formatted_details.encode())
    else:
        server_socket.send("Invalid account number".encode()) 
    mydb.close()
 

def handle_close_account(server_socket):
    mydb = mysql.connector.connect(host='localhost', user='root', password='Vikash04', database='bank_management')
    data = server_socket.recv(1024).decode()
    ac,p = data.split(',')
    data = (ac,p)
    a = 'SELECT Name FROM amount WHERE AccNo = %s AND Pin = %s'

    sql1 = 'DELETE FROM account WHERE AccNo = %s'
    sql2 = 'DELETE FROM amount WHERE AccNo = %s'

    x = mydb.cursor()
    x.execute(a, data)
    result = x.fetchone()
    print(result)
    if result:
        x.execute(sql1, (ac,))
        x.execute(sql2, (ac,))
        server_socket.send("Account closed ".encode())
    else:
        server_socket.send("Account No or pin incorrect".encode())
    mydb.commit()
    mydb.close()

def handle_Transfer_amount(server_socket):
    mydb = mysql.connector.connect(host='localhost', user='root', password='Vikash04', database='bank_management')
    data = server_socket.recv(1024).decode()
    ac1, ac2, p, amount = data.split(',')
    print(data)
    
    # Update balance for account 1
    data1 = (ac1, p)
    print(data1)
    query_ac1 = 'SELECT balance FROM amount WHERE AccNo = %s AND Pin = %s'

    x = mydb.cursor()
    x.execute(query_ac1, data1)
    result_ac1 = x.fetchone()

    if result_ac1:
        updated_balance_ac1 = result_ac1[0] - int(amount)
        update_query_ac1 = 'UPDATE amount SET balance = %s WHERE AccNo = %s'
        data_ac1 = (updated_balance_ac1, ac1)
        x.execute(update_query_ac1, data_ac1)
        mydb.commit()
        # server_socket.send(str(updated_balance_ac1).encode())
    else:
        server_socket.send("Account 1 details not found".encode())
        x.close()  
        mydb.close()
    # Update balance for account 2
    data2 = (ac2, )
    print(data2)
    query_ac2 = 'SELECT balance FROM amount WHERE AccNo = %s'
    
    x.execute(query_ac2, data2)
    result_ac2 = x.fetchone()
    
    if result_ac2:
        updated_balance_ac2 = result_ac2[0] + int(amount)
        update_query_ac2 = 'UPDATE amount SET balance = %s WHERE AccNo = %s'
        data_ac2 = (updated_balance_ac2, ac2)
        x.execute(update_query_ac2, data_ac2)
        mydb.commit()
        res = "Amount transfered successfully. Current Balance ="+ str(updated_balance_ac1)
        server_socket.send(res.encode())
    else:
        server_socket.send("Account 2 details not found".encode())

    x.close()  
    mydb.close() 

def process_request(data):
    if data.lower().strip() == '1':
        return "OpenAcc"
    elif data.lower().strip() == '2':
        return "DepositAmount"
    elif data.lower().strip() == '3':
        return "WithdrawAmount"
    elif data.lower().strip() == '4':
        return "Balcheck"
    elif data.lower().strip() == '5':
        return "Disdetails"
    elif data.lower().strip() == '6':
        return "Transfer Amount"
    elif data.lower().strip() == '7':
        return "CloseAcc"
    else:
        return "Invalid request"
    
def handle(conn):
    while True:

        data = conn.recv(1024).decode()
        
        if not data or data.lower().strip() == 'exit':
            break
        
        response = process_request(data)

        if response == 'OpenAcc':
            handle_open_account(conn)
        elif response == 'DepositAmount':
            handle_deposit_amount(conn)
        elif response == 'WithdrawAmount':
            handle_withdraw_amount(conn)
        elif response == 'Balcheck':
            handle_check_balance(conn)
        elif response == 'Disdetails':
            handle_display_details(conn)
        elif response == 'CloseAcc':
            handle_close_account(conn)
        elif response == 'Transfer Amount':
            handle_Transfer_amount(conn)
        else:
            conn.send("Invalid request".encode())

def bank_server():
    print("Bank server started...")
    while True:
        conn, address = server_socket.accept()
        print("Connection from: " + str(address))

        thread = td.Thread(target=handle, args=(conn,))
        thread.start()

    conn.close()

if __name__ == '__main__':
    bank_server()
