import tkinter as tk 
from tkinter import filedialog, messagebox, ttk
import subprocess
import os
import sys
import re
import urllib.request
import zipfile
import shutil
import requests
import tempfile
from tqdm import tqdm
import yt_dlp as youtube_dl
import unicodedata  # Hinzugefügt für Unicode-Funktionalität
from change_language import change_language
from packaging import version

current_version = "v0.0.4-alpha"

def compare_versions(v1, v2):
    return version.parse(v1) < version.parse(v2)

labels = change_language("de")

def check_for_updates():
    repo_url = "https://github.com/blobb999/ffmpegGUI"
    latest_version_url = f"{repo_url}/releases/latest/download/version.txt"
    new_exe_url = f"{repo_url}/releases/latest/download/ffmpegGUI.exe"

    # Update youtube-dl.exe without asking
    try:
        subprocess.run([os.path.join(bin_dir, "youtube-dl.exe"), "-U"], check=True, cwd=bin_dir)
    except Exception as e:
        messagebox.showerror(labels["error"], f"Fehler beim Aktualisieren von youtube-dl.exe:\n{e}")

    try:
        with urllib.request.urlopen(latest_version_url) as response:
            latest_version_info = response.read().decode("utf-8").strip()
            latest_version_lines = latest_version_info.split("\n")
            latest_version = latest_version_lines[0]
            changes = "\n".join(latest_version_lines[1:])

        is_update_needed = compare_versions(current_version, latest_version)

        if is_update_needed:
            update_message = labels["update_available"].format(latest_version=latest_version, changes=changes)
            if messagebox.askyesno(labels["info"], update_message):
                temp_dir = tempfile.gettempdir()
                new_exe_path = os.path.join(temp_dir, "ffmpegGUI_new.exe")
                urllib.request.urlretrieve(new_exe_url, new_exe_path)

                bat_script_path = os.path.join(temp_dir, "update_ffmpegGUI.bat")
                current_exe_path = os.path.realpath(sys.argv[0])
                with open(bat_script_path, 'w') as bat_file:
                    bat_file.write(f"""
                    @echo off
                    timeout /t 3 /nobreak
                    move /y "{new_exe_path}" "{current_exe_path}"
                    start "" "{current_exe_path}"
                    del "%~f0"
                    """)

                subprocess.Popen([bat_script_path], shell=True)
                root.quit()
            else:
                messagebox.showinfo(labels["info"], labels["update_aborted"])
        else:
            messagebox.showinfo(labels["info"], labels["success"])
    except Exception as e:
        messagebox.showerror(labels["error"], f"{labels['error']}:\n{e}")

def update_youtube_dl():
    try:
        youtube_dl_path = os.path.join(bin_dir, "youtube-dl.exe")
        subprocess.run([youtube_dl_path, "-U"], check=True, cwd=bin_dir)  # Update im bin-Verzeichnis ausführen
        messagebox.showinfo(labels["info"], "youtube-dl.exe wurde erfolgreich aktualisiert.")
    except Exception as e:
        messagebox.showerror(labels["error"], f"Fehler beim Aktualisieren von youtube-dl.exe:\n{e}")

def update_labels(language):
    global labels
    labels = change_language(language)

    source_label.config(text=labels["source"])
    target_label.config(text=labels["target"])
    browse_button.config(text=labels["browse"])
    browse_button_target.config(text=labels["browse"])
    convert_button.config(text=labels["convert"])
    repair_button.config(text=labels["repair"])
    info_button.config(text=labels["info"])
    extract_audio_button.config(text=labels["extract_audio"])
    split_video_button.config(text=labels["split_video"])
    cut_segment_button.config(text=labels["cut_segment"])
    download_button.config(text=labels["download"])
    video_options_label.config(text=labels["video_options"])
    speed_label.config(text=labels["speed"])
    split_duration_label.config(text=labels["split_duration"])
    audio_extract_label.config(text=labels["audio_extract"])
    segment_extract_label.config(text=labels["segment_extract"])
    from_to_label.config(text=labels["from_to"])
    youtube_url_label.config(text=labels["youtube_url"])
    twitter_url_label.config(text=labels["twitter_url"])
    tiktok_url_label.config(text=labels["tiktok_url"])
    twitter_download_button.config(text=labels["download_twitter"])
    tiktok_download_button.config(text=labels["download_tiktok"])
    mirror_label.config(text=labels["mirror"])
    update_button.config(text=labels["check_update"])

    notebook.tab(main_frame, text=labels["main_tab"])
    notebook.tab(youtube_frame, text=labels["youtube_tab"])
    notebook.tab(language_frame, text=labels["language_tab"])
    notebook.tab(info_frame, text=labels["info_tab"])


if not os.path.exists("img"):
    os.makedirs("img")

bin_dir = os.path.join(os.getcwd(), "bin")
if not os.path.exists(bin_dir):
    os.makedirs(bin_dir)

def move_to_bin(file):
    if os.path.exists(file):
        shutil.move(file, os.path.join(bin_dir, os.path.basename(file)))

def download_flag(country_code, save_path):
    urls = [
        f"https://flagcdn.com/w320/{country_code}.png",
        f"https://flagcdn.com/48x36/{country_code}.png",
        f"https://flagcdn.com/w40/{country_code}.png"
    ]
    for url in urls:
        try:
            urllib.request.urlretrieve(url, save_path)
            if os.path.exists(save_path):
                break
        except Exception as e:
            print(f"Error downloading flag for {country_code} from {url}: {e}")

def check_ffmpeg_and_ffprobe():
    def show_ffmpeg_error():
        def open_ffmpeg_download(event):
            import webbrowser
            webbrowser.open_new("https://ffmpeg.org/download.html")

        def download_and_install_ffmpeg():
            url = "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip"
            download_path = os.path.join(os.getcwd(), "ffmpeg-release-essentials.zip")
            install_path = os.path.join(os.getcwd(), "ffmpeg")

            try:
                # Download ffmpeg
                urllib.request.urlretrieve(url, download_path)

                # Extract the zip file
                with zipfile.ZipFile(download_path, 'r') as zip_ref:
                    zip_ref.extractall(install_path)

                # Locate the ffmpeg and ffprobe binaries
                ffmpeg_bin_path = None
                for root, dirs, files in os.walk(install_path):
                    if 'ffmpeg.exe' in files and 'ffprobe.exe' in files:
                        ffmpeg_bin_path = root
                        break

                if ffmpeg_bin_path:
                    # Move the binaries to the bin directory
                    shutil.move(os.path.join(ffmpeg_bin_path, 'ffmpeg.exe'), os.path.join(bin_dir, 'ffmpeg.exe'))
                    shutil.move(os.path.join(ffmpeg_bin_path, 'ffprobe.exe'), os.path.join(bin_dir, 'ffprobe.exe'))

                # Clean up
                os.remove(download_path)
                shutil.rmtree(install_path)

                # Restart the program
                python = sys.executable
                os.execl(python, python, *sys.argv)

            except Exception as e:
                messagebox.showerror(labels["error_download_ffmpeg"], f"{labels['error_download_ffmpeg']}\n{e}")

        error_window = tk.Toplevel(root)
        error_window.title(labels["error_ffmpeg"])
        error_window.geometry("400x150")
        error_window.transient(root)
        error_window.grab_set()

        message = tk.Label(error_window, text=labels["error_ffmpeg"])
        message.pack(pady=10)

        link = tk.Label(error_window, text="https://ffmpeg.org/download.html", fg="blue", cursor="hand2")
        link.pack()
        link.bind("<Button-1>", open_ffmpeg_download)

        install_button = tk.Button(error_window, text=labels["download"], command=download_and_install_ffmpeg)
        install_button.pack(pady=10)

        error_window.protocol("WM_DELETE_WINDOW", root.destroy)

        error_window.attributes('-topmost', True)
        error_window.update()
        error_window.attributes('-topmost', False)

    try:
        if os.path.exists("ffmpeg.exe"):
            move_to_bin("ffmpeg.exe")
        if os.path.exists("ffprobe.exe"):
            move_to_bin("ffprobe.exe")

        ffmpeg_path = os.path.join(bin_dir, "ffmpeg.exe")
        ffprobe_path = os.path.join(bin_dir, "ffprobe.exe")

        ffmpeg_result = subprocess.run([ffmpeg_path, "-version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        ffprobe_result = subprocess.run([ffprobe_path, "-version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        if ffmpeg_result.returncode != 0 or ffprobe_result.returncode != 0:
            show_ffmpeg_error()
            return False

    except FileNotFoundError:
        show_ffmpeg_error()
        return False

    return True


def run_ffmpeg_command(cmd):
    try:
        cmd[0] = os.path.join(bin_dir, cmd[0])
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        stdout, stderr = process.communicate()
        if process.returncode != 0:
            messagebox.showerror("Fehler", f"Fehler bei der Ausführung von {cmd[0]}:\n{stderr}")
        return process.returncode, stdout, stderr
    except FileNotFoundError:
        show_ffmpeg_error()
        return 1, "", f"{cmd[0]} not found"



def select_source_file():
    source_file = filedialog.askopenfilename()
    source_entry.delete(0, tk.END)
    source_entry.insert(0, source_file)
    update_target_file()
    update_segment_times()

def update_target_file():
    source_file = source_entry.get()
    if source_file:
        base, ext = os.path.splitext(source_file)
        target_file = f"{base}-edit{ext}"
        target_entry.delete(0, tk.END)
        target_entry.insert(0, target_file)

def update_segment_times():
    source_file = source_entry.get()
    if source_file:
        # Get video duration
        cmd_duration = [os.path.join(bin_dir, "ffprobe"), "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", source_file]
        result = subprocess.run(cmd_duration, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode == 0:
            try:
                total_duration = float(result.stdout.strip())
                duration_formatted = str(int(total_duration // 3600)).zfill(2) + ":" + str(int((total_duration % 3600) // 60)).zfill(2) + ":" + str(int(total_duration % 60)).zfill(2)
                start_time_entry.delete(0, tk.END)
                start_time_entry.insert(0, "00:00:00")
                end_time_entry.delete(0, tk.END)
                end_time_entry.insert(0, duration_formatted)
            except ValueError:
                pass

def select_target_file():
    target_file = filedialog.asksaveasfilename(defaultextension=".mp4")
    target_entry.delete(0, tk.END)
    target_entry.insert(0, target_file)

def convert():
    source_file = source_entry.get()
    target_file = target_entry.get()

    if not source_file or not target_file:
        messagebox.showerror(labels["error_select_source_target"], labels["error_select_source_target"])
        return

    speed_factor = float(speed_entry.get()) if speed_var.get() else 1
    temp_video_file = "temp_video.mp4"
    temp_audio_file = "temp_audio.mp4"

    # Video mit geänderter Geschwindigkeit und/oder Spiegelung
    video_filters = []
    if speed_var.get():
        video_filters.append(f"setpts={1/speed_factor}*PTS")
    if mirror_var.get():
        video_filters.append("hflip")
    video_filter_str = ",".join(video_filters) if video_filters else "null"

    cmd_video = [
        "ffmpeg", "-y", "-i", source_file,
        "-filter:v", video_filter_str,
        "-an", temp_video_file
    ]
    returncode, _, stderr = run_ffmpeg_command(cmd_video)
    if returncode != 0:
        return

    # Audio mit geänderter Geschwindigkeit
    cmd_audio = [
        "ffmpeg", "-y", "-i", source_file,
        "-filter:a", f"atempo={speed_factor}",
        "-vn", temp_audio_file
    ]
    returncode, _, stderr = run_ffmpeg_command(cmd_audio)
    if returncode != 0:
        return

    if os.path.exists(temp_video_file) and os.path.exists(temp_audio_file):
        cmd = [
            "ffmpeg", "-y", "-i", temp_video_file, "-i", temp_audio_file,
            "-c:v", "copy", "-c:a", "aac", "-strict", "experimental",
            target_file
        ]
        returncode, _, stderr = run_ffmpeg_command(cmd)
        if returncode != 0:
            return

        os.remove(temp_video_file)
        os.remove(temp_audio_file)
        messagebox.showinfo(labels["success_conversion"], labels["success_conversion"])
    else:
        cmd = ["ffmpeg", "-y", "-i", source_file, target_file]
        returncode, _, stderr = run_ffmpeg_command(cmd)
        if returncode == 0:
            messagebox.showinfo(labels["success_conversion"], labels["success_conversion"])
        else:
            messagebox.showerror(labels["error_ffmpeg_command"], f"{labels['error_ffmpeg_command']}\n{stderr}")


def repair_video():
    source_file = source_entry.get()
    target_file = target_entry.get()

    if not source_file or not target_file:
        messagebox.showerror(labels["error_select_source_target"], labels["error_select_source_target"])
        return

    # Reparatur des Videos durch Kopieren der Datenströme
    cmd = ["ffmpeg", "-y", "-i", source_file, "-c", "copy", target_file]
    returncode, _, stderr = run_ffmpeg_command(cmd)
    if returncode == 0:
        messagebox.showinfo(labels["success_repair"], labels["success_repair"])
    else:
        messagebox.showerror(labels["error_ffmpeg_command"], f"{labels['error_ffmpeg_command']}\n{stderr}")


def show_video_info():
    source_file = source_entry.get()

    if not source_file:
        messagebox.showerror(labels["error_select_file"], labels["error_select_file"])
        return

    cmd = ["ffmpeg", "-i", source_file, "-f", "null", "-"]
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    
    info_window = tk.Toplevel(root)
    info_window.title(labels["info"])
    info_window.geometry("600x400")

    text = tk.Text(info_window, wrap=tk.WORD)
    text.insert(tk.END, result.stderr)  # stderr enthält die Informationen
    text.pack(expand=True, fill=tk.BOTH)

def extract_audio():
    source_file = source_entry.get()
    audio_format = audio_format_var.get()
    target_file = target_entry.get()

    if not source_file or not target_file or not audio_format:
        messagebox.showerror(labels["error_select_source_target"], labels["error_select_source_target"])
        return

    if not target_file.endswith(f".{audio_format}"):
        target_file += f".{audio_format}"

    cmd = ["ffmpeg", "-y", "-i", source_file, "-q:a", "0", "-map", "a", target_file]

    returncode, _, stderr = run_ffmpeg_command(cmd)
    if returncode == 0:
        messagebox.showinfo(labels["success_audio_extraction"], labels["success_audio_extraction"])
    else:
        messagebox.showerror(labels["error_extraction"], f"{labels['error_extraction']}\n{stderr}")

def split_video():
    source_file = source_entry.get()
    target_directory = os.path.dirname(source_file)
    split_duration = int(split_duration_entry.get()) if split_duration_entry.get().strip() else 139

    if not source_file:
        messagebox.showerror("Fehler", "Bitte wählen Sie eine Quelldatei.")
        return

    cmd_duration = [os.path.join(bin_dir, "ffprobe"), "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", source_file]
    result = subprocess.run(cmd_duration, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if result.returncode != 0:
        messagebox.showerror("Fehler", f"Fehler beim Abrufen der Videodauer:\n{result.stderr}")
        return

    try:
        total_duration = float(result.stdout.strip())
    except ValueError:
        messagebox.showerror("Fehler", "Ungültige Videodauer.")
        return

    num_segments = int(total_duration // split_duration)
    for i in range(num_segments):
        start_time = i * split_duration
        segment_file = os.path.join(target_directory, f"{os.path.splitext(os.path.basename(source_file))[0]}_part{i+1}.mp4")
        cmd = [
            os.path.join(bin_dir, "ffmpeg"), "-y", "-i", source_file,
            "-ss", str(start_time), "-t", str(split_duration),
            "-c:a", "copy", "-c:v", "copy",
            segment_file
        ]
        returncode, _, stderr = run_ffmpeg_command(cmd)
        if returncode != 0:
            messagebox.showerror("Fehler", f"Fehler beim Splitten des Videos:\n{stderr}")
            return

    if total_duration % split_duration != 0:
        last_segment_file = os.path.join(target_directory, f"{os.path.splitext(os.path.basename(source_file))[0]}_part{num_segments+1}.mp4")
        cmd_last = [
            os.path.join(bin_dir, "ffmpeg"), "-y", "-i", source_file,
            "-ss", str(num_segments * split_duration),
            "-c:v", "copy", "-c:a", "copy", last_segment_file
        ]
        returncode, _, stderr = run_ffmpeg_command(cmd_last)
        if returncode != 0:
            messagebox.showerror(labels["error_split"], f"{labels['error_split']}:\n{stderr}")
            return

    messagebox.showinfo(labels["success_video_split"], labels["success_video_split"].format(num_segments=num_segments+1))


def show_supported_formats(parent):
    formats = ['mp4', 'avi', 'mov', 'mkv', 'flv', 'wmv', 'webm', 'mpeg']
    format_frame = tk.Frame(parent)
    format_frame.grid(row=1, column=3, padx=5, pady=5, sticky="nw")
    
    row, col = 0, 0
    for i, format_extension in enumerate(formats):
        format_button = tk.Button(format_frame, text=format_extension, command=lambda ext=format_extension: format_selected(ext))
        format_button.grid(row=row, column=col, padx=5, pady=5)
        col += 1
        if (i + 1) % 4 == 0:
            row += 1
            col = 0

def format_selected(format_extension):
    target_file = target_entry.get()
    if target_file:
        base, _ = os.path.splitext(target_file)
        target_entry.delete(0, tk.END)
        target_entry.insert(0, f"{base}.{format_extension}")

def cut_segment():
    source_file = source_entry.get()
    target_file = target_entry.get()
    start_time = start_time_entry.get()
    end_time = end_time_entry.get()

    if not source_file or not target_file or not start_time or not end_time:
        messagebox.showerror(labels["error"], labels["error_select_source_target"])
        return

    # Schneide das Segment aus dem Video
    cmd = [
        "ffmpeg", "-y", "-i", source_file, "-ss", start_time, "-to", end_time,
        "-c", "copy", target_file
    ]
    returncode, _, stderr = run_ffmpeg_command(cmd)
    if returncode != 0:
        messagebox.showerror(labels["error"], f"{labels['error_extraction']}:\n{stderr}")
        return

    messagebox.showinfo(labels["success"], labels["success_segment"])

# Funktion, um youtube-dl und aria2c zu überprüfen und ggf. zu installieren
def check_youtube_dl_and_aria2c():
    def download_and_install_youtube_dl():
        url = "https://github.com/ytdl-org/ytdl-nightly/releases/download/2024.07.03/youtube-dl.exe"
        download_path = os.path.join(bin_dir, "youtube-dl.exe")

        try:
            urllib.request.urlretrieve(url, download_path)
            subprocess.run([download_path, "-U"], check=True, cwd=bin_dir)  # Aktualisieren Sie youtube-dl.exe nach dem Herunterladen im bin-Verzeichnis
        except Exception as e:
            messagebox.showerror("Fehler", f"Fehler beim Download von youtube-dl:\n{e}")

    def download_and_install_aria2c():
        url = "https://altushost-swe.dl.sourceforge.net/project/aria2/stable/aria2-1.19.0/aria2-1.19.0-win-64bit-build1.zip?viasf=1"
        download_path = os.path.join(os.getcwd(), "aria2-64bit.zip")
        install_path = os.path.join(os.getcwd(), "aria2")

        try:
            # Download aria2
            urllib.request.urlretrieve(url, download_path)

            # Extract the zip file
            with zipfile.ZipFile(download_path, 'r') as zip_ref:
                zip_ref.extractall(install_path)

            # Locate the aria2c binary
            aria2c_bin_path = None
            for root, dirs, files in os.walk(install_path):
                if 'aria2c.exe' in files:
                    aria2c_bin_path = root
                    break

            if aria2c_bin_path:
                # Move the binary to the bin directory
                shutil.move(os.path.join(aria2c_bin_path, 'aria2c.exe'), os.path.join(bin_dir, 'aria2c.exe'))

            # Clean up
            os.remove(download_path)
            shutil.rmtree(install_path)

        except Exception as e:
            messagebox.showerror("Fehler", f"Fehler beim Download und Installation von aria2:\n{e}")

    if not os.path.exists(bin_dir):
        os.makedirs(bin_dir)

    if not os.path.exists(os.path.join(bin_dir, "youtube-dl.exe")):
        download_and_install_youtube_dl()
    else:
        subprocess.run([os.path.join(bin_dir, "youtube-dl.exe"), "-U"], check=True, cwd=bin_dir)  # Aktualisieren Sie youtube-dl.exe im bin-Verzeichnis

    if not os.path.exists(os.path.join(bin_dir, "aria2c.exe")):
        download_and_install_aria2c()

# Prüfen und Aktualisieren von youtube-dl.exe beim Start der Anwendung
check_youtube_dl_and_aria2c()



def download_youtube_video():
    youtube_url = youtube_url_entry.get()
    if not youtube_url:
        messagebox.showerror(labels["error"], labels["error_no_youtube_url"])
        return

    # Überprüfen, ob eine Twitter-URL oder eine X-URL eingegeben wurde
    if "twitter.com" in youtube_url or "x.com" in youtube_url:
        messagebox.showinfo(labels["info"], labels["info_twitter_url_moved"])
        twitter_url_entry.delete(0, tk.END)
        twitter_url_entry.insert(0, youtube_url)
        youtube_url_entry.delete(0, tk.END)
        return

    # Überprüfen, ob eine TikTok-URL eingegeben wurde
    if "tiktok.com" in youtube_url:
        messagebox.showinfo(labels["info"], labels["info_tiktok_url_moved"])
        tiktok_url_entry.delete(0, tk.END)
        tiktok_url_entry.insert(0, youtube_url)
        youtube_url_entry.delete(0, tk.END)
        return

    # Extrahiere Videoinformationen, um den Titel zu erhalten
    cmd_info = [
        os.path.join(bin_dir, "youtube-dl.exe"), "--get-title", youtube_url
    ]

    result = subprocess.run(cmd_info, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, cwd=bin_dir)
    if result.returncode != 0:
        messagebox.showerror(labels["error"], f"{labels['error_ffmpeg_command']}:\n{result.stderr}")
        return

    title = sanitize_filename(result.stdout.strip())

    # Verwende den bereinigten Titel für den Dateinamen
    output_template = f"{title}.%(ext)s"

    cmd_download = [
        os.path.join(bin_dir, "youtube-dl.exe"),
        "--external-downloader", os.path.join(bin_dir, "aria2c.exe"),
        "--external-downloader-args", "-x 16 -s 16 -k 1M --file-allocation=none",
        "--no-check-certificate", "--write-auto-sub", "--youtube-skip-dash-manifest",
        "--write-description", "--ignore-errors", "--no-call-home", "--console-title",
        "--add-metadata", "-f", "bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4",
        "--restrict-filenames", "--output", output_template, youtube_url
    ]

    returncode, _, stderr = run_ffmpeg_command(cmd_download)
    if returncode == 0:
        messagebox.showinfo(labels["success"], labels["success_youtube_download"])
    else:
        messagebox.showerror(labels["error"], f"{labels['error_ffmpeg_command']}:\n{stderr}")



def sanitize_filename(value):
    """
    Bereinigt den Dateinamen von Sonderzeichen und kürzt ihn auf eine sichere Länge.
    """
    value = str(value)
    value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
    value = re.sub(r'[^\w\s-]', '', value).strip().lower()
    value = re.sub(r'[-\s]+', '-', value)
    return value[:32]  # Kürze auf 32 Zeichen, was für die meisten Dateisysteme sicher ist.

def download_twitter_video_gui():
    twitter_url = twitter_url_entry.get()
    if not twitter_url:
        messagebox.showerror(labels["error"], labels["error_no_twitter_url"])
        return

    # Überprüfen, ob eine YouTube-URL eingegeben wurde
    if "youtube.com" in twitter_url or "youtu.be" in twitter_url:
        messagebox.showinfo(labels["info"], labels["info_youtube_url_moved"])
        youtube_url_entry.delete(0, tk.END)
        youtube_url_entry.insert(0, twitter_url)
        twitter_url_entry.delete(0, tk.END)
        return

    # Überprüfen, ob eine TikTok-URL eingegeben wurde
    if "tiktok.com" in twitter_url:
        messagebox.showinfo(labels["info"], labels["info_tiktok_url_moved"])
        tiktok_url_entry.delete(0, tk.END)
        tiktok_url_entry.insert(0, twitter_url)
        twitter_url_entry.delete(0, tk.END)
        return

    download_twitter_video(twitter_url)

def download_twitter_video(twitter_url):
    ydl_opts = {
        'outtmpl': '%(title)s.%(ext)s',
        'format': 'best',
        'noplaylist': True,
        'postprocessors': [{
            'key': 'FFmpegVideoConvertor',
            'preferedformat': 'mp4'
        }],
        'no_warnings': True,
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9'
        }
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        try:
            info_dict = ydl.extract_info(twitter_url, download=False)
            title = sanitize_filename(info_dict.get('title', 'video'))
            sanitized_filename = f'{title}.mp4'
            ydl_opts['outtmpl'] = sanitized_filename
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.download([twitter_url])
            messagebox.showinfo(labels["success"], labels["success_twitter_download"].format(filename=sanitized_filename))
        except Exception as e:
            messagebox.showerror(labels["error"], f"{labels['error_ffmpeg_command']}:\n{e}")

def download_tiktok_video_gui():
    tiktok_url = tiktok_url_entry.get()
    if not tiktok_url:
        messagebox.showerror(labels["error"], labels["error_no_tiktok_url"])
        return

    # Überprüfen, ob eine YouTube-URL eingegeben wurde
    if "youtube.com" in tiktok_url or "youtu.be" in tiktok_url:
        messagebox.showinfo(labels["info"], labels["info_youtube_url_moved"])
        youtube_url_entry.delete(0, tk.END)
        youtube_url_entry.insert(0, tiktok_url)
        tiktok_url_entry.delete(0, tk.END)
        return

    # Überprüfen, ob eine Twitter-URL eingegeben wurde
    if "twitter.com" in tiktok_url or "x.com" in tiktok_url:
        messagebox.showinfo(labels["info"], labels["info_twitter_url_moved"])
        twitter_url_entry.delete(0, tk.END)
        twitter_url_entry.insert(0, tiktok_url)
        tiktok_url_entry.delete(0, tk.END)
        return

    download_tiktok_video(tiktok_url)

def download_tiktok_video(tiktok_url):
    ydl_opts = {
        'outtmpl': '%(title)s.%(ext)s',
        'format': 'best',
        'noplaylist': True,
        'postprocessors': [{
            'key': 'FFmpegVideoConvertor',
            'preferedformat': 'mp4'
        }],
        'no_warnings': True,
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9'
        },
        'extractor_args': {
            'tiktok': {
                'skip_watermark': ['1']
            }
        }
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        try:
            info_dict = ydl.extract_info(tiktok_url, download=False)
            title = sanitize_filename(info_dict.get('title', 'video'))
            sanitized_filename = f'{title}.mp4'
            ydl_opts['outtmpl'] = sanitized_filename
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.download([tiktok_url])
            messagebox.showinfo(labels["success"], labels["success_tiktok_download"].format(filename=sanitized_filename))
        except Exception as e:
            messagebox.showerror(labels["error"], f"{labels['error_ffmpeg_command']}:\n{e}")


def download_update(urls):
    update_dir = os.path.join(tempfile.gettempdir(), "ffmpegGUI_update")
    if not os.path.exists(update_dir):
        os.makedirs(update_dir)

    for url in urls:
        local_filename = os.path.join(update_dir, url.split('/')[-1])
        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            total_size = int(r.headers.get('content-length', 0))
            with open(local_filename, 'wb') as f, tqdm(
                desc=local_filename,
                total=total_size,
                unit='B',
                unit_scale=True,
                unit_divisor=1024,
            ) as bar:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
                    bar.update(len(chunk))

    messagebox.showinfo("Update heruntergeladen", "Das Update wurde heruntergeladen. Bitte entpacken und installieren Sie es manuell.")

def add_flag_button(country_code, country_name, row, col, language_code):
    img_path = f"img/{country_code}.png"
    if not os.path.exists(img_path):
        download_flag(country_code, img_path)
    
    flag_image = tk.PhotoImage(file=img_path).subsample(2, 2)  # Verkleinern auf die Hälfte der ursprünglichen Größe
    button = tk.Button(language_frame, image=flag_image, command=lambda: update_labels(language_code))
    button.image = flag_image
    button.grid(row=row, column=col, padx=5, pady=5)
    button.config(command=lambda: [update_labels(language_code), root.update_idletasks()])

root = tk.Tk()
root.title("ffmpegGUI")

# Überprüfen, ob ffmpeg und ffprobe verfügbar sind
if not check_ffmpeg_and_ffprobe():
    root.mainloop()  # Die GUI läuft weiter, um die Fehlermeldung anzuzeigen
else:
    notebook = ttk.Notebook(root)
    notebook.pack(expand=True, fill="both")

    main_frame = ttk.Frame(notebook)
    main_frame.grid_propagate(True)
    notebook.add(main_frame, text="Main")

    youtube_frame = ttk.Frame(notebook)
    youtube_frame.grid_propagate(True)
    notebook.add(youtube_frame, text="Video Download")

    language_frame = ttk.Frame(notebook)
    language_frame.grid_propagate(True)
    notebook.add(language_frame, text="Language")

    info_frame = ttk.Frame(notebook)
    info_frame.grid_propagate(True)
    notebook.add(info_frame, text="Info")

    # Haupt-Tab (Main)
    source_label = tk.Label(main_frame, text=labels["source"])
    source_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
    source_entry = tk.Entry(main_frame, width=50)
    source_entry.grid(row=0, column=1, padx=5, pady=5, sticky="we")
    browse_button = tk.Button(main_frame, text=labels["browse"], command=select_source_file)
    browse_button.grid(row=0, column=2, padx=5, pady=5, sticky="e")

    target_label = tk.Label(main_frame, text=labels["target"])
    target_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")
    target_entry = tk.Entry(main_frame, width=50)
    target_entry.grid(row=1, column=1, padx=5, pady=5, sticky="we")
    browse_button_target = tk.Button(main_frame, text=labels["browse"], command=select_target_file)
    browse_button_target.grid(row=1, column=2, padx=5, pady=5, sticky="e")

    show_supported_formats(main_frame)

    video_options_label = tk.Label(main_frame, text=labels["video_options"])
    video_options_label.grid(row=2, column=0, padx=5, pady=5, sticky="w")

    speed_var = tk.BooleanVar()
    speed_label = tk.Checkbutton(main_frame, text=labels["speed"], variable=speed_var)
    speed_label.grid(row=3, column=0, padx=20, pady=5, sticky="w")
    speed_entry = tk.Entry(main_frame, width=10)
    speed_entry.grid(row=3, column=1, padx=(0, 5), pady=5, sticky="w")
    speed_entry.insert(0, "1.0")

    mirror_var = tk.BooleanVar()
    mirror_label = tk.Checkbutton(main_frame, text=labels["mirror"], variable=mirror_var)
    mirror_label.grid(row=4, column=0, padx=20, pady=5, sticky="w")

    split_duration_label = tk.Label(main_frame, text=labels["split_duration"])
    split_duration_label.grid(row=5, column=0, padx=5, pady=5, sticky="w")
    split_duration_entry = tk.Entry(main_frame, width=10)
    split_duration_entry.grid(row=5, column=1, padx=(0, 5), pady=5, sticky="w")
    split_duration_entry.insert(0, "139")
    split_video_button = tk.Button(main_frame, text=labels["split_video"], command=split_video)
    split_video_button.grid(row=5, column=3, padx=(0, 5), pady=5, sticky="w")

    audio_extract_label = tk.Label(main_frame, text=labels["audio_extract"])
    audio_extract_label.grid(row=6, column=0, padx=5, pady=5, sticky="w")
    audio_format_var = tk.StringVar(value="mp3")
    audio_format_menu = ttk.Combobox(main_frame, textvariable=audio_format_var)
    audio_format_menu['values'] = ('mp3', 'wav', 'm4a')
    audio_format_menu.grid(row=6, column=1, padx=(0, 5), pady=5, sticky="we")
    extract_audio_button = tk.Button(main_frame, text=labels["extract_audio"], command=extract_audio)
    extract_audio_button.grid(row=6, column=3, padx=(0, 5), pady=5, sticky="w")

    segment_extract_label = tk.Label(main_frame, text=labels["segment_extract"])
    segment_extract_label.grid(row=7, column=0, padx=5, pady=5, sticky="w")

    start_time_entry = tk.Entry(main_frame, width=10)
    start_time_entry.grid(row=7, column=1, padx=5, pady=5, sticky="w")

    from_to_label = tk.Label(main_frame, text=labels["from_to"])
    from_to_label.grid(row=7, column=1, padx=5, pady=5)

    end_time_entry = tk.Entry(main_frame, width=10)
    end_time_entry.grid(row=7, column=2, padx=5, pady=5, sticky="w")

    cut_segment_button = tk.Button(main_frame, text=labels["cut_segment"], command=cut_segment)
    cut_segment_button.grid(row=7, column=3, padx=(0, 5), pady=5, sticky="w")

    repair_button = tk.Button(main_frame, text=labels["repair"], command=repair_video)
    repair_button.grid(row=10, column=0, padx=5, pady=5, sticky="w")
    convert_button = tk.Button(main_frame, text=labels["convert"], command=convert)
    convert_button.grid(row=10, column=1, padx=5, pady=5, sticky="we")
    info_button = tk.Button(main_frame, text=labels["info"], command=show_video_info)
    info_button.grid(row=10, column=3, padx=(0, 5), pady=5, sticky="w")

    youtube_url_label = tk.Label(youtube_frame, text=labels["youtube_url"])
    youtube_url_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
    youtube_url_entry = tk.Entry(youtube_frame, width=50)
    youtube_url_entry.grid(row=0, column=1, padx=5, pady=5, sticky="we")
    download_button = tk.Button(youtube_frame, text=labels["download"], command=download_youtube_video)
    download_button.grid(row=0, column=2, padx=5, pady=5, sticky="e")

    # Twitter Download
    twitter_url_label = tk.Label(youtube_frame, text=labels["twitter_url"])
    twitter_url_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")
    twitter_url_entry = tk.Entry(youtube_frame, width=50)
    twitter_url_entry.grid(row=1, column=1, padx=5, pady=5, sticky="we")
    twitter_download_button = tk.Button(youtube_frame, text=labels["download_twitter"], command=download_twitter_video_gui)
    twitter_download_button.grid(row=1, column=2, padx=5, pady=5, sticky="e")

    # TikTok Download
    tiktok_url_label = tk.Label(youtube_frame, text=labels["tiktok_url"])
    tiktok_url_label.grid(row=2, column=0, padx=5, pady=5, sticky="w")
    tiktok_url_entry = tk.Entry(youtube_frame, width=50)
    tiktok_url_entry.grid(row=2, column=1, padx=5, pady=5, sticky="we")
    tiktok_download_button = tk.Button(youtube_frame, text=labels["download_tiktok"], command=download_tiktok_video_gui)
    tiktok_download_button.grid(row=2, column=2, padx=5, pady=5, sticky="e")

    # Info Tab
    info_text = f"""ffmpegGUI Version {current_version}
    Author: blobb999
    Dieses Programm verwendet ffmpeg für Video- und Audiooperationen.
    Mehr Informationen finden Sie auf der offiziellen Projektseite."""

    info_label = tk.Label(info_frame, text=info_text, justify="left")
    info_label.pack(padx=10, pady=10)

    update_button = tk.Button(info_frame, text=labels["check_update"], command=check_for_updates)
    update_button.pack(padx=10, pady=10)

    add_flag_button('de', 'Germany', 0, 0, 'de')
    add_flag_button('es', 'Spain', 0, 1, 'es')
    add_flag_button('gb', 'United Kingdom', 0, 2, 'en')
    add_flag_button('cn', 'China', 0, 3, 'zh')
    add_flag_button('ru', 'Russia', 0, 4, 'ru')
    add_flag_button('in', 'India', 1, 0, 'hi')
    add_flag_button('jp', 'Japan', 1, 1, 'ja')
    add_flag_button('sa', 'Saudi Arabia', 1, 2, 'ar')
    add_flag_button('br', 'Brazil', 1, 3, 'pt')
    add_flag_button('kr', 'Korea', 1, 4, 'ko')
    add_flag_button('dk', 'Denmark', 2, 0, 'da')
    add_flag_button('nl', 'Netherlands', 2, 1, 'nl')
    add_flag_button('pl', 'Poland', 2, 2, 'pl')
    add_flag_button('no', 'Norway', 2, 3, 'no')
    add_flag_button('fi', 'Finland', 2, 4, 'fi')
    add_flag_button('it', 'Italy', 3, 0, 'it')
    add_flag_button('fr', 'France', 3, 1, 'fr')
    add_flag_button('tr', 'Turkey', 3, 2, 'tr')
    add_flag_button('hu', 'Hungary', 3, 3, 'hu')
    add_flag_button('ar', 'Argentina', 3, 4, 'es_ar')

    def on_tab_change(event):
        selected_tab = event.widget.nametowidget(event.widget.select())
        root.update_idletasks()
        extra_height = 40  # Noch mehr Platz im unteren Bereich
        extra_width = 5  # Zusätzlicher Platz auf der rechten Seite
        root.geometry(f"{selected_tab.winfo_reqwidth() + extra_width}x{selected_tab.winfo_reqheight() + extra_height}")

    notebook.bind("<<NotebookTabChanged>>", on_tab_change)

    root.mainloop()
