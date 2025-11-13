# backend/__init__.py

# Hacemos que los módulos esenciales estén disponibles directamente bajo 'backend.'
# Esto ayuda a Python a resolver las importaciones como 'from backend import crud'
from . import crud
from . import models
from . import schemas