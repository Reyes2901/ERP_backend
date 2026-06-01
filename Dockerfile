# 1. Usar la imagen oficial de AWS Lambda para Python 3.11 (o la versión que estés usando)
FROM public.ecr.aws/lambda/python:3.11

# 2. Copiar el archivo de requerimientos al directorio raíz de la Lambda
COPY requirements.txt ${LAMBDA_TASK_ROOT}

# 3. Instalar las dependencias de Python
RUN pip install -r requirements.txt

# 4. Copiar toda tu carpeta "app" al contenedor
COPY ./app ${LAMBDA_TASK_ROOT}/app

# 5. Indicarle a Lambda dónde está el "handler" de Mangum
CMD ["app.main.handler"]