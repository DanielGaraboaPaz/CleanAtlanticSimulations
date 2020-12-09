#!/bin/bash
#set +x

echo 'Welcome to user-pwd replacer for MOSI json.'
echo '-> CMEMS username:'
read user
echo '-> password for' $user':'
read pass

function replace_pwd_user(){

	if grep -q 'user\|pwd' $1 ;then

        echo '-> Replacing in: ' $1
		user_replace='"user":"'$user_cmems'",'
		pass_replace='"pwd":"'$pass_cmems'",'
		sed -i '/"user":/c\\    '$user_replace $1
		sed -i '/"pwd":/c\\    '$pass_replace $1
		
	fi
}
 
export user_cmems=$user
export pass_cmems=$pass
export -f replace_pwd_user
find . -name "*.json" -exec bash -c 'replace_pwd_user "$1"' - {} \;
