from datetime import datetime
from app import db
#from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List, Optional


# Modelo Pessoa
class Pessoa(db.Model):
    id: Mapped[int] = mapped_column(db.Integer, primary_key=True)
    nome: Mapped[str] = mapped_column(db.String(255))
    tem_acesso : Mapped[bool] = mapped_column(db.Boolean)
    # lado Many da relacao one-to-many
    imagens : Mapped[List["Imagem"]] = relationship(back_populates="pessoa")
    eventos : Mapped[List["Evento"]] = relationship(back_populates="pessoa")

    def __repr__(self) -> str:
        return f"Pessoa(id={self.id!r}, nome={self.nome!r}, tem_acesso={self.tem_acesso!r})"


# Modelo Imagem
class Imagem(db.Model):
    #__tablename__ = "imagem"
    id_img: Mapped[int] = mapped_column(db.Integer, primary_key=True)
    #id_img = db.Column(db.Integer, primary_key=True)
    timestamp: Mapped[datetime] = mapped_column(db.DateTime, default=datetime.utcnow)
    photo_path: Mapped[str] = mapped_column(db.String(255)) #Guarda o caminho para salvar
    pessoa_id = mapped_column(db.ForeignKey("pessoa.id")) #Chave estrangeira
    # lado One da relacao one-to-many
    pessoa : Mapped["Pessoa"] = relationship(back_populates="imagens")
    # lado One da relacao one-to-one uma imagem esta em um evento apenas ja que foi tirada em teoria uma unica
    evento : Mapped["Evento"] = relationship(back_populates="imagem")
    
    def __repr__(self) -> str:
        return f"Imagem(id_img={self.id_img!r}, timestamp={self.timestamp!r}, photo_path={self.photo_path!r})"
    


class Evento(db.Model):
    id_evento: Mapped[int] = mapped_column(db.Integer, primary_key=True)
    data: Mapped[datetime] = mapped_column(db.DateTime, default=datetime.utcnow) 
    #nome_pessoa = db.Column(db.String(255)) # Pode ser obtido da tabela Pessoa
    descricao: Mapped[Optional[str]] = mapped_column(db.String)

    # evento tem uma pessoa associada
    pessoa_id = mapped_column(db.ForeignKey("pessoa.id")) #Chave estrangeira
    pessoa : Mapped["Pessoa"] = relationship(back_populates="eventos")

    # evento tem uma imagem associada
    imagem_id = mapped_column(db.ForeignKey("imagem.id_img")) #Chave estrangeira
    imagem : Mapped["Imagem"] = relationship(back_populates="evento")

    def __repr__(self) -> str:
        return f"Evento(id_evento={self.id_evento!r}, data={self.data!r}, descricao={self.descricao!r})"

