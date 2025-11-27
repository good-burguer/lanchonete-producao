Feature: Gestão de Produtos
  Como um sistema de controle de produtos
  Quero permitir criar, buscar, listar, atualizar e deletar produtos
  Para garantir o funcionamento correto da API de produtos

  # ---------------------------------------------------------
  # CENÁRIO: Criar Produto
  # ---------------------------------------------------------
  Scenario: Criar um novo produto com sucesso
    Given que eu possuo dados válidos de um produto
    When eu envio uma requisição POST para "/produtos/"
    Then o sistema deve retornar status 201
    And o corpo deve conter os dados do produto criado

  Scenario: Falha ao criar produto por erro de integridade
    Given que eu envio dados inválidos para criação de produto
    When eu envio uma requisição POST para "/produtos/"
    Then o sistema deve retornar status 400
    And a mensagem deve ser "Erro de integridade ao criar o produto"

  # ---------------------------------------------------------
  # CENÁRIO: Listar Produtos
  # ---------------------------------------------------------
  Scenario: Listar todos os produtos com sucesso
    When eu envio uma requisição GET para "/produtos/"
    Then o sistema deve retornar status 200
    And deve retornar uma lista de produtos

  Scenario: Erro inesperado ao listar produtos
    Given que ocorre um erro ao listar produtos
    When eu envio uma requisição GET para "/produtos/"
    Then o sistema deve retornar status 400
    And a mensagem deve ser "Erro de integridade ao buscar os produtos"

  Scenario: Listar produtos por categoria
    Given que existe uma categoria de produtos com ID 2
    When eu envio uma requisição GET para "/produtos/categoria/2"
    Then o sistema deve retornar status 200
    And deve retornar os produtos da categoria

  Scenario: Erro inesperado ao listar produtos por categoria
    Given que ocorre um erro ao buscar produtos da categoria 5
    When eu envio uma requisição GET para "/produtos/categoria/5"
    Then o sistema deve retornar status 400
    And a mensagem deve ser "Erro de integridade ao buscar o produto"

  # ---------------------------------------------------------
  # CENÁRIO: Buscar Produto por ID
  # ---------------------------------------------------------
  Scenario: Buscar produto existente por ID
    Given que existe um produto com ID 1
    When eu envio uma requisição GET para "/produtos/1"
    Then o sistema deve retornar status 200
    And os dados do produto devem ser retornados

  Scenario: Produto não encontrado ao buscar por ID
    Given que não existe produto com ID 999
    When eu envio uma requisição GET para "/produtos/999"
    Then o sistema deve retornar status 404
    And a mensagem deve ser "Produto não encontrado"

  Scenario: Erro inesperado ao buscar produto por ID
    Given que ocorre um erro ao consultar o produto com ID 10
    When eu envio uma requisição GET para "/produtos/10"
    Then o sistema deve retornar status 400
    And a mensagem deve ser "Erro de integridade ao buscar o produto"

  # ---------------------------------------------------------
  # CENÁRIO: Atualizar Produto
  # ---------------------------------------------------------
  Scenario: Atualizar produto com sucesso
    Given que existe um produto com ID 5
    And que eu forneço dados válidos para atualização
    When eu envio uma requisição PUT para "/produtos/5"
    Then o sistema deve retornar status 200
    And retornar os dados atualizados do produto

  Scenario: Produto não encontrado ao atualizar
    Given que não existe produto com ID 777
    When eu envio uma requisição PUT para "/produtos/777"
    Then o sistema deve retornar status 404
    And a mensagem deve ser "Produto não encontrado"

  Scenario: Erro ao atualizar produto por integridade
    Given que envio dados inválidos ao atualizar o produto 5
    When eu envio uma requisição PUT para "/produtos/5"
    Then o sistema deve retornar status 400
    And a mensagem deve ser "Erro de integridade ao atualizar o produto"

  # ---------------------------------------------------------
  # CENÁRIO: Deletar Produto
  # ---------------------------------------------------------
  Scenario: Deletar produto com sucesso
    Given que existe um produto com ID 3
    When eu envio uma requisição DELETE para "/produtos/3"
    Then o sistema deve retornar status 204

  Scenario: Produto não encontrado ao deletar
    Given que não existe produto com ID 999
    When eu envio uma requisição DELETE para "/produtos/999"
    Then o sistema deve retornar status 404
    And a mensagem deve ser "Produto não encontrado"

  Scenario: Erro inesperado ao deletar produto
    Given que ocorre um erro ao deletar o produto de ID 10
    When eu envio uma requisição DELETE para "/produtos/10"
    Then o sistema deve retornar status 400
    And a mensagem deve ser "Erro de integridade ao remover o produto"
