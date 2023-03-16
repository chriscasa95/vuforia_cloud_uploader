import json
from ImageUploader import ImageUploader

################### KEYS ###########################################################
server_access_key = "eb861e363ecf1563a824b290xxxxxxx"
server_secret_key = "0aba77815d86e9861597d6226b4c2fxxxxxxx"

################### PLANT DATA #####################################################
plant_name = "TestPlant"
width = 2
meta = "Hier wird der infotext zur Pflanze eingetragen."

################### IMAGE SOURCE ###################################################
image_path = "../data/IMG_20221206_141113.jpg"  # zum deaktivieren: image_path = ""

################### FOLDER SOURCE ###################################################
folder_path = "../data/"  # zum deaktivieren: folder_path = ""

################### VIDEO SOURCE ###################################################
video_path = "../data/VID_20230110_104750.mp4"  # zum deaktivieren: video_path = ""
number_of_images = 30


####################################################################################
################### INTERN #########################################################
####################################################################################

metadata = json.dumps({"name": plant_name, "meta": meta})

uploader = ImageUploader(server_access_key, server_secret_key)

# if image_path:
#     uploader.upload_image(image_path, plant_name, width, metadata)

# if video_path:
#     uploader.upload_video(video_path, plant_name, width, number_of_images, metadata)

if folder_path:
    uploader.upload_images_from_folder(folder_path, plant_name, width, metadata)
