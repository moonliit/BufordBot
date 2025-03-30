# csl chan bot
### aceptenme en la org de csl plssss

---

## rust dataclasses and enums

el bot mismo me demoro como 30 min max en hacer

lo que mas me demoro es intentar hacer q los rust-like datatypes funcionen ( me torture mucho para hacer esto pero oh well 
¯\\\_(ツ)_/¯ )

funcionan lo suficientemente bien:

(ejemplo en `utlity.debug`)
```python
Debug._is_debug = \
    EnvLoader.get("IS_DEBUG").\ # EnvLoader.get() returns an option
    map(bool)(lambda s: s.lower() == "true").\
    unwrap_or_else(False)
```

---

## utility classes

quiero intentar abstraer y generalizar cosas para q sea mas piola. `utlity` sirve para clases y funciones q son mas q nada de uso general por sobre datatypes (generalmente son estaticas o tienen alguna cosa tipo singleton)

por ejemplo, tenemos `utlity.debug` para imprimir y/o lanzar excepciones (tipo rust, usamos panic). su funcionamiento depende de una variable de entorno q estara mas abajo

```python
from utility.debug import Debug

Debug.log("message") # will only print if debug is enabled
Debug.panic("err") # will only shutdown program if debug is enabled

```

y luego el otro solo es por conveniencia. una clase q lee variables de entorno (`utility.env_loader`):

```python
from utility.env_loader import EnvLoader

# returns an option with Some(content) or Empty()
EnvLoader.get("ENV_VAR")
```

--

## .env

de momento el .env se ve asi:

```bash
IS_DEBUG = "true" #true activa el modo debug

# Discord Token
DISCORD_TOKEN = "(inserte token de discord aqui)"
```

---

## contributing

open source, licencia gpl3

añadan cogs para q csl chan pueda hablar xd

mas info en `CONTRIBUTING.md`