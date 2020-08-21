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
    from_ = string[0:5]
    if(not(fromString == from_)):
        print("ERROR -- mail-from-cmd")
        return False
    string = string[5:]
    #    <nullspace>
    string = nullspace(string)
    #   <reverse-path>
    string = reverse_path(string)
    if(not(string)):
        print("ERROR -- reverse-path")
        return False
    #    <nullspace>
    string = nullspace(string)
    if(not(string)):
        return False
    #   <CLRF>
    string = CRLF(string)
    if(not(string)):
        return False
    print("Sender ok")
    return True


def whitespace(string):
    #   <SP> | <SP> <whitespace>
    if(not(SP(string[0]))):
        return string[0:]
    return whitespace(string[1:])


def SP(c):
    #   the space or tab char
    if(c == '\t' or c == ' '):
        return True
    return False


def nullspace(string):
    if(null(string[0])):
        return string
    return whitespace(string)


def null(c):
    if((c != ' ') or (c != '\t')):
        return True
    return False


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
    if(char(string[0]) == False):
        return string
    return string_(string[1:])


def char(c):
    #   any one of the printable ASCII characters, but not any
    #       of <special> or <SP>
    if(special(c) or SP(c) or not(ord(c) < 128) or CRLF(c)):
        return False
    return True


def domain(string):
    string = element(string)
    if(string[0] == '.'):
        string = domain(string[1:])
    return string


def element(string):
    if(not(letter(string[0]))):
        return string
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
    mail_from_cmd("MAIL FROM:<hi@hi.com>\n")


main()
