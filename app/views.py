from app import app
from flask import request
import json
import os
import re

home = os.environ['HOME']
credentials_path = "%s/.aws/credentials" % home

def creds_parser(credentials):
   return_creds = {}
   creds = credentials.split("[")
   for cred in creds:
      fields = cred.split('\n')
      if "]" in fields[0]:
         fields[0] = fields[0].replace("]","")
         cred_row = {}
         for field in fields[1:]:
            try:
              k = re.search("(.*?) ", field).group(1)
              v = re.search(".* (.*)", field).group(1)
              cred_row[k]=v
            except:
              continue
         return_creds[fields[0]] = cred_row
   return return_creds


def creds_format_for_profile(credentials):
   outlines = ""
   for cred in credentials.keys():
      outlines += "[%s]" % cred
      outlines += '\n'
      for k in credentials[cred].keys():
         outlines += "%s = %s" % (k, credentials[cred][k])
         outlines += '\n'
      outlines += '\n'
   return outlines


def write_aws_profiles(profiles):
   profile_file = open(credentials_path, "w")
   profile_file.write(profiles)
   profile_file.close()
   return()

@app.route('/')
@app.route('/index')
def index():
   print request.get_json()


@app.route('/', methods=['POST'])
def update_profile():
   # Get the new profile
   data = request.get_data()
   data = json.loads(data)
   new_profile = {}
   try:
      profile_name = data['profile_name']
      new_profile['aws_access_key_id'] = data['aws_access_key_id']
      new_profile['aws_secret_access_key'] = data['aws_access_key_secret']
      new_profile['aws_session_token'] = data['session_token']
      new_profile['expiration'] = data['token_expiration']
   except:
      return "Thank you, come again"

   # Get current profiles
   creds = open(credentials_path, "r")
   cred = creds.read()
   creds.close()
   cred = creds_parser(cred)

   #Add or Update the new profile
   cred[profile_name] = new_profile
   outfile = creds_format_for_profile(cred)

   #Write to credentials file
   write_aws_profiles(outfile)

   print outfile
   return "Thank you, come again"
