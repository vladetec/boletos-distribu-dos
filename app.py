from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///boletos.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Modelo de Boleto
class Boleto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    valor_total = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), default="Pendente")
    juros = db.Column(db.Float, default=0.0)
    boleto_pai = db.Column(db.Integer, db.ForeignKey('boleto.id'), nullable=True)
    filhos = db.relationship('Boleto', backref=db.backref('pai', remote_side=[id]), lazy=True)

# Criar banco de dados se não existir
with app.app_context():
    if not os.path.exists("boletos.db"):
        db.create_all()

# Página Inicial
@app.route('/')
def index():
    boletos = Boleto.query.all()
    return render_template('index.html', boletos=boletos)

# Criar Boleto
@app.route('/criar', methods=['POST'])
def criar_boleto():
    valor = float(request.form['valor'])
    novo_boleto = Boleto(valor_total=valor)
    db.session.add(novo_boleto)
    db.session.commit()
    return redirect(url_for('index'))

# Parcelar Boleto
@app.route('/parcelar', methods=['POST'])
def parcelar_boleto():
    boleto_id = int(request.form['boleto_id'])
    num_parcelas = int(request.form['parcelas'])
    juros = float(request.form['juros'])

    boleto = Boleto.query.get(boleto_id)
    if not boleto or boleto.status == "Pago":
        return redirect(url_for('index'))

    valor_parcela = (boleto.valor_total * (1 + juros / 100)) / num_parcelas
    
    for _ in range(num_parcelas):
        nova_parcela = Boleto(valor_total=round(valor_parcela, 2), juros=juros, boleto_pai=boleto.id)
        db.session.add(nova_parcela)

    db.session.commit()
    return redirect(url_for('index'))

# Quitar Boleto
@app.route('/quitar/<int:boleto_id>')
def quitar_boleto(boleto_id):
    boleto = Boleto.query.get(boleto_id)

    if not boleto:
        return redirect(url_for('index'))

    # Verifica se todas as parcelas estão pagas
    def verificar_pagamento(boleto):
        for filho in boleto.filhos:
            if filho.status != "Pago" or not verificar_pagamento(filho):
                return False
        return True

    if verificar_pagamento(boleto):
        boleto.status = "Pago"
        db.session.commit()

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
