from kivy.app import App
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from webview import WebView
from os import listdir
from textwrap import fill

class BrowserApp(App):
    def build(self):
        self._create_local_file()
        self.browser = None
        b1 = Button(text='Ir a TaskHub',
                    on_press=self.view_web)
        b2 = Button(text='Página web de Jotalea',
                    on_press=self.view_web2)
        b3 = Button(text='Más Información',
                    on_press=self.view_local_file)
        self.label = Label(text='')
        box = BoxLayout(orientation='vertical')
        box.add_widget(b1)
        box.add_widget(b2)
        #box.add_widget(b3)
        box.add_widget(self.label)
        return box
        
    def view_web(self,b):
        self.browser = WebView('http://tarea.jotalea.com.ar',
                               enable_javascript = True,
                               enable_downloads = True,
                               enable_zoom = True)
    def view_web2(self,b):
        self.browser = WebView('http://jotalea.com.ar',
                               enable_javascript = True,
                               enable_downloads = True,
                               enable_zoom = True)
        
    def view_local_file(self,b):
        self.browser = WebView('file://'+self.filename,
                               enable_javascript = True)

    def view_downloads(self,b):
        if self.browser:
            d = self.browser.downloads_directory()
            self.label.text = fill(d,40) + '\n'
            l = listdir(d)
            if l:
                for f in l:
                    self.label.text += f + '\n'
            else:
                self.label.text = 'No files downloaded'
        else:
            self.label.text = 'Open a browser first'
                
    def on_pause(self): 
        if self.browser:
            self.browser.pause()
        return True

    def on_resume(self):
        if self.browser:
            self.browser.resume()
        pass

    def _create_local_file(self):
        # Create a file for testing
        from android.storage import app_storage_path
        from jnius import autoclass
        from os.path import join, exists
        from os import mkdir
        
        Environment = autoclass('android.os.Environment')
        path = join(app_storage_path(), Environment.DIRECTORY_DOCUMENTS)
        if not exists(path):
            mkdir(path)
        self.filename = join(path,'welcome.html')
        with open(self.filename, "w") as f:
            f.write("<html>\n")
            f.write(" <head>\n")
            f.write("  <style>\n")
            f.write("   body { font-family: Arial, sans-serif; background-color: #1e1e1e; margin: 0; padding: 0; color: #fff; transition: background-color 0.5s ease;}\n")
            f.write("   header { background-color: #2e2e2e; padding: 20px; text-align: center;}")
            f.write("   h1 { color: #fc9421;text-align: center;margin-bottom: 16px;}")
            f.write("   h2 { color: #ffffff;text-align: center;margin-bottom: 16px; padding: 8px;border-radius: 4px;}")
            f.write("   p { margin-bottom: 16px; color: #ccc;}")
            f.write("   a { color: #0099cc; text-decoration: none;}")
            f.write("   button { padding: 8px; margin-bottom: 16px; border: 1px solid #555555; border-radius: 4px; font-size: 16px; background-color: #333333; color: #ffffff; cursor: pointer;}")
            f.write("   button:hover { background-color: #fc9421;}")
            f.write("   .container {max-width: 85%; margin: 20px auto; background-color: #333; padding: 20px; border-radius: 8px; box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2);}")
            f.write("   .loader-container { position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(30, 30, 30, 1); display: flex; align-items: center; justify-content: center; z-index: 1000; transition: opacity 0.5s ease;}")
            f.write("   .loader { border: 8px solid #333333; border-top: 8px solid #fc9421; border-radius: 50%; width: 50px; height: 50px; animation: spin 1s linear infinite;}")
            f.write("   .loader-container.hidden { opacity: 0; pointer-events: none;}")
            f.write("   @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); }}")
            f.write("   .notification { position: fixed; top: 0; left: 50%; transform: translateX(-50%); background-color: rgba(64, 64, 64, 0.9); border: 1px solid #383838; padding: 10px; box-shadow: 0 4px 8px rgba(255, 255, 255, 0.1); z-index: 1000; transition: top 0.5s ease; backdrop-filter: blur(5px); border-radius: 8px; margin-top: 10px;}")
            f.write("   .notification:hover { background-color: rgba(72, 72, 72, 0.8);}")
            f.write("   .close-btn { position: absolute; top: 5px; right: 10px; cursor: pointer;}")
            f.write("   .noselect { -webkit-user-select: none; /* Chrome, Safari, Opera */ -moz-user-select: none; /* Firefox */ -ms-user-select: none; /* IE/Edge */ user-select: none;}")
            f.write("  </style>\n")
            f.write(" </head>\n")
            f.write(" <body>\n")
            f.write("  <div class='loader-container'><div class='loader'></div></div>\n")
            f.write("  <div class='container'>\n")
            f.write("   <h1>Bienvenido a TaskHub</h1>\n")
            f.write("   <h2>Creditos:</h2>\n")
            f.write("   <p>Servidor Flask: Jotalea<p>\n")
            f.write("   <p>Front-end: Jotalea<p>\n")
            f.write("   <p>Back-end: Jotalea<p>\n")
            f.write("   <p>Aplicacion de escritorio: Jotalea<p>\n")
            f.write("   <p>App de Android: Jotalea, basado en el código de Android for Python. <a href='https://github.com/Android-for-Python/Webview-Example'>Ver código fuente original en GitHub</a><p>\n")
            f.write("  </div>\n")
            f.write(" <script>document.addEventListener('DOMContentLoaded', function () { setTimeout(function () { const loaderContainer = document.querySelector('.loader-container'); loaderContainer.classList.add('hidden'); document.body.style.overflow = 'auto';}, 2000);});</script>\n")
            f.write(" <script>function compartir(taskID, materia) { const pageUrl = 'https://taskhub.jotaleaex.repl.co/tarea/' + taskID; const title = 'Tarea de ' + materia; const textToCopy = 'Respuestas de la tarea de ' + materia + ' en TaskHub'; if (navigator.share) { navigator.share({ title: title, text: textToCopy, url: pageUrl }) .then(() => console.log('Este pibe se sabe la de compartir')) .catch((error) => console.error('Error al compartir:', error)); } else { const textToCopy = 'Respuestas de la tarea de ' + materia + ' en TaskHub\n' + pageUrl; copyTextToClipboard(textToCopy); showNotification('Enlace copiado en el portapapeles'); } }</script>\n")
            f.write(" <script>function copyTextToClipboard(text) {navigator.clipboard.writeText(text).then(() => console.log('Text copied: ' + text)).catch((err) => console.error('Error copying to clipboard: ', err));}</script>\n")
            f.write(" </body>\n")
            f.write("</html>\n")

BrowserApp().run()