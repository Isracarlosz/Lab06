
from flask import Flask, render_template, request, send_from_directory, url_for
import yt_dlp
import os  

app = Flask(__name__)


DOWNLOAD_FOLDER = 'descargas'

if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

@app.route('/', methods=['GET', 'POST'])
def index():
    """
    Ruta principal que muestra el formulario (GET) 
    y procesa la URL (POST).
    """
    video_info = None
    error = None

    if request.method == 'POST':
        url = request.form['url']
        
        if not url:
            error = "Por favor, ingresa una URL."
        else:
            try:
               
                user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36'
                
            
                ydl_opts = {
                    'outtmpl': f'{DOWNLOAD_FOLDER}/%(id)s.%(ext)s', 
                    

                    'format': 'best[ext=mp4][vcodec^=avc][acodec^=mp4a][height<=1080]/best[ext=mp4][acodec!=none]/best[acodec!=none]/best',
         
                    
                    'quiet': True,
                    'noplaylist': True,
                    
       
                    'http_headers': {
                        'User-Agent': user_agent
                    }
                }

              
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    
                    info = ydl.extract_info(url, download=True) 

                    file_id = info.get('id', '')
               
                    ext = 'mp4' 
                    filename = f"{file_id}.{ext}"
                    
              
                    original_ext = info.get('ext', 'mp4')
                    original_filename = f"{file_id}.{original_ext}"
                    
                   
                    if original_ext != 'mp4':
                        base_path = os.path.join(DOWNLOAD_FOLDER, file_id)
                        try:
                            os.rename(f"{base_path}.{original_ext}", f"{base_path}.mp4")
                        except OSError as e:
                            print(f"No se pudo renombrar el archivo: {e}")
                            pass 

                   
                    thumbnail_url = info.get('thumbnail', '') 
                    thumbnails = info.get('thumbnails', [])
                    if thumbnails:
                        thumbnail_url = thumbnails[-1].get('url', thumbnail_url) 

                    video_info = {
                        'title': info.get('title', 'Título no encontrado'),
                        'thumbnail': thumbnail_url,
                        'filename': filename 
                    }

            except yt_dlp.utils.DownloadError as e:
                print(e)
                error = "Error al procesar la URL. Es posible que el video sea privado o haya sido eliminado."
            except Exception as e:
                print(e)
                error = f"Ocurrió un error inesperado. {e}"


    return render_template('downloader.html', video_info=video_info, error=error)


@app.route('/download/<path:filename>')
def download_file(filename):
    """
    Esta ruta toma el nombre del archivo y se lo envía al usuario
    como una descarga (as_attachment=True).
    """
    return send_from_directory(
        DOWNLOAD_FOLDER, 
        filename, 
        as_attachment=True 
    )

if __name__ == '__main__':
    app.run(debug=True)