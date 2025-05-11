# 🏪 API de Agendamento de Consultas

Esta API permite o cadastro, autenticação de usuários e o agendamento de consultas médicas. Desenvolvida com Flask, SQLAlchemy, autenticação via JWT e documentação interativa com Flasgger. Ideal para uso didático, projetos pessoais e como base para sistemas maiores.

---

## 🚀 Tecnologias Utilizadas

* 🐍 Python + Flask
* 📂 SQLAlchemy (ORM)
* 🔐 JWT (JSON Web Token)
* 📆 SQLite
* 📘 Flasgger (Swagger UI para documentação)

---

## 📁 Estrutura

```
.
├── app.py               # Arquivo principal com as rotas
├── database.py          # Configuração do banco e modelos
├── scheduling.db        # Banco de dados SQLite
├── requirements.txt     # Dependências do projeto
└── ...
```

---

## 🔑 Autenticação

* O sistema usa JWT.
* Após o login, o token deve ser enviado no header:

  ```
  x-access-token: seu_token
  ```

---

## 👥 Usuários

* Tipos permitidos: `medico`, `paciente`, `dev`

### 📌 Rotas

| Método | Rota      | Descrição                 | Protegida |
| ------ | --------- | ------------------------- | --------- |
| POST   | /register | Registra um novo usuário  | ❌         |
| POST   | /login    | Gera token para o usuário | ❌         |

---

## 🗕️ Consultas

| Método | Rota                         | Descrição                     | Protegida |
| ------ | ---------------------------- | ----------------------------- | --------- |
| GET    | /consultas                   | Lista todas as consultas      | ✅         |
| GET    | /consultas/`<id>`            | Consulta específica por ID    | ✅         |
| GET    | /consultas/paciente/`<nome>` | Consultas de um paciente      | ✅         |
| GET    | /consultas/medico/`<nome>`   | Consultas de um médico        | ✅         |
| POST   | /consultas                   | Cria um novo agendamento      | ✅         |
| PUT    | /consultas/`<id>`            | Edita uma consulta            | ✅         |
| DELETE | /consultas/`<id>`            | Cancela (deleta) uma consulta | ✅         |

---

## 📄 Documentação Interativa

A documentação completa e interativa está disponível após rodar o projeto em:

```
http://localhost:5000/apidocs/
```

![Swagger UI - Flasgger](https://raw.githubusercontent.com/CauanNeves/API-Agendamento-Consultas/main/flasgger.png)

---

## 📦 Como usar

1. Clone o repositório:

   ```bash
   git clone https://github.com/cauanneves/API-AGENDAMENTO-CONSULTAS.git
   cd API-AGENDAMENTO-CONSULTAS
   ```

2. Instale as dependências:

   ```bash
   pip install -r requirements.txt
   ```

3. Inicie o banco de dados:

   ```bash
   python database.py
   ```

4. Execute a API:

   ```bash
   python app.py
   ```

---

## 📬 Exemplo de Registro (JSON)

```json
POST /register
{
  "name": "João da Silva",
  "email": "joao@email.com",
  "password": "senha123",
  "type": "paciente"
}
```

---

## ✍️ Autor

Desenvolvido por **Cauan Neves** 🧠
Conecte-se comigo no [LinkedIn](https://www.linkedin.com/in/cauan-neves)

---

## 📝 Licença

Este projeto está sob a licença MIT. Sinta-se livre para usar e adaptar! 🚀
