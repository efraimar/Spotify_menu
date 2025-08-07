import pandas as pd
import tkinter as tk

class pincfloid:
    def __init__(self):
        self.data = {
                        "albums": [],
                        "year": [],
                        "name": [],
                        "composer": [],
                        "time": [],
                        "lyrics": []
                    }
        self.file = "Pink_Floyd_DB.TXT"
        self.years = []
        self.read_file()
        self.df = pd.DataFrame(self.data)

    def read_file(self):
        current_lyrics = None
        with open(self.file, 'r', encoding='utf-8') as f:
            for i, line in enumerate(f):
                if line.startswith("#"):
                    parts = line.split("::")
                    current_album = parts[0][1:]
                    current_year = parts[1].strip()
                    self.years.append(parts[1].strip())

                elif line.startswith("*"):
                    self.data["albums"].append(current_album)
                    self.data["year"].append(current_year)
                    if current_lyrics:
                        self.data["lyrics"].append(current_lyrics)
                    current_lyrics = ""
                    parts = line.split("::")
                    current_song_name = parts[0][1:]
                    current_composer = parts[1]
                    current_time = parts[2]
                    self.data["name"].append(current_song_name)
                    self.data["composer"].append(current_composer)
                    self.data["time"].append(current_time)
                    current_lyrics = parts[3].strip() + " "
                else:
                    current_lyrics += " " + line.strip()
            self.data["lyrics"].append(current_lyrics)


class SongSearchApp:
    def __init__(self, root ,pf):
        self.root = root
        self.root.title("חיפוש שירים")
        self.root.geometry("600x500")
        self.data = pf.data
        self.df_pf = pf.df
        self.albums = list(pf.df["albums"].unique())

        self.title_label = tk.Label(self.root, text="🎶 Welcome to the song search engine! 🎶", font=("Arial", 14, "bold"))
        self.title_label.pack(pady=10)

        self.entry = tk.Entry(self.root, width=40)
        self.entry.pack(pady=10)
        self.entry.bind("<FocusIn>", self.update_listbox)
        self.entry.bind("<KeyRelease>", self.update_listbox)
        self.choose_text = tk.Label(self.root, text="Choose album:")

        self.listbox = None
        self.back_button = None
        self.album_buttons = []

        self.albums_list_chose()

    def albums_list_chose(self):
        self.choose_text.pack()
        for album in self.albums:
            btn = tk.Button(self.root, text=album, command=lambda a=album: self.album_selected(a))
            btn.pack(pady=2)
            self.album_buttons.append(btn)

    def hide_album_buttons(self):
        for btn in self.album_buttons:
            btn.pack_forget()

    def show_album_buttons(self):
        for btn in self.album_buttons:
            btn.pack(pady=2)

    def create_listbox(self):
        if self.listbox is None:
            self.listbox = tk.Listbox(self.root, width=40, height=10)
            self.listbox.pack()
            self.listbox.bind("<<ListboxSelect>>", self.on_select)

            self.back_button = tk.Button(self.root, text="⬅ Back", command=self.back_to_menu)
            self.back_button.pack(pady=10)

    def update_listbox(self, event=None):
        typed = self.entry.get().lower()
        if typed == "":
            self.hide_listbox()
            self.show_album_buttons()
            return

        self.hide_album_buttons()
        self.create_listbox()
        self.listbox.delete(0, tk.END)

        seen = set()
        for song in self.data["name"]:
            if typed in song.lower() and song not in seen:
                self.listbox.insert(tk.END, song)
                seen.add(song)

        for album in self.albums:
            if typed in album.lower() and album not in seen:
                self.listbox.insert(tk.END, album)
                seen.add(album)

        for i, lyrics in enumerate(self.data["lyrics"]):
            lyrics_words = [word.lower() for word in lyrics.split()]
            if typed in lyrics_words:
                song = self.data["name"][i]
                if song not in seen:
                    self.listbox.insert(tk.END, song)
                    seen.add(song)

    def on_select(self, event):
        selection = self.listbox.curselection()
        if selection:
            selected = self.listbox.get(selection)
            if selected in self.data["albums"]:
                self.album_selected(selected)
            if selected in self.data["name"]:
                i = self.data["name"].index(selected)
                self.song_selected(i)

    def album_selected(self,album):
        self.cleen_all()

        tk.Label(self.root, text=album, font=("Arial", 16, "bold")).pack(pady=10)

        scroll_frame = tk.Frame(self.root)
        scroll_frame.pack(expand=True, fill="both")

        canvas = tk.Canvas(scroll_frame)
        canvas.pack(side="left", fill="both", expand=True)

        scrollbar = tk.Scrollbar(scroll_frame, orient="vertical", command=canvas.yview)
        scrollbar.pack(side="right", fill="y")

        canvas.configure(yscrollcommand=scrollbar.set)

        button_frame = tk.Frame(canvas)
        canvas.create_window((0, 0), window=button_frame, anchor="nw")

        def on_frame_configure(event):
            canvas.configure(scrollregion=canvas.bbox("all"))

        button_frame.bind("<Configure>", on_frame_configure)

        songs = self.df_pf[self.df_pf["albums"] == album]["name"]
        for i, song in enumerate(songs):
            real_index = self.data["name"].index(song)
            button = tk.Button(button_frame, text=song, command=lambda idx=real_index: self.song_selected(idx))
            button.pack(pady=4, padx=10, anchor="w")

        self.back_button = tk.Button(self.root, text="⬅ Back", command=self.back_to_menu)
        self.back_button.pack(pady=10)

    def back_to_menu(self):
        self.cleen_all()
        self.listbox = None
        self.back_button = None

        self.title_label.pack(pady=10)
        self.entry.pack(pady=10)
        self.entry.delete(0, tk.END)
        self.choose_text.pack()

        self.show_album_buttons()

    def song_selected(self, i):
        self.cleen_all()
        tk.Label(self.root, text="The song you chose:", font=("Arial", 18, "bold")).pack(pady=5)
        tk.Label(self.root, text=self.data["name"][i], font=("Arial", 14)).pack(pady=5)

        text_frame = tk.Frame(self.root)
        text_frame.pack(pady=10)

        scrollbar = tk.Scrollbar(text_frame)
        scrollbar.pack(side="right", fill="y")

        text_widget = tk.Text(text_frame, wrap="word", width=60, height=15, font=("Arial", 12),
                              yscrollcommand=scrollbar.set)
        text_widget.pack(side="left", fill="both")

        scrollbar.config(command=text_widget.yview)

        text_widget.insert("end", "Song lyrics:\n", "bold")

        lyrics_lines = self.data["lyrics"][i].split(', ')
        for line in lyrics_lines:
            clean_line = line.strip()
            if clean_line:
                text_widget.insert("end", clean_line + '.\n\n')

        text_widget.tag_configure("bold", font=("Arial", 12, "bold"))
        text_widget.config(state="disabled")

        tk.Label(self.root, text=f"Duration of the song: {self.data['time'][i]}", font=("Arial", 10, "italic")).pack(pady=3)

        name_album = self.df_pf["albums"][i]
        tk.Button(self.root, text="ALBUM: "+name_album, command=lambda : self.album_selected(name_album)).pack()
        tk.Button(self.root, text="⬅ Back", command=self.back_to_menu).pack()

    def hide_listbox(self):
        if self.listbox:
            self.listbox.pack_forget()
            self.listbox = None
        if self.back_button:
            self.back_button.pack_forget()
            self.back_button = None

    def cleen_all(self):
        for widget in self.root.winfo_children():
            widget.pack_forget()


if __name__ == '__main__':
    root = tk.Tk()
    pf = pincfloid()
    app = SongSearchApp(root, pf)
    root.mainloop()