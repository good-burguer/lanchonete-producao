# Lanchonete – Produção

Este repositório representa o **ambiente de Produção** do projeto **Good Burguer**, desenvolvido como parte do **Tech Challenge – Fase 4 (FIAP SOAT)**.

Ele consolida os padrões finais de **CI/CD, qualidade de código, testes automatizados, cobertura e análise estática (SonarCloud)** aplicados aos serviços do ecossistema.

---

## 🎯 Objetivo do Repositório

- Centralizar a configuração de **deploy em Produção**
- Garantir **paridade total** com os pipelines de Dev/Homologação
- Aplicar **quality gates obrigatórios** antes de qualquer deploy
- Servir como **referência final de entrega** do projeto

---

## 🧱 Padrões Técnicos Adotados

- **Python 3.12**
- **FastAPI**
- **Pytest + Pytest-Cov**
- **Coverage via `coverage.xml`**
- **SonarCloud (Quality Gate ativo)**
- **GitHub Actions (CI / CD)**
- **Kubernetes (EKS)**
- **Clean / Hexagonal Architecture**

---

## 🔄 Pipeline de CI (Integração Contínua)

O pipeline de CI executa obrigatoriamente:

1. Checkout do código (`fetch-depth: 0` para SCM/Sonar)
2. Instalação de dependências
3. Execução de testes automatizados
4. Geração do relatório de cobertura (`coverage.xml`)
5. Análise de qualidade com **SonarCloud**

📌 O pipeline **falha automaticamente** se:
- Os testes falharem
- O arquivo `coverage.xml` não for gerado
- O Quality Gate do SonarCloud reprovar

---

## 🚀 Pipeline de CD (Entrega Contínua – Produção)

O pipeline de CD é acionado **somente após CI bem-sucedido** e realiza:

- Build da imagem Docker
- Push para o repositório de imagens
- Deploy no cluster Kubernetes (EKS)
- Atualização controlada do serviço em Produção

⚠️ **Não há bypass de qualidade em Produção.**

---

## 📁 Estrutura do Repositório

```
.
├── k8s/                 # Manifests Kubernetes (Deploy e Service)
├── .github/workflows/   # Pipelines CI e CD
├── pyproject.toml       # Configuração única de testes e coverage
├── sonar-project.properties
└── README.md
```

---

## 🧪 Testes e Cobertura

- Todos os testes são executados via:
  ```bash
  python -m pytest
  ```
- As configurações de coverage são **centralizadas no `pyproject.toml`**
- O arquivo `coverage.xml` é usado pelo SonarCloud para cálculo de cobertura

---

## 🔐 Qualidade e Governança

- Branch `main` protegida
- CI obrigatório para merge
- Quality Gate do SonarCloud ativo
- Padrão replicado em todos os repositórios do ecossistema

---

## 📌 Contexto Acadêmico

Este repositório faz parte da entrega do:

**FIAP – Pós-Tech Software Architecture (SOAT)**  
**Tech Challenge – Fase 4**

O foco desta fase é:
- DevOps
- CI/CD
- Observabilidade
- Qualidade de Software
- Arquitetura aplicada em produção

---

## 👤 Autor

**The Code Crafters**  
FIAP | Pós-Tech Software Architecture