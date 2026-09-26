#!/usr/bin/env python3
import os
import sys
from pathlib import Path
sys.path.insert(0,os.path.join(os.path.dirname(__file__),'module'))
import importlib.util
MODULE_PATH=os.path.join(os.path.dirname(__file__),'module','media-compress_v1.2.py')
spec=importlib.util.spec_from_file_location("media_compress",MODULE_PATH)
mc=importlib.util.module_from_spec(spec)
spec.loader.exec_module(mc)
class C:
    CYAN='\033[96m';BLUE='\033[94m';WHITE='\033[97m';GREEN='\033[92m'
    YELLOW='\033[93m';RED='\033[91m';BOLD='\033[1m';DIM='\033[2m';RESET='\033[0m'
BANNER=r"""
    __  ___         ___            _  __
   /  |/  /__  ____/ (_)___ _     | |/ /
  / /|_/ / _ \/ __  / / __ `/_____|   /
 / /  / /  __/ /_/ / / /_/ /_____/   |
/_/  /_/\___/\__,_/_/\__,_/     /_/|_|
"""
VERSION="v1.2.0.0  -  stable"
def clear_screen():
    os.system('cls' if os.name=='nt' else 'clear')
def print_header():
    clear_screen()
    print()
    for line in BANNER.strip('\n').split('\n'):
        print(f"{C.CYAN}{C.BOLD}{line}{C.RESET}")
    print()
    print(f"{C.CYAN}{VERSION}{C.RESET}")
    print()
def print_menu():
    print(f"  {C.WHITE}{C.BOLD}SELECT MEDIA TYPE{C.RESET}")
    print()
    menu_items=[
        ('1','Image','JPG / JPEG / PNG / WEBP / BMP',C.CYAN),
        ('2','Video','MP4 / AVI / MOV / MKV / FLV',C.CYAN),
        ('3','Audio','MP3 / WAV / OGG / M4A / FLAC',C.CYAN),
        ('4','GIF','Animated GIF compression',C.CYAN),
        ('5','PDF','PDF document compression',C.CYAN),
        ('6','All','Auto-detect & compress any',C.GREEN),
        ('0','Exit','Quit application',C.RED),
    ]
    for num,name,desc,color in menu_items:
        print(f"   {C.WHITE}{C.BOLD}[{num}]{C.RESET}  {color}{C.BOLD}{name:<8}{C.RESET}  {C.DIM}{desc}{C.RESET}")
    print()
def print_level_menu():
    print()
    print(f"  {C.WHITE}{C.BOLD}SELECT COMPRESSION LEVEL{C.RESET}")
    print()
    levels=[
        ('1','Light','High quality, small reduction',C.CYAN),
        ('2','Balanced','Recommended for daily use',C.CYAN),
        ('3','Strong','Good compression, decent quality',C.YELLOW),
        ('4','Extreme','Maximum compression, lower quality',C.RED),
        ('0','Back','Return to media menu',C.WHITE),
    ]
    for num,name,desc,color in levels:
        print(f"   {C.WHITE}{C.BOLD}[{num}]{C.RESET}  {color}{C.BOLD}{name:<9}{C.RESET}  {C.DIM}{desc}{C.RESET}")
    print()
def get_input(prompt,color=C.CYAN):
    return input(f"  {color}{C.BOLD}❯{C.RESET} {C.WHITE}{prompt}{C.RESET} ").strip()
def pause():
    input(f"  {C.DIM}Press Enter to continue...{C.RESET}")
def validate_file(path):
    p=Path(path)
    if not p.exists():
        mc.print_status('!',f'File not found: {path}',C.RED)
        return False
    if not p.is_file():
        mc.print_status('!',f'Not a file: {path}',C.RED)
        return False
    return True
def ask_level():
    level_map={'1':'light','2':'balanced','3':'strong','4':'extreme'}
    print_level_menu()
    choice=get_input('Choose level [0-4]:',C.CYAN)
    if choice=='0':return None
    if choice not in level_map:
        mc.print_status('!',f'Invalid level: {choice}, using Balanced',C.YELLOW)
        return 'balanced'
    return level_map[choice]
def handle_image():
    path=get_input('Enter image path:',C.CYAN)
    if not path or not validate_file(path):return
    level=ask_level()
    if level is None:return
    cfg=mc.PRESETS[level]
    mc.print_status('?',f'Level: {cfg["label"]}  |  Quality: {cfg["image_quality"]}',C.CYAN)
    mc.compress_image(path,'compression_result',quality=cfg['image_quality'])
def handle_video():
    path=get_input('Enter video path:',C.CYAN)
    if not path or not validate_file(path):return
    level=ask_level()
    if level is None:return
    cfg=mc.PRESETS[level]
    mc.print_status('?',f'Level: {cfg["label"]}  |  Bitrate: {cfg["video_bitrate"]}',C.CYAN)
    mc.compress_video(path,'compression_result',bitrate=cfg['video_bitrate'])
def handle_audio():
    path=get_input('Enter audio path:',C.CYAN)
    if not path or not validate_file(path):return
    level=ask_level()
    if level is None:return
    cfg=mc.PRESETS[level]
    mc.print_status('?',f'Level: {cfg["label"]}  |  Bitrate: {cfg["audio_bitrate"]}',C.CYAN)
    mc.compress_audio(path,'compression_result',bitrate=cfg['audio_bitrate'])
def handle_gif():
    path=get_input('Enter GIF path:',C.CYAN)
    if not path or not validate_file(path):return
    level=ask_level()
    if level is None:return
    cfg=mc.PRESETS[level]
    mc.print_status('?',f'Level: {cfg["label"]}  |  Scale: {cfg["gif_scale"]}  |  FPS: {cfg["gif_fps"]}',C.CYAN)
    mc.compress_gif(path,'compression_result',scale=cfg['gif_scale'],fps=cfg['gif_fps'])
def handle_pdf():
    path=get_input('Enter PDF path:',C.CYAN)
    if not path or not validate_file(path):return
    mc.compress_pdf(path,'compression_result')
def handle_all():
    path=get_input('Enter media path, auto-detect:',C.CYAN)
    if not path or not validate_file(path):return
    level=ask_level()
    if level is None:return
    mc.compress_any(path,'compression_result',level=level)
def main():
    handlers={'1':handle_image,'2':handle_video,'3':handle_audio,'4':handle_gif,'5':handle_pdf,'6':handle_all}
    while True:
        print_header()
        print_menu()
        choice=get_input('Choose option [0-6]:',C.CYAN)
        if choice=='0':
            clear_screen()
            print()
            mc.print_status('✓','Goodbye!',C.GREEN)
            print()
            break
        if choice in handlers:
            print()
            try:
                handlers[choice]()
            except KeyboardInterrupt:
                print()
                mc.print_status('!','Cancelled by user',C.YELLOW)
            except Exception as e:
                mc.print_status('!',f'Error: {e}',C.RED)
            print()
            pause()
        else:
            print()
            mc.print_status('!',f'Invalid option: {choice}',C.RED)
            print()
            pause()
if __name__=='__main__':
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n  {C.YELLOW}[!]{C.RESET} {C.WHITE}Interrupted. Bye!{C.RESET}\n")
        sys.exit(0)
