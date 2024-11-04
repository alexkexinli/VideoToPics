import os
from moviepy.editor import VideoFileClip
from PIL import Image
from multiprocessing import Pool, cpu_count

def process_mp4(args):
    mp4_path, input_root, output_root = args
    try:
        print(f'正在处理: {mp4_path}')
        # 打开视频文件
        clip = VideoFileClip(mp4_path)
        duration = int(clip.duration)  # 获取视频时长（秒）
        # 构造输出文件夹路径，保持与输入的目录结构一致
        relative_path = os.path.relpath(mp4_path, start=input_root)
        relative_dir = os.path.dirname(relative_path)
        mp4_filename = os.path.splitext(os.path.basename(mp4_path))[0]
        frames_folder = os.path.join(output_root, relative_dir, mp4_filename)
        os.makedirs(frames_folder, exist_ok=True)
        # 每秒截取一帧
        for t in range(duration):
            frame = clip.get_frame(t)
            frame_image = Image.fromarray(frame)
            frame_filename = os.path.join(frames_folder, f'frame_{t:04d}.jpg')
            frame_image.save(frame_filename)
        clip.reader.close()
        if clip.audio:
            clip.audio.reader.close_proc()
    except Exception as e:
        print(f"处理文件 {mp4_path} 时出错: {e}")

def get_all_mp4_files(input_root):
    mp4_files = []
    for dirpath, dirnames, filenames in os.walk(input_root):
        for filename in filenames:
            if filename.lower().endswith('.mp4'):
                mp4_path = os.path.join(dirpath, filename)
                mp4_files.append(mp4_path)
    return mp4_files

def process_folder(input_root, output_root):
    mp4_files = get_all_mp4_files(input_root)
    args_list = [(mp4_path, input_root, output_root) for mp4_path in mp4_files]

    num_processes = cpu_count()  # 获取 CPU 核心数
    print(f"使用 {num_processes} 个进程进行处理")
    with Pool(processes=num_processes) as pool:
        pool.map(process_mp4, args_list)

if __name__ == '__main__':
    input_root_folder = r'E:\videos-to-cut'
    output_root_folder = r'E:\image-cut-rst'
    process_folder(input_root_folder, output_root_folder)
