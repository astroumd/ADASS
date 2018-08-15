#! /usr/bin/env python
#
# alternative ideas:
#     http://naelshiab.com/tutorial-send-email-python/
#     https://www.geeksforgeeks.org/send-mail-attachment-gmail-account-using-python/
#     https://medium.freecodecamp.org/send-emails-using-code-4fcea9df63f?gi=61be8b3ff3dd
#     https://arjunkrishnababu96.github.io/Send-Emails-Using-Code/
#


# This needs to be in python3


import sys

def get_file(filename):
    """
    read file, return list of lines, but skip comment and blank lines
    """
    out = []
    f = open(filename)
    lines = f.readlines()
    f.close()
    for line in lines:
        if line[0] == '#': continue
        line = line.strip()
        if len(line) == 0: continue
        out.append(line)
    return out

# Function to read the contacts from a given contact file and return a
# list of names and email addresses
def get_contacts(filename):
    names = []
    emails = []
    with open(filename, mode='r', encoding='utf-8') as contacts_file:
        for a_contact in contacts_file:
            names.append(a_contact.split()[0])
            emails.append(a_contact.split()[1])
    return names, emails

from string import Template

def read_template(filename):
    with open(filename, 'r', encoding='utf-8') as template_file:
        template_file_content = template_file.read()
    return Template(template_file_content)


# import the smtplib module. It should be included in Python by default
import smtplib


if __name__ == "__main__":
    emails = sys.argv[1]
    template = sys.argv[2]
