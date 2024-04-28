#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pand
import os
import cv2
from matplotlib import pyplot as plt


# In[2]:


def txt_encode(text):
    l=len(text)
    i=0
    add=''
    while i<l:
        t=ord(text[i])
        if(t>=32 and t<=64):
            t1=t+48
            t2=t1^170       #170: 10101010
            res = bin(t2)[2:].zfill(8)
            add+="0011"+res
        
        else:
            t1=t-48
            t2=t1^170
            res = bin(t2)[2:].zfill(8)
            add+="0110"+res
        i+=1
    res1=add+"111111111111"
    print("The string after binary conversion appyling all the transformation :- " + (res1))   
    length = len(res1)
    print("Length of binary after conversion:- ",length)
    HM_SK=""
    ZWC={"00":u'\u200C',"01":u'\u202C',"11":u'\u202D',"10":u'\u200E'}      
    file1 = open("cover_text.txt","r+")
    nameoffile = "new_file.txt"
    file3= open(nameoffile,"w+", encoding="utf-8")
    word=[]
    for line in file1: 
        word+=line.split()
    i=0
    while(i<len(res1)):  
        s=word[int(i/12)]
        j=0
        x=""
        HM_SK=""
        while(j<12):
            x=res1[j+i]+res1[i+j+1]
            HM_SK+=ZWC[x]
            j+=2
        s1=s+HM_SK
        file3.write(s1)
        file3.write(" ")
        i+=12
    t=int(len(res1)/12)     
    while t<len(word): 
        file3.write(word[t])
        file3.write(" ")
        t+=1
    file3.close()  
    file1.close()
    print("\nStego file has successfully generated")


# In[3]:


def encode_txt_data(cover_text_file_path, text1):
    count2=0
    with open(cover_text_file_path, "r+") as file1:
        for line in file1: 
            for word in line.split():
                count2=count2+1
    file1.close()       
    bt=int(count2)
    print("Maximum number of words that can be inserted :- ",int(bt/6))
    l=len(text1)
    if(l<=bt):
        print("\nInputed message can be hidden in the cover file\n")
        txt_encode(text1)
    else:
        print("\nString is too big please reduce string size")
        encode_txt_data()


# In[4]:


def BinaryToDecimal(binary):
    string = int(binary, 2)
    return string


# In[5]:


def decode_txt_data(filename):
    ZWC_reverse={u'\u200C':"00",u'\u202C':"01",u'\u202D':"11",u'\u200E':"10"}
    stego=filename
    file4= open(stego,"r", encoding="utf-8")
    temp=''
    for line in file4: 
        for words in line.split():
            T1=words
            binary_extract=""
            for letter in T1:
                if(letter in ZWC_reverse):
                     binary_extract+=ZWC_reverse[letter]
            if binary_extract=="111111111111":
                break
            else:
                temp+=binary_extract
    # print("\nEncrypted message presented in code bits:",temp) 
    lengthd = len(temp)
    # print("\nLength of encoded bits:- ",lengthd)
    i=0
    a=0
    b=4
    c=4
    d=12
    final=''
    while i<len(temp):
        t3=temp[a:b]
        a+=12
        b+=12
        i+=12
        t4=temp[c:d]
        c+=12
        d+=12
        if(t3=='0110'):
            decimal_data = BinaryToDecimal(t4)
            final+=chr((decimal_data ^ 170) + 48)
        elif(t3=='0011'):
            decimal_data = BinaryToDecimal(t4)
            final+=chr((decimal_data ^ 170) - 48)
        
    return final + "(Length of the Data: " + str(lengthd) + ")"
    # print("\nMessage after decoding from the stego file:- ",final)


# In[6]:


def txt_steg():
    while True:
        print("\n\t\tTEXT STEGANOGRAPHY OPERATIONS") 
        print("1. Encode the Text message")  
        print("2. Decode the Text message")  
        print("3. Exit")  
        choice1 = int(input("Enter the Choice:"))   
        if choice1 == 1:
            encode_txt_data()
        elif choice1 == 2:
            decrypted=decode_txt_data() 
        elif choice1 == 3:
            break
        else:
            print("Incorrect Choice")
        print("\n")


# In[7]:


def msgtobinary(msg):
    if type(msg) == str:
        result= ''.join([ format(ord(i), "08b") for i in msg ])
    
    elif type(msg) == bytes or type(msg) == np.ndarray:
        result= [ format(i, "08b") for i in msg ]
    
    elif type(msg) == int or type(msg) == np.uint8:
        result=format(msg, "08b")

    else:
        raise TypeError("Input type is not supported in this function")
    
    return result


# In[8]:


def encode_img_data(image, data):
    img=cv2.imread(str(image))

    if (len(data) == 0): 
        raise ValueError('Data entered to be encoded is empty')
  
    nameoffile = "new_img.png"
    
    no_of_bytes=(img.shape[0] * img.shape[1] * 3) // 8
    
    print("\t\nMaximum bytes to encode in Image :", no_of_bytes)
    
    if(len(data)>no_of_bytes):
        raise ValueError("Insufficient bytes Error, Need Bigger Image or give Less Data !!")
    
    data +='*^*^*'    
    
    binary_data=msgtobinary(data)
    print("\n")
    print(binary_data)
    length_data=len(binary_data)
    
    print("\nThe Length of Binary data",length_data)
    
    index_data = 0
    
    for i in img:
        for pixel in i:
            r, g, b = msgtobinary(pixel)
            if index_data < length_data:
                pixel[0] = int(r[:-1] + binary_data[index_data], 2) 
                index_data += 1
            if index_data < length_data:
                pixel[1] = int(g[:-1] + binary_data[index_data], 2) 
                index_data += 1
            if index_data < length_data:
                pixel[2] = int(b[:-1] + binary_data[index_data], 2) 
                index_data += 1
            if index_data >= length_data:
                break
    cv2.imwrite(nameoffile,img)
    print("\nEncoded the data successfully in the Image and the image is successfully saved with name ",nameoffile)
    return;

# In[9]:


def decode_img_data(image):
    img = cv2.imread(image);
    data_binary = ""
    for i in img:
        for pixel in i:
            r, g, b = msgtobinary(pixel) 
            data_binary += r[-1]  
            data_binary += g[-1]  
            data_binary += b[-1]  
            total_bytes = [ data_binary[i: i+8] for i in range(0, len(data_binary), 8) ]
            decoded_data = ""
            for byte in total_bytes:
                decoded_data += chr(int(byte, 2))
                if decoded_data[-5:] == "*^*^*": 
                    print("\n\nThe Encoded data which was hidden in the Image was :--  ",decoded_data[:-5])
                    return decoded_data[:-5]


# In[10]:


def img_steg():
    while True:
        print("\n\t\tIMAGE STEGANOGRAPHY OPERATIONS\n") 
        print("1. Encode the Text message") 
        print("2. Decode the Text message") 
        print("3. Exit")  
        choice1 = int(input("Enter the Choice: "))   
        if choice1 == 1:
            image=cv2.imread("Sample_cover_files/1.png")
            encode_img_data(image)
        elif choice1 == 2:
            image1=cv2.imread(input("Enter the Image you need to Decode to get the Secret message :  "))
            decode_img_data(image1)
        elif choice1 == 3:
            break
        else:
            print("Incorrect Choice")
        print("\n")


# In[11]:


def encode_aud_data(audio_file_path, data_to_encode):
    import wave

    song = wave.open(audio_file_path, mode='rb')

    nframes = song.getnframes()
    frames = song.readframes(nframes)
    frame_list = list(frames)
    frame_bytes = bytearray(frame_list)

    res = ''.join(format(i, '08b') for i in bytearray(data_to_encode, encoding='utf-8'))
    print("\nThe string after binary conversion:", res)
    length = len(res)
    print("\nLength of binary after conversion:", length)

    data_to_encode += '*^*^*'

    result = []
    for c in data_to_encode:
        bits = bin(ord(c))[2:].zfill(8)
        result.extend([int(b) for b in bits])

    j = 0
    for i in range(0, len(result), 1):
        res = bin(frame_bytes[j])[2:].zfill(8)
        if res[len(res)-4] == result[i]:
            frame_bytes[j] = (frame_bytes[j] & 253)  # 253: 11111101
        else:
            frame_bytes[j] = (frame_bytes[j] & 253) | 2
            frame_bytes[j] = (frame_bytes[j] & 254) | result[i]
        j = j + 1

    frame_modified = bytes(frame_bytes)

    stegofile = "new_audio.wav"
    with wave.open(stegofile, 'wb') as fd:
        fd.setparams(song.getparams())
        fd.writeframes(frame_modified)
    print("\nEncoded the data successfully in the audio file.")
    song.close()



# In[12]:


def decode_aud_data(audio_file_path):
    import wave

    song = wave.open(audio_file_path, mode='rb')

    nframes = song.getnframes()
    frames = song.readframes(nframes)
    frame_list = list(frames)
    frame_bytes = bytearray(frame_list)

    extracted = ""
    p = 0
    for i in range(len(frame_bytes)):
        if p == 1:
            break
        res = bin(frame_bytes[i])[2:].zfill(8)
        if res[len(res)-2] == '0':
            extracted += res[len(res)-4]
        else:
            extracted += res[len(res)-1]
    
        all_bytes = [extracted[i: i+8] for i in range(0, len(extracted), 8)]
        decoded_data = ""
        for byte in all_bytes:
            decoded_data += chr(int(byte, 2))
            if decoded_data[-5:] == "*^*^*":
                print("The Encoded data was:", decoded_data[:-5])
                p = 1
                break  
    song.close()
    return decoded_data[:-5];



# In[13]:


def aud_steg():
    while True:
        print("\n\t\tAUDIO STEGANOGRAPHY OPERATIONS") 
        print("1. Encode the Text message")  
        print("2. Decode the Text message")  
        print("3. Exit")  
        choice1 = int(input("Enter the Choice:"))   
        if choice1 == 1:
            audio=cv2.imread("Sample_cover_files/")
            encode_aud_data()
        elif choice1 == 2:
            decode_aud_data()
        elif choice1 == 3:
            break
        else:
            print("Incorrect Choice")
        print("\n")


# In[14]:


def KSA(key):
    key_length = len(key)
    S=list(range(256)) 
    j=0
    for i in range(256):
        j=(j+S[i]+key[i % key_length]) % 256
        S[i],S[j]=S[j],S[i]
    return S


# In[15]:


def PRGA(S,n):
    i=0
    j=0
    key=[]
    while n>0:
        n=n-1
        i=(i+1)%256
        j=(j+S[i])%256
        S[i],S[j]=S[j],S[i]
        K=S[(S[i]+S[j])%256]
        key.append(K)
    return key


# In[16]:


def preparing_key_array(s):
    return [ord(c) for c in s]


# In[17]:


def encryption(plaintext, key):
    key=preparing_key_array(key)

    S=KSA(key)

    keystream=np.array(PRGA(S,len(plaintext)))
    plaintext=np.array([ord(i) for i in plaintext])

    cipher=keystream^plaintext
    ctext=''
    for c in cipher:
        ctext=ctext+chr(c)
    return ctext


# In[18]:


def decryption(ciphertext, key):
    key=preparing_key_array(key)

    S=KSA(key)

    keystream=np.array(PRGA(S,len(ciphertext)))
    ciphertext=np.array([ord(i) for i in ciphertext])

    decoded=keystream^ciphertext
    dtext=''
    for c in decoded:
        dtext=dtext+chr(c)
    return dtext


# In[19]:


def embed(frame, data_to_encode, key):
    data=encryption(data_to_encode, key)
    print("The encrypted data is : ",data)
    if (len(data) == 0): 
        raise ValueError('Data entered to be encoded is empty')

    data +='*^*^*'
    
    binary_data=msgtobinary(data)
    length_data = len(binary_data)
    
    index_data = 0
    
    for i in frame:
        for pixel in i:
            r, g, b = msgtobinary(pixel)
            if index_data < length_data:
                pixel[0] = int(r[:-1] + binary_data[index_data], 2) 
                index_data += 1
            if index_data < length_data:
                pixel[1] = int(g[:-1] + binary_data[index_data], 2) 
                index_data += 1
            if index_data < length_data:
                pixel[2] = int(b[:-1] + binary_data[index_data], 2) 
                index_data += 1
            if index_data >= length_data:
                break
        return frame


# In[20]:


def extract(frame, key):
    data_binary = ""
    final_decoded_msg = ""
    for i in frame:
        for pixel in i:
            r, g, b = msgtobinary(pixel) 
            data_binary += r[-1]  
            data_binary += g[-1]  
            data_binary += b[-1]  
            total_bytes = [ data_binary[i: i+8] for i in range(0, len(data_binary), 8) ]
            decoded_data = ""
            for byte in total_bytes:
                decoded_data += chr(int(byte, 2))
                if decoded_data[-5:] == "*^*^*": 
                    for i in range(0,len(decoded_data)-5):
                        final_decoded_msg += decoded_data[i]
                    final_decoded_msg = decryption(final_decoded_msg, key)
                    print("\n\nThe Encoded data which was hidden in the Video was :--\n",final_decoded_msg)
                    return final_decoded_msg




# In[21]:


def encode_vid_data(video_file_path, frame_number, data_to_encode, key):
    cap = cv2.VideoCapture(video_file_path)
    vidcap = cv2.VideoCapture(video_file_path)
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    frame_width = int(vidcap.get(3))
    frame_height = int(vidcap.get(4))

    size = (frame_width, frame_height)
    out = cv2.VideoWriter("stego_video.mp4", fourcc, 25.0, size)
    max_frame = 0

    while cap.isOpened():
        ret, frame = cap.read()
        if ret == False:
            break
        max_frame += 1
    cap.release()

    print("Total number of Frame in selected Video:", max_frame)
    print("Frame number where you want to embed data:", frame_number)
    n = frame_number
    frame_count = 0

    while vidcap.isOpened():
        frame_count += 1
        ret, frame = vidcap.read()
        if ret == False:
            break
        if frame_count == n:
            change_frame_with = embed(frame, data_to_encode, key)
            frame_ = change_frame_with
            frame = change_frame_with
        out.write(frame)

    print("\nEncoded the data successfully in the video file.")
    return frame_




# In[22]:


def decode_vid_data(frame_, number, decode_video_file, key):
    cap = cv2.VideoCapture(decode_video_file)
    max_frame=0;
    while(cap.isOpened()):
        ret, frame = cap.read()
        if ret == False:
            break
        max_frame+=1
        
    print("Total number of Frame in selected Video :",max_frame)
    print("Enter the secret frame number from where you want to extract data")
    n=number
    vidcap = cv2.VideoCapture(decode_video_file)
    frame_number = 0
    while(vidcap.isOpened()):
        frame_number += 1
        ret, frame = vidcap.read()
        if ret == False:
            break
        if frame_number == n:
            return extract(frame_, key)
            


# In[23]:


def vid_steg():
    while True:
        print("\n\t\tVIDEO STEGANOGRAPHY OPERATIONS") 
        print("1. Encode the Text message")  
        print("2. Decode the Text message")  
        print("3. Exit")  
        choice1 = int(input("Enter the Choice:"))   
        if choice1 == 1:
            a=encode_vid_data()
        elif choice1 == 2:
            decode_vid_data(a)
        elif choice1 == 3:
            break
        else:
            print("Incorrect Choice")
        print("\n")


# In[24]:


def main():
    print("\t\t      STEGANOGRAPHY")   
    while True:  
        print("\n\t\t\tMAIN MENU\n")  
        print("1. IMAGE STEGANOGRAPHY {Hiding Text in Image cover file}")  
        print("2. TEXT STEGANOGRAPHY {Hiding Text in Text cover file}")  
        print("3. AUDIO STEGANOGRAPHY {Hiding Text in Audio cover file}")
        print("4. VIDEO STEGANOGRAPHY {Hiding Text in Video cover file}")
        print("5. Exit\n")  
        choice1 = int(input("Enter the Choice: "))   
        if choice1 == 1: 
            img_steg()
        elif choice1 == 2:
            txt_steg()
        elif choice1 == 3:
            aud_steg()
        elif choice1 == 4:
            vid_steg()
        elif choice1 == 5:
            break
        else:
            print("Incorrect Choice")
        print("\n\n")


# In[27]:


if __name__ == "__main__":
    main()


# In[ ]:




