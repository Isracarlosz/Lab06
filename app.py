# app.py
from flask import Flask, render_template, request
import requests

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    pokemon_data = None  
    error = None         
    
    if request.method == 'POST':
       
        pokemon_name = request.form['pokemon_name'].lower().strip()
        
        if not pokemon_name:
            error = "Por favor, ingresa un nombre."
        else:
            
            url = f'https://pokeapi.co/api/v2/pokemon/{pokemon_name}'
            response = requests.get(url)
            
            if response.status_code == 200:
               
                data = response.json()
                
               
                pokemon_data = {
                    'name': data['name'].capitalize(),
                    'types': [t['type']['name'] for t in data['types']],
                    'moves': [m['move']['name'] for m in data['moves']], 
                    'sprites': [
                        data['sprites']['front_default'],
                        data['sprites']['back_default'],
                        data['sprites']['front_shiny'], 
                        data['sprites']['back_shiny']   
                    ]
                }
            else:
                
                error = f"No se pudo encontrar el Pokémon: '{pokemon_name}'"

 
    return render_template('index.html', pokemon=pokemon_data, error=error)

if __name__ == '__main__':
    app.run(debug=True)