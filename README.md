# SECURITY-LOG-ANALYSER-FOR-IT-SYSTEMS-
It is an tool designed for monitoring the security logs of the system


This is an log analyser developed using python programing .

I) #Post libraries requirements:
    1)OS
    2)win32eventlog
    3)datetime
    4)xml.etree.ElementTree
    5)tkinter
    6)paramiko

    ![Screenshot (9)](https://github.com/BALASUBRAMANIYANB/SECURITY-LOG-ANALYSER-FOR-IT-SYSTEMS-/assets/109799408/f44a3617-c3db-49f7-a649-8609ffcaf1f2)

    
II) #import or gitcolne the repository "Security log analyser"

    1)install the pakages needed for the application to run .

    2)create a file named log.xml in the project folder.

    3)specify the xml file path in the main or log analyser python file.the Application runs only if the path specified correctly.
    this XML file is to save the security logs collected from the local system .

    4)This application collects the log from the system with the waiting time of 5 seconds ,this collects the data in realtime scenario and updates the log in the xml file.

    5)The collected log files wiil be visualized in an table with tha follwing attribute details:
                           *ID
                           *LOG TYPE
                           *LOG NAME
                           *DATE AND TIME
                           *DETAILS OF LOG 
                           *USERNAME
                           *MACHINE NAME
   6)We can able to access the raw logs visit the xml file created .

   7) The xml file cannot be understood ,this is because only the raw data will be available in the xml file.

      
III) To execute the applcation 

   1) run the log anlyser file with the admin privillage in windows and for linux execute it with root privillage.
   2) once executing the file the logs wiil be start collecting and a box wiil be opened to view the logs and the details of same.


![Screenshot (5)](https://github.com/BALASUBRAMANIYANB/SECURITY-LOG-ANALYSER-FOR-IT-SYSTEMS-/assets/109799408/13dcccc8-4e8d-4001-8932-71393e8a058a)
