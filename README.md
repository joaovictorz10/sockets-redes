# Sockets TCP/IP

Implementação e testes de programação em sockets utilizando os protocolos UDP, TCP e TCP Concorrente (Multithread).

---

**Aluno:** João Victor Russo Marquito  
**Curso:** Engenharia de Software  
**Disciplina:** Redes de Computadores 3  
**Professor:** Marco Aurelio de Souza Birchal  

---

## 📋 Conteúdo

- **UDPServer.py** – Servidor UDP que converte mensagens para maiúsculas
- **UDPClient.py** – Cliente UDP que envia mensagens e recebe respostas
- **TCPServer.py** – Servidor TCP sequencial (um cliente por vez)
- **TCPClient.py** – Cliente TCP que se conecta ao servidor
- **TCPConcurrentServer.py** – Servidor TCP com múltiplas threads (atende vários clientes)
- **TCPConcurrentClient.py** – Cliente TCP que se conecta ao servidor concorrente
- **relatorioSockets** – Relatório completo com todas as informações.

## 🚀 Como Executar

### UDP

**Terminal 1 (Servidor):**
```bash
py UDPServer.py
```

**Terminal 2 (Cliente):**
```bash
py UDPClient.py
```
Digite uma frase em minúsculas e pressione Enter. O servidor retorna em maiúsculas.

### TCP

**Terminal 1 (Servidor):**
```bash
py TCPServer.py
```

**Terminal 2 (Cliente):**
```bash
py TCPClient.py
```
Digite uma frase e pressione Enter. O servidor retorna em maiúsculas.

### TCP Concorrente

**Terminal 1 (Servidor):**
```bash
py TCPConcurrentServer.py
```

**Terminal 2+ (Múltiplos Clientes – abra quantos quiser):**
```bash
py TCPConcurrentClient.py
```
Digite mensagens. Pressione CTRL+C para sair.

## 📝 Características

| Protocolo | Conexão | Confiabilidade | Múltiplos Clientes | Porta |
|-----------|---------|----------------|-------------------|-------|
| UDP | Não | Não garantida | Sim (sem estado) | 12000 |
| TCP | Sim | Garantida | Não (sequencial) | 12000 |
| TCP Concorrente | Sim | Garantida | Sim (threads) | 50000 |

## 📖 Referência

Baseado no slide: **REDES3_ES_TCP_Sockets_Parte2.pdf**

Disciplina: Redes de Computadores 3
