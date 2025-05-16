FINE_PER_DAY = 1 # 1 rupee per day fine for late submission from the due date 
BORROW_PERIOD = 15 # Due date will be 15 DAYS from date of borrow.

import pandas as  p
fp = p.read_csv('Book_list.csv')

def getDate(a):
    import datetime
    now = datetime.datetime.now() + datetime.timedelta(days=a)
    return now.strftime('%d') + '-' + now.strftime('%m') + '-' + now.strftime('%Y')


def fine(a, b, cost_per_day):
    from datetime import datetime
    date_format = '%d-%m-%Y'
    d1 = datetime.strptime(a, date_format)
    d2 = datetime.strptime(b, date_format)
    diff = d2 - d1
    Fine = diff.days * (cost_per_day)
    if (Fine<0):
         return 0 
    else:
        return Fine


def aval():
    print('The available books are:')
    aval = []
    for i in range(fp.shape[0]):
        if fp.iloc[i, 2] == 'AVAILABLE':
            aval.append(fp.iloc[i, 0])
    print(aval)


def borrow():
    borrower_id = input('please input the ID: ') 
    if borrower_id in list(fp.loc[:, 'BORROWER ID']):
        l = list(fp.loc[:, 'BORROWER ID'])
        print('The borrowed books are:')
        for x in [i for i, x in enumerate(l) if x == borrower_id]:
            print(list(fp.loc[x]))

    def validd():
        global code
        code = (input('ENTER THE BOOK CODE OF THE BOOK TO BE BORROWED: '))
        if code not in list(fp.loc[:, 'BOOK CODE']):
            print('Please enter valid book code.')
            validd()

    validd()
    f2 = fp.set_index('BOOK CODE')
    col = f2.index.get_loc(code)
    if fp.iloc[col, 2] == 'BORROWED':
        print('This book is already borrowed.')
    else:
        fp.iloc[col, 2] = 'BORROWED'
        fp.iloc[col, 3] = borrower_id
        fp.iloc[col, 4] = getDate(BORROW_PERIOD)
        print(list(fp.loc[col]))
        print("Book borrowed successfully.")


def give_back():
    import datetime
    borrower_id = input('please input the ID ')
    if borrower_id not in list(fp.loc[:, 'BORROWER ID']):
        print('No books have been borrowed!')
    elif borrower_id in list(fp.loc[:, 'BORROWER ID']):
        l = list(fp.loc[:, 'BORROWER ID'])
        print('The borrowed books are:')
        for x in [i for i, x in enumerate(l) if x == borrower_id]:
            print(list(fp.loc[x]))

        def valid():
            code = input('Enter the book code of the book to be returned: ')
            if code in list(fp['BOOK CODE'].where(fp['BORROWER ID'] == borrower_id)):
                f2 = fp.set_index('BOOK CODE')
                col = f2.index.get_loc(code)
                fp.iloc[col, 2] = 'AVAILABLE'
                print('\nBook returned successfully.')
                print('LATE SUBMISSION FINE : ',fine(fp.iloc[col, 4], getDate(0), FINE_PER_DAY),'Rupees')
                fp.iloc[col, 3] = ''
                fp.iloc[col, 4] = ''

            else:
                print('Please enter valid book code.')
                valid()

        valid()


# start
while (True):
    print('')
    print("********************************************************************")
    print('                      LIBRARY MANAGEMENT SYSTEM                     ')
    print("Date: ",getDate(0))
    print("********************************************************************")
    print('')
    print("Enter 1. To Display all the books")
    print('Enter 2. To Display the available books.')
    print("Enter 3. To Borrow a book")
    print("Enter 4. To return a book")
    print("Enter 5. To Quit")
    opt = int(input())
    if opt == 1:
        print(fp)
    elif opt == 2:
        aval()
    elif opt == 3:
        borrow()
    elif opt == 4:
        give_back()
    elif opt == 5:
        fp.to_csv('Book_list.csv', index=False)
        exit()
    else:
        print('please enter valid input')
    fp.to_csv('Book_list.csv', index=False)
    print("")
    input("press ENTER..")
