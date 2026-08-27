# DEMO de CWE-94 'Code Injection'

## Demos

- `VulnerableLogin.py` - login con la vulnerabilidad
- `FixedLogin.py` - login con la vulnerabilidad arreglada

## Ejecución local

### Requisitos

Tener Python instalado y ejecutar:

```bash
pip install flask
```

### Pasos para ejecutar la demo

1. Correr la versión vulnerable:

```bash
python VulnerableLogin.py
```

2. Abrir `http://127.0.0.1:5000/` en el navegador.

3. Realizar las pruebas indicadas en: [Pasos para reproducir las vulnerabilidades](#pasos-para-reproducir-las-vulnerabilidades).

## Ejecución con Docker

### Requisitos

Tener Docker instalado.

### Pasos para ejecutar la demo

1. Ejecutar el siguiente comando en la terminal:

```bash
docker compose up --build
```

2. Abrir `http://127.0.0.1:5000/` en el navegador para acceder a la versión vulnerable.

3. Abrir `http://127.0.0.1:5001/` en el navegador para acceder a la versión corregida.

## Pasos para reproducir las vulnerabilidades

Los siguientes casos deben realizarse utilizando la versión vulnerable (`VulnerableLogin.py`).

1. Abrir `http://127.0.0.1:5000/` en el navegador.

### Vulnerabilidad 1 - Iniciar sesión como usuario sin ninguna credencial

1. En el campo **Usuario**, ingresar:

```text
x') or True or ('x
```

2. En el campo **Contraseña** ingresar cualquier valor o no ingresar nada.

3. Presionar **Ingresar**.

4. Se puede observar que la aplicación permite iniciar sesión sin proporcionar un usuario y una contraseña válidos.

Esto ocurre porque los datos ingresados por el usuario se incorporan directamente a una expresión de Python que posteriormente es ejecutada mediante `eval()`.

### Vulnerabilidad 2 - Iniciar sesión como Juan sin conocer su contraseña

1. En el campo **Usuario** ingresar:

```text
juan
```

2. En el campo **Contraseña** ingresar:

```text
' or True or '
```

3. Presionar **Ingresar**.

4. Se puede observar que la aplicación permite iniciar sesión como `juan` sin conocer su contraseña real (`juan1234`).

La entrada introducida en el campo de contraseña modifica la expresión que genera la aplicación y hace que `eval()` la evalúe como verdadera.

### Vulnerabilidad 3 - Iniciar sesión como administrador sin conocer su contraseña

1. En el campo **Usuario**, ingresar:

```text
admin
```

2. En el campo **Contraseña**, ingresar:

```text
' or True or '
```

3. Presionar **Ingresar**.

4. Se puede observar que la aplicación acepta la autenticación sin conocer la contraseña real del administrador (`1234`).

5. La aplicación redirige al **Panel de administración**, que debería estar protegido y disponible únicamente para el usuario administrador.

Esto demuestra que la vulnerabilidad puede permitir el acceso a funcionalidades protegidas sin conocer las credenciales reales del usuario.

## Comprobación de la versión corregida

Para comprobar que la vulnerabilidad fue solucionada, se deben repetir las mismas pruebas utilizando `FixedLogin.py`.

### Ejecución local

1. Detener la versión vulnerable o abrir una nueva terminal.

2. Ejecutar:

```bash
python FixedLogin.py
```

**Ejecución local o con Docker**: Abrir `http://127.0.0.1:5001/` en el navegador.

### Prueba de las entradas utilizadas anteriormente

1. Repetir la **Vulnerabilidad 1** utilizando:

```text
Usuario: x') or True or ('x
Contraseña: cualquier valor (o vacío)
```

2. La aplicación debe rechazar las credenciales y mostrar:

```text
Usuario o contraseña incorrectos
```

3. Repetir la **Vulnerabilidad 2** utilizando:

```text
Usuario: juan
Contraseña: ' or True or '
```

4. La aplicación debe rechazar las credenciales y mostrar:

```text
Usuario o contraseña incorrectos
```

5. Repetir la **Vulnerabilidad 3** utilizando:

```text
Usuario: admin
Contraseña: ' or True or '
```

6. La aplicación debe rechazar las credenciales y no permitir el acceso al panel de administración.

### Inicio de sesión válido

Para comprobar que el login funciona correctamente:

1. En el campo **Usuario**, ingresar:

```text
admin
```

2. En el campo **Contraseña**, ingresar:

```text
1234
```

3. Presionar **Ingresar**.

4. La aplicación permite el acceso y redirige al **Panel de administración**.

## Comparación entre ambas versiones

La diferencia entre ambas versiones se encuentra en la forma en que se procesan los datos introducidos por el usuario.

### Versión vulnerable

La aplicación construye una expresión de Python utilizando los datos introducidos por el usuario:

```python
condition = f"users.get('{username}') == '{password}'"
```

Luego esta expresión se ejecuta mediante:

```python
authenticated = eval(condition)
```

Esto permite que los datos introducidos por el usuario puedan modificar el código que será interpretado por la aplicación.

### Versión corregida

La aplicación realiza una comparación directa entre el usuario y la contraseña:

```python
authenticated = users.get(username) == password
```

Los datos introducidos por el usuario se tratan como datos y no como código ejecutable.

Por lo tanto, las entradas utilizadas en las pruebas de la versión vulnerable no permiten modificar la lógica de autenticación en la versión corregida.

Esta versión es segura frente a vulnerabilidades de Code Injection (CWE-94).

### Fuentes

1. CWE - CWE-94: Improper control of Generation of Code ('Code Injection’) (4.20). (n.d.). https://cwe.mitre.org/data/definitions/94.html

2. Documentación de Flask. https://flask.palletsprojects.com/en/stable/
