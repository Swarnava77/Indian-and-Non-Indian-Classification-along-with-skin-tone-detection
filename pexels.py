from pexels_api import API
import requests
import os

PEXELS_API_KEY = '563492ad6f9170000100000137fec6ab873648a2a212313816e85ae1'


keyword = input("Enter your keyword")
SAVE_FOLDER=keyword

def main():

    if not os.path.exists(SAVE_FOLDER):
        os.mkdir(SAVE_FOLDER)
    download_images()

def download_images():

    api = API(PEXELS_API_KEY)

    
    api.search(keyword, page=1, results_per_page=100)

    photos = api.get_entries()

    links=[]
    for photo in photos:
        
            links.append(photo.medium)

    print(f'Downloading {len(links)} images....')

    # Access the data URI and download the image to a file
    for i, link in enumerate(links):
        response = requests.get(link)

        image_name = SAVE_FOLDER + '/' + keyword + str(i + 1) + '.jpg'
        with open(image_name, 'wb') as raw_img:
            raw_img.write(response.content)

if __name__=='__main__':
    main()
