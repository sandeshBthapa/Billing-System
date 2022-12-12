import datetime
import os.path
import csv
import shutil
from tempfile import NamedTemporaryFile


def customer_billing():
    print('*** WELCOME TO CUSTOMER BILLING SYSTEM ***')

    choices = input('''
    *************************************************
    Please Enter one option from the given
    1) Type 1 and press enter for customer menu
    2) Type 2 and press enter for subscription menu
    3) Type 3 and press enter to exit program

    *************************************************
    ''')

    choice_2 = {'1': customer_section, '2': subscription_page,
                '3': exit_all_program}

    if choices in choice_2:
        choice_2[choices]()

    else:
        print('invalid choices')
        customer_billing()


# creating a customer


def create_customer():
    print('*** WELCOME TO CUSTOMER CREATE INTERFACE ***')
    print(' Please enter the required details?? ')
    name = input('enter your name\n')

    file_exists = os.path.isfile('customer.csv')

    with open('customer.csv') as read_customer:
        reader = csv.DictReader(read_customer)
        for data in reader:
            if data['name'] == name:
                print('Name already exist !!!')
                return create_customer()
    phone = input('enter your phone number\n')
    email = input('enter your email address\n')
    created_at = datetime.datetime.now()
    status = input('select choices\n 1) active 2) inactive\n')

    with open('customer.csv', 'a+') as customer_file:
        header = ['name', 'phone', 'email', 'status', 'created_at']
        writer = csv.DictWriter(
            customer_file, delimiter=',', fieldnames=header)
        if not file_exists:
            writer.writeheader()

        writer.writerow({'name': name, 'phone': phone, 'email': email,
                        'status': status, 'created_at': created_at})


# retrieving individual customer
def customer_retrieve():
    print(' WELCOME TO CUSTOMER RETRIVE SECTION ')

    name = input('PLEASE ENTER A VALID CUSTOMER NAME\n')

    with open('customer.csv') as read_customer:
        content = csv.DictReader(read_customer)
        result_found = False
        for particular_data in content:
            if name == particular_data['name']:
                print(particular_data)
                result_found = True
                break
        if not result_found:
            print('No record found')
            customer_retrieve()

# deleting individual customer


def delete_customer():
    print('*** WELCOME TO CUSTOMER DELETE SCETION ***')
    customer_name = input('PLEASE ENTER NAME OF CUSTOMER')
    file_name = 'customer.csv'
    fileds_name = ['name', 'phone', 'email', 'status', 'created_at']
    tempfile_delete = NamedTemporaryFile(mode='w', delete=False)
    with open(file_name, 'r') as csv_file, tempfile_delete:
        reader = csv.DictReader(csv_file, fieldnames=fileds_name)
        writer = csv.DictWriter(
            tempfile_delete, fieldnames=fileds_name)
        for row in reader:
            if not str(customer_name) == row['name']:
                writer.writerow({'name': row['name'], 'phone': row['phone'], 'email': row['email'],
                                'status': row['status'], 'created_at': row['created_at']})
    shutil.move(tempfile_delete.name, file_name)

    # subscription deletion
    file_name = 'subscription.csv'
    fileds_name = ['customer_name', 'amount', 'start_date',
                   'expiry_date', 'email', 'status']
    tempfile_delete1 = NamedTemporaryFile(mode='w', delete=False)
    with open(file_name, 'r') as csv_file, tempfile_delete1:
        reader = csv.DictReader(csv_file, fieldnames=fileds_name)
        writer = csv.DictWriter(
            tempfile_delete1, fieldnames=fileds_name)
        for row in reader:
            if not str(customer_name) == row['customer_name']:
                writer.writerow({'customer_name': row['customer_name'], 'amount': row['amount'], 'start_date': row['start_date'],
                                'expiry_date': row['expiry_date'], 'email': row['email'], 'status': row['status']})
    shutil.move(tempfile_delete1.name, file_name)


# filtering the customer according to serch crietria
def filtering_customer():
    print('WELCOME TO FILTER SECTION')
    print('PLEASE ENTER YOUR CHOICES')
    filter_item = input('1) all\n 2)active/inactive\n 3)exit')
    with open('customer.csv') as read_customer:
        content = csv.DictReader(read_customer)

        if filter_item == 'all':
            for result in content:
                print(result)
        elif filter_item == 'active':
            active_customer = (
                filter(lambda x: x['status'] == 'active', content))
            for result in active_customer:
                print(result)
        elif filter_item == 'inactive':
            inactive_customer = (
                filter(lambda x: x['status'] == 'inactive', content))
            for result1 in inactive_customer:
                print(result1)
        else:
            print('thank you')


# customer update section
def update_customer():
    print('*** WELCOME TO CUSTOMER UPDATE SCETION ***')
    filter_item = input('PLEASE ENTER NAME OF CUSTOMER')
    filename = 'customer.csv'
    tempfile = NamedTemporaryFile(mode='w', delete=False)
    fileds_name = ['name', 'phone', 'email', 'status', 'created_at']
    with open(filename, 'r') as csvfile, tempfile:
        reader = csv.DictReader(csvfile, fieldnames=fileds_name)
        writer = csv.DictWriter(tempfile, fieldnames=fileds_name)
        for rows in reader:
            if rows['name'] == filter_item:
                phone = input('enter your phone number')
                email = input('enter your email address')
                created_at = datetime.datetime.now()
                status = input('''
                        select choices
                         1) active
                         2) inactive

                        ''')

                # now updating value
                rows['name'], rows['phone'], rows['email'], rows['status'], rows[
                    'created_at'] = filter_item, phone, email, status, created_at

            rows = {'name': rows['name'], 'phone': rows['phone'], 'email': rows['email'],
                    'status': rows['status'], 'created_at': rows['created_at']}
            writer.writerow(rows)
    shutil.move(tempfile.name, filename)


def exit_program():
    print('Thank you for using our services')


# main section for customer
def customer_section():
    print('*** WELCOME TO CUSTOMER SUB MENU ***')

    customer_choices = input('''
        Please enter required number from the options
        1) create customer
        2) retrieve customer
        3) delete customer
        4) filter customer
        5) update customer
        6) Exit
        '''
                             )
    choices_2 = {'1': create_customer, '2': customer_retrieve,
                 '3': delete_customer, '4': filtering_customer, '5': update_customer,
                 '6': exit_program}

    if customer_choices in choices_2:
        choices_2[customer_choices]()

    else:
        print('invalid choices')
        customer_section()


# this is for the subscription section

def create_subscription():
    print('WELCOME TO SUBSCRIPTION CREATE INTERFACE')
    customer_name = input('please enter the valid customer name\n')
    with open('customer.csv') as read_customer:
        content = csv.DictReader(read_customer)

        for particular_data in content:
            if customer_name == particular_data['name']:
                email = particular_data['email']
                amount = input('please enter your amount ')
                start_date = datetime.datetime.now()
                date_entry = input(
                    'Enter a expiry date in YYYY-MM-DD format')
                year, month, day = map(int, date_entry.split('-'))
                expiry_date = datetime.date(year, month, day)
                status = input('''
                        please select type
                         1)press 1 for paid
                         2)press 2 upaid
                        ''')

                file_exists = os.path.isfile('subscription.csv')
                with open('subscription.csv', 'a+') as customer_file:
                    header = ['customer_name', 'amount', 'start_date',
                              'expiry_date', 'email', 'status']
                    writer = csv.DictWriter(
                        customer_file, delimiter=',', fieldnames=header)
                    if not file_exists:
                        writer.writeheader()
                    writer.writerow({'customer_name': customer_name, 'amount': amount, 'start_date': start_date,
                                     'expiry_date': expiry_date, 'email': email,
                                     'status': status})
                    print('Subscription created successfully')
                    break
        else:
            print('given name not found !!!')
            create_subscription()


def retrieve_subscription():
    print(' *** WELCOME TO CUSTOMER RETRIVE SECTION ***')
    name = input(
        '***  PLEASE ENTER A VALID CUSTOMER NAME TO VIEW SUBSCRIPTION ***')

    with open('subscription.csv') as read_subscription:
        content = csv.DictReader(read_subscription)
        result_found = False
        for particular_data in content:
            if name == particular_data['customer_name']:
                print(particular_data)
                result_found = True
                break
        if not result_found:
            print('No record found')
            retrieve_subscription()


def delete_subscription():
    print('*** WELCOME TO SUBSCRIPTION DELETE SCETION ***')
    customer_name = input(
        ' *** PLEASE ENTER NAME OF CUSTOMER TO DELETE SUBSCRIPTION ***')
    file_name = 'subscription.csv'
    fileds_name = ['customer_name', 'amount', 'start_date',
                   'expiry_date', 'email', 'status']
    tempfile_delete = NamedTemporaryFile(mode='w', delete=False)
    with open(file_name, 'r') as csv_file, tempfile_delete:
        reader = csv.DictReader(csv_file, fieldnames=fileds_name)
        writer = csv.DictWriter(
            tempfile_delete, fieldnames=fileds_name)
        for row in reader:
            if not str(customer_name) == row['customer_name']:
                writer.writerow({'customer_name': row['customer_name'], 'amount': row['amount'], 'start_date': row['start_date'],
                                'expiry_date': row['expiry_date'], 'email': row['email'], 'status': row['status']})
    shutil.move(tempfile_delete.name, file_name)


def filtering_subscription():
    print('WELCOME TO FILTER SECTION')
    filter_item = input('''
           PLEASE ENTER YOUR PARTICULAR CHOICE
           1) paid
           2) unpaid
           3) amount by descending
           4) all
           5) amount by ascending
           ''')
    with open('subscription.csv') as read_customer:
        content = csv.DictReader(read_customer)
        # displaying all subscriber

        def allsub():
            for result in content:
                print(result)
            # displaying onlt paid subscriber

        def paid_sub():
            paid_subscriber = (
                filter(lambda x: x['status'] == 'paid', content))
            for result in paid_subscriber:
                print(result)

            # displaying only unpaid subscriber
        def unpaid():
            unpaid_subscriber = (
                filter(lambda x: x['status'] == 'unpaid', content))
            for result1 in unpaid_subscriber:
                print(result1)

            # displaying all subscriber by amount arrange in descending order
        def desc_amount():
            sorted_by_amount = sorted(
                content, key=lambda value: value['amount'], reverse=True)
            print(sorted_by_amount)

            # displaying all subscriber by amount arrange in ascending order
        def asc_amount():
            sorted_by_amount = sorted(
                content, key=lambda value: value['amount'])
            print(sorted_by_amount)

        choices = {'4': allsub, '1': paid_sub, '2': unpaid,
                   '3': desc_amount, '5': asc_amount}

        if filter_item in choices:
            choices[filter_item]()
        else:
            print('no match found')
            filtering_subscription()


def update_subscription():
    print('*** WELCOME TO SUBSCRIPTION UPDATE SCETION ***')
    customer_name = input('*** PLEASE ENTER NAME OF CUSTOMER ***')
    filename = 'subscription.csv'
    tempfile = NamedTemporaryFile(mode='w', delete=False)
    fileds_name = ['customer_name', 'amount', 'start_date',
                   'expiry_date', 'email', 'status']
    with open(filename, 'r') as csvfile, tempfile:
        reader = csv.DictReader(csvfile, fieldnames=fileds_name)
        writer = csv.DictWriter(tempfile, fieldnames=fileds_name)
        for rows in reader:
            if rows['customer_name'] == customer_name:
                amount = input('enter your phone number')
                email = input('enter your email address')
                start_date = datetime.datetime.now()
                date_entry = input(
                    'Enter a expiry date in YYYY-MM-DD format')
                year, month, day = map(int, date_entry.split('-'))
                expiry_date = datetime.date(year, month, day)
                status = input(
                    'select choices\n 1) paid\n 2) unpaid\n')
                # now updating value
                rows['customer_name'], rows['amount'], rows['start_date'], rows['expiry_date'], rows[
                    'email'], rows['status'] = customer_name, amount, start_date, expiry_date, email, status

            rows = {'customer_name': rows['customer_name'], 'amount': rows['amount'], 'start_date': rows['start_date'],
                    'expiry_date': rows['expiry_date'], 'email': rows['email'], 'status': rows['status']}
            writer.writerow(rows)
    shutil.move(tempfile.name, filename)


def exit_prog():
    print('thank for using subscription page')
    customer_section()


# main subscription section
def subscription_page():
    print(' *** WELCOME TO SUBSCRIPTION PAGE ***')

    enter_choices = (input('''
        Please Enter the required choice
        ************************************
        1) create subscription
        2) retrieve subscription
        3) delete subscription
        4) filter subscription
        5) update subscription
        6) Exit
        ************************************
        '''))

    subscription_choices = {'1': create_subscription, '2': retrieve_subscription,
                            '3': delete_subscription, '4': filtering_subscription, '5': update_subscription,
                            '6': exit_prog}

    if enter_choices in subscription_choices:
        subscription_choices[enter_choices]()

    else:
        print('invalid choices')
        subscription_page()


def exit_all_program():
    print('thank for using our program')


# main exit program
customer_billing()
