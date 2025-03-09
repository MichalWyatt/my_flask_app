"""Updated Flask website with password update form, NIST password validation, and logging."""
from datetime import datetime
import re
import logging
from flask import Flask, render_template, request, redirect, url_for, session, flash

app = Flask(__name__)
app.secret_key = 'mysecretkey123'  # Needed for session management

# Dummy user data for demonstration purposes
users = {'user@example.com': 'Password123!'}

# Common passwords list from provided document
COMMON_PASSWORDS = {
    'password', '123456', '12345678', '1234', 'qwerty', '12345', 'dragon', 'baseball',
    'football', 'letmein', 'monkey', 'abc123', 'mustang', 'michael', 'shadow', 'master',
    'jennifer', '111111', '2000', 'jordan', 'superman', 'harley', '1234567', 'hunter',
    'trustno1', 'ranger', 'buster', 'thomas', 'robert', 'soccer', 'batman', 'test', 'pass',
    'killer', 'hockey', 'george', 'charlie', 'andrew', 'michelle', 'love', 'sunshine',
    'jessica', 'pepper', 'daniel', 'access', '123456789', '654321', 'joshua', 'maggie',
    'starwars', 'silver', 'william', 'dallas', 'yankees', '123123', 'ashley', '666666',
    'hello', 'amanda', 'orange', 'biteme', 'freedom', 'computer', 'sexy', 'thunder',
    'nicole', 'ginger', 'heather', 'hammer', 'summer', 'corvette', 'taylor', 'austin',
    '1111', 'merlin', 'matthew', '121212', 'golfer', 'cheese', 'princess', 'martin',
    'chelsea', 'patrick', 'richard', 'diamond', 'yellow', 'bigdog', 'secret', 'asdfgh',
    'sparky', 'cowboy', 'camaro', 'anthony', 'matrix', 'falcon', 'iloveyou', 'bailey',
    'guitar', 'jackson', 'purple', 'scooter', 'phoenix', 'aaaaaa', 'morgan', 'tigers',
    'porsche', 'mickey', 'maverick', 'cookie', 'nascar', 'peanut', 'justin', '131313',
    'money', 'samantha', 'steelers', 'joseph', 'snoopy', 'boomer', 'whatever', 'iceman',
    'smokey', 'gateway', 'dakota', 'cowboys', 'eagles', 'chicken', 'black', 'zxcvbn',
    'please', 'andrea', 'ferrari', 'knight', 'hardcore', 'melissa', 'compaq', 'coffee',
    'booboo', 'johnny', 'bulldog', 'xxxxxx', 'welcome', 'james', 'player', 'ncc1701',
    'wizard', 'scooby', 'charles', 'junior', 'internet', 'mike', 'brandy', 'tennis',
    'banana', 'monster', 'spider', 'lakers', 'miller', 'rabbit', 'enter', 'mercedes',
    'brandon', 'steven', 'fender', 'john', 'yamaha', 'diablo', 'chris', 'boston', 'tiger',
    'marine', 'chicago', 'rangers', 'gandalf', 'winter', 'barney', 'edward', 'raiders',
    'badboy', 'spanky', 'bigdaddy', 'johnson', 'chester', 'london', 'midnight', 'blue',
    'fishing', '0', 'hannah', 'slayer', '11111111', 'rachel', 'redsox', 'thx1138', 'asdf',
    'marlboro', 'panther', 'zxcvbnm', 'arsenal', 'oliver', 'qazwsx', 'mother', 'victoria',
    '7777777', 'jasper', 'angel', 'david', 'winner', 'crystal', 'golden', 'butthead',
    'viking', 'jack', 'iwantu', 'shannon', 'murphy', 'angels', 'prince', 'cameron',
    'girls', 'madison', 'wilson', 'carlos', 'willie', 'startrek', 'captain', 'maddog',
    'jasmine', 'butter', 'booger', 'angela', 'golf', 'lauren', 'rocket', 'tiffany',
    'theman', 'dennis', 'liverpoo', 'flower', 'forever', 'green', 'jackie', 'muffin',
    'turtle', 'sophie', 'danielle', 'redskins', 'toyota', 'jason', 'sierra', 'winston',
    'debbie', 'giants', 'packers', 'newyork', 'jeremy', 'casper', 'bubba', '112233',
    'sandra', 'lovers', 'mountain', 'united', 'cooper', 'driver', 'tucker', 'helpme',
    'pookie', 'lucky', 'maxwell', '8675309', 'bear', 'gators', '5150', '222222', 'jaguar',
    'monica', 'fred', 'happy', 'hotdog', 'gemini', 'lover', 'xxxxxxxx', '777777', 'canada',
    'nathan', 'victor', 'florida', '88888888', 'nicholas', 'rosebud', 'metallic', 'doctor',
    'trouble', 'success', 'stupid', 'tomcat', 'warrior', 'peaches', 'apples', 'fish',
    'qwertyui', 'magic', 'buddy', 'dolphins', 'rainbow', 'gunner', '987654', 'freddy',
    'alexis', 'braves', '2112', '1212', 'cocacola', 'xavier', 'dolphin', 'testing',
    'bond007', 'member', 'calvin', 'voodoo', '7777', 'samson', 'alex', 'apollo', 'fire',
    'tester', 'walter', 'beavis', 'voyager', 'bonnie', 'rush2112', 'beer', 'apple',
    'scorpio', 'jonathan', 'skippy', 'sydney', 'scott', 'red123', 'power', 'gordon',
    'travis', 'beaver', 'star', 'jackass', 'flyers', '232323', 'zzzzzz', 'steve',
    'rebecca', 'scorpion', 'doggie', 'legend', 'ou812', 'yankee', 'blazer', 'bill',
    'runner', 'birdie', '555555', 'parker', 'topgun', 'asdfasdf', 'heaven', 'viper',
    'animal', '2222', 'bigboy', '4444', 'arthur', 'baby', 'private', 'godzilla',
    'donald', 'williams', 'lifehack', 'phantom', 'dave', 'rock', 'august', 'sammy',
    'cool', 'brian', 'platinum', 'jake', 'bronco', 'paul', 'mark', 'frank', 'heka6w2',
    'copper', 'billy', 'garfield', 'willow', 'little', 'carter', 'albert', 'kitten',
    'super', 'jordan23', 'eagle1', 'shelby', 'america', '11111', 'jessie', 'house',
    'free', '123321', 'chevy', 'white', 'broncos', 'horney', 'surfer', 'nissan', '999999',
    'saturn', 'airborne', 'elephant', 'marvin', 'action', 'adidas', 'qwert', 'kevin',
    '1313', 'explorer', 'walker', 'police', 'christin', 'december', 'benjamin', 'wolf',
    'sweet', 'therock', 'king', 'online', 'brooklyn', 'teresa', 'cricket', 'sharon',
    'dexter', 'racing', 'gregory', 'teens', 'redwings', 'dreams', 'michigan', 'hentai',
    'magnum', '87654321', 'nothing', 'donkey', 'trinity', 'digital', '333333', 'stella',
    'cartman', 'guinness', '123abc', 'speedy', 'buffalo'
}

# Configure logging
#failed_logins.log are written to a file named failed_logins.log
#level=logging.INFO logs messages at the INFO level or higher
#format='%(asctime)s - %(message)s' logs the timestamp and message
#logger = logging.getLogger() creates a logger object
logging.basicConfig(
    filename='failed_logins.log',
    level=logging.INFO,
    format='%(asctime)s - %(message)s'
)
logger = logging.getLogger()

# Password validation
# checks if the lowercase cersion of the password is in set
#adhering to NIST SP 800-63B guidlines
def validate_password(password):
    """Check password complexity: 12+ chars, 1 upper, 1 lower, 1 num, 1 special."""
    if len(password) < 12:
        return False, "Password must be at least 12 characters long"
    if not re.search(r"[A-Z]", password):
        return False, "Password must contain at least 1 uppercase letter"
    if not re.search(r"[a-z]", password):
        return False, "Password must contain at least 1 lowercase letter"
    if not re.search(r"[0-9]", password):
        return False, "Password must contain at least 1 number"
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        return False, "Password must contain at least 1 special character"
    if password.lower() in COMMON_PASSWORDS:
        return False, "Password is too common, please choose a different one"
    return True, "Password is valid"

# Routes
@app.route('/')
def home():
    """Home page of the website."""
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('home.html', current_time=datetime.now())

@app.route('/about')
def about():
    """About page of the website."""
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('about.html')

@app.route('/contact')
def contact():
    """Contact page of the website."""
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('contact.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    """User registration page."""
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if email in users:
            flash('Email already registered.')
        else:
            is_valid, message = validate_password(password)
            if not is_valid:
                flash(message)
            else:
                users[email] = password
                flash('Registration successful. Please log in.')
                return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login page."""
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if email in users and users[email] == password:
            session['user'] = email
            flash('Login successful.')
            return redirect(url_for('home'))
        else:
            # Log failed login attempt with lazy % formatting
            ip_address = request.remote_addr
            logger.info("Failed login attempt - Email: %s, IP: %s", email, ip_address)
            flash('Invalid email or password.')
    return render_template('login.html')

@app.route('/logout')
def logout():
    """User logout."""
    session.pop('user', None)
    flash('You have been logged out.')
    return redirect(url_for('login'))

@app.route('/update_password', methods=['GET', 'POST'])
def update_password():
    """Password update page."""
    if 'user' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        current_password = request.form['current_password']
        new_password = request.form['new_password']
        confirm_password = request.form['confirm_password']

        email = session['user']

        # Verify current password
        if users[email] != current_password:
            flash('Current password is incorrect.')
        # Check if new passwords match
        elif new_password != confirm_password:
            flash('New passwords do not match.')
        else:
            # Validate new password
            is_valid, message = validate_password(new_password)
            if not is_valid:
                flash(message)
            elif new_password == current_password:
                flash('New password must be different from current password.')
            else:
                users[email] = new_password
                flash('Password updated successfully.')
                return redirect(url_for('home'))

    return render_template('update_password.html')

# Run application
if __name__ == '__main__':
    app.run(debug=True)
