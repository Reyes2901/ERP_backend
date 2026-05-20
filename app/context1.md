Proyecto: ERP Mobile Inteligente con IA Local

Objetivo General:
Desarrollar una aplicación móvil ERP para gestión de clientes, inventario, compras y ventas, integrada con un modelo de inteligencia artificial ejecutándose localmente en el dispositivo móvil mediante llama.cpp y modelos GGUF.

La IA debe interpretar lenguaje natural o voz del usuario y convertirlo en JSON estructurado para consumir endpoints del ERP Python mediante HTTP.

La IA NO realiza lógica de negocio.
La lógica principal sigue en el ERP backend.

Arquitectura General:

Usuario
↓
Aplicación Mobile
↓
Modelo IA Local (llama.cpp + GGUF)
↓
Generación JSON estructurado
↓
HTTP Request
↓
ERP Python API
↓
Base de Datos

Tecnologías Principales:

- Flutter (mobile)
- Python FastAPI (ERP backend)
- llama.cpp
- llama-cpp-python
- Modelos GGUF
- GBNF Grammar
- Speech-to-Text (micrófono)

Modelo IA:

Ejemplo:
- Gemma 2B Q4 GGUF
- TinyLlama
- Phi-2

Ejemplo de carga:

from llama_cpp import Llama

llm = Llama.from_pretrained(
  repo_id="bartowski/gemma-2-2b-it-GGUF",
  filename="gemma-2-2b-it-Q4_K_M.gguf",
)

Prompt Engineering:

Archivo:
prompt.txt

Ejemplo:

"Eres un asistente experto en ERP.
Debes responder SOLO JSON válido.
Nunca expliques nada.

Rutas disponibles:
- create.customer
- add.product
- create.purchase
- create.sale"

GBNF:

Objetivo:
Forzar respuestas JSON válidas.

Ejemplo:

root ::= object

object ::= "{" route "," data "}"

route ::= "\"route\"" ":" string
data ::= "\"data\"" ":" object

Funcionalidad General de la App:

La aplicación permitirá:

- escribir instrucciones
- usar voz mediante micrófono
- generar JSON automáticamente
- enviar datos al ERP
- mostrar respuesta del servidor

La app tendrá una barra de navegación inferior con 4 vistas principales:

1. CLIENTES
2. INVENTARIO
3. COMPRAS
4. VENTAS

========================================
VISTA 1: CLIENTES
========================================

Objetivo:
Gestionar clientes usando IA local.

Funciones:
- crear clientes
- buscar clientes
- actualizar datos
- listar clientes

Ejemplo usuario:
"Crea un cliente llamado Juan Pérez"

Respuesta IA:

{
  "route": "create.customer",
  "data": {
    "nombre": "Juan Pérez"
  }
}

Componentes UI:
- título: Gestión de Clientes
- input prompt
- botón micrófono
- botón solicitar
- área JSON
- botón guardar
- historial de operaciones

========================================
VISTA 2: INVENTARIO
========================================

Objetivo:
Administrar productos y stock.

Funciones:
- agregar productos
- actualizar stock
- consultar inventario
- eliminar productos

Ejemplo:
"Agregar 20 Coca Colas"

Respuesta IA:

{
  "route": "add.product",
  "data": {
    "producto": "Coca Cola",
    "cantidad": 20
  }
}

Componentes UI:
- título Inventario
- input texto
- botón micrófono
- botón solicitar
- resultado JSON
- tabla productos
- botón guardar

Tabla:
- producto
- stock
- precio
- estado

========================================
VISTA 3: COMPRAS
========================================

Objetivo:
Registrar compras y proveedores.

Funciones:
- crear compras
- registrar proveedores
- historial compras
- estados de compra

Ejemplo:
"Comprar 30 teclados Logitech"

Respuesta IA:

{
  "route": "create.purchase",
  "data": {
    "producto": "Teclado Logitech",
    "cantidad": 30
  }
}

Componentes UI:
- título Compras
- input IA
- botón micrófono
- resultado JSON
- lista compras
- botón confirmar

Estados:
- pendiente
- aprobada
- recibida

========================================
VISTA 4: VENTAS
========================================

Objetivo:
Gestionar ventas y facturación.

Funciones:
- crear ventas
- buscar cliente
- calcular total
- historial ventas

Ejemplo:
"Vender 2 monitores Samsung a Carlos"

Respuesta IA:

{
  "route": "create.sale",
  "data": {
    "cliente": "Carlos",
    "producto": "Monitor Samsung",
    "cantidad": 2
  }
}

Componentes UI:
- título Ventas
- input IA
- botón micrófono
- resultado JSON
- lista ventas
- botón procesar

Tabla:
- cliente
- producto
- total
- fecha

========================================
MÓDULO IA
========================================

Funciones:
- interpretar lenguaje natural
- convertir voz a texto
- generar JSON
- seleccionar endpoint ERP

La IA trabaja completamente local en el dispositivo móvil.

Solo existe una llamada HTTP:
la llamada al ERP backend.

========================================
FLUJO GENERAL
========================================

Usuario escribe o habla
↓
Speech-to-Text (opcional)
↓
Modelo IA Local
↓
Prompt + GBNF
↓
JSON estructurado
↓
Validación
↓
HTTP POST al ERP
↓
Respuesta servidor
↓
Mostrar resultado

========================================
ESTRUCTURA RECOMENDADA
========================================

mobile_app/

├── models/
│   └── gemma-2b.gguf
│
├── prompts/
│   └── prompt.txt
│
├── grammar/
│   └── erp.gbnf
│
├── screens/
│   ├── customers.dart
│   ├── inventory.dart
│   ├── purchases.dart
│   └── sales.dart
│
├── services/
│   ├── llm_service.dart
│   ├── speech_service.dart
│   └── api_service.dart

========================================
OBJETIVO FINAL
========================================

Crear un ERP móvil inteligente donde la IA local actúe como traductor entre lenguaje humano y endpoints del ERP, usando prompts, GBNF y modelos GGUF ejecutados mediante llama.cpp.