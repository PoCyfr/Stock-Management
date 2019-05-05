import sqlite3, csv
from bottle import route, run, debug, template, request, static_file, redirect


#create database of items
conn = sqlite3.connect('items.sqlite3')
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS ITEMS
         (BARCODE INT PRIMARY KEY     ,
         NAME           TEXT    ,
         DESCRIPTION    TEXT    ,
         PRICE          INT     ,
         MINQUANTITY    INT     ,
         AVAILABILITY   INT     );''')
cursor.close()

conn.close()


#create database of members debt
conn = sqlite3.connect('debt.sqlite3')
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS DEBT
         (NAME TEXT PRIMARY KEY     ,
        DEBT          INT     ,
         BALANCE    INT     );''')
cursor.close()
conn.close()


@route('/stock')
def show_list():
    conn = sqlite3.connect('items.sqlite3')
    c = conn.cursor()

    c.execute("SELECT * FROM items")
    rows = c.fetchall()

    output = template('items.html', rows=rows)

    c.close()

    return output



@route('/<filename>')
def help(filename):
    return static_file(filename, root=r'C:\Users\rap19\Desktop\fst_bar')



@route('/new', method='GET')
def new_item():
    barcode = request.GET.barcode.strip()
    name = request.GET.name.strip()
    price = request.GET.price.strip()
    availability = request.GET.availability.strip()
    minQuantity = request.GET.minQuantity.strip()
    description = request.GET.description.strip()
    conn = sqlite3.connect('items.sqlite3')
    c = conn.cursor()

    c.execute("INSERT INTO items (name, barcode, price, availability, minQuantity, description) VALUES (?,?,?,?,?,?)",
              (name, barcode, price, availability, minQuantity, description))


    conn.commit()
    c.close()
    redirect('/stock')

@route('/edit/<barcode:int>', method='GET')
def edit_item(barcode):
    name = request.GET.name.strip()
    price = request.GET.price.strip()
    availability = request.GET.availability.strip()
    minQuantity = request.GET.minQuantity.strip()
    description = request.GET.description.strip()
    conn = sqlite3.connect('items.sqlite3')
    c = conn.cursor()
    print(availability);
    c.execute("UPDATE items SET name=?, price=?, availability=?, minQuantity=?, description=? WHERE BARCODE LIKE ?",
              (name, price, availability, minQuantity, description, barcode))


    conn.commit()
    c.close()
    redirect('/stock')


@route('/delete/<delete:int>', method='GET')
def delete_item(delete):
    conn = sqlite3.connect('items.sqlite3')
    c = conn.cursor()

    c.execute("DELETE FROM items WHERE BARCODE LIKE ?", (delete,))

    conn.commit()
    c.close()

    redirect('/stock')

@route('/item/<no:int>')
def show_item(no):
    print("oka")


@route('/order', method='GET')
def order_by():
    conn = sqlite3.connect('items.sqlite3')
    c = conn.cursor()

    order = request.query.get('order')
    print(order)
    if(order=="1"): c.execute("SELECT * FROM items ORDER BY PRICE ASC")
    elif(order=="2"): c.execute("SELECT * FROM items ORDER BY PRICE DESC")
    elif (order == "3"):c.execute("SELECT * FROM items ORDER BY AVAILABILITY ASC")
    elif (order == "4"):c.execute("SELECT * FROM items ORDER BY AVAILABILITY DESC")
    elif (order == "5"):c.execute("SELECT * FROM items WHERE AVAILABILITY < MINQUANTITY")

    rows = c.fetchall()
    output = template('items.html', rows=rows)
    c.close()
    return output

@route('/search', method='GET')
def search():
    conn = sqlite3.connect('items.sqlite3')
    c = conn.cursor()

    searchChoice = request.query.get('searchChoice')
    searchText = request.query.get('searchText')

    c.execute("SELECT * FROM items WHERE "+searchChoice+" LIKE ?", (searchText,))
    print(searchChoice + searchText)
    rows = c.fetchall()
    output = template('items.html', rows=rows)
    c.close()
    return output


@route('/upload', method='POST')
def upload():
    conn = sqlite3.connect('items.sqlite3')
    c = conn.cursor()

    file = request.POST.file.strip()
    not_added=0
    with open(file, encoding='utf-8-sig') as f:
        reader = csv.reader(f)
        for field in reader:
            if not field or field is None: #if line is empty
                continue
            print(field)

            c.execute("SELECT rowid FROM items WHERE BARCODE = ?", (field[0],))
            data = c.fetchall()
            if len(data) == 0:
                print('added')
                c.execute("INSERT INTO items VALUES (?,?,?,?,?,?);", field)
            else:
                print('NOT added')
                not_added+=1




    print(not_added)
    conn.commit()
    conn.close()
    redirect('/stock')



@route('/debt')
def show_debt():
    conn = sqlite3.connect('debt.sqlite3')
    c = conn.cursor()

    c.execute("SELECT * FROM debt")
    rows = c.fetchall()

    output = template('debt.html', rows=rows)

    c.close()

    return output

@route('/newPerson', method='GET')
def new_item():
    name = request.GET.name.strip()
    debt = request.GET.debt.strip()
    balance = request.GET.balance.strip()

    conn = sqlite3.connect('debt.sqlite3')
    c = conn.cursor()

    c.execute("INSERT INTO debt (name, debt, balance) VALUES (?,?,?)",
              (name, debt, balance))


    conn.commit()
    c.close()
    redirect('/debt')


@route('/edit/<name>', method='GET')
def edit_item(name):
    debt = request.GET.debt.strip()
    balance = request.GET.balance.strip()

    conn = sqlite3.connect('debt.sqlite3')
    c = conn.cursor()

    c.execute("UPDATE debt SET debt=?, balance=? WHERE NAME LIKE ?",(debt, balance, name))


    conn.commit()
    c.close()
    redirect('/debt')

@route('/deletePerson/<delete>', method='GET')
def delete_item(delete):
    conn = sqlite3.connect('debt.sqlite3')
    c = conn.cursor()

    c.execute("DELETE FROM debt WHERE NAME LIKE ?", (delete,))

    conn.commit()
    c.close()

    redirect('/debt')

@route('/buy', method='GET')
def upload():
    conn = sqlite3.connect('items.sqlite3')
    c = conn.cursor()
    conn2 = sqlite3.connect('debt.sqlite3')
    c2 = conn2.cursor()

    balance = 0
    total=0
    file = request.GET.buyFile.strip()

    with open(file, encoding='utf-8-sig') as f:
        reader = csv.reader(f)
        name = next(reader)[0]
        avai = 0
        print(name)

        c2.execute("SELECT * FROM debt WHERE NAME = ?", (name,))
        person = c2.fetchall()
        if(len(person)==0):
            print("Person not found")
            redirect('/stock')
            return

        for row in person:
            balance = row[2]
            print("blance"+str(balance))

        for field in reader:
            if not field or field is None: #if line is empty
                continue
            print(field)

            c.execute("SELECT * FROM items WHERE BARCODE = ?", (field[0],))
            item = c.fetchall()

            for row in item:
                total += int(row[3])
                avai = int(row[5]) - int(field[1])

            c.execute("UPDATE items SET availability=?  WHERE BARCODE = ?", (avai, field[0]))


        balance -= total
        c2.execute("UPDATE debt SET BALANCE=? WHERE NAME = ?", (balance, name))
    print("total", str(balance))

    conn.commit()
    conn.close()
    conn2.commit()
    conn2.close()
    redirect('/stock')

run()
