"""
Font List Sample

TkEasyGUI
ref: https://github.com/kujirahand/tkeasygui-python

Pro4： TkEasyGUI-test を pip install したが、import でエラーとなる。
       Python3.12 を再インストールする。

repo: https://github.com/yampan/my-first-repo.git

git 操作は、Pi5a.local で行う。(V:)
pi5a.local:/home/jupyter/work/GUI-test/my-first-repo/fontlist.py

  作業ディレクトリ(Working Directory)、索引(Index)、コミット、
  作業最後のコミットを指す HEAD
  
  1.共有リポジトリがない場合、リポジトリを作成
   git init
  
  2.共有リポジトリを、クローン(clone)して作業ディレクトリを作成
    git clone https://username@domain/path/to/repository
    
  3. ファイルの追加 & コミット
    git add <filename>, or git add *
  
  4. git commit -m "1st commit"
    変更内容が索引からコミットされ、HEADに格納されました。
  5. 共有リポジトリにプッシュする
    git push origin master
  
  6. ローカルでリポジトリを作成( git init )や共有リポジトリからクローン(clone)していない場合、共有リポジトリを登録することができます。
    git remote add origin <server>
  
  7. 作業ディレクトリを最新のコミットに更新
    git pull
      
=============================================================================
JROD-gui.py:
    1) GUI用に、Fontを選択する。
    2)

ref: get_clipboard(), set_clipboard(), screenshot(),
     load_json_file(fn), save_json_file(fn, dat)

"""
import TkEasyGUI as eg
import json, os, sys


f_size = 13 # 16
# list fonts
# file が存在するか？
fn_conf = "JROD_config.json"
font_items=[]
if os.path.exists(fn_conf):
    print(f"{fn_conf} は存在します")
    with open(fn_conf, "r") as f:
      config = json.load(f)
    for i in config.keys():
        if config[i]:
            font_items.append(i)
else:
    print(f"{fn_conf} は存在しません")
    ans = input(f"{fn_conf}を作成します。([yes]/no)> ")
    if ans[0].lower() != "y":
        sys.exit()
    font_items2 = sorted(eg.get_font_list())
    
    config = {}
    for f in font_items2:
        if f[0:1] in ['@', "$", "%", "&"]: continue
        elif "HGrep" in f or "CR" in f or "AR" in f or "HG" in f or \
            "Jsut" in f or "ＤＦ" in f or "明朝" in f or "TA" in f or \
              "symbol" in f.lower():
            continue
        font_items.append(f)
        config[f] = 1
        # save font-name
        with open(fn_conf, "w") as f:
            json.dump(config, f, indent=2, ensure_ascii=False)

# define layout
layout = [
    [eg.Frame(
            "Sample",
            expand_x=True,
            layout=[[eg.Text(f"Hello, 123 こんにちは?  Size:{f_size},len={len(font_items)}", key="-sample-")]],  )
    ],
    [eg.Listbox(
            values=font_items,  size=(40, 20),
            key="-fontlist-",   enable_events=True,   )
    ],
    [eg.Input("-", key="-font-", expand_x=True), eg.Button("Copy")],
    [eg.Button("font +"), eg.Button("font -"), eg.Text("   "),
     eg.Button("Save", color="#2222A0",font=("Arial",16,"bold")),eg.Text("   "),
     eg.Button("Exit", color="#FF2222", font=("Arial",16,"bold"))],
]
# create Window
flag = 1 # メイリオ,"Arial"
with eg.Window("JROD-GUI", layout, font=("メイリオ", f_size), finalize=True,
               size=(1200,1450),  # x,y 適当にFITされる。
               resizable=True, center_window=False, location=(100,100)) as window:
    if flag:
        flag = 0
        
        print("get_center_location=", window.get_center_location())
        print("get_screen_size=", window.get_screen_size())
        aaa = 0.95
        print("set_alpha_channel=", aaa)
        window.set_alpha_channel(aaa)
        w_size = (600,800) # Width, Height
        print("set_size=", w_size)
        window.set_size(w_size)
        print("get_size=", window.get_size())
    # set_theme
    eg.set_theme("alt") # 変化しない。
    ''' - macOS --- ('aqua', 'clam', 'alt', 'default', 'classic')
    - Windows --- ('winnative', 'clam', 'alt', 'default', 'classic', 'vista', 'xpnative')
    - Linux --- ('clam', 'alt', 'default', 'classic')'''
    # event loop
    for event, values in window.event_iter():
        print(f"# event: {event}, {values}")
        if event == "Exit" or event == eg.WINDOW_CLOSED:
            break
        if event == "Save":
            config["f_size"] = f_size
            config["sel_font"] = values["-font-"]
            with open(fn_conf, "w") as f:
              json.dump(config, f, indent=2, ensure_ascii=False)
        if event in ["-fontlist-", "font +", "font -"]:
            if event == "font +": f_size += 1
            if event == "font -": f_size -= 1
            print("f_size=", f_size)
            # get font name from listbox
            fontlist: eg.Listbox = window["-fontlist-"]
            index = fontlist.get_cursor_index()
            if index >= 0:
                font_name = font_items[index]
                window["-font-"].update(font_name)
                #window["-sample-"].update(font=(font_name, 18))
                window["-sample-"].set_text(f"Hello, 123 こんにちは?  Size:{f_size} len={len(font_items)}")
                window["-sample-"].update(font=(font_name, f_size))
        if event == "Copy":
            eg.set_clipboard(values["-font-"])
            eg.print("Copied to clipboard:\n" + values["-font-"])


