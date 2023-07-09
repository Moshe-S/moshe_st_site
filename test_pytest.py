import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import re

# ==============================================================================================================
# Moshe Siman Tov   058-4494254
# python, selenium, pytest automation project.
# February 2023


@pytest.fixture()
def setup():
    driver = webdriver.Chrome()
    driver.get('https://svburger1.co.il/')      # open "SV Burger" website
    driver.implicitly_wait(5)
    driver.maximize_window()
    yield driver
    driver.close()      # close the test function


login_data = [['maximnudler4@gmail.com', 'max123']]     # login data of a registered user.


# sanity test:
@pytest.mark.parametrize('my_users', login_data)
def test_sanity(setup, my_users):
    # call the setup func to open and start the test func
    driver = setup  
    # click on "sign in" button
    driver.find_element(By.XPATH, '//a[@href="#/SignIn"]').click() 
    # insert email 
    driver.find_element(By.XPATH, '//input[@placeholder="Enter your email"]').send_keys(my_users[0])  
    # insert password 
    driver.find_element(By.XPATH, '//input[@type="password"]').send_keys(my_users[1])  
    # click on "sign in" button
    driver.find_element(By.XPATH, '//button[@type="submit"]').click()   
    # click on "kids meal" to select
    driver.find_element(By.XPATH, '//h5[text()="Kids Meal"]').click()  
    # scroll down the page
    driver.execute_script("window.scrollBy(0, 600)")    
    # wait for the page to scroll down
    time.sleep(0.5)    
    # click on "reserve" button
    driver.find_element(By.XPATH, '//button[text()=" Reserve "]').click()  
    # find the table num input field
    table_num = driver.find_element(By.XPATH, '//div[@class="row"]/div[5]/input')  
    # clear the table num field 
    table_num.clear()   
    # insert "1" to the table num field
    table_num.send_keys(1)    
    # click on "send" to finish the order
    driver.find_element(By.XPATH, '//button[text()="Send"]').click()  
    # popup modal with the order confirmation and information with:
    # summary
    summary = driver.find_element(By.XPATH, '//h3[text()=" Your order has been successfully received "]')   # title
    # display the order price, including 10% service fees 
    price = driver.find_element(By.XPATH, '//h2[text()="42.9"]')   
    # verifying order confirmation with the correct price
    assert summary.is_displayed() and price.is_displayed()     


# login with wrong password: Error message needs to popup, "Failed to log in"
@pytest.mark.parametrize('my_users', login_data)
def test_login_wrong_pass(setup, my_users):  
    driver = setup
    driver.find_element(By.XPATH, '//a[@href="#/SignIn"]').click()
    driver.find_element(By.XPATH, '//input[@placeholder="Enter your email"]').send_keys(my_users[0])
    driver.find_element(By.XPATH, '//input[@type="password"]').send_keys('moshe')   # this is a wrong password
    driver.find_element(By.XPATH, '//button[@type="submit"]').click()
    time.sleep(1)
    alert = driver.switch_to.alert
    assert alert.text == "Failed to log in"
    alert.accept()


# sign up suite:
# note: for every time we run the sign-up tests, the email addresses need to change.
def test_register_only_with_required_fields():  # sign up only with required field (func 1)
    driver = setup
    driver.find_element(By.XPATH, '//button[text()="Sign Up"]').click()
    driver.find_element(By.XPATH, '//input[@placeholder="Enter your email"]').send_keys('moshest30@gmail.com')
    driver.find_element(By.XPATH, '//input[@placeholder="Create Password"]').send_keys('Max123!')
    driver.find_element(By.XPATH, '//input[@placeholder="Confirm Password"]').send_keys('Max123!')
    driver.find_element(By.XPATH, '//button[text()="Sign Up"]').click()
    success = driver.find_element(By.XPATH, '//button[text()=" Log out "]')
    assert success.is_displayed()   # verifying registration success


# note: for the rest of the sign-up tests to work,
# it needs at least 2 characters in first name and in last name fields (because of a bug).
seven_data = [['moshest', 'st', 'moshest31@gmail.com', 'Max123!']]             # func 2
eight_data = [['mo', 'simantov', 'moshest32@gmail.com', 'Max123!']]            # func 3
five_eight_data = [['moshe', 'simantov', 'moshest33@gmail.com', 'Max123!']]    # fanc 4
walla_data = [['mo', 'st', 'moshest34@walla.com', 'Max123!']]                  # func 5
existing_data = [['moshe', 'simantov', 'moshe7st@gmail.com', 'moshe1234!']]    # EH 1
confirm_data = [['mo', 'st', 'moshest35@gmail.com', 'Max123!', 'mAx!321']]     # EH 2


@pytest.mark.parametrize('my_users', seven_data)
def test_seven_chars_first_name(setup, my_users):  # sign up with 7 chars on 1st name (func 2)
    driver = setup
    driver.find_element(By.XPATH, '//button[text()="Sign Up"]').click()
    driver.find_element(By.XPATH, '//input[@placeholder="Type your first name"]').send_keys(my_users[0])
    driver.find_element(By.XPATH, '//input[@placeholder="Type your last name"]').send_keys(my_users[1])
    driver.find_element(By.XPATH, '//input[@placeholder="Enter your email"]').send_keys(my_users[2])
    driver.find_element(By.XPATH, '//input[@placeholder="Create Password"]').send_keys(my_users[3])
    driver.find_element(By.XPATH, '//input[@placeholder="Confirm Password"]').send_keys(my_users[3])
    driver.find_element(By.XPATH, '//button[text()="Sign Up"]').click()
    success = driver.find_element(By.XPATH, '//button[text()=" Log out "]')
    assert success.is_displayed()   # verifying registration success


@pytest.mark.parametrize('my_users', eight_data)
def test_six_chars_last_name(setup, my_users):  # sign up with 8 chars on last name (func 3)
    driver = setup
    driver.find_element(By.XPATH, '//button[text()="Sign Up"]').click()
    driver.find_element(By.XPATH, '//input[@placeholder="Type your first name"]').send_keys(my_users[0])
    driver.find_element(By.XPATH, '//input[@placeholder="Type your last name"]').send_keys(my_users[1])
    driver.find_element(By.XPATH, '//input[@placeholder="Enter your email"]').send_keys(my_users[2])
    driver.find_element(By.XPATH, '//input[@placeholder="Create Password"]').send_keys(my_users[3])
    driver.find_element(By.XPATH, '//input[@placeholder="Confirm Password"]').send_keys(my_users[3])
    driver.find_element(By.XPATH, '//button[text()="Sign Up"]').click()
    success = driver.find_element(By.XPATH, '//button[text()=" Log out "]')
    assert success.is_displayed()   # verifying registration success


@pytest.mark.parametrize('my_users', five_eight_data)
def test_five_first_eight_last(setup, my_users):  # sign up with 5 chars on 1st name and 8 chars on last name (func 4)
    driver = setup
    driver.find_element(By.XPATH, '//button[text()="Sign Up"]').click()
    driver.find_element(By.XPATH, '//input[@placeholder="Type your first name"]').send_keys(my_users[0])
    driver.find_element(By.XPATH, '//input[@placeholder="Type your last name"]').send_keys(my_users[1])
    driver.find_element(By.XPATH, '//input[@placeholder="Enter your email"]').send_keys(my_users[2])
    driver.find_element(By.XPATH, '//input[@placeholder="Create Password"]').send_keys(my_users[3])
    driver.find_element(By.XPATH, '//input[@placeholder="Confirm Password"]').send_keys(my_users[3])
    driver.find_element(By.XPATH, '//button[text()="Sign Up"]').click()
    success = driver.find_element(By.XPATH, '//button[text()=" Log out "]')
    assert success.is_displayed()   # verifying registration success


@pytest.mark.parametrize('my_users', walla_data)
def test_walla_mail(setup, my_users):  # sign up with walla mail (func 5)
    driver = setup
    driver.find_element(By.XPATH, '//button[text()="Sign Up"]').click()
    driver.find_element(By.XPATH, '//input[@placeholder="Type your first name"]').send_keys(my_users[0])
    driver.find_element(By.XPATH, '//input[@placeholder="Type your last name"]').send_keys(my_users[1])
    driver.find_element(By.XPATH, '//input[@placeholder="Enter your email"]').send_keys(my_users[2])
    driver.find_element(By.XPATH, '//input[@placeholder="Create Password"]').send_keys(my_users[3])
    driver.find_element(By.XPATH, '//input[@placeholder="Confirm Password"]').send_keys(my_users[3])
    driver.find_element(By.XPATH, '//button[text()="Sign Up"]').click()
    success = driver.find_element(By.XPATH, '//button[text()=" Log out "]')
    assert success.is_displayed()   # verifying registration success


@pytest.mark.parametrize('my_users', existing_data)
def test_register_existing_mail(setup, my_users):  # sign up with existing mail (EH 1)
    driver = setup
    driver.find_element(By.XPATH, '//button[text()="Sign Up"]').click()
    driver.find_element(By.XPATH, '//input[@placeholder="Type your first name"]').send_keys(my_users[0])
    driver.find_element(By.XPATH, '//input[@placeholder="Type your last name"]').send_keys(my_users[1])
    driver.find_element(By.XPATH, '//input[@placeholder="Enter your email"]').send_keys(my_users[2])
    driver.find_element(By.XPATH, '//input[@placeholder="Create Password"]').send_keys(my_users[3])
    driver.find_element(By.XPATH, '//input[@placeholder="Confirm Password"]').send_keys(my_users[3])
    driver.find_element(By.XPATH, '//button[text()="Sign Up"]').click()
    time.sleep(1)
    alert = driver.switch_to.alert
    assert alert.text == "Error: The email address is already in use by another account."
    alert.accept()


@pytest.mark.parametrize('my_users', confirm_data)
def test_pass_and_confirm_different(setup, my_users):  # sign up password and Confirm Password are different (EH 2)
    driver = setup
    driver.find_element(By.XPATH, '//button[text()="Sign Up"]').click()
    driver.find_element(By.XPATH, '//input[@placeholder="Type your first name"]').send_keys(my_users[0])
    driver.find_element(By.XPATH, '//input[@placeholder="Type your last name"]').send_keys(my_users[1])
    driver.find_element(By.XPATH, '//input[@placeholder="Enter your email"]').send_keys(my_users[2])
    driver.find_element(By.XPATH, '//input[@placeholder="Create Password"]').send_keys(my_users[3])
    driver.find_element(By.XPATH, '//input[@placeholder="Confirm Password"]').send_keys(my_users[4])
    driver.find_element(By.XPATH, '//button[text()="Sign Up"]').click()
    alert = driver.switch_to.alert
    assert alert.text == "password and confirm error"
    alert.accept()


# ==============================================================================================================
# ordering suite:
# note: for the tests to pass, the price needs to be calculated without the tip, (it's a bug) except in the sanity test

@pytest.mark.parametrize('my_users', login_data)
def test_order_two_dishes(setup, my_users):  # ordering 2 dishes (func 1)
    driver = setup
    driver.find_element(By.XPATH, '//a[@href="#/SignIn"]').click()
    driver.find_element(By.XPATH, '//input[@placeholder="Enter your email"]').send_keys(my_users[0])
    driver.find_element(By.XPATH, '//input[@type="password"]').send_keys(my_users[1])
    driver.find_element(By.XPATH, '//button[@type="submit"]').click()
    driver.find_element(By.XPATH, '//h5[text()="Combo Meal"]').click()
    driver.find_element(By.XPATH, '//h5[text()="Vegan"]').click()
    driver.execute_script("window.scrollBy(0, 600)")
    time.sleep(0.5)
    driver.find_element(By.XPATH, '//button[text()=" Reserve "]').click()
    table_num = driver.find_element(By.XPATH, '//div[@class="popup"]/div/div/div/div[2]/div[4]/div[5]/input')
    table_num.clear()
    table_num.send_keys(1)
    driver.find_element(By.XPATH, '//button[text()="Send"]').click()
    summary = driver.find_element(By.XPATH, '//h3[text()=" Your order has been successfully received "]')
    price = driver.find_element(By.XPATH, '//h2[text()="104"]')
    assert summary.is_displayed() and price.is_displayed()


@pytest.mark.parametrize('my_users', login_data)
def test_double_click_to_cancel(setup, my_users):   # double click to cancel dish selection (func 2)
    driver = setup
    driver.find_element(By.XPATH, '//a[@href="#/SignIn"]').click()
    driver.find_element(By.XPATH, '//input[@placeholder="Enter your email"]').send_keys(my_users[0])
    driver.find_element(By.XPATH, '//input[@type="password"]').send_keys(my_users[1])
    driver.find_element(By.XPATH, '//button[@type="submit"]').click()
    driver.find_element(By.XPATH, '//h5[text()="Sides"]').click()   # first click to select the dish
    driver.find_element(By.XPATH, '//h5[text()="Sides"]').click()   # second click to cancel the selection
    element = driver.find_element(By.XPATH, '//div[@class="productsMain"]/div[5]/div')
    style = element.get_attribute("style")     # Get the value of the style attribute
    match = re.search(r"background-color:\s*([\w\d#]+)", style)  # Extract the value of the background-color property
    if match:
        background_color = match.group(1)
    else:
        background_color = None
    assert background_color == "white", f"Background color is {background_color}"  # Verify background color is white


@pytest.mark.parametrize('my_users', login_data)
def test_change_table_num(setup, my_users):  # change the table number (func 3)
    driver = setup
    driver.find_element(By.XPATH, '//a[@href="#/SignIn"]').click()
    driver.find_element(By.XPATH, '//input[@placeholder="Enter your email"]').send_keys(my_users[0])
    driver.find_element(By.XPATH, '//input[@type="password"]').send_keys(my_users[1])
    driver.find_element(By.XPATH, '//button[@type="submit"]').click()
    driver.find_element(By.XPATH, '//h5[text()="Burger"]').click()
    driver.execute_script("window.scrollBy(0, 600)")
    time.sleep(0.5)
    driver.find_element(By.XPATH, '//button[text()=" Reserve "]').click()
    table_num = driver.find_element(By.XPATH, '//div[@class="popup"]/div/div/div/div[2]/div[3]/div[5]/input')
    table_num.clear()
    table_num.send_keys(2)
    driver.find_element(By.XPATH, '//button[text()="Send"]').click()
    summary = driver.find_element(By.XPATH, '//h3[text()=" Your order has been successfully received "]')
    price = driver.find_element(By.XPATH, '//h2[text()="45"]')
    table = driver.find_element(By.XPATH, '//div[@class="row"]/div[2]/h3[2][text()="2"]')
    assert summary.is_displayed() and price.is_displayed() and table.is_displayed()


@pytest.mark.parametrize('my_users', login_data)
def test_log_out(setup, my_users):  # click on log out in the menu page (func 4)
    driver = setup
    driver.find_element(By.XPATH, '//a[@href="#/SignIn"]').click()
    driver.find_element(By.XPATH, '//input[@placeholder="Enter your email"]').send_keys(my_users[0])
    driver.find_element(By.XPATH, '//input[@type="password"]').send_keys(my_users[1])
    driver.find_element(By.XPATH, '//button[@type="submit"]').click()
    driver.find_element(By.XPATH, '//h5[text()="Burger"]').click()
    driver.execute_script("window.scrollBy(0, 600)")
    time.sleep(0.5)
    driver.find_element(By.XPATH, '//button[text()=" Log out "]').click()
    sign_out = driver.find_element(By.XPATH, '//a[@href="#/SignIn"]')
    assert sign_out.is_displayed()


@pytest.mark.parametrize('my_users', login_data)
def test_back_to_menu(setup, my_users):  # press on Back To Menu button on the popup (func 5)
    driver = setup
    driver.find_element(By.XPATH, '//a[@href="#/SignIn"]').click()
    driver.find_element(By.XPATH, '//input[@placeholder="Enter your email"]').send_keys(my_users[0])
    driver.find_element(By.XPATH, '//input[@type="password"]').send_keys(my_users[1])
    driver.find_element(By.XPATH, '//button[@type="submit"]').click()
    driver.find_element(By.XPATH, '//h5[text()="Kids Meal"]').click()
    driver.execute_script("window.scrollBy(0, 600)")
    time.sleep(0.5)
    driver.find_element(By.XPATH, '//button[text()=" Reserve "]').click()
    table_num = driver.find_element(By.XPATH, '//div[@class="row"]/div[5]/input')
    table_num.clear()
    table_num.send_keys(1)
    driver.find_element(By.XPATH, '//button[text()="Back To Menu"]').click()
    back = driver.find_element(By.XPATH, '//button[text()=" Log out "]')
    assert back.is_displayed()


@pytest.mark.parametrize('my_users', login_data)
def test_change_meal_quantity_to_two(setup, my_users):  # change quantity of burger to 2 (func 6)
    driver = setup
    driver.find_element(By.XPATH, '//a[@href="#/SignIn"]').click()
    driver.find_element(By.XPATH, '//input[@placeholder="Enter your email"]').send_keys(my_users[0])
    driver.find_element(By.XPATH, '//input[@type="password"]').send_keys(my_users[1])
    driver.find_element(By.XPATH, '//button[@type="submit"]').click()
    driver.find_element(By.XPATH, '//h5[text()="Burger"]').click()
    driver.execute_script("window.scrollBy(0, 600)")
    time.sleep(0.5)
    driver.find_element(By.XPATH, '//button[text()=" Reserve "]').click()
    quantity = driver.find_element(By.XPATH, '//div[@class="col-6"]/div/input')
    quantity.clear()
    quantity.send_keys(2)
    table_num = driver.find_element(By.XPATH, '//div[@class="row"]/div[5]/input')
    table_num.clear()
    table_num.send_keys(1)
    driver.find_element(By.XPATH, '//button[text()="Send"]').click()
    summary = driver.find_element(By.XPATH, '//h3[text()=" Your order has been successfully received "]')
    price = driver.find_element(By.XPATH, '//h2[text()="90"]')
    assert summary.is_displayed() and price.is_displayed()


@pytest.mark.parametrize('my_users', login_data)
# change the quantity of burger to 3, the allowed max is 2 (EH 1)
def test_error_change_quantity_to_three(setup, my_users):
    driver = setup
    driver.find_element(By.XPATH, '//a[@href="#/SignIn"]').click()
    driver.find_element(By.XPATH, '//input[@placeholder="Enter your email"]').send_keys(my_users[0])
    driver.find_element(By.XPATH, '//input[@type="password"]').send_keys(my_users[1])
    driver.find_element(By.XPATH, '//button[@type="submit"]').click()
    driver.find_element(By.XPATH, '//h5[text()="Burger"]').click()
    driver.execute_script("window.scrollBy(0, 600)")
    time.sleep(0.5)
    driver.find_element(By.XPATH, '//button[text()=" Reserve "]').click()
    quantity = driver.find_element(By.XPATH, '//div[@class="col-6"]/div/input')
    quantity.clear()
    quantity.send_keys(3)
    table_num = driver.find_element(By.XPATH, '//div[@class="row"]/div[5]/input')
    table_num.clear()
    table_num.send_keys(1)
    driver.find_element(By.XPATH, '//button[text()="Send"]').click()
    alert = driver.switch_to.alert
    assert alert.text == "Invalid value in quantity"
    alert.accept()


@pytest.mark.parametrize('my_users', login_data)
# select and order 4 dishes (max is 3) - the fourth dish background should stay white (EH 2)
def test_error_select_four_meals(setup, my_users):
    driver = setup
    driver.find_element(By.XPATH, '//a[@href="#/SignIn"]').click()
    driver.find_element(By.XPATH, '//input[@placeholder="Enter your email"]').send_keys(my_users[0])
    driver.find_element(By.XPATH, '//input[@type="password"]').send_keys(my_users[1])
    driver.find_element(By.XPATH, '//button[@type="submit"]').click()
    driver.find_element(By.XPATH, '//h5[text()="Combo Meal"]').click()  # select first dish
    driver.find_element(By.XPATH, '//h5[text()="Burger"]').click()  # select second dish
    driver.find_element(By.XPATH, '//h5[text()="Kids Meal"]').click()  # select third dish
    driver.find_element(By.XPATH, '//h5[text()="Sides"]').click()  # select fourth dish - should stay white
    element = driver.find_element(By.XPATH, '//div[@class="productsMain"]/div[5]/div')
    style = element.get_attribute("style")     # Get the value of the style attribute
    match = re.search(r"background-color:\s*([\w\d#]+)", style)    # Extract the value of the background-color property
    if match:
        background_color = match.group(1)
    else:
        background_color = None
    assert background_color == "white", f"Background color is {background_color}"  # Verify background color is white
    time.sleep(1)

