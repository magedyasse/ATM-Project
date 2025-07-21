"""
Enhanced ATM Simulation Project written in Python, using functions and global variables.

## New Features Added

- **Multiple Account Support:** Switch between Savings and Checking accounts
- **Transaction History with Timestamps:** Full transaction logging with dates/times
- **Daily Withdrawal Limits:** Configurable daily withdrawal limits
- **Account Transfer:** Transfer money between your own accounts
- **Bill Payment:** Pay utilities, phone, and credit card bills
- **Interest Calculation:** Earn interest on savings account balance
- **Account Statements:** Generate detailed monthly statements
- **PIN Change:** Change your PIN securely
- **Transaction Fees:** Small fees for certain transactions
- **Account Lockout:** Enhanced security with temporary lockouts
- **Balance Alerts:** Warnings for low balances
- **Transaction Categories:** Categorized spending tracking
- **Quick Cash:** Preset withdrawal amounts
- **Deposit Limits:** Maximum deposit validation
- **Session Timeout:** Auto-logout after inactivity

## Usage Instructions

1. Default PIN: 1234
2. Starting balances: Savings $1000, Checking $500
3. Daily withdrawal limit: $500
4. Transaction fees apply to some operations
5. Interest is calculated daily on savings balance
"""

import datetime
import random
import time

# Global variables - moved to top for clarity
balance_savings = 1000.0
balance_checking = 500.0
current_account = "savings"
transactions = []
pin_attempts = 3
pin = "1234"

daily_withdrawal_limit = 500.0
daily_withdrawn = 0.0
last_withdrawal_date = None
account_locked = False
lockout_time = None
session_start_time = None
session_timeout = 300 # 5 minutes session timeout
transaction_fee = 1.50
last_interest_date = None

def main():
    global session_start_time
    
    initialize_system()
    session_start_time = datetime.datetime.now()
    
    if not authenticate_user():
        print("Too many incorrect attempts. Exiting.")
        return
    
    print("🏦 Welcome to Enhanced ATM System!")
    print("=" * 40)
    
    while True:
        if check_session_timeout():
            print("⏰ Session timed out for security. Please restart.")
            break
            
        if account_locked:
            print("🔒 Account is temporarily locked. Please try again later.")
            break
            
        show_menu()
        action = input("\nEnter your choice (1-15): ").strip()
        
        if action == "1":
            show_balance()
        elif action == "2":
            deposit_money()
        elif action == "3":
            withdraw_money()
        elif action == "4":
            quick_cash()
        elif action == "5":
            show_statement()
        elif action == "6":
            transfer_between_accounts()
        elif action == "7":
            pay_bills()
        elif action == "8":
            switch_account()
        elif action == "9":
            change_pin()
        elif action == "10":
            show_transaction_history()
        elif action == "11":
            generate_monthly_statement()
        elif action == "12":
            calculate_interest()
        elif action == "13":
            show_account_info()
        elif action == "14":
            check_daily_limits()
        elif action == "15":
            print("💰 Thank you for using Enhanced ATM. Goodbye!")
            break
        else:
            print("❌ Invalid choice. Please try again.")
            
     
        time.sleep(0.7)

def initialize_system():
    """Initialize system variables and calculate any pending interest"""
    global last_interest_date, last_withdrawal_date, balance_savings, balance_checking
    global daily_withdrawn, daily_withdrawal_limit, current_account, transactions
    global pin_attempts, pin, account_locked, lockout_time, session_start_time
    global session_timeout, transaction_fee
    
    current_date = datetime.datetime.now().date()
    
    if last_interest_date is None:
        last_interest_date = current_date
    
    if last_withdrawal_date is None:
        last_withdrawal_date = current_date
    
    # Calculate any pending interest
    calculate_daily_interest()

def authenticate_user():
    """Enhanced authentication with account lockout"""
    global pin_attempts, pin, account_locked, lockout_time
    
    # Check if account is locked
    if account_locked and lockout_time:
        time_diff = datetime.datetime.now() - lockout_time
        if time_diff.total_seconds() < 1800:  # 30 minutes lockout
            remaining = 1800 - time_diff.total_seconds()
            print(f"🔒 Account locked. Try again in {remaining/60:.1f} minutes.")
            return False
        else:
            account_locked = False
            lockout_time = None
            pin_attempts = 3
  
    while pin_attempts > 0:
        user_pin = input("🔐 Enter your PIN: ").strip()
        if user_pin == pin:
            print("✅ Authentication successful!")
            pin_attempts = 3  # Reset attempts on success
            return True
        else:
            pin_attempts -= 1
            if pin_attempts == 0:
                account_locked = True
                lockout_time = datetime.datetime.now()
                print("🔒 Account locked due to multiple failed attempts.")
                log_transaction("SECURITY", "Account locked - multiple failed PIN attempts", 0)
                return False
            print(f"❌ Incorrect PIN. You have {pin_attempts} attempts left.")
    
    return False

def show_menu():
    """Display the enhanced ATM menu"""
    print(f"\n🏦 ATM Menu - Current Account: {current_account.title()}")
    print("=" * 40)
    print("1.  💰 Check Balance")
    print("2.  📥 Deposit Money")
    print("3.  📤 Withdraw Money")
    print("4.  ⚡ Quick Cash")
    print("5.  📋 Mini Statement")
    print("6.  🔄 Transfer Between Accounts")
    print("7.  💳 Pay Bills")
    print("8.  🔀 Switch Account")
    print("9.  🔑 Change PIN")
    print("10. 📊 Transaction History")
    print("11. 📄 Monthly Statement")
    print("12. 💹 Calculate Interest")
    print("13. ℹ️  Account Information")
    print("14. 📈 Check Daily Limits")
    print("15. 🚪 Exit")

def show_balance():
    """Display current account balance with alerts"""
    global balance_savings, balance_checking, current_account
    
    current_balance = balance_savings if current_account == "savings" else balance_checking
    
    print(f"\n💰 {current_account.title()} Account Balance: ${current_balance:.2f}")
    
    # Balance alerts
    if current_balance < 100:
        print("⚠️  Warning: Low balance!")
    elif current_balance < 50:
        print("🚨 Alert: Very low balance!")
    
    # Show other account balance too
    other_account = "checking" if current_account == "savings" else "savings"
    other_balance = balance_checking if current_account == "savings" else balance_savings
    print(f"📊 {other_account.title()} Account Balance: ${other_balance:.2f}")

def deposit_money():
    """Enhanced deposit with limits and validation"""
    global balance_savings, balance_checking, current_account, transactions
    
    try:
        amount = float(input("💵 Enter the amount to deposit: $"))
        
        if amount <= 0:
            print("❌ Deposit amount must be positive.")
            return
        
        if amount > 10000:  # Daily deposit limit
            print("❌ Daily deposit limit is $10,000.")
            return
        
        # Process deposit
        if current_account == "savings":
            balance_savings += amount
            new_balance = balance_savings
        else:
            balance_checking += amount
            new_balance = balance_checking
        
        log_transaction("DEPOSIT", f"Deposited to {current_account}", amount)
        print(f"✅ Successfully deposited ${amount:.2f}")
        print(f"💰 New {current_account} balance: ${new_balance:.2f}")
        
    except ValueError:
        print("❌ Invalid input. Please enter a numeric value.")

def withdraw_money():
    """Enhanced withdrawal with daily limits and fees"""
    global balance_savings, balance_checking, current_account
    global daily_withdrawn, daily_withdrawal_limit, last_withdrawal_date
    
    try:
        # Check daily limit reset
        check_daily_limit_reset()
        
        amount = float(input("💸 Enter the amount to withdraw: $"))
        
        if amount <= 0:
            print("❌ Withdrawal amount must be positive.")
            return
        
        current_balance = balance_savings if current_account == "savings" else balance_checking
        
        # Check daily withdrawal limit
        if daily_withdrawn + amount > daily_withdrawal_limit:
            remaining = daily_withdrawal_limit - daily_withdrawn
            print(f"❌ Daily withdrawal limit exceeded. Remaining: ${remaining:.2f}")
            return
        
        # Check sufficient funds (including potential fee)
        total_cost = amount + transaction_fee if amount > 200 else amount
        
        if total_cost > current_balance:
            print("❌ Insufficient funds for this withdrawal.")
            return
        
        # Process withdrawal
        if current_account == "savings":
            balance_savings -= total_cost
            new_balance = balance_savings
        else:
            balance_checking -= total_cost
            new_balance = balance_checking
        
        daily_withdrawn += amount
        
        log_transaction("WITHDRAWAL", f"Withdrew from {current_account}", amount)
        
        if amount > 200:
            log_transaction("FEE", "Withdrawal fee", transaction_fee)
            print(f"ℹ️  Transaction fee: ${transaction_fee:.2f}")
        
        print(f"✅ Successfully withdrew ${amount:.2f}")
        print(f"💰 New {current_account} balance: ${new_balance:.2f}")
        
    except ValueError:
        print("❌ Invalid input. Please enter a numeric value.")

def quick_cash():
    """Quick cash withdrawal with preset amounts"""
    global balance_savings, balance_checking, current_account
    
    print("\n⚡ Quick Cash Options:")
    print("1. $20    2. $40    3. $60    4. $80    5. $100")
    
    choice = input("Select amount (1-5): ").strip()
    amounts = {"1": 20, "2": 40, "3": 60, "4": 80, "5": 100}
    
    if choice in amounts:
        amount = amounts[choice]
        print(f"Processing withdrawal of ${amount}...")
        
        # Simulate the withdrawal process
        current_balance = balance_savings if current_account == "savings" else balance_checking
        
        if amount <= current_balance:
            if current_account == "savings":
                balance_savings -= amount
            else:
                balance_checking -= amount
            
            log_transaction("QUICK_CASH", f"Quick cash from {current_account}", amount)
            print(f"✅ Quick cash: ${amount} withdrawn successfully!")
        else:
            print("❌ Insufficient funds.")
    else:
        print("❌ Invalid selection.")

def transfer_between_accounts():
    """Transfer money between savings and checking accounts"""
    global balance_savings, balance_checking, current_account
    
    try:
        amount = float(input("🔄 Enter transfer amount: $"))
        
        if amount <= 0:
            print("❌ Transfer amount must be positive.")
            return
        
        if current_account == "savings":
            if amount > balance_savings:
                print("❌ Insufficient funds in savings account.")
                return
            balance_savings -= amount
            balance_checking += amount
            log_transaction("TRANSFER", "Transfer: Savings → Checking", amount)
            print(f"✅ Transferred ${amount:.2f} from Savings to Checking")
        else:
            if amount > balance_checking:
                print("❌ Insufficient funds in checking account.")
                return
            balance_checking -= amount
            balance_savings += amount
            log_transaction("TRANSFER", "Transfer: Checking → Savings", amount)
            print(f"✅ Transferred ${amount:.2f} from Checking to Savings")
        
        print(f"💰 Savings: ${balance_savings:.2f} | Checking: ${balance_checking:.2f}")
        
    except ValueError:
        print("❌ Invalid input. Please enter a numeric value.")

def pay_bills():
    """Bill payment feature"""
    global balance_savings, balance_checking, current_account, transaction_fee
    
    print("\n💳 Bill Payment Options:")
    print("1. Electricity    2. Water    3. Phone    4. Internet    5. Credit Card")
    
    choice = input("Select bill type (1-5): ").strip()
    bill_types = {
        "1": "Electricity", "2": "Water", "3": "Phone", 
        "4": "Internet", "5": "Credit Card"
    }
    
    if choice in bill_types:
        bill_type = bill_types[choice]
        try:
            amount = float(input(f"Enter {bill_type} bill amount: $"))
            
            if amount <= 0:
                print("❌ Bill amount must be positive.")
                return
            
            current_balance = balance_savings if current_account == "savings" else balance_checking
            total_cost = amount + transaction_fee
            
            if total_cost > current_balance:
                print("❌ Insufficient funds for bill payment.")
                return
            
            # Process payment
            if current_account == "savings":
                balance_savings -= total_cost
            else:
                balance_checking -= total_cost
            
            log_transaction("BILL_PAYMENT", f"Paid {bill_type} bill", amount)
            log_transaction("FEE", "Bill payment fee", transaction_fee)
            
            print(f"✅ {bill_type} bill of ${amount:.2f} paid successfully!")
            print(f"ℹ️  Service fee: ${transaction_fee:.2f}")
            
        except ValueError:
            print("❌ Invalid input. Please enter a numeric value.")
    else:
        print("❌ Invalid selection.")

def switch_account():
    """Switch between savings and checking accounts"""
    global current_account
    
    print(f"\n🔀 Current account: {current_account.title()}")
    print("1. Savings Account    2. Checking Account")
    
    choice = input("Select account (1-2): ").strip()
    
    if choice == "1":
        current_account = "savings"
        print("✅ Switched to Savings Account")
    elif choice == "2":
        current_account = "checking"
        print("✅ Switched to Checking Account")
    else:
        print("❌ Invalid selection.")

def change_pin():
    """Change PIN with security verification"""
    global pin
    
    current_pin = input("🔐 Enter current PIN: ").strip()
    
    if current_pin != pin:
        print("❌ Current PIN is incorrect.")
        return
    
    new_pin = input("🔑 Enter new PIN (4 digits): ").strip()
    
    if len(new_pin) != 4 or not new_pin.isdigit():
        print("❌ PIN must be exactly 4 digits.")
        return
    
    confirm_pin = input("🔑 Confirm new PIN: ").strip()
    
    if new_pin != confirm_pin:
        print("❌ PINs don't match.")
        return
    
    pin = new_pin
    log_transaction("SECURITY", "PIN changed", 0)
    print("✅ PIN changed successfully!")

def show_statement():
    """Show mini statement with recent transactions"""
    global transactions
    
    print("\n📋 Mini Statement (Last 5 Transactions):")
    print("=" * 50)
    
    if not transactions:
        print("No recent transactions.")
    else:
        recent_transactions = transactions[-5:]
        for i, transaction in enumerate(recent_transactions, 1):
            print(f"{i}. {transaction}")
    
    print("=" * 50)

def show_transaction_history():
    """Show complete transaction history"""
    global transactions
    
    print("\n📊 Complete Transaction History:")
    print("=" * 60)
    
    if not transactions:
        print("No transactions found.")
    else:
        for i, transaction in enumerate(transactions, 1):
            print(f"{i:2d}. {transaction}")
    
    print("=" * 60)

def generate_monthly_statement():
    """Generate a detailed monthly statement"""
    global transactions, balance_savings, balance_checking
    
    print("\n📄 Monthly Account Statement")
    print("=" * 50)
    print(f"Statement Date: {datetime.datetime.now().strftime('%B %Y')}")
    print(f"Account Holder: ATM User")
    print("=" * 50)
    
    print(f"💰 Current Balances:")
    print(f"   Savings Account:  ${balance_savings:.2f}")
    print(f"   Checking Account: ${balance_checking:.2f}")
    print(f"   Total Balance:    ${balance_savings + balance_checking:.2f}")
    
    print(f"\n📊 Transaction Summary:")
    deposits = sum(1 for t in transactions if "DEPOSIT" in t)
    withdrawals = sum(1 for t in transactions if "WITHDRAWAL" in t or "QUICK_CASH" in t)
    transfers = sum(1 for t in transactions if "TRANSFER" in t)
    payments = sum(1 for t in transactions if "BILL_PAYMENT" in t)
    
    print(f"   Deposits:     {deposits}")
    print(f"   Withdrawals:  {withdrawals}")
    print(f"   Transfers:    {transfers}")
    print(f"   Bill Payments: {payments}")
    print(f"   Total Transactions: {len(transactions)}")
    
    print("=" * 50)

def calculate_interest():
    """Calculate and apply interest to savings account"""
    global balance_savings, last_interest_date
    
    current_date = datetime.datetime.now().date()
    
    if last_interest_date == current_date:
        print("💹 Interest already calculated today.")
        return
    
    # Simple daily interest calculation (0.01% daily = ~3.65% annual)
    daily_interest_rate = 0.0001
    interest_earned = balance_savings * daily_interest_rate
    
    if interest_earned > 0:
        balance_savings += interest_earned
        log_transaction("INTEREST", "Daily interest earned", interest_earned)
        print(f"💹 Interest earned: ${interest_earned:.2f}")
        print(f"💰 New savings balance: ${balance_savings:.2f}")
        last_interest_date = current_date
    else:
        print("💹 No interest earned (zero balance).")

def calculate_daily_interest():
    """Calculate any pending daily interest"""
    global last_interest_date, balance_savings, transactions
    
    current_date = datetime.datetime.now().date()
    
    if last_interest_date and last_interest_date < current_date:
        days_passed = (current_date - last_interest_date).days
        if days_passed > 0:
            print(f"💹 Calculating {days_passed} day(s) of pending interest...")
            for _ in range(days_passed):
                calculate_interest()

def show_account_info():
    """Display detailed account information"""
    global balance_savings, balance_checking, current_account
    global daily_withdrawal_limit, daily_withdrawn, pin
    
    print("\nℹ️  Account Information:")
    print("=" * 40)
    print(f"👤 Account Holder: ATM User")
    print(f"🏦 Current Account: {current_account.title()}")
    print(f"💰 Savings Balance: ${balance_savings:.2f}")
    print(f"💳 Checking Balance: ${balance_checking:.2f}")
    print(f"💵 Total Balance: ${balance_savings + balance_checking:.2f}")
    print(f"📉 Daily Withdrawal Limit: ${daily_withdrawal_limit:.2f}")
    print(f"📊 Today's Withdrawals: ${daily_withdrawn:.2f}")
    print(f"📈 Remaining Limit: ${daily_withdrawal_limit - daily_withdrawn:.2f}")
    print(f"🔐 PIN: {'*' * len(pin)}")
    print(f"📅 Last Login: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 40)

def check_daily_limits():
    """Check and display daily transaction limits"""
    global daily_withdrawal_limit, daily_withdrawn
    
    print("\n📈 Daily Transaction Limits:")
    print("=" * 35)
    print(f"💸 Withdrawal Limit: ${daily_withdrawal_limit:.2f}")
    print(f"📊 Used Today: ${daily_withdrawn:.2f}")
    print(f"💰 Remaining: ${daily_withdrawal_limit - daily_withdrawn:.2f}")
    print(f"💵 Deposit Limit: $10,000.00")
    print("=" * 35)

def check_daily_limit_reset():
    """Reset daily withdrawal limit if new day"""
    global daily_withdrawn, last_withdrawal_date
    
    current_date = datetime.datetime.now().date()
    
    if last_withdrawal_date != current_date:
        daily_withdrawn = 0.0
        last_withdrawal_date = current_date

def check_session_timeout():
    """Check if session has timed out"""
    global session_start_time, session_timeout
    
    if session_start_time:
        elapsed = (datetime.datetime.now() - session_start_time).total_seconds()
        return elapsed > session_timeout
    
    return False

def log_transaction(transaction_type, description, amount):
    """Log transaction with timestamp and details"""
    global transactions
    
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    if amount > 0:
        transaction_log = f"[{timestamp}] {transaction_type}: {description} - ${amount:.2f}"
    else:
        transaction_log = f"[{timestamp}] {transaction_type}: {description}"
    
    transactions.append(transaction_log)
    
    # Keep only last 100 transactions to manage memory
    if len(transactions) > 100:
        transactions = transactions[-100:]

if __name__ == "__main__":
    main()