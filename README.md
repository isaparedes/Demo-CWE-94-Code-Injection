# DEMO de SQL Injection

## Requisitos

```bash
pip install flask
```

## Demos

- `VulnerableLogin.py` - login con la vulnerabilidad
- `FixedLogin.py` - login con la vulnerabilidad arreglada

## Pasos para reproducir la vulnerabilidad

1. **Correr la demo**

```bash
python VulnerableLogin.py
```

2. Abrir `http://127.0.0.1:5000/`

3. Iniciar sesion con el usuario 'admin' y contraseña '1234'
4. Iniciar sesion de nuevo pero en el input del usuario ingresa `' or True or '`
5. Ver como se puede iniciar sesion sin tener las credenciales requeridas
