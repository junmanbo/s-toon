import os
import tkinter as tk
from urllib.request import build_opener, install_opener
from main import get_ep, get_img_src, save_img


def add_id():
    global cnt

    cnt += 1
    lbl_id = tk.Label(frm_form, text=f'웹툰ID {cnt}')
    lbl_id.grid(row=cnt-1, column=0, sticky="w")

    globals()[f'ent_id{cnt}'] = tk.Entry(frm_form)
    eval(f'ent_id{cnt}').grid(row=cnt-1, column=1, sticky="w")


def save_webtoon():
    global webtoons, cnt
    for i in range(cnt):
        webtoons.append(eval(f'ent_id{i+1}').get())
    print(webtoons)
    # Access Denied 에러 우회
    opener = build_opener()
    opener.addheaders = [
        ('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')]
    install_opener(opener)

    if not os.path.isdir('webtoon'):
        os.mkdir('webtoon')

    # 웹툰
    try:
        for webtoon in webtoons:
            last_ep, webtoon_name = get_ep(webtoon)
            print(f'"{webtoon_name}" 의 최종화: {last_ep}')

            # 에피소드
            try:
                for ep in range(1, last_ep+1):
                    if not os.path.isdir(f'webtoon/{webtoon_name}/{ep}'):
                        os.mkdir(f'webtoon/{webtoon_name}/{ep}')

                        images = get_img_src(webtoon, ep)
                        save_img(images, webtoon_name, ep)
                        print(f'{webtoon_name} - {ep}화 저장 완료')

            except Exception as e:
                print(e)
    except Exception as e:
        print(e)


webtoons = []

# Set up the window
window = tk.Tk()
window.title("웹툰 저장기")
window.resizable(width=True, height=True)

frm_desc = tk.Frame(window)
frm_desc.pack()

desc = "% 설명: 웹툰을 자동으로 저장합니다.\n소장하고 싶은 웹툰을 저장해 보세요!"
lbl_desc = tk.Label(frm_desc, text=desc).grid(
    row=0, column=0, sticky="w")

how = "% 사용법: 저장하고자 하는 웹툰 사이트에 들어갑니다.\nURL주소에 적혀 있는 웹툰 ID를 아래에 적어 주세요."
lbl_how = tk.Label(frm_desc, text=how).grid(row=1, column=0, sticky="w")

frm_form = tk.Frame(window)
frm_form.pack()

cnt = 1
lbl_id = tk.Label(frm_form, text=f'웹툰ID {cnt}')
lbl_id.grid(row=0, column=0, sticky="w")

ent_id1 = tk.Entry(frm_form)
ent_id1.grid(row=0, column=1, sticky="w")

btn_add = tk.Button(frm_form, text="웹툰 추가", command=add_id)
btn_add.grid(row=0, column=2, padx=10, pady=10)

btn_save = tk.Button(frm_form, text="저장 시작", command=save_webtoon)
btn_save.grid(row=0, column=3, padx=10, pady=10)

window.mainloop()
