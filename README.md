A program that determines if a message (a text string) is a valid SMTP “MAIL FROM” message. This is a message that tells a mail server who (which user) is trying to send an email
message. 

This part of the SMTP server is finished and fully functional. 


-----Grammar-----



<mail-from-cmd_> ::= “MAIL” <SP_> “FROM:” <reverse-path_> <CRLF_>


<reverse-path_> ::= <path_> 


<path_> ::= "<" <mailbox_> ">"


<mailbox_> ::= <local-part_> "@" <domain_>


<local-part_> ::= <string_>


<string_> ::= <char_> | <char_> <string_>


<char_> ::= any one of the printable ASCII characters, but not any <special_> or <SP_>


<domain_> ::= <element_> | <element_> "." <domain_>


<element_> ::= <letter_> | <name_>


<name_> ::= <letter_> <let-dig-str_>


<letter_> ::= any one of the 52 alphabetic characters A through Z in upper case and a through z in lower case


<let-dig-str_> ::= <let-dig_> | <let-dig_> <let-dig-str_>


<let-dig_> ::= <letter_> | <digit_>


<digit_> ::= any one of the ten digits 0 through 9


<CRLF_> ::= the newline character


<SP_> ::= the space or tab character


<special_> ::= "<" | ">" | "(" | ")" | "[" | "]" | "\" | "."
| "," | ";" | ":" | "@" | """  
  

(Some of the grammar tokens are not the same as the comments in the code. This is because github is hiding the token names inside the <>. That is also why there are extra '_'.)
