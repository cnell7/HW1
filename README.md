A program that determines if a message (a text string) is a valid SMTP “MAIL FROM” message. This is a message that tells a mail server who (which user) is trying to send an email
message. 

This part of the SMTP server is finished and fully functional. 


-----Grammar-----


<mail-from-cmd> ::= “MAIL” <SP> “FROM:” <reverse-path> <CRLF>
<reverse-path> ::= <path>
<path> ::= "<" <mailbox> ">"
<mailbox> ::= <local-part> "@" <domain>
<local-part> ::= <string>
<string> ::= <char> | <char> <string>
<char> ::= any one of the printable ASCII characters, but not any
<special> or <SP>
<domain> ::= <element> | <element> "." <domain>
<element> ::= <letter> | <name>
<name> ::= <letter> <let-dig-str>
<letter> ::= any one of the 52 alphabetic characters A through Z
in upper case and a through z in lower case
<let-dig-str> ::= <let-dig> | <let-dig> <let-dig-str>
<let-dig> ::= <letter> | <digit>
<digit> ::= any one of the ten digits 0 through 9
<CRLF> ::= the newline character
<SP> ::= the space or tab character
<special> ::= "<" | ">" | "(" | ")" | "[" | "]" | "\" | "."
| "," | ";" | ":" | "@" | """ 
