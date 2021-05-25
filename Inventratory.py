from tkinter import *
from db_Invent import Database, Data
from tkinter import messagebox

d_b = Data('count.db')
db = Database('storage.db')
list_marked_to_sell = []
total = []


def search_item():
    item_list.delete(0, END)
    part_data = item_text.get()
    # desc_data = desc_text.get()

    if part_data is '':
        messagebox.showerror('Required Fields', 'Please include fields')
        return
    for row in db.fetch():
        if part_data in row[1]:
            item_list.insert(END, row)

    # if desc_data is '':
    #     messagebox.showerror('Required Fields', 'Please include Desc field')
    #     return
    # for row in db.fetch():
    #     if desc_data in row[3]:
    #         sell_list.insert(END, row)


def populate_list():
    item_list.delete(0, END)
    for row in db.fetch():
        item_list.insert(END, row)


def populate_total():
    total_list.delete(0, END)
    total_list.insert(END, ' ' + str(total_value))


def add_item():
    '''show error is used to stop an event from occurring while showing info about the error
    while show info is used to info about the error or info'''
    if item_text.get() == '' or qty_text.get() == '' or desc_text.get() == '' or price_text.get() == '':
        messagebox.showerror('Required Fileds', 'Please include all fields')
        return
    db.insert(item_text.get(), qty_text.get(),
              desc_text.get(), price_text.get())
    item_list.delete(0, END)
    item_list.insert(END, (item_text.get(), qty_text.get(),
                           desc_text.get(), price_text.get()))
    clear_input()
    item_entry.focus()
    populate_list()


# selecting item for adjustment or deleteing
def select_item(event):
    ''' Global is used to make a variable available through out the code'''
    try:
        global selected_item
        index = item_list.curselection()[0]
        selected_item = item_list.get(index)

        item_entry.delete(0, END)
        item_entry.insert(END, selected_item[1])
        qty_entry.delete(0, END)
        qty_entry.insert(END, selected_item[2])
        desc_entry.delete(0, END)
        desc_entry.insert(END, selected_item[3])
        price_entry.delete(0, END)
        price_entry.insert(END, selected_item[4])

    except Exception as e:
        raise e


def remove_item():
    db.remove(selected_item[0])
    clear_input()
    populate_list()


# Saving to output file and db also calling count from DB
d_b.insert('0')


def save_sell():
    global count
    for row in d_b.fetch():
        count = row
    add_count = count[0]
    print(add_count)
    count_value = int(add_count) + 1
    count = count_value
    file = open('Output_' + str(count_value) + '.txt', 'a')
    for line in list_marked_to_sell:
        file.write(str(line) + '\n')
    file.write('TOTAL: ' + str(total_value))
    d_b.update(count[0], str(count))
    clear_screen()


def sell_item():
    global total_value
    part_name = item_text.get()
    qty = qty_text.get()
    if part_name and qty is not '':

        for row in db.fetch():
            items_val = row

            print("----------")
            if part_name in items_val[1]:
                print(items_val[1], 'first')
                qtyz = items_val[2]
                price_ = int(items_val[4])
                price_value = int(qty) * price_
                # print('price value >>', price_value)
                # print(items_val[2])
                # print(items_val[3])
                # print(items_val[4])
                new_qtyz = int(qtyz) - int(qty)
                total.append(price_value)
                db.update(items_val[0], items_val[1], new_qtyz, items_val[3], items_val[4])

                total_value = 0
                for val in total:
                    total_value = total_value + val
                    total_value = total_value

                sell_list.insert(END, 'Part Name: ' + str(items_val[1]))
                sell_list.insert(END, 'Quantity: ' + str(qty))
                sell_list.insert(END, 'Desc: ' + str(items_val[3]))
                sell_list.insert(END, 'Price: ' + str(price_value))
                sell_list.insert(END, '      ')
                populate_total()

                list_marked_to_sell.append('Part Name: ' + str(items_val[1]))
                list_marked_to_sell.append('Quantity: ' + str(qty))
                list_marked_to_sell.append('Description: ' + str(items_val[3]))
                list_marked_to_sell.append('Price: ' + str(price_value))
                print(list_marked_to_sell)

                populate_list()
            else:
                print('Done')

    else:
        messagebox.showerror('Required Fields', 'Please add Name and QTY')
        return


def Update_item():
    db.update(selected_item[0], item_text.get(), qty_text.get(),
              desc_text.get(), price_text.get())
    populate_list()


def clear_input():
    item_entry.delete(0, END)
    qty_entry.delete(0, END)
    desc_entry.delete(0, END)
    price_entry.delete(0, END)


def clear_screen():
    item_entry.delete(0, END)
    qty_entry.delete(0, END)
    desc_entry.delete(0, END)
    price_entry.delete(0, END)
    sell_list.delete(0, END)
    total_list.delete(0, END)
    total.clear()
    list_marked_to_sell.clear()
    total_list.insert(END, ' ' + str(0))
    item_entry.focus()


# Create window object
app = Tk()

app.title('Inventory')
app.maxsize(1500, 720)
app.minsize(1250, 600)
app.geometry('1350x620')

# part
item_text = StringVar()
item_label = Label(app, text='Item Name', font=('bold', 14), pady=20, padx=10)
item_label.grid(row=0, column=0, sticky=W)
item_entry = Entry(app, textvariable=item_text, width=30)
item_entry.grid(row=0, column=1,  sticky=W)

# Quantity
qty_text = StringVar()
qty_label = Label(app, text='Quantity', font=('bold', 14), padx=10)
qty_label.grid(row=0, column=2, sticky=W)
qty_entry = Entry(app, textvariable=qty_text, width=30)
qty_entry.grid(row=0, column=3)

# Description
desc_text = StringVar()
desc_label = Label(app, text='Description', font=('bold', 14), padx=10)
desc_label.grid(row=1, column=0, sticky=W)
desc_entry = Entry(app, textvariable=desc_text, width=30)
desc_entry.grid(row=1, column=1, sticky=W)

# Price
price_text = StringVar()
price_label = Label(app, text='Price', font=('bold', 14), padx=10)
price_label.grid(row=1, column=2, sticky=W)
price_entry = Entry(app, textvariable=price_text, width=30)
price_entry.grid(row=1, column=3)

# Parts List (Listbox)
item_list = Listbox(app, height=20, width=80, border=0)
item_list.grid(row=3, column=0, columnspan=2, rowspan=5, padx=15)

# Create Scroll bar
scrollbar = Scrollbar(app)
scrollbar.grid(row=3, column=2)
# setting scroll to list box
item_list.configure(yscrollcommand=scrollbar.set)
scrollbar.configure(command=item_list.yview)
# Bind select
item_list.bind('<<ListboxSelect>>', select_item)

# selling List (Listbox)
sell_list = Listbox(app, height=20, width=80, border=0)
sell_list.grid(row=3, column=3, columnspan=2, rowspan=5, padx=15)

# Create Scroll bar 2
scrollbar = Scrollbar(app)
scrollbar.grid(row=3, column=5)
# setting scroll to list box
sell_list.configure(yscrollcommand=scrollbar.set)
scrollbar.configure(command=sell_list.yview)
# Bind select
sell_list.bind('<<ListboxSelect>>', select_item)

# Total Price Box
total_label = Label(app, text='TOTAL:', font=('bold', 14), pady=5)
total_label.grid(row=8, column=4)
total_list = Listbox(app, height=2, width=7, border=1)
total_list.grid(row=8, column=4, rowspan=5, columnspan=2, padx=20, pady=5)

# Buttons
add_btn = Button(app, text='Add Part', width=12, command=add_item)
add_btn.grid(row=2, column=0, pady=15)

remove_btn = Button(app, text='Remove Part', width=12, command=remove_item)
remove_btn.grid(row=2, column=1)

update_btn = Button(app, text='Update Part', width=12, command=Update_item)
update_btn.grid(row=2, column=2)

clear_btn = Button(app, text='Clear Inputs', width=12, command=clear_input)
clear_btn.grid(row=2, column=3)

search_btn = Button(app, text='Search', width=12, command=search_item)
search_btn.grid(row=2, column=4, padx=5)

sell_btn = Button(app, text='Sell', width=12, command=sell_item)
sell_btn.grid(row=2, column=5, padx=30)

save_btn = Button(app, text='SAVE SELL', width=12, command=save_sell)
save_btn.grid(row=8, column=1, columnspan=2)

# Populate data
populate_list()
total_list.insert(END, ' ' + str(0))

# start program
app.mainloop()