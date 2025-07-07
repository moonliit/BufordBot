# BufordBot
## Integrantes
- Alejandro Joel Ore Garcia
- Iam André Salvador Cucho Jordán
- Jose Guillermo Gálvez Pacori
- Héctor Sebastian Nieto Paz

## Comandos

El grupo de comandos principales es el `!prediction`:

- `!prediction debug (on/off)`: Activa/Desactiva el modo debug. Para ver resultados clasificados como 'not_cyberbullying'.
- `!prediction model (bert/tf_idf)`: Cambia el modelo a 'bert' o a 'tf_idf' respectivamente.

Esta información también es obtenible mediante el comando `!help`.

## Ejecución

Primero, se debe clonar el repo. Para ello, se necesita tener instalado **Git LFS**, puesto a que el modelo de BERT está almacenado en el Large File Storage de GitHub, y no se puede acceder de otra forma.

Más info en: https://docs.github.com/en/repositories/working-with-files/managing-large-files/installing-git-large-file-storage


Para ejecutar al bot, se necesita del archivo `.env` (se hablará de eso después) y de las librerías:

```
pip install -r requirements.txt
```

Y luego ejecutarlo como:

```
python3 main.py
```

Alternativamente, se puede ejecutar con Docker:

```
docker build -t bufordbot .
docker run bufordbot
```

## .env

Se requiere de un archivo `.env` para poder ejecutar al bot. El archivo debe tener la siguiente estructura:

```bash
IS_DEBUG = "true" #true activa el modo debug

# Discord Token
DISCORD_TOKEN = "(inserte token de discord aqui)" # este se consigue en el Discord Developer Portal
```

El modo "debug" cambia el funcionamiento del módulo Debug. De momento este no ha sido utilizado para el proyecto, pero de ser necesario está listo para ser usado.

## Contributing

Open Source, licencia GPL3

Más información en `CONTRIBUTING.md`