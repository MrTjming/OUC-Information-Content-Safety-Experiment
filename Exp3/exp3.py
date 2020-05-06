from PIL import Image


# source_path:原图路径, target_path水印图片路径, new_path加水印后的图片路径
def lsb(source_path, target_path, new_path):
    source_im = Image.open(source_path)
    target_im = Image.open(target_path)
    # 获取图片的宽和高
    im_width, im_height = source_im.size

    for width in range(im_width):
        for height in range(im_height):
            source_px = source_im.getpixel((width, height))
            target_px = target_im.getpixel((width, height))
            if target_px > 127:  # 二值化
                target_px = 1
            else:
                target_px = 0

            # 将原图的红通道最后一位先置0, 再加上要隐藏图片的值
            new_red_px = source_px[0] - (source_px[0] % 2) + target_px
            source_im.putpixel((width, height), (new_red_px, source_px[1], source_px[2]))

    source_im.save(new_path)


# source_path:加水印后的图片路径, target_path解析出来的水印图片的保存路径
def get_hidden_photo(source_path, target_path):
    source_im = Image.open(source_path)
    target_im = source_im.copy()
    im_width, im_height = source_im.size

    for width in range(im_width):
        for height in range(im_height):
            source_px = source_im.getpixel((width, height))
            target_px = (source_px[0] % 2)
            if (target_px % 2) == 1:
                target_px = 255

            target_im.putpixel((width, height), (target_px, target_px, target_px))

    target_im.save(target_path)


if __name__ == '__main__':
    lsb("lena.bmp", "姓名.bmp", "隐藏图片.bmp")
    get_hidden_photo("隐藏图片.bmp", "解析的姓名.bmp")
