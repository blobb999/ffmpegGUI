![ffmpegGUI](https://github.com/blobb999/ffmpeGUI/assets/89486466/fe9f8d3e-9c26-43b8-a6cf-1ae12896ea85)

ffmpegGUI Video Tool

Dieses Projekt ist eine Python-basierte GUI-Anwendung, die verschiedene Videobearbeitungsfunktionen mit ffmpeg bereitstellt. Es wurde mit tkinter entwickelt und bietet folgende Hauptfunktionen:

	Videokonvertierung: Ändern Sie das Format Ihrer Videodateien in verschiedene gängige 
		Formate wie mp4, avi, mov, mkv, flv, wmv, webm und mpeg.

	Geschwindigkeitsanpassung: Passen Sie die Geschwindigkeit des Videos an, um es schneller 
		oder langsamer abzuspielen.

	Videoreparatur: Reparieren Sie beschädigte Videodateien durch einfaches Kopieren der Datenströme, 
		um kleine Fehler zu beheben.
		
	Video Spiegeln: Videos können mit dem Selektieren einer Checkbox einfach gespiegelt werden.

	Video-Informationen anzeigen: Zeigen Sie detaillierte Informationen über Ihre Videodateien an, 
		wie z.B. Codec-Informationen, Bitrate und Dauer.

	Audioextraktion: Extrahieren Sie Audiodaten aus Videodateien in verschiedene 
		Formate wie mp3, wav und m4a.

	Video-Split: Teilen Sie Videos in Segmente einer bestimmten Länge auf, 
		ideal zum Teilen von langen Videos in kürzere Clips.

	Video-Extrahieren: Extrahieren Sie einen Teil aus dem Video anhand frei definierbarer 
		Anfangs- und Endzeit.

	YouTube-Download: Laden Sie YouTube-Videos mit Unterstützung von youtube-dl und aria2 herunter, 
		um die beste Videoqualität zu erhalten.

	Twitter-Download: Laden Sie Twitter-Videos mit Unterstützung von youtube-dl herunter.

	TikTok-Download: Laden Sie TikTok-Videos mit Unterstützung von youtube-dl herunter, 
		wobei das Wasserzeichen automatisch entfernt wird.

	GUI-Sprache anpassen: Unterstützt Sprachen wie Deutsch, Spanisch, Englisch, Chinesisch, 
		Russisch, Indisch, Japanisch, Arabisch, Portugiesisch, Koreanisch, Dänisch, 
		Holländisch, Polnisch, Norwegisch, Finnisch, Italienisch, Französisch, 
		Türkisch und Ungarisch, was etwa 70% der Erdbevölkerung abdeckt.
		
	Update Funktion: Das Tool verfügt über eine Update Funktion die von GitHub den aktuellsten Release vergleicht.
	
![ffmpegGUI-Language](https://github.com/blobb999/ffmpeGUI/assets/89486466/ef30dca4-2063-4df6-a4d5-253b747a760b)

Falls ffmpeg, ffprobe, youtube-dl oder aria2 auf dem System nicht installiert sind, bietet das Tool eine einfache Möglichkeit, diese Komponenten ins Programverzeichnis herunterzuladen und zu installieren.
![Video-Download-ffmpegGUI](https://github.com/blobb999/ffmpeGUI/assets/89486466/57011d2e-a777-4589-8807-0928c2dee289)

Anforderungen:

    ffmpeg und ffprobe: Werden auf Wunsch heruntergeladen und im Programverzeichnis installiert oder 
		können von der offiziellen FFmpeg-Website heruntergeladen werden. https://ffmpeg.org/download.html
    youtube-dl: Wird automatisch heruntergeladen und im Programverzeichnis installiert, falls nicht vorhanden. 
		Quelle: https://github.com/ytdl-org/ytdl-nightly
    aria2: Wird automatisch heruntergeladen und im Programverzeichnis installiert, 
		falls nicht vorhanden. Quelle: https://sourceforge.net/projects/aria2/
