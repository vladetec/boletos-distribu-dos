# boletos-distribu-dos
Simples demonstração de um sistema que permita dividir um boleto em parcelas, aplicando uma taxa de juros, e armazenar as parcelas geradas até que o pagamento total seja quitado.

## para rodar o projeto

```shell
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate  # Windows
pip install flask flask-sqlalchemy
```
```python
from app import db
db.create_all()
exit()
```
```shell
python app.py

```
Agora acesse http://127.0.0.1:5000/ no navegador. 🚀


Author: @VladeSouza 😉

Github: https://github.com/vladetec/boletos-distribu-dos

Linkedin: https://www.linkedin.com/in/vlademir-souza-ads

