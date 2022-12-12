import datetime
import os.path
import csv
import shutil
from tempfile import NamedTemporaryFile
from email_validator import validate_email, EmailNotValidError


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

    # this customer menu
    if str(choices) == '1':
        print('*** WELCOME TO CUSTOMER SUB MENU ***')
        print('')
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

        # Cutomer creation section
        if str(customer_choices) == '1':
            print('*** WELCOME TO CUSTOMER CREATE INTERFACE ***')
            print(' Please enter the required details?? ')
            name = input('enter your name\n')
            phone = input('enter your phone number')
            email = input('enter your email address')
            check_valid_email(email)
            created_at = datetime.datetime.now()
            status = input('select choices\n 1) active 2) inactive')

            file_exists = os.path.isfile('customer.csv')
            with open('customer.csv', 'a+') as customer_file:
                header = ['name', 'phone', 'email', 'status', 'created_at']

                writer = csv.DictWriter(
                    customer_file, delimiter=',', fieldnames=header)
                if not file_exists:
                    writer.writeheader()

                writer.writerow({'name': name, 'phone': phone, 'email': email,
                                'status': status, 'created_at': created_at})
                print('customer created successfully')

        # retrieve customer
        elif str(customer_choices) == '2':
            print(' WELCOME TO CUSTOMER RETRIVE SECTION ')

            name = input('PLEASE ENTER A VALID CUSTOMER NAME')

            with open('customer.csv') as read_customer:
                content = csv.DictReader(read_customer)
                result_found = False
                for particular_data in content:
                    if name == particular_data['name']:
                        print(particular_data)
                        result_found = True
                        break
                if not result_found:
                    print('No record found')  # need to be modified

        # delete customer
        elif str(customer_choices) == '3':
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

        # filtering the customer according to serch crietria
        elif str(customer_choices) == '4':
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
        elif str(customer_choices) == '5':
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

        elif str(customer_choices) == '5':
            print('thank you')

        else:
            print('please enter valid choices')
            customer_billing()

    # 2. subscription page
    elif str(choices) == '2':
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

        # subscription creation page
        if str(enter_choices) == '1':
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

                    else:
                        print('please enter valid customer name')

        # individual subscription viewing page
        elif str(enter_choices) == '2':
            print(' *** WELCOME TO CUSTOMER RETRIVE SECTION ***')
            name = input('''
            ***  PLEASE ENTER A VALID CUSTOMER NAME TO VIEW SUBSCRIPTION ***
            
            ''')

            with open('subscription.csv') as read_subscription:
                content = csv.DictReader(read_subscription)
                for particular_data in content:
                    if name == particular_data['customer_name']:
                        print(particular_data)

        # subscription deletion page
        elif str(enter_choices) == '3':
            print('*** WELCOME TO SUBSCRIPTION DELETE SCETION ***')
            customer_name = input(
                ' *** PLEASE ENTER NAME OF CUSTOMER TO DELETE SUBSCRIPTION ***\n')
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

        # subscription filtering section based on crietria
        elif str(enter_choices) == '4':
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
                if str(filter_item) == '4':
                    for result in content:
                        print(result)
                # displaying onlt paid subscriber
                elif str(filter_item) == '1':
                    paid_subscriber = (
                        filter(lambda x: x['status'] == 'paid', content))
                    for result in paid_subscriber:
                        print(result)

                # displaying only unpaid subscriber
                elif str(filter_item) == '2':
                    unpaid_subscriber = (
                        filter(lambda x: x['status'] == 'unpaid', content))
                    for result1 in unpaid_subscriber:
                        print(result1)

                # displaying all subscriber by amount arrange in descending order
                elif str(filter_item) == '3':
                    sorted_by_amount = sorted(
                        content, key=lambda value: value['amount'], reverse=True)
                    print(sorted_by_amount)

                # displaying all subscriber by amount arrange in ascending order
                elif str(filter_item) == '5':
                    sorted_by_amount = sorted(
                        content, key=lambda value: value['amount'])
                    print(sorted_by_amount)

                else:
                    print('thank you')

        # subscription update section
        elif str(enter_choices) == '5':
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
                            'select choices\n 1) paid\n 2) upaid\n')
                        # now updating value
                        rows['customer_name'], rows['amount'], rows['start_date'], rows['expiry_date'], rows[
                            'email'], rows['status'] = customer_name, amount, start_date, expiry_date, email, status

                    rows = {'customer_name': rows['customer_name'], 'amount': rows['amount'], 'start_date': rows['start_date'],
                            'expiry_date': rows['expiry_date'], 'email': rows['email'], 'status': rows['status']}
                    writer.writerow(rows)
            shutil.move(tempfile.name, filename)

        # exit the subscription page
        elif str(enter_choices) == '6':
            print('exit')

        else:
            print('enter valid option')

    elif choices == 3:
        print('thank you using services')
    else:
        print('enter the valid choice')


def check_valid_email(email):
    try:
      # validate and get info
        v = validate_email(email)
        # replace with normalized form
        email = v["email"]
    except EmailNotValidError as e:
        # email is not valid, exception message is human-readable form ma
        print(str(e))
        # return print customer_create()


customer_billing()
