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
    if (string[i] != "<"):
        print("ERROR -- path")
        return exit()
    i += 1
    if(length_check(i, string) == False):
        return exit()
    #    <mailbox>
    if (mailbox(i, string) == False):
        return exit()
    i = mailbox(i, string)
    #   ">"
    if(not(string[i] == ">")):
        print("ERROR -- path")
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
    if((special(c) or SP(c)) or not(ord(c) < 128) or not(CRLF(c))):
        return True
    return False


def domain(i, string):
    #    <element> | <element> "." <domain>
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
        if(name(i, string) == null):
            return exit()
        # print(string[i])
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
    elif(let_dig_str(i, string) == null):
        return null
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
    if(string[i] == '\\'):
        return null
    if(let_dig(string[i])):
        if(not(length_check(i, string))):
            return False
        i += 1
        if(end_check(i, string) & let_dig(string[i])):
            return i
        return let_dig_str(i, string)
    if(string[i] == '.'):
        return i
    return exit()


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
    for line in fileinput.input():
        line = line.rstrip()
        print(line)
        mail_from_cmd(line)


main()
