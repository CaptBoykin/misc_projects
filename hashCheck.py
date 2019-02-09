# Author: @CaptBoykin

# hashCheck.py is an exercise in utilizing 
# tkinter as well as cryptographic hashing

# hashCheck.py compares the hash values of two 
# supplied files and reports upon a collision or
# sign of modification
try:
    import os, hashlib, tkinter, tkinter.filedialog
except ImportError:
    raise ImportError()


# Main Window Settings  
mainWindow = tkinter.Tk()
mainWindow.title("Hash Tampering & Collision Tool")
mainWindow.geometry('800x600')
mainWindow['padx'] = 15
mainWindow['pady'] = 15

mainWindow.columnconfigure(0,weight=0)
mainWindow.columnconfigure(1,weight=0)
mainWindow.columnconfigure(2,weight=0)
mainWindow.columnconfigure(3,weight=0)
mainWindow.columnconfigure(4,weight=0)
mainWindow.columnconfigure(5,weight=0)

mainWindow.rowconfigure(0,weight=0)
mainWindow.rowconfigure(1,weight=0)
mainWindow.rowconfigure(2,weight=0)
mainWindow.rowconfigure(3,weight=0)
mainWindow.rowconfigure(4,weight=0)
mainWindow.rowconfigure(5,weight=0)
mainWindow.rowconfigure(6,weight=0)

# Top Label / Title
label = tkinter.Label(mainWindow, text= "Hash Tampering & Collision Tool")
label.config(height=1)
label.grid(row=0, column=0, columnspan=4, sticky='NEW')

# File Handling and output to Screen
# Yes...Globals REEEEEEEEEEEEE
fileName1 = ''
fileName2 = ''
outfileName = ''
outfileToggle = tkinter.IntVar()
def openFile1():
    global fileName1
    fileResult1.delete(1.0,tkinter.END)
    fileName1 = tkinter.filedialog.askopenfilename()
    if fileName1:
        fileResult1.insert(1.0,fileName1)
    else:
        pass
        
def openFile2():
    global fileName2
    fileResult2.delete(1.0,tkinter.END)
    fileName2 = tkinter.filedialog.askopenfilename()
    if fileName2:
        fileResult2.insert(1.0,fileName2)
    else:
        pass
            
def saveFile():
    global outfileName
    outFileResult.delete(1.0,tkinter.END)
    outfileName = tkinter.filedialog.asksaveasfilename()
    if outfileName:
        outFileResult.insert(1.0,outfileName)
    else:
        pass

def toggleFunc():
    if outfileToggle.get() == 1:
        outFileResult.config(background='#000000', state='normal')
        fileButton3.config(state='normal')
        return
    elif outfileToggle.get() == 0:
        outFileResult.config(background='#E0E0E0', state='disabled')
        fileButton3.config(state='disabled')
        return
    else:
        pass
        
        
# Hashing and output onto screen.
def hashCompare(mode):
    hashResult1.delete(1.0,tkinter.END)
    hashResult2.delete(1.0,tkinter.END)
    
    if not fileName1 or not fileName2:
        hashResult1.insert(1.0,"[-] Please Select Files\n")
        return
    
    if not outfileName and outfileToggle.get() == 1:
        hashResult1.insert(1.0,"[-] Please Select Outfile\n")
        return
        
    if outfileName and outfileToggle.get() == 1:
        outfile = open(outfileName,'w+')
    
    # Blocksize for file input
    BLOCKSIZE = 65535
    
    # FileName1
    m11 = hashlib.md5()
    m12 = hashlib.sha1()
    m13 = hashlib.sha256()
    m14 = hashlib.sha512()
    
    # FileName2
    m21 = hashlib.md5()
    m22 = hashlib.sha1()
    m23 = hashlib.sha256()
    m24 = hashlib.sha512()
    
    
    # Putting the filenames in a list due to escaping issues
    fileList = []
    fileList.append(fileName1)
    fileList.append(fileName2)
    
    # hashing file 1
    m11.update(open(fileList[0],'rb').read(BLOCKSIZE))
    m12.update(open(fileList[0],'rb').read(BLOCKSIZE))
    m13.update(open(fileList[0],'rb').read(BLOCKSIZE))
    m14.update(open(fileList[0],'rb').read(BLOCKSIZE))
    M11 = m11.hexdigest()
    M12 = m12.hexdigest()
    M13 = m13.hexdigest()
    M14 = m14.hexdigest()
    
    # hashing file 2
    m21.update(open(fileList[1],'rb').read(BLOCKSIZE))
    m22.update(open(fileList[1],'rb').read(BLOCKSIZE))
    m23.update(open(fileList[1],'rb').read(BLOCKSIZE))
    m24.update(open(fileList[1],'rb').read(BLOCKSIZE))
    M21 = m21.hexdigest()
    M22 = m22.hexdigest()
    M23 = m23.hexdigest()
    M24 = m24.hexdigest()       

    # I was forced to use ganky kind of tab scheme for the output as that's
    # what I managed to get working with the tkinter output textbox
    OUTPUT = """
File1:  {0}
MD5:    {1}
SHA1:   {2}
SHA256: {3}
SHA512: {4}

File2:  {5}
MD5:    {6}
SHA1:   {7}
SHA256: {8}
SHA512: {9}
    """.format(fileList[0],M11,M12,M13,M14,
               fileList[1],M21,M22,M23,M24)
    
    
    # Write to a file if needed
    if outfileName:
        outfile.write(OUTPUT)
    else:
        hashResult2.insert(1.0,OUTPUT)
    
    
    # Comparison of hashes, generates an error per mismatch.
    WARN1 = ''
    WARN2 = ''
    GOOD = ''
    hashList0 = ['MD5','SHA1','SHA256','SHA512']
    hashList1 = [M11,M12,M13,M14]
    hashList2 = [M21,M22,M23,M24]
    for i in range(0,4):
        if mode == 'tamper':
            if hashList1[i] != hashList2[i]:
                WARN1 = """[!] TAMPERING DETECTED!\n\n\n"""
                WARN2 = """
File1:  {0}
{1}:    {2}
File2:  {3}
{4}:    {5}
                """.format(fileList[0],hashList0[i],
                           hashList1[i],fileList[1],
                           hashList0[i],hashList2[i])
                if outfileName:
                    outfile.write(WARN2)
                    hashResult1.config(foreground="#FF0000")
                    hashResult1.insert(1.0,WARN1)
                    hashResult2.insert(1.0,"[+] OUTFILE SUCCESSFULLY WRITTEN!\n")
                else:
                    hashResult1.config(foreground="#FF0000")
                    hashResult1.insert(1.0,WARN1)
                    hashResult2.insert(1.0,WARN2)
        if mode == 'collision':
            if hashList1[i] == hashList2[i]:
                WARN1 = """[!] COLLISION DETECTED!\n\n\n"""
                WARN2 = """
File1:  {0}
{1}:    {2}
File2:  {3}
{4}:    {5}
                """.format(fileList[0],hashList0[i],
                           hashList1[i],fileList[1],
                           hashList0[i],hashList2[i])
                if outfileName:
                    outfile.write(WARN2)
                    hashResult1.config(foreground="#FF0000")
                    hashResult1.insert(1.0,WARN1)
                    hashResult2.insert(1.0,"[+] OUTFILE SUCCESSFULLY WRITTEN!\n")
                else:
                    hashResult1.config(foreground="#FF0000")
                    hashResult1.insert(1.0,WARN1)
                    hashResult2.insert(1.0,WARN2)
    if (mode == 'collision') and (not WARN1 or not WARN2):
        GOOD = """[+] NO COLLISIONS DETECTED!\n\n\n"""
        if outfileName:
            outfile.write(GOOD)
            hashResult1.config(foreground="#00FF00")
            hashResult1.insert(1.0,GOOD)
            hashResult2.insert(1.0,"[+] OUTFILE SUCCESSFULLY WRITTEN!\n")
        else:       
            hashResult1.config(foreground="#00FF00")
            hashResult1.insert(1.0,GOOD)
    if mode == 'tamper' and (not WARN1 or not WARN2):
        GOOD = """[+] NO TAMPERING DETECTED!\n\n\n"""
        if outfileName:
            outfile.write(GOOD)
            hashResult1.config(foreground="#00FF00")
            hashResult1.insert(1.0,GOOD)
            hashResult2.insert(1.0,"[+] OUTFILE SUCCESSFULLY WRITTEN!\n")
        else:
            hashResult1.config(foreground="#00FF00")
            hashResult1.insert(1.0,GOOD)    

        
    listScroll = tkinter.Scrollbar(mainWindow, orient=tkinter.VERTICAL, command=hashResult2.yview)
    listScroll.grid(row=6, column=5, sticky='NSW', rowspan=1)
    hashResult2['yscrollcommand'] = listScroll.set
    
    if outfileName:
        outfile.close()

    return
            
            
#### FILE UPLOADS       
fileButton1 = tkinter.Button(mainWindow, text="Select File 1", command=openFile1)
fileButton1.config(height=1)
fileButton1.grid(row=1,column=0,sticky='NEWS', padx=3)

fileResult1 = tkinter.Text(mainWindow, background='#000000', foreground='#FFFFFF', relief='sunken')
fileResult1.config(height=1,width=10)
fileResult1.grid(row=1, column=1, sticky='NEWS', pady=2, padx=2, columnspan=3)

fileButton2 = tkinter.Button(mainWindow, text="Select File 2", command=openFile2)
fileButton2.config(height=1)
fileButton2.grid(row=2,column=0, sticky='NEWS', padx=3)

fileResult2 = tkinter.Text(mainWindow, background='#000000', foreground='#FFFFFF', relief='sunken')
fileResult2.config(height=1,width=10)
fileResult2.grid(row=2, column=1, sticky='NEWS', pady=2, padx=2, columnspan=3)


#### CHECK TAMPER/ COLLISION/ CANCEL    
hashButton1 = tkinter.Button(mainWindow, text="Check Tampering")
hashButton1['command'] = lambda arg1 = 'tamper': hashCompare(arg1)
hashButton1.grid(row=4,column=1,pady=2, sticky='NEWS')
hashButton1.config(width=10)

hashButton2 = tkinter.Button(mainWindow, text="Check Collisions")
hashButton2['command'] = lambda arg1 = 'collision': hashCompare(arg1)
hashButton2.grid(row=4,column=2,pady=2, sticky='NEWS')
hashButton2.config(width=10)

cancelButton = tkinter.Button(mainWindow, text="Cancel", command=mainWindow.destroy)
cancelButton.grid(row=4,column=4,pady=2, sticky='NEWS')
hashButton2.config(width=10)


#### OUTPUTS
hashResult1 = tkinter.Text(mainWindow, relief='sunken', background='#000000', foreground='#FFFFFF')
hashResult1.grid(row=5,column=1,columnspan=4, sticky='NEWS',pady=3)
hashResult1.config(height=2)

hashResult2 = tkinter.Text(mainWindow, relief='sunken', background='#000000', foreground='#FFFFFF')
hashResult2.grid(row=6,column=1,columnspan=4, sticky='NEWS',pady=3)

#### LABELS AND FRAMES
outfileFrame = tkinter.LabelFrame(mainWindow, text='Options', bd=2)
outfileFrame.grid(row=0,column=4, rowspan=4, sticky='NEWS', padx=2)

outputLabel1 = tkinter.Label(mainWindow, text='Status')
outputLabel1.grid(row=5,column=0,sticky='NE')

outputLabel2 = tkinter.Label(mainWindow, text='Output')
outputLabel2.grid(row=6,column=0,sticky='NE')


#### FILE OUTPUT
outFileResult = tkinter.Text(mainWindow, background='#E0E0E0', foreground='#FFFFFF',state='disabled')
outFileResult.config(height=1,width=10)
outFileResult.grid(row=3, column=1, sticky='NEWS', pady=2, padx=2, columnspan=3)

fileButton3 = tkinter.Button(mainWindow, text="Select Outfile")
fileButton3.config(height=1, state='disabled')
fileButton3['command'] = saveFile
fileButton3.grid(row=3,column=0, sticky='NEWS', padx=3)

checkButton = tkinter.Checkbutton(outfileFrame, text="Write to Outfile", variable=outfileToggle)
checkButton.config(height=1)
checkButton['command'] = toggleFunc
checkButton.grid(row=3,column=4, sticky='NEWS', padx=3)


mainWindow.mainloop()
