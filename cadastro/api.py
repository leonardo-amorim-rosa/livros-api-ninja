from django.forms import model_to_dict
from django.shortcuts import get_object_or_404
from ninja import ModelSchema, NinjaAPI, UploadedFile #, Schema
from .models import Livro

# Schema livre
# class LivroSchema(Schema):
#     titulo: str
#     descricao: str
#     autor: str = None

# Schema baseado em um model
class LivroSchema(ModelSchema):
    class Config:
        model = Livro
        model_fields = ['titulo', 'descricao', 'autor']

api = NinjaAPI()

@api.get('livros/')
def livros(request):
    livros = Livro.objects.all()
    response = [{'id': i.id, 'titulo': i.titulo, 'descricao': i.descricao, 'autor': i.autor} for i in livros]
    return response

@api.get('livro/{id}')
def livro(request, id: int):
    livro = get_object_or_404(Livro, id=id)
    return model_to_dict(livro)

@api.get('livro_consulta')
def livro_consulta(request, id: int = 1):
    livro = get_object_or_404(Livro, id=id)
    return model_to_dict(livro)

# caso precisemos utilizar uma lista de objetos
# podemos fazer como as linhas abaixo
# from typing import List
# lista = Lis[LivroSchema]

@api.post('livros', response=LivroSchema) # utilizando responses tipados (facilta no parser)
def salvar_livro(request, livro: LivroSchema):
    print(livro)
    livro = Livro(**livro.dict())
    livro.save()
    return livro

# upload de arquivos
@api.post('livro_upload')
def file_upload(request, file: UploadedFile):
    print(file.size)
    return file.size