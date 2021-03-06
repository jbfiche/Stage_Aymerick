#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 12 11:42:36 2020

This file contains all the methods to Read and copy files with threading 

@author: aymerick

"""

import glob
import time
import json
import os
import ManipulationParameters as MP                     # No need to specify the path to "ManipulationParameters" if all the scripts are in the same folders
from threading import Thread

NewFile=[]                              # Create a dictionnary
NumberOfNewFiles=0                      # Count the amount of new files in the depository
AlreadyCopied=0                         # Count the amount of file already copied 
CheckFinished=False                     # Check if the class read has finished to check the folder

class Read(Thread):
    """
    
    The goal of this class is to check if there is a new file in target folder.
    If there is, we want to identify wich one et copy it with the other class.
    We want to be able to do both Read and Copy at the same time, so we will use thread.

    Parameters
    ----------
    None.
    
    Returns
    -------
    None.

    
    """
    
    def __init__(self):
        """
        Initialisation of the class
        
        Returns
        -------
        None.
        
        """
        Thread.__init__(self)        # Initialisation of thread
        self.waitBeforeNewCheck = 1
        
    def run(self): 
        """
        The run method is checking if there is any new file in target folder.
        If there is, we will copy it to target folder with the class Copy

        Returns
        -------
        None.
        
        """
        global NewFile                                          # Call the variable defined outside the class
        global NumberOfNewFiles                                 # We want the variable to be global, because we will use it in the other class 
        global CheckFinished                                    # This is how the class will be able to interact with each other.
      
        for i in range (0,MP.Duration):                         # We want to check the file during all the manipulation. So, the user will write the duration of the manipulation in ManipulationParameters.py
            OLD=glob.glob(MP.Path1+"*"+MP.Format)               # Check what contains the folder. MP.Path1 → Path to the folder; MP.Format → Format of the data (.csv,.jpg,.....)
            time.sleep(self.waitBeforeNewCheck)                                       # Wait one second
            NEW=glob.glob(MP.Path1+"*"+MP.Format)               # Check if the programms in the folder has changed. (Important: If there is new data but their format are not corresponding to MP.Format, NEW and OLD will be the same)
            if OLD != NEW:                                      # Check if something has changed during the one second delay
                if len(OLD)==0:                                 # See if it's the first time a new file (or more) is in the folder
                    NewFile=NEW
                    NumberOfNewFiles=len(NEW)
                    print("Original list of files: \n{}".format(NEW))
                else:                                           # If it's not the first time a file is added to the folder
                    listNewFiles=[x for x in NEW if x not in OLD]
                    NumberOfNewFiles=len(listNewFiles)
                    NewFile.append(listNewFiles)
                    print("New file added: \n{}".format(listNewFiles))
                           
        CheckFinished=True                                      # The class has finished to check the folder (The manipulation is finished)
        print("Check Finished")
                
            
            
class Copy(Thread):
    """
    
    The goal of this class is to copy new files to a specific folder.
    We want to copy them in JSON, beacause it will be easier to use when processingt (analyzing data,....)
    We want to be able to do both Read and Copy at the same time, so we will use thread.

    Parameters
    ----------
    None.
    
    Returns
    -------
    None.

    
    """
    def __init__(self):
        """
        Initialisation of the class
        
        Returns
        -------
        None.
        
        """
        Thread.__init__(self)                            # Initialisation of thread
        
    def run(self):  
        """
        The run method is checking if a new file has been detected by the class Read.
        If there is, we will copy it to target folder in .JSON format.

        Returns
        -------
        None.
        
        """

        global NewFile                                               # Call the variable defined outside the class and modified (or not) by the class Read()
        global NumberOfNewFiles
        global AlreadyCopied
        global CheckFinished
        
        while CheckFinished==False or AlreadyCopied != NumberOfNewFiles:      # We want to check if a new file has been detected by Read() but when Read() has finished (manipulation is over), we want to stop checking.     
            if AlreadyCopied != NumberOfNewFiles:                             # If Read() has detected new files
                for i in range (AlreadyCopied,NumberOfNewFiles):              # We want to copy all of the new files
                    AlreadyCopied=AlreadyCopied+1                             # We copied one file so we add one to the value of AlreadyCopied
                    time.sleep(4)                                             # This time is to simulate a long time for the copy (you can delete it)
                    Caractere="/"
                    Prog=NewFile[i].split(Caractere)                          # We are looking for the name of the new file
                    os.chdir(MP.Path1)                                        # Change the working directory to MP.Path1 (Directory 1 in our case)
                    File=open(str(Prog[len(Prog)-1]),"r")                     # Open the file in read mode
                    lines=File.readlines()                                    # Save all the content of the file in lines
                    File.close()                                              # Close the file
                    try: 
                        os.chdir(MP.Path2)                                    # Change the working directory to MP.Path2 (Where we want to copy the file; Directory 2 in our case)
                        Caractere=(".")
                        Prog=Prog[len(Prog)-1].split(Caractere)               # Just some formating to have "Test.json" in the new directory and not "Test.csv.json"
                        File=open(str(Prog[0])+".json","x")                   # CREATE a new file in the folder in .json
                        File.write(json.dumps(lines))                         # Write all the data in json format in the file
                        File.close()                                          # Close the file
                    except FileExistsError:                                   # If the file is already existing, we can't create a new one. So, we manage the error with try and except
                        print("File already exist")
        print("Copy Finished")
                
 
if __name__ == "__main__":           
        
    Thread_1=Read()
    Thread_2=Copy()

    Thread_1.start()
    Thread_2.start()

    Thread_1.join()
    Thread_2.join()
