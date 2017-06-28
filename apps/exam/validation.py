from dateutil.relativedelta import relativedelta
import datetime, re, bcrypt

# test_input_reqs = [
#     ('alpha', 'f_name', ''),
#     ('alpha', 'l_name', ''),
#     ('email', 'email', 'rob@gmailcom'),
#     ('text', 'desc', 'sjfadlfkjaf dlsfj dalkfjd slfldfjf f1?.,', 0,100),
#     ('pass_check', 'password', 'asdf', 'asdfjklasdfjkl', 8, 16)
# ]



class Validation(object):
    """docstring for Validation."""

    def __init__(self, inputs_reqs):
        self.alpha = []
        self.pw = []
        self.email = []
        self.text = []
        self.birthdate = None
        self.errors = []
        self.data = {}

        for input in inputs_reqs:
            if input[0] == 'alpha':
                self.alpha.append(input)
            elif input[0] == 'email':
                self.email.append(input)
            elif input[0] == 'pass_check':
                self.pw.append(input)
            elif input[0] == 'text':
                self.text.append(input)
            elif input[0] == 'birthdate':
                self.birthdate = input
            else:
                self.errors.append(
                    input[1] + " has errors: " + input[0] + " is not a supported method")

        self.alpha_check(self.alpha)
        self.email_check(self.email)
        self.pass_check(self.pw)
        self.text_check(self.text)
        self.birthdate_check(self.birthdate)

    def len_check(self, str, min=0, max=140):
        if len(str) == 0:
            return False
        if len(str) > min and len(str) < max:
            return True
        else:
            return False

    def birthdate_check(self, birthdate):
        try:
            bday = datetime.datetime.strptime(birthdate[1], '%Y-%m-%d')
            today = datetime.datetime.today()
            age = relativedelta(today, bday)
            self.data['age'] = age
            self.data[birthdate[0]] = birthdate[1]
            if age.years < 18:
                self.errors.append("Please return when you meet the age requirement")
        except:
            self.errors.append("There was an error processing your age. Please try again")
            self.data['age'] = birthdate

    def email_check(self, email_list):
        for email in email_list:
            if self.len_check(email[2]):
                EMAIL_REGEX = re.compile(
                    r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
                if not EMAIL_REGEX.match(email[2]):
                    self.errors.append(
                        email[2] + " is not a valid email address")
                else:
                    self.data[email[1]] = email[2]
            else:
                self.errors.append("Please provide a valide email address")

    def text_check(self, text_list):
        for text in text_list:
            if self.len_check(text[2]):
                TEXT_REGEX = re.compile(r'^[ .,;!?a-zA-Z0-9]+$')
                if not TEXT_REGEX.match(text[2]):
                    self.errors.append(text[1] + " contains in valid characters. Allowed Characters letters, numbers, spaces and symbols")
                else:
                    self.data[text[1]] = text[2]
            else:
                self.errors.append('Your ' + text[1] + ' does not meet length requirements.')

    def alpha_check(self, alpha_list):
        for alpha in alpha_list:
            if self.len_check(alpha[2]):
                if not alpha[2].isalpha():
                    self.errors.append(
                        "Provided " + alpha[1] + " contains invalid characters! alpha 0:" + alpha[0] + " alpha 2:" + alpha[2])
                else:
                    self.data[alpha[1]] = alpha[2]
            else:
                self.errors.append("Please provide a valid " + alpha[1])

    def pass_check(self, pass_list):
        for pw in pass_list:
            if len(pw) == 6:
                length = self.len_check(pw[2], pw[4], pw[5])
            else:
                length = self.len_check(pw[2], pw[4])
            if length:
                if pw[2] != pw[3]:
                    self.errors.append("Please verify your password match")
                else:
                    self.data[pw[1]] = bcrypt.hashpw(pw[2].encode(), bcrypt.gensalt())
            else:
                self.errors.append(
                    "Your password does not meet the length requirements")



# sanitize = Validation(test_input_reqs)
#
# print sanitize.data
# print sanitize.errors
