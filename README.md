1.
  Max Starreveld
  Chapman ID# 2380029
  starreveld@chapman.edu
  CPSC-408-01 (German)
  Assignment 1: Student Database
  
2. Files Submitted
  SDBInterface.py: The script for the database access application.
  README.md: overview document

3. Errors
  -Not really an error but an environment requirement to prevent errors. The program uses f-strings for input at some points, introduced from what I can tell in python 3.6. If the python version in your container predates that, the program will not compile or work. As a result, the code executes perfectly fine with no errors or issues past python 3.6 but will not function before. I learned this the hard way when moving testing from my ide virtual runtime environment to my docker container.

4. References used
  -A number of various API pages for certain methods.
        
  -ChatGPT: Primary functions being menial python assistance and information as I am not too well versed in the language, bug fixing, and a few minute features, such as F-Strings. Code solutions were independent of the chatbot.
     
5. Run instructions

  -Run in docker: python SDBInterface.py
  -As mentioned above in the errors section, make sure docker container has python 3.6 or greater. Previous versions will be incapable of compiling it. 