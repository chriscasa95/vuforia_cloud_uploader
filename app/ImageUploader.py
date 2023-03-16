import cv2
import base64
import json
import time
import sys
import os
import filetype

from cv2 import Mat
from requests import Response
from app.TargetAPI import TargetAPI

MEGABYTE = 1024 * 1024


class ImageUploader(TargetAPI):
    def upload_image(
        self, img_path: str, img_name: str, width: str, metadata: str = ""
    ) -> tuple[bool, Response]:
        img = cv2.imread(img_path)
        img_name = self.__generate_img_name(img_name, 0)

        return self.__upload(img, img_name, width, metadata)

    # def upload_multiple_images(self, img_paths: list[str]):
    #     pass

    def upload_images_from_folder(
        self, folder_path: str, img_name: str, width: str, metadata: str = ""
    ) -> tuple[bool, Response]:
        for filename in os.listdir(folder_path):

            img_path = f"{folder_path}/{filename}"
            idx = 0

            # TODO: exclude .png
            if filetype.is_image(img_path):
                print(f"{filename} is a valid image...")

                img = cv2.imread(img_path)

                unique_img_name = self.__generate_img_name(img_name, idx)
                [success, r] = self.__upload(img, unique_img_name, width, metadata)

                idx += 1

    def upload_video(
        self,
        video_path: str,
        img_name: str,
        width: float,
        number_of_images: int,
        metadata: str = "",
    ) -> list[tuple[bool, Response]]:
        responses = []

        extracted_frames = self.__extract_farmes(video_path, number_of_images)

        for idx, img in enumerate(extracted_frames):
            unique_img_name = self.__generate_img_name(img_name, idx)
            [success, r] = self.__upload(img, unique_img_name, width, metadata)

            if not success:
                break

            responses.append([success, r])

        return responses

    # def get_image_information(self, target_id: str):
    #     pass

    # def update_image(self, target_id: str, image_path: str):
    #     pass

    # def delete_image(self, target_id: str):
    #     pass

    def __upload(
        self, img: Mat, img_name: str, width: float, metadata: str
    ) -> tuple[bool, Response]:
        print(f"upload: {img_name}...")
        upload_path = "./uploaded"

        img_compressed = self.__compress_image(img)

        html_body = self.__generate_body(img_compressed, img_name, width, metadata)

        [success, r] = self._post(html_body)

        if success:
            # TODO: implement better solution
            try:
                os.mkdir(upload_path)
            except OSError as error:
                # print(error)
                pass
            cv2.imwrite(f"{upload_path}/{img_name}.jpg", img_compressed)

            print("...success! :)\n")

        return [success, r]

    def __generate_img_name(self, img_name: str, counter: int) -> str:
        # ts stores the time in seconds
        ts = int(time.time())

        return f"{img_name}_{ts}_{counter}"

    def __get_jpg_byte_size(self, image: Mat) -> int:

        return sys.getsizeof(cv2.imencode(".jpg", image)[1])

    def __compress_image(self, image: Mat) -> Mat:

        img_byte_size = self.__get_jpg_byte_size(image)
        scale_percent = 80  # percent of original size

        while img_byte_size >= 1 * MEGABYTE:

            width = int(image.shape[1] * scale_percent / 100)
            height = int(image.shape[0] * scale_percent / 100)
            dim = (width, height)

            # resize image
            image = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)
            img_byte_size = self.__get_jpg_byte_size(image)

        print(f"image size: {img_byte_size} byte")

        return image

    def __generate_body(
        self, image: Mat, name: str, width: float, metadata: str
    ) -> str:
        jpg_as_b64 = base64.b64encode(cv2.imencode(".jpg", image)[1]).decode()
        metadata_as_b64 = base64.b64encode(metadata.encode("ascii")).decode()

        dictonary = {
            "name": name,
            "width": width,
            "image": jpg_as_b64,
            "application_metadata": metadata_as_b64,
        }

        return json.dumps(dictonary, ensure_ascii=False, indent=4)

    def __extract_farmes(self, video_path: str, number_of_images: int) -> list[Mat]:
        captured_frames = []
        # Start capturing the feed
        cap = cv2.VideoCapture(video_path)

        number_of_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) - 1
        capture_nth_frame = number_of_frames / (number_of_images - 1)
        print(
            f"Video has {number_of_frames} frame; Capture every {int(capture_nth_frame)}th frame\nStart capturing..."
        )

        count = 0

        while cap.isOpened():
            ret, frame = cap.read()

            if ret:
                captured_frames.append(frame)
                count += capture_nth_frame  # i.e. at 30 fps, this advances one second
                cap.set(cv2.CAP_PROP_POS_FRAMES, count)
            else:
                cap.release()
                break

        print("Finished capturing!\n")
        return captured_frames
