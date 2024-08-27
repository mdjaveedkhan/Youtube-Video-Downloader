import yt_dlp
from tkinter import *
from tkinter import filedialog, messagebox

# Initialize the main window
root = Tk()
root.geometry('600x400')
root.resizable(0, 0)
root.title("YouTube Video Downloader")

# Add title label
Label(root, text='YouTube Video Downloader', font='arial 20 bold').pack()

# Variable to store the YouTube link, format, and quality options
link = StringVar()
format_type = StringVar(value='mp4')  # Default to MP4
quality = StringVar(value='')

# Add label and entry for link input
Label(root, text='Paste Link Here:', font='arial 15 bold').place(x=20, y=60)
link_enter = Entry(root, width=80, textvariable=link)
link_enter.place(x=20, y=90)

# Add radio buttons for format selection
Label(root, text='Select Format:', font='arial 15 bold').place(x=20, y=130)
Radiobutton(root, text='MP4', variable=format_type, value='mp4', font='arial 15').place(x=20, y=160)
Radiobutton(root, text='MP3', variable=format_type, value='mp3', font='arial 15').place(x=100, y=160)

# Add label and dropdown for quality selection
Label(root, text='Select Quality:', font='arial 15 bold').place(x=20, y=200)
quality_options = {'mp4': ['1080p', '720p', '360p'], 'mp3': ['192kbps', '128kbps', '64kbps']}
quality_menu = OptionMenu(root, quality, *quality_options['mp4'])
quality_menu.place(x=20, y=230)

# Function to update quality options based on format selection
def update_quality_options(*args):
    selected_format = format_type.get()
    options = quality_options[selected_format]
    quality_menu['menu'].delete(0, 'end')
    for option in options:
        quality_menu['menu'].add_command(label=option, command=lambda value=option: quality.set(value))

# Bind format_type to update quality options
format_type.trace('w', update_quality_options)

# Function to download the video
def Downloader():
    try:
        # Open a dialog to select the destination folder
        download_path = filedialog.askdirectory()
        if download_path:
            url = link.get()
            selected_format = format_type.get()
            ydl_opts = {'outtmpl': f'{download_path}/%(title)s.%(ext)s'}
            if selected_format == 'mp4':
                if quality.get() in ['1080p', '720p', '360p']:
                    ydl_opts['format'] = f'bestvideo[height<={quality.get()}]+bestaudio/best[height<={quality.get()}]'
                else:
                    ydl_opts['format'] = 'bestvideo+bestaudio/best'
            elif selected_format == 'mp3':
                if quality.get() in ['192kbps', '128kbps', '64kbps']:
                    ydl_opts['format'] = f'bestaudio[abr<={quality.get()}]'
                else:
                    ydl_opts['format'] = 'bestaudio'
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            messagebox.showinfo("Success", "Video downloaded successfully!")
        else:
            messagebox.showwarning("Cancelled", "Download cancelled.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

# Add download button
Button(root, text='DOWNLOAD', font='arial 15 bold', bg='pale violet red', padx=2, command=Downloader).place(x=20, y=270)

# Run the main event loop
root.mainloop()
