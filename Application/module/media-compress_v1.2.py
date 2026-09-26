import os
import shutil
from pathlib import Path
class Color:
    CYAN='\033[96m';BLUE='\033[94m';WHITE='\033[97m';GREEN='\033[92m'
    YELLOW='\033[93m';RED='\033[91m';BOLD='\033[1m';DIM='\033[2m';RESET='\033[0m'
PRESETS={
'light':{'label':'Light','desc':'High quality, small reduction','image_quality':85,'video_bitrate':'2500k','audio_bitrate':'192k','gif_scale':0.90,'gif_fps':15},
'balanced':{'label':'Balanced','desc':'Recommended for daily use','image_quality':70,'video_bitrate':'1500k','audio_bitrate':'128k','gif_scale':0.70,'gif_fps':12},
'strong':{'label':'Strong','desc':'Good compression, decent quality','image_quality':50,'video_bitrate':'800k','audio_bitrate':'96k','gif_scale':0.50,'gif_fps':10},
'extreme':{'label':'Extreme','desc':'Maximum compression, lower quality','image_quality':25,'video_bitrate':'400k','audio_bitrate':'64k','gif_scale':0.35,'gif_fps':8},
}
def print_status(icon,message,color=Color.WHITE):
    print(f"  {color}{Color.BOLD}[{icon}]{Color.RESET} {Color.WHITE}{message}{Color.RESET}")
def get_file_size(path):
    return os.path.getsize(path)
def human_size(bytes_size):
    for unit in ['B','KB','MB','GB']:
        if bytes_size<1024:return f"{bytes_size:.2f} {unit}"
        bytes_size/=1024
    return f"{bytes_size:.2f} TB"
def ensure_output_dir(output_dir):
    Path(output_dir).mkdir(parents=True,exist_ok=True)
def compress_image(input_path,output_dir,quality=70):
    try:
        from PIL import Image
    except ImportError:
        print_status('!','Pillow not installed. Run: pip install Pillow',Color.RED)
        return None
    ensure_output_dir(output_dir)
    filename=Path(input_path).stem
    ext=Path(input_path).suffix.lower()
    output_path=os.path.join(output_dir,f"{filename}_compressed{ext}")
    original_size=get_file_size(input_path)
    print_status('*','Compressing image...',Color.CYAN)
    img=Image.open(input_path)
    if img.mode in ('RGBA','P'):img=img.convert('RGB')
    if ext in ('.jpg','.jpeg'):img.save(output_path,'JPEG',quality=quality,optimize=True)
    elif ext=='.png':img.save(output_path,'PNG',optimize=True)
    elif ext=='.webp':img.save(output_path,'WEBP',quality=quality)
    else:img.save(output_path,quality=quality)
    new_size=get_file_size(output_path)
    _report(input_path,output_path,original_size,new_size)
    return output_path
def compress_video(input_path,output_dir,bitrate='1500k',preset='medium'):
    try:
        from moviepy.editor import VideoFileClip
    except ImportError:
        print_status('!','moviepy not installed. Run: pip install moviepy',Color.RED)
        return None
    ensure_output_dir(output_dir)
    filename=Path(input_path).stem
    output_path=os.path.join(output_dir,f"{filename}_compressed.mp4")
    original_size=get_file_size(input_path)
    print_status('*','Processing video, this may take a while...',Color.CYAN)
    clip=VideoFileClip(input_path)
    clip.write_videofile(output_path,bitrate=bitrate,preset=preset,audio_codec='aac',logger=None)
    clip.close()
    new_size=get_file_size(output_path)
    _report(input_path,output_path,original_size,new_size)
    return output_path
def compress_audio(input_path,output_dir,bitrate='128k'):
    try:
        from pydub import AudioSegment
    except ImportError:
        print_status('!','pydub not installed. Run: pip install pydub',Color.RED)
        return None
    ensure_output_dir(output_dir)
    filename=Path(input_path).stem
    output_path=os.path.join(output_dir,f"{filename}_compressed.mp3")
    original_size=get_file_size(input_path)
    print_status('*','Compressing audio...',Color.CYAN)
    audio=AudioSegment.from_file(input_path)
    audio.export(output_path,format='mp3',bitrate=bitrate)
    new_size=get_file_size(output_path)
    _report(input_path,output_path,original_size,new_size)
    return output_path
def compress_gif(input_path,output_dir,scale=0.7,fps=12):
    try:
        from moviepy.editor import VideoFileClip
    except ImportError:
        print_status('!','moviepy not installed. Run: pip install moviepy',Color.RED)
        return None
    ensure_output_dir(output_dir)
    filename=Path(input_path).stem
    output_path=os.path.join(output_dir,f"{filename}_compressed.gif")
    original_size=get_file_size(input_path)
    print_status('*','Compressing GIF...',Color.CYAN)
    clip=VideoFileClip(input_path)
    resized=clip.resize(scale)
    resized.write_gif(output_path,fps=fps,logger=None)
    clip.close()
    new_size=get_file_size(output_path)
    _report(input_path,output_path,original_size,new_size)
    return output_path
def compress_pdf(input_path,output_dir):
    ensure_output_dir(output_dir)
    filename=Path(input_path).stem
    output_path=os.path.join(output_dir,f"{filename}_compressed.pdf")
    original_size=get_file_size(input_path)
    print_status('*','Compressing PDF...',Color.CYAN)
    gs_cmd=shutil.which('gs')
    if gs_cmd:
        import subprocess
        cmd=[gs_cmd,'-sDEVICE=pdfwrite','-dCompatibilityLevel=1.4','-dPDFSETTINGS=/ebook','-dNOPAUSE','-dQUIET','-dBATCH',f'-sOutputFile={output_path}',input_path]
        subprocess.run(cmd,check=True)
    else:
        print_status('!','Ghostscript not found, using basic PyPDF2',Color.YELLOW)
        try:
            from PyPDF2 import PdfReader,PdfWriter
            reader=PdfReader(input_path)
            writer=PdfWriter()
            for page in reader.pages:writer.add_page(page)
            for page in writer.pages:page.compress_content_streams()
            with open(output_path,'wb') as f:writer.write(f)
        except ImportError:
            shutil.copy(input_path,output_path)
    new_size=get_file_size(output_path)
    _report(input_path,output_path,original_size,new_size)
    return output_path
def compress_any(input_path,output_dir,level='balanced'):
    ext=Path(input_path).suffix.lower()
    image_ext={'.jpg','.jpeg','.png','.webp','.bmp','.tiff'}
    video_ext={'.mp4','.avi','.mov','.mkv','.flv','.wmv'}
    audio_ext={'.mp3','.wav','.ogg','.m4a','.flac'}
    cfg=PRESETS.get(level,PRESETS['balanced'])
    print_status('?',f'Detected: {ext}  |  Level: {cfg["label"]}',Color.CYAN)
    if ext in image_ext:return compress_image(input_path,output_dir,quality=cfg['image_quality'])
    elif ext in video_ext:return compress_video(input_path,output_dir,bitrate=cfg['video_bitrate'])
    elif ext in audio_ext:return compress_audio(input_path,output_dir,bitrate=cfg['audio_bitrate'])
    elif ext=='.gif':return compress_gif(input_path,output_dir,scale=cfg['gif_scale'],fps=cfg['gif_fps'])
    elif ext=='.pdf':return compress_pdf(input_path,output_dir)
    else:
        print_status('!',f'Unsupported format: {ext}',Color.RED)
        return None
def _report(input_path,output_path,old_size,new_size):
    saved=old_size-new_size
    percent=(saved/old_size*100) if old_size>0 else 0
    print()
    print_status('✓','Compression complete!',Color.GREEN)
    print_status('#',f'Input  : {input_path}',Color.CYAN)
    print_status('#',f'Output : {output_path}',Color.CYAN)
    print_status('#',f'Before : {human_size(old_size)}',Color.YELLOW)
    print_status('#',f'After  : {human_size(new_size)}',Color.YELLOW)
    print_status('+',f'Saved  : {human_size(saved)} ({percent:.1f}%)',Color.GREEN)
    print()
