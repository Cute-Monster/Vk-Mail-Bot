#!/bin/bash

#===================================#

#####################################
#                                   #
# Variables used to connect to mail #
# smtp server and checking for new  #
#                                   #
#####################################
export MAIL_LINK=''
export MAIL_USERNAME=''
export MAIL_PASSWORD=''

#===================================#

#####################################
#                                   #
# String value used as seed for     #
# generating hash from mail text    #
# and storing it at DataBase. This  #
# is used to optimize data storage  #
# and message existing checks       #
#                                   #
#####################################
export DB_SEED=''

#===================================#

#####################################
#                                   #
# Vars used to connect to VK API    #
# and send notifications            #
#####################################
export VK_API_TOKEN='' # VK API token for group based auth

# Username and Password for user based auth
export VK_USERNAME=''
export VK_PASSWORD=''

# User ID used as admin ID to send INFO notifications
# also some exception notifications
# and of course for new mails as well 
export VK_ADMIN_ID=''

#===================================#
