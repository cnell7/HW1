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
#   Purpose: Checks to make sure the string is not incomplete at the spot it is working on
#               so there is no indexoutofbounds exception.


def length_check(i, string):
    if i > (len(string) - 1):
        print("ERROR -- incomplete input")
        return exit()
    return True
#   Purpose: To check if last char before ">" in domain.


def end_check(i, string):
    if ((len(string) - i) <= 2):
        return True
    return False


def exit():
    return False


def mail_from_cmd(string):
    mailString = "MAIL"
    fromString = "FROM:"
    #   "MAIL"
    if(not(mailString == string[0:4])):
        print("ERROR -- mail-from-cmd")
        return exit()
    i = 4
    #    <whitespace>
    if(not(whitespace(i, string))):
        return exit()
    i = whitespace(i, string)
    #   "FROM:"
    if(not(fromString == string[i:i+5])):
        print("ERROR -- mail-from-cmd")
        return exit()
    i += 5
    #    <nullspace>
    if (nullspace(i, string) == False):
        return exit()
    i = nullspace(i, string)
    #   <reverse-path>
    if (reverse_path(i, string) == False):
        return exit()
    #    <nullspace>
    if (nullspace(i, string) == False):
        return exit()
    i = nullspace(i, string)
    #   <CLRF>
    CRLF(string[i])
    print("Sender ok")
    return True


def whitespace(i, string):
    #   <SP> | <SP> <whitespace>
    if(SP(string[i]) == False):
        print("ERROR -- whitespace")
        return exit()
    while SP(string[i]):
        i += 1
        length_check(i, string)
    return i


def SP(c):
    #    the space or tab character
    if ((" " == c) or ("  " == c)):
        return True
    else:
        return exit()


def nullspace(i, string):
    #   <null> | <whitespace>
    if(null(i, string) == True):
        return exit()
    if(not(SP(string[i]))):
        return i
    i = whitespace(i, string)
    return i


def null(i, string):
    #   no character
    if (not(length_check(i, string))):
        return True
    return exit()


def reverse_path(i, string):
    #    <path>
    return path(i, string)


def path(i, string):
    #   "<"
    if string[i] != "<":
        print("ERROR -- path")
        return exit()
    i += 1
    length_check(i, string)
    #    <mailbox>
    if (mailbox(i, string) == False):
        return exit()
    i = mailbox(i, string)
    #   ">"
    if(not(string[i] == ">")):
        print("ERROR -- no >")
        return exit()
    if(length_check(i, string)):
        return True
    print("ERROR -- path")


def mailbox(i, string):
    #    <local-part>
    if (local_part(i, string) == False):
        return exit()
    i = local_part(i, string)
    #   "@"
    if(not(string[i] == '@')):
        print("ERROR -- mailbox")
        return exit
    if(not(length_check(i, string))):
        return exit()
    i += 1
    #   <domain>
    if (domain(i, string) == False):
        return exit()
    return domain(i, string)


def local_part(i, string):
    local_part_start = i
    #   <string>
    if(string_(i, string) == False):
        print("ERROR -- local-part")
        return exit()
    i = string_(i, string)
    if local_part_start == i:
        print("ERROR -- local-part")
        return exit()
    return i


def string_(i, string):
    #   <char> | <char> <string>
    if(char(string[i])):
        return exit()
    i += 1
    length_check(i, string)
    if(string[i] == '@'):
        return i
    return string_(i, string)


def char(c):
    #   any one of the printable ASCII characters, but not any
    #       of <special> or <SP>
    if(special(c) or SP(c)):
        return True
    return False


def domain(i, string):
    #    <element> | <element> "." <domain>
    '''
    while i != (len(string)):
        if special(string[i]):
            print("ERROR -- domain")
            return exit()
        i += 1
    '''
    if(element(i, string) == False):
        print("ERROR -- domain")
        return exit()
    i = element(i, string)
    while(string[i] == '.'):
        i += 1
        if(element(i, string) == False):
            print("ERROR -- domain")
            return exit()
        i = element(i, string)
    if(not(length_check(i + 1, string))):
        return exit()
    i += 1
    return i


def element(i, string):
    #   <letter> | <name>
    if(name(i, string) != False):
        return name(i, string)
    elif(letter(string[i])):
        return i
    else:
        return exit()


def name(i, string):
    #   <letter> <let-dig-str>
    if(not(letter(string[i]))):
        return exit()
    if(end_check(i, string)):
        return i
    if(let_dig_str(i, string) == False):
        return exit()
    i = let_dig_str(i, string)
    return i


def letter(c):
    #   any one of the 52 alphabetic characters A through Z
    #       in upper case and a through z in lower case
    if c.isalpha():
        return True
    return exit()


def let_dig_str(i, string):
    #    <let-dig> | <let-dig> <let-dig-str>
    if(let_dig(string[i])):
        if(not(length_check(i, string))):
            return False
        i += 1
        if(end_check(i, string)):
            return i
        return let_dig_str(i, string)
    elif(string[i] == '.'):
        return i


def let_dig(c):
    #    <letter> | <digit>
    if(letter(c) | digit(c)):
        return True
    return False


def digit(c):
    #    any one of the ten digits 0 through 9
    digits = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    if c in digits:
        return True
    return exit()


def CRLF(c):
    #    the newline character
    if(c == '\n'):
        print("ERROR -- CRLF")
        return exit()
    return True


def special(c):
    #   special list ... shouldn't be in input
    special_list = ['<', '>', '(', ')', '[', ']',
                    '\\', '.', ',', ';', ':', '@', '"']
    if c in special_list:
        return True
    return False


def main():
    # Get user input from keyboard
    # mail_from = raw_input()
    '''
    for line in sys.stdin:
        if 'q' == line.rstrip():
            break
            '''
    pass1 = "MAIL FROM:<he@h>"
    pass2 = "MAIL  FROM:<eh@h>"
    pass3 = "MAIL  FROM: <he@h>"
    pass4 = "MAIL        FROM:       <123@h>"
    pass5 = "MAIL                 FROM:          <dijie2ei2ieie2j@e23456>"
    pass6 = "MAIL FROM:<hi@e2.e4.e6>"

    fail1 = "mAIL FROM:<he@h"
    fail2 = "MAIL fROM:<he@h"
    fail3 = "MAIL FROM:< he@h"
    fail4 = " MAIL FROM:<heh@h"
    fail5 = "MAIL    FROM:"
    fail6 = "MAILFROM:<"
    fail7 = "MAIL ! FROM:<hi@hi"
    fail8 = "MAIL! FROM:<hi@hi"
    fail9 = "MAIL FROM:<hi\@dd"
    fail10 = "MAIL FROM:<cnell@h.hi"
    fail11 = "MAIL FROM:<cd@."
    fail12 = "MAIL FROM:<hi@hi.com"
    fail13 = "MAIL FROM:<hi@hi.>"
    fail14 = "MAIL FROM:<cnell@he.h.i"

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

    print("\nfail")
    print("1 = mail from")
    mail_from_cmd(fail1)
    print("2 = mail from")
    mail_from_cmd(fail2)
    print("3 = local part")
    mail_from_cmd(fail3)
    print("4 = mail from")
    mail_from_cmd(fail4)
    print("5 = incomplete")
    mail_from_cmd(fail5)
    print("6 = whitespace")
    mail_from_cmd(fail6)
    print("7 = mail from")
    mail_from_cmd(fail7)
    print("8 = whitespace")
    mail_from_cmd(fail8)
    print("9 = special in local part")
    mail_from_cmd(fail9)
    print("10 = domain")
    mail_from_cmd(fail10)
    print("11 = domain")
    mail_from_cmd(fail11)
    print("12 = no end >")
    mail_from_cmd(fail12)
    print("13 = no domain after .")
    mail_from_cmd(fail13)
    print("14 = no end >.")
    mail_from_cmd(fail14)


main()
