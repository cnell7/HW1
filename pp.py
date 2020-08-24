#   SMTP "MAIL FROM" message checker
#   Author: Christian Nell
#   Onyen: cnell
#   PID: 7302-29326
#   Date: 8/11/20
#   Purpose: To check a Simple Mail Transfer Protocol "MAIL FROM" message
#               and make sure it is following the correct syntax. This
#               message tells the mail server which person is trying to
#               email a message.
#
#   UNC Honor Pledge: I certify that no unauthorized assistance has been received or
#       given in the completion of this work
#       Signature: _Christian Nell__
import sys
import fileinput


def mail_from_cmd(string):
    mailString = "MAIL"
    fromString = "FROM:"
    # MAIL
    mail = string[0:4]
    if(not(mailString == mail)):
        print("ERROR -- mail-from-cmd")
        return False
    string = string[4:]
    #    <whitespace>
    string = whitespace(string)
    #   "FROM:"
    if(not(fromString == string[0:5])):
        print("ERROR -- mail-from-cmd")
        return False
    string = string[5:]
    #    <nullspace>
    string = nullspace(string)
    #   <reverse-path>
    string = reverse_path(string)
    if(not(string)):
        return False
    #    <nullspace>
    string = nullspace(string)
    if(not(string)):
        return False
    #   <CLRF>
    string = CRLF(string)
    if(not(string)):
        print("ERROR -- CRLF")
        return False
    print("Sender ok")
    return True


def whitespace(string):
    #   <SP> | <SP> <whitespace>
    if(SP(string) == False):
        return string[0:]
    string = SP(string)
    return whitespace(string)


def SP(string):
    #   the space or tab char
    if(string[0] == ' ' or string[0] == '\t'):
        return string[1:]
    elif(string[0] == '\\'):
        if(string[1] == 't'):
            return string[2:]
    return False


def nullspace(string):
    if(null(string[0])):
        return string
    return whitespace(string)


def null(c):
    if((c != ' ') or (c != '\t')):
        return False
    return True


def reverse_path(string):
    return path(string)


def path(string):
    if(string[0] != '<'):
        print("ERROR -- path")
        return False
    string = mailbox(string[1:])
    if(string == False):
        return False
    if(string[0] != '>'):
        print("ERROR -- path")
        return False
    return string[1:]


def mailbox(string):
    string = local_part(string)
    if(string == False):
        return False
    if(string[0] != '@'):
        print("ERROR -- mailbox")
        return False
    string = domain(string[1:])
    if(string == False):
        return False
    return string


def local_part(string):
    string = string_(string)
    return string


def string_(string):
    if(char(string) == False):
        return string
    return string_(string[1:])


def char(string):
    #   any one of the printable ASCII characters, but not any
    #       of <special> or <SP>
    if(special(string[0]) or SP(string) or not(ord(string[0]) < 128) or CRLF(string[0])):
        return False
    return True


def domain(string):
    string = element(string)
    if(string == False):
        print("ERROR -- domain")
        return False
    if(string[0] == '.'):
        string = domain(string[1:])
    return string


def element(string):
    if(not(letter(string[0]))):
        return False
    if(name(string) != False):
        string = name(string)
    elif():
        string = string[1:]
    return string


def name(string):
    if(not(letter(string[0]))):
        return False
    return let_dig_str(string)


def letter(c):
    #   any one of the 52 alphabetic characters A through Z
    #       in upper case and a through z in lower case
    if c.isalpha():
        return True
    return False


def let_dig_str(string):
    if(not(let_dig(string[0]))):
        return string
    return let_dig_str(string[1:])


def let_dig(c):
    if(letter(c) or digit(c)):
        return True
    return False


def digit(c):
    #    any one of the ten digits 0 through 9
    digits = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    if c in digits:
        return True
    return False


def CRLF(c):
    #    the newline character
    if(c == '\n'):
        return True
    return False


def special(c):
    #   special list ... shouldn't be in input
    special_list = ['<', '>', '(', ')', '[', ']',
                    '\\', '.', ',', ';', ':', '@', '"']
    if c in special_list:
        return True
    return False


def main():
    '''
    with open(sys.argv[1], 'r') as file:
        for line in file:
            copy = line.rstrip()
            print(copy)
            mail_from_cmd(line)
    '''
    for line in sys.stdin:
        copy = line.rstrip()
        print(copy)
        mail_from_cmd(line)
    '''
    pass1 = "MAIL FROM:<he@h>\n"
    pass2 = "MAIL  FROM:<eh@h>\n"
    pass3 = "MAIL  FROM: <he@h>\n"
    pass4 = "MAIL        FROM:       <123@h>\n"
    pass5 = "MAIL                 FROM:          <dijie2ei2ieie2j@e23456>\n"
    pass6 = "MAIL FROM:<hi@e2.e4.e6>\n"
    pass7 = "MAIL FROM:<jeffay@cs.unc.edu>\n"
    pass8 = "MAIL FROM:<a@domain.com>\n"
    pass9 = "MAIL    FROM:<test@domain.com>\n"
    pass10 = "MAIL\tFROM: <jeffay@cs.unc.edu>\n"
    pass11 = "MAIL \tFROM: <jeffay@cs.unc.edu>\n"
    pass12 = "MAIL\t \tFROM: <jeffay@cs.unc.edu>\n"
    pass13 = "MAIL \t\tFROM: <jeffay@cs.unc.edu>\n"
    pass14 = "MAIL  \t\tFROM:<jeffay@cs.unc.edu>\n"

    fail1 = "mAIL FROM:<he@h\n"
    fail2 = "MAIL fROM:<he@h\n"
    fail3 = "MAIL FROM:< he@h\n"
    fail4 = " MAIL FROM:<heh@h\n"
    fail5 = "MAIL    FROM:\n"
    fail6 = "MAILFROM:<\n"
    fail7 = "MAIL ! FROM:<hi@hi\n"
    fail8 = "MAIL! FROM:<hi@hi\n"
    fail9 = "MAIL FROM:<hi\@dd\n"
    fail10 = "MAIL FROM:<cnell@h.hi\n"
    fail11 = "MAIL FROM:<cd@.\n"
    fail12 = "MAIL FROM:<hi@hi.com\n"
    fail13 = "MAIL FROM:<hi@hi.>\n"
    fail14 = "MAIL FROM:<cnell@he.h.i\n"
    fail15 = "MAIL FROM:<\n"
    fail16 = "MAIL FROM:<hihi@hi\dd.com>\n"
    fail17 = "MAIL FROM:<h\d@hi.com>\n"
    fail18 = "\MAIL FROM:<d@d>\n"
    fail19 = "MAIL FROM:<\dd@hi.com>\n"
    fail20 = "MAIL FROM:\<hi@hi>\n"
    fail21 = "MAIL FROM:<hi@hi.d\d.comm>\n"
    fail22 = hex(0)
    fail23 = "MAIL FROM:<test.email.with+symbol@domain.com>\n"
    fail24 = "MAIL FROM:<example.com>\n"
    fail25 = "MAIL FROM:<A@b@c@domain.com>\n"
    fail26 = "MAIL FROM:<abc\"test\"email@domain.com>\n"
    fail27 = "MAIL FROML<.test@domain.com>\n"
    fail28 = "MAIL FROM:<test@domain..com>\n"
    fail29 = "MAIL FROM:< test@domain.com>\n"
    fail30 = "MAIL FROM:<test@domain.com >\n"
    fail31 = "MAIL FROM:<test @domain.com>\n"
    fail32 = "MAIL FROM:<test@domain .com>\n"
    fail33 = "MAIL FROM:<test@9round.com>\n"
    fail34 = "MAIL FROM:<hi\n@test.com>\n"

    print("pass")
    print("1")
    mail_from_cmd(pass1)
    print("2")
    mail_from_cmd(pass2)
    print("3")
    mail_from_cmd(pass3)
    print("4")
    mail_from_cmd(pass4)
    print("5")
    mail_from_cmd(pass5)
    print("6")
    mail_from_cmd(pass6)
    print("7")
    mail_from_cmd(pass7)
    print("8")
    mail_from_cmd(pass8)
    print("9")
    mail_from_cmd(pass9)
    print("10")
    mail_from_cmd(pass10)
    print("11")
    mail_from_cmd(pass11)
    print("12")
    mail_from_cmd(pass12)
    print("13")
    mail_from_cmd(pass13)
    print("14")
    mail_from_cmd(pass14)

    print("\nfail")
    print("1")
    mail_from_cmd(fail1)
    print("2")
    mail_from_cmd(fail2)
    print("3")
    mail_from_cmd(fail3)
    print("4")
    mail_from_cmd(fail4)
    print("5")
    mail_from_cmd(fail5)
    print("6")
    mail_from_cmd(fail6)
    print("7")
    mail_from_cmd(fail7)
    print("8")
    mail_from_cmd(fail8)
    print("9")
    mail_from_cmd(fail9)
    print("10")
    mail_from_cmd(fail10)
    print("11")
    mail_from_cmd(fail11)
    print("12")
    mail_from_cmd(fail12)
    print("13")
    mail_from_cmd(fail13)
    print("14")
    mail_from_cmd(fail14)
    print("15")
    mail_from_cmd(fail15)
    print("16")
    mail_from_cmd(fail16)
    print("17")
    mail_from_cmd(fail17)
    print("18")
    mail_from_cmd(fail18)
    print("19")
    mail_from_cmd(fail19)
    print("20")
    mail_from_cmd(fail20)
    print("21")
    mail_from_cmd(fail21)
    print("22")
    mail_from_cmd(fail22)
    print("23")
    mail_from_cmd(fail23)
    print("24")
    mail_from_cmd(fail24)
    print("25")
    mail_from_cmd(fail25)
    print("26")
    mail_from_cmd(fail26)
    print("27")
    mail_from_cmd(fail27)
    print("28")
    mail_from_cmd(fail28)
    print("29")
    mail_from_cmd(fail29)
    print("30")
    mail_from_cmd(fail30)
    print("31")
    mail_from_cmd(fail31)
    print("32")
    mail_from_cmd(fail32)
    print("33")
    mail_from_cmd(fail33)
    print("34")
    mail_from_cmd(fail34)
    '''


main()
