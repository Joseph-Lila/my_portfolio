from pathlib import Path

import cv2
from rembg import remove
from PIL import Image


video_path = 'D:/CAMERA/site/VID_20230318_161226.mp4'

box = [
    (0, 1080, 800, 1920),
    (0, 1080, 300, 1920),
]


def files_sort(elem):
    name = str(elem)
    return int(name[name.rfind('_') + 1:name.rfind('.')])


def process_fragment(
        folder_path,
        video_path=video_path,
        start_duration=0,
        end_duration=0,
        delta_duration=100,
        rotate_degrees=180,
        left=0,
        right=1080,
        top=800,
        bottom=1920,
        only_gif=False,
):
    if not only_gif:

        # generate images
        vp = VideoProcessor(video_path)
        vp.set_duration(start_duration)
        i = 1
        while start_duration <= end_duration:
            vp.save_current_image(f"{folder_path}/img_{i}")
            i += 1
            start_duration += delta_duration

    # process them
    p = Path(folder_path).glob('*')
    files = [x for x in p if x.is_file() and str(x).endswith('.png')]
    files.sort(key=files_sort)

    frames = []
    for file in files:
        im = Image.open(file)

        if not only_gif:
            im = im.rotate(rotate_degrees)
            im = im.crop((left, top, right, bottom))
            im = remove(im)
            im.save(str(file))

        frames.append(im)

    if len(frames) > 1:
        frames[0].save(
            f'img/{folder_path[folder_path.rfind("/"):]}.gif',
            save_all=True,
            format='GIF',
            append_images=frames[1:],
            optimize=True,
            duration=delta_duration // 2,
            disposal=2,
            loop=0,
        )


class VideoProcessor:
    def __init__(self, video_path):
        self.cap = cv2.VideoCapture(video_path)
        self.image_cnt = 0

    def set_duration(self, duration):
        self.cap.set(cv2.CAP_PROP_POS_MSEC, duration)

    def get_current_image(self):
        success, image = self.cap.read()
        if success:
            return image

    @staticmethod
    def save_image(image, title):
        if image is not None:
            cv2.imwrite(title, image)

    def save_current_image(self, title=None):
        current_image = self.get_current_image()
        self.save_image(current_image, f"{self.image_cnt}.png" if title is None else f"{title}.png")
        if title is None:
            self.image_cnt += 1

    def close(self):
        cv2.destroyAllWindows()
        self.cap.release()


def main():
    indexes   = [0,       1,         2,         3,         4,         5,         6,         7,         8,         9,         10,        11,        12,        13,        14,        15,        16,        17,        18,        19,        20,        21,        22,        23,        24,        25,        ]
    starts    = [637_000, 1_049_100, 1_604_090, 1_617_120, 1_651_020, 1_715_020, 1_858_210, 1_889_220, 1_910_190, 1_938_090, 2_023_050, 2_060_290, 2_072_140, 2_093_090, 2_215_020, 2_420_170, 2_464_090, 2_489_240, 2_718_200, 2_733_300, 2_775_170, 2_806_290, 2_954_260, 3_000_000, 3_504_150, 3_695_000, ]
    ends      = [650_000, 1_052_280, 1_611_220, 1_629_190, 1_661_020, 1_728_270, 1_884_140, 1_901_200, 1_914_100, 1_947_210, 2_026_050, 2_062_210, 2_077_020, 2_119_210, 2_282_100, 2_426_070, 2_466_090, 2_504_240, 2_724_000, 2_737_200, 2_777_000, 2_810_000, 2_979_000, 3_008_000, 3_520_100, 3_711_000, ]
    boxes     = [box[0],  box[0],    box[0],    box[0],    box[0],    box[0],    box[0],    box[0],    box[0],    box[0],    box[1],    box[1],    box[1],    box[1],    box[1],    box[1],    box[1],    box[1],    box[1],    box[1],    box[1],    box[1],    box[1],    box[1],    box[1],    box[1],    ]

    for i in indexes:
        p = Path(f'videos/{i}')
        if not p.exists():
            p.mkdir(parents=True, exist_ok=True)

        left, right, top, bottom = boxes[i]
        process_fragment(
            folder_path=f'videos/{i}',
            start_duration=starts[i],
            end_duration=ends[i],
            delta_duration=100,
            only_gif=False,
            left=left,
            right=right,
            top=top,
            bottom=bottom,
        )


if __name__ == '__main__':
    main()
