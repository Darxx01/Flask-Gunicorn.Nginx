from flask import Flask, render_template, request
import redis

app = Flask(__name__)
app.config['DEBUG'] = True
r = redis.Redis(host='redis', port=6379, db=0)

@app.route('/',methods=['GET','POST'])
def index():
  data = {}
  if request.method == 'POST':
    r.set(request.form['nombre'], request.form['significado'])
    data['mensaje'] = "Palabra ingresada"
  data['palabras'] = obtenerPalabras()
  return render_template('index.html',data=data)

@app.route('/eliminar/<nombre>',methods=['GET'])
def eliminar(nombre):
  r.delete(nombre)
  data = {'mensaje': 'Palabra eliminada'}
  data['palabras'] = obtenerPalabras()
  return render_template('index.html',data=data)

@app.route('/editar/<nombre>', methods=['GET'])
def editar(nombre):
  data = {'palabra':{'significado':r.get(nombre).decode('UTF-8'),'nombre':nombre}}
  data['palabras'] = obtenerPalabras()
  return render_template('index.html',data=data)

@app.route('/editar/<nombre>', methods=['POST'])
def editar2(nombre):
  r.set(nombre, request.form['significado'])
  data = {'mensaje':'Palabra editada'}
  data['palabras'] = obtenerPalabras()
  return render_template('index.html',data=data)

def obtenerPalabras():
  palabras = []
  for i in r.keys():
    palabras.append({
      'nombre': i.decode("UTF-8"),
      'significado': r.get(i).decode('UTF-8')
    })
  return palabras

if __name__ == "__main__":
  app.run(host='0.0.0.0', debug=True)
