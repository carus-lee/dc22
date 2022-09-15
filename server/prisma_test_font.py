from PIL import Image, ImageDraw, ImageFont


def get_size_font2image(draw_text, font_name, font_size, font_dir='/root/dc22/server/test'):
    # font_name = 'BATANG.TTC'
    # # font_name='ARIAL.TTF'
    # font_size = 100
    # draw_text = '스케쥴 기능 테스트 자막송출 TEST 입니다. 1234567890 ABCDEFGHIJKLNMopqrstuvwxyz'
    # font = ImageFont.truetype("/root/dc22/server/test/BATANG.TTC", font_size)
    font = ImageFont.truetype(f'{font_dir}/{font_name}', font_size)


    w, h = font.getsize(draw_text)
    print(f'font: {font_name}')
    print(f'text : {draw_text}')
    print(f'font_size : {font_size}')
    print(f'size: width-{w}, height-{h}')

    return w, h


def test222():
    draw_text = '스케쥴 기능 테스트 자막송출 TEST 입니다. 1234567890 ABCDEFGHIJKLNMopqrstuvwxyz'
    font_size = 100

    list_font = ['1_Font1_Arial.ttf', '2_Font2_SUIT Regular.ttf', '3_Font3_IBM Plex Sans KR.ttf', '4_Font4_Gulim.ttf', '5_Font5_MGungJeong.ttf', '6_HYwulM.ttf']
    for item_font in list_font:
        get_size_font2image(draw_text, item_font, font_size)
        print('------')


def test():
    font_name='BATANG.TTC'
    # font_name='ARIAL.TTF'
    font_size =100
    draw_text ='스케쥴 기능 테스트 자막송출 TEST 입니다. 1234567890 ABCDEFGHIJKLNMopqrstuvwxyz'
    # font = ImageFont.truetype("/root/dc22/server/test/BATANG.TTC", font_size)
    font = ImageFont.truetype(f'/root/dc22/server/test/{font_name}', font_size)

    # 이미지 사이즈 지정
    text_width = 30 * 3
    text_height = 30

    # 이미지 객체 생성 (배경 검정)


    # 가운데에 그리기 (폰트 색: 하양)

    w, h = font.getsize(draw_text)
    print(f'font: {font_name}')
    print(f'text : {draw_text}')
    print(f'font_size : {font_size}')
    print(f'size: w-{w}, h-{h}')

    canvas = Image.new('RGB', (w, h), "black")
    draw = ImageDraw.Draw(canvas)
    draw.text((0, 0), draw_text, 'white', font)


    # png로 저장 및 출력해서 보기

    canvas.save("/root/dc22/server/test/font_size_test.png", "PNG")
    # canvas.show()

test222()