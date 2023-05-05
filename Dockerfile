FROM python:3.11
EXPOSE 5000
#va a trabajar en el puerto 5000 y lo va abrir
WORKDIR /app
#aca mueve la carpeta de la aplicacion#
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
#va a crear todo el conteindo  de la app local en el workdir
CMD ["flask", "run","--host", "0.0.0.0"]
#el 0.0.0.0 permite que un externo haga peticiones