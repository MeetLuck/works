:: redirection
command > filename        Redirect command output to a file  
command >> filename       APPEND into a file  
command < filename        Type a text file and pass the text to command  
commandA  |  commandB     Pipe the output from commandA into commandB  
commandA &  commandB      Run commandA and then run commandB  
commandA && commandB      Run commandA, if it succeeds then run commandB  
commandA || commandB      Run commandA, if it fails then run commandB  
commandA && commandB || commandC` If commandA succeeds run commandB, if it fails commandC 
