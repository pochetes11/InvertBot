# InvertBot

/bot
    __init__.py           # Este módulo está vacío por ahora.
    main.py               # Archivo principal donde se inicializa el bot y se gestionan los comandos.

/db
    __init__.py           # Este módulo está vacío por ahora.
    script_para_crear_la_base_de_datos.sql  # Contiene el script SQL para crear las tablas.
    script_para_inicializar_base_de_datos.py  # Este archivo ejecuta el script SQL para crear las tablas.
    db.py                 # Este archivo maneja las operaciones con la base de datos.

/perfil_de_inversor
    __init__.py           # Este módulo está vacío por ahora.
    determinar_perfil_inversor.py   # Este archivo contiene la lógica para determinar el perfil del inversor.
    obetener_perfil_inversor.py    # Este archivo maneja la lógica para obtener el perfil de un inversor.
    
/opciones
    __init__.py           # Este módulo está vacío por ahora.
    obtener_opciones_inversion.py      # Este archivo maneja las opciones de inversión disponibles.
    obtener_opciones_de_inversion_de_acuerdo_al_perfil_del_inversor.py    # Este archivo maneja la lógica para obtener opciones de inversión basadas en el perfil del inversor.

Comando para iniciar: pipenv run bot

siempre fijarse que el pipenv este instalado con pipenv --version