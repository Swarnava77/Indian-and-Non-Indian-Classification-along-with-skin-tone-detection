import os
from cv2 import cv2
import matplotlib.pyplot as plt
import numpy as np
import pickle
from skimage.io import imread
from skimage.transform import resize
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn import svm
from sklearn.metrics import accuracy_score,confusion_matrix

new_name = ''

def rename(path):
    
    rename_i = 0
    new_name = str(input('Enter the new name of the file:(all the images will be saved with 0,1,2,3... after the name assigned by you) '))
    for filename in os.listdir(path):
       
        New_img =new_name+str(rename_i) + ".jpg"
        Img_source =path + filename
        New_img =path + New_img
        os.rename(Img_source, New_img)
        rename_i += 1

def crop_images():
    
    label1 = 1
    label2 = 1
    path = str(input('Path of the folder:(wiht forward slash"/") '))

    rename(path)
    onlyfiles = next(os.walk(path))[2]      #find the number of files in that folder
    
    for i in range(1,len(onlyfiles)+1):
        
        img_name = '/'+str(i)+'.jpg'        
        path_img = str(path + img_name)
        print(path_img)
        img = cv2.imread(path_img)
        
        # Convert into grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # Load the cascade
        face_cascade = cv2.CascadeClassifier(r'C:\Users\thete\Desktop\ML-major project\haarcascade_frontalface_default.xml')
        
        # Detect faces
        faces = face_cascade.detectMultiScale(gray)
        
        # Draw rectangle around the faces and crop the faces
        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x+w, y+h), (0, 0, 0), 2)
            faces = img[y:y + h, x:x + w]
            
            if len(faces)>=1:
                print("Human")
                os.chdir('C:/Users/thete/Desktop/ML-major project/Relevent')
                name = 'new'+str(label1)+'.jpg'
                cv2.imwrite(name, faces)
                label1+=1
            else:
                print("Non Human")
                os.chdir('C:/Users/thete/Desktop/ML-major project/Irrelevent')
                name = 'new'+str(label2)+'.jpg'
                cv2.imwrite(name, faces)
                label2+=1



def train_model():

    target = []     #The output here
    images = []     #data
    flat_data = []  #flatten data

    datadir = 'C:/Users/thete/Desktop/ML-major project/dataset'

    categories = ['Indian','Non Indian']

    for category in categories:
        num = categories.index(category)        #Label Encoding values
        path = datadir + '/' + category

        onlyfiles = next(os.walk(path))[2]
        
        rename(path)
        for i in range(len(onlyfiles)):

            img_path = path + '/' + new_name +str(i)+'.jpg'         
            img_array = imread(img_path)
            
            img_resized = resize(img_array,(40,40,3))       #resizing of data and also normalizes th value from 0-1
            flat_data.append(img_resized.flatten())         #flattening of data
            images.append(img_resized)
            target.append(num)

    flat_data = np.array(flat_data)
    target = np.array(target)
    images = np.array(images)

    #unique, count = np.unique(target, return_counts=True)
    #plt.bar(categories,count)
    #plt.show()

    x_train, x_test, y_train, y_test = train_test_split(flat_data, target, test_size = 0.2, random_state = 0)

    param_grid = [
                        {'C': [1, 10, 100, 1000], 'kernel':['linear']},
                        {'C': [1, 10, 100, 1000], 'gamma':[0.001,0.0001], 'kernel':['rbf']}
                 ]


    svc = svm.SVC(probability=True)
    clf = GridSearchCV(svc, param_grid)
    clf.fit(x_train,y_train)


    y_pred = clf.predict(x_test)

    score = accuracy_score(y_pred,y_test)
    print(score)

    pickle.dump(clf,open('img_model.p', 'wb'))

def addon():

    model = pickle.load(open('img_model.p','rb'))
    flat_data = []
    choice4 = input("how many images to test?")

    for times in range(2):

        for i in range(choice4) :
            
            img_path = input('Enter the path of the file')
            file_name = input("enter file name")+'.jpg'
            img = imread(img_path)
            img_resized = resize(img,(40,40,3))
            if times == 0:
                flat_data.append(img_resized.flatten())
            elif times > 0:
                if targets[i] == 0:
                    print('Indian')
                    os.chdir(r'C:\Users\thete\Desktop\ML-major project\Indian')
                    plt.imsave(file_name, img)
                elif targets[i] == 1:
                    print('Non Indian')
                    os.chdir(r'C:\Users\thete\Desktop\ML-major project\Non Indian')
                    plt.imsave(file_name, img)
        if times == 0:
            flat_data = np.array(flat_data)
            targets = model.predict(flat_data)

def main():

    print('\n\n\t\t\tFirst Phase: Human and Non-Human\n\n')
    if not os.path.exists('Relevent') and not os.path.exists('Irrelevent'):
        os.mkdir('Relevent')
    
    print('\n\n\t\t\tSecoond Phase: Indian and Non-Indian\n\n')

    choice1 = input("Do you want to crop the images for better results?(y/n) ")
    if choice1 == 'y' or choice1 == 'Y':
        crop_images()

    choice2 = input("Are you training the model for first time?(y/n) ")
    if choice2 == 'y' or choice2 == 'Y':
        train_model()
    else:
        addon()

    choice3 = input('Want to rename new data set?(y/n) ') 
    if choice3 == 'y' or choice3 =='Y':   
        categories = ['Indian', 'Non Indian']
        datadir="C:/Users/thete/Desktop/ML-major project/dataset/"
        for category in categories:
            path = datadir + category
            rename(path)
            

if __name__ == '__main__':
   main()
