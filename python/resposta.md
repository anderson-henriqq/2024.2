# Relatório: Criando um Servidor TCP Simples em Python

## Informações gerais
- **Aluno**: Anderson Henrique Silva Santos
- **Disciplina**: Sistemas Operacionais (SO)
- **Professor**: [Leonardo A. Minora](https://github.com/leonardo-minora)
- **Instituição**: Instituto Federal do Rio Grande do Norte (IFRN) - Campus Natal-Central
---

## 1. Servidor HTTP sem thread

O código apresentado cria um servidor HTTP simples sem uso de threads. Isso significa que ele trata cada requisição de forma sequencial, atendendo uma por vez. Esse comportamento pode impactar o desempenho quando há múltiplas requisições simultâneas.

---

## 2. Experimento 1 - Uso de Threads no Servidor

### 2.1 Testes com o Servidor Sem Threads

#### Passos executados:
1. Iniciar o servidor HTTP **sem thread**.
2. Executar o cliente para os seguintes casos:
   - Apenas 1 cliente.
   - 2 clientes simultâneos.
   - 5 clientes simultâneos.
   - 10 clientes simultâneos.
3. Observar o comportamento do servidor e dos clientes.

#### Resultados:
| Número de Clientes | Comportamento Observado |
|--------------------|------------------------|
| **1 Cliente**  | Respondeu rapidamente. |
| **2 Clientes**  | O segundo cliente aguardou até que o primeiro fosse atendido. |
| **5 Clientes**  | Os clientes foram atendidos um por um, gerando fila de espera. |
| **10 Clientes** | Houve demora significativa na resposta, pois o servidor trata um cliente por vez. |

**Conclusão:**  
O servidor sem threads apresenta gargalo de desempenho, pois as requisições são tratadas sequencialmente, resultando em atrasos quando há muitos clientes.

---

### 2.2 Testes com o Servidor Com Threads

#### Passos executados:
1. Parar o servidor sem threads.
2. Iniciar o servidor **com threads**.
3. Executar o cliente para os mesmos casos:
   - Apenas 1 cliente.
   - 2 clientes simultâneos.
   - 5 clientes simultâneos.
   - 10 clientes simultâneos.
4. Observar o comportamento do servidor e dos clientes.

#### Resultados:
| Número de Clientes | Comportamento Observado |
|--------------------|------------------------|
| **1 Cliente**  | Respondeu rapidamente. |
| **2 Clientes**  | Ambos foram atendidos simultaneamente, sem espera. |
| **5 Clientes**  | Todos foram atendidos ao mesmo tempo, sem formação de fila. |
| **10 Clientes** | O servidor respondeu a todas as requisições simultaneamente, com boa performance. |

**Conclusão:**  
O uso de threads permite que múltiplas conexões sejam atendidas ao mesmo tempo, melhorando o desempenho do servidor.

---

### 2.3 Comparação entre Servidor Sem Threads e Com Threads

| Característica  | Servidor Sem Threads | Servidor Com Threads |
|---------------|---------------------|---------------------|
| **Paralelismo**  | Não há | Sim, múltiplas conexões simultâneas |
| **Desempenho**  | Baixo para muitos clientes | Alto para múltiplos clientes |
| **Latência**  | Alta quando há muitos clientes | Baixa, pois as requisições são paralelas |

**Conclusão Geral:**  
A versão com threads do servidor é claramente superior para aplicações com múltiplos clientes simultâneos. Em um ambiente real, onde há diversas conexões concorrentes, o uso de threads ou modelos assíncronos (como `asyncio`) é essencial para evitar gargalos.


## Referências
- [Documentação do módulo `http.server`](https://docs.python.org/3/library/http.server.html)
- [Documentação do módulo `socketserver`](https://docs.python.org/3/library/socketserver.html)
