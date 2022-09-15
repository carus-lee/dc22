from PIL import Image, ImageDraw, ImageFont


def get_size_font2image(draw_text, font_size, font_id=0, font_dir='/root/dc22/server/font'):
    list_font = ['1_Font1_Arial.ttf', '2_Font2_SUIT Regular.ttf', '3_Font3_IBM Plex Sans KR.ttf', '4_Font4_Gulim.ttf',
                 '5_Font5_MGungJeong.ttf', '6_HYwulM.ttf']
    font = ImageFont.truetype(f'{font_dir}/{list_font[font_id]}', font_size)

    w, h = font.getsize(draw_text)
    print(f'get_size_font2image.font: {font_name}')
    print(f'get_size_font2image.text : {draw_text}')
    print(f'get_size_font2image.font_size : {font_size}')
    print(f'get_size_font2image.size: width-{w}, height-{h}')

    return w, h


def get_duration_text2font(draw_text, font_size, font_speed, font_name, scr_width=1920):
    font_id = 0
    w, h = get_size_font2image(draw_text, font_size, font_id=font_id)

    i_duration = int((w+scr_width)/font_speed)

    return i_duration

