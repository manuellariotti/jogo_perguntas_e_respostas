import random  # Importa o módulo para realizar operações aleatórias
import tkinter as tk  # Importa o módulo para criar interfaces gráficas
from tkinter import messagebox  # Importa o submódulo para exibir caixas de mensagem

# Declaração das perguntas categorizadas por níveis de dificuldade
eventos = {
    1: {  # Dificuldade nível 1
        "Qual é a palavra reservada para: \n Representar o valor booleano falso.": "False",
        "Qual é a palavra reservada para: \n Representar a ausência de valor ou um valor nulo.": "None",
        "Qual é a palavra reservada para: \n Operador lógico que retorna verdadeiro se ambos os operandos forem verdadeiros.": "and",
        "Qual é a palavra reservada para: \n Ser usado em estruturas condicionais, executar um bloco de código se a condição anterior for falsa.": "else",
        "Qual é a palavra reservada para: \n Usar para definir uma nova função.": "def",
    },
    2: {  # Dificuldade nível 2
        "Qual é a palavra reservada para: \n Interromper o loop mais interno": "break",
        "Qual é a palavra reservada para: \n Usar para definir uma nova classe.": "class",
        "Qual é a palavra reservada para: \n Usar para deletar um objeto.": "del",
        "Qual é a palavra reservada para: \n O operador lógico que inverte o valor booleano.": "not",
        "Qual é a palavra reservada para: \n Criar um comando nulo que não faz nada.": "pass",
    },
    3: {  # Dificuldade nível 3
        "Qual é a palavra reservada para: \n  Usar para retornar um valor de uma função geradora.": "yield",
        "Qual é a palavra reservada para: \n Usar para criar funções anônimas.": "lambda",
        "Qual é a palavra reservada para: \n Declarar que uma variável não é local, mas também não é global.": "nonlocal",
        "Qual é a palavra reservada para: \n Definir um bloco de código que será executado independentemente de uma exceção ter sido levantada ou não.": "finally",
        "Qual é a palavra reservada para: \n Declarar uma função assíncrona.": "async",
    },
}

# Classe principal que gerencia o jogo
class Jogo:
    def __init__(self, master):
        # Inicializa a janela principal
        self.master = master
        self.master.title("Jogo de Perguntas de Python")  # Título da janela
        self.inicio()  # Configura a interface inicial do jogo

    def inicio(self):
        # Limpa a janela para garantir que não haja widgets de sessões anteriores
        for widget in self.master.winfo_children():
            widget.destroy()

        # Exibe a mensagem de boas-vindas
        self.label = tk.Label(
            self.master,
            text="Bem-vindo ao Jogo: \n\n Programação em Python!\n \nAcerte a palavra reservada e mostre seu conhecimento durante o semestre! \n \n Não se esqueça das letras maiúsculas e minúsculas. Boa sorte!",
        )
        self.label.pack(pady=20)

        # Campo para o jogador inserir o número de perguntas que deseja responder
        self.label_perguntas = tk.Label(self.master, text="Quantas perguntas você quer responder?")
        self.label_perguntas.pack(pady=10)

        self.perguntas_entry = tk.Entry(self.master)
        self.perguntas_entry.pack(pady=10)

        # Botão para iniciar o jogo
        self.iniciar_button = tk.Button(self.master, text="Iniciar Jogo", command=self.selecionar_dificuldade)
        self.iniciar_button.pack(pady=10)

        # Botão para sair do jogo
        self.sair_button = tk.Button(self.master, text="Sair", command=self.master.quit)
        self.sair_button.pack(pady=10)

    def selecionar_dificuldade(self):
        try:
            # Obtém o número de perguntas que o jogador deseja responder
            self.num_perguntas = int(self.perguntas_entry.get())
            if self.num_perguntas <= 0:  # Verifica se o número é válido
                raise ValueError("Por favor, insira um número maior que zero.")

            # Limpa a janela e solicita ao jogador que escolha o nível de dificuldade
            for widget in self.master.winfo_children():
                widget.destroy()

            self.label = tk.Label(self.master, text="Escolha o nível de dificuldade (1-3):")
            self.label.pack(pady=30)

            self.dificuldade_entry = tk.Entry(self.master)
            self.dificuldade_entry.pack(pady=20)

            self.enviar_button = tk.Button(self.master, text="Enviar", command=self.iniciar_jogo)
            self.enviar_button.pack(pady=20)

        except ValueError as e:
            # Mostra uma mensagem de erro em caso de entrada inválida
            messagebox.showerror("Erro", str(e))

    def iniciar_jogo(self):
        try:
            # Obtém e valida o nível de dificuldade escolhido
            self.dificuldade = int(self.dificuldade_entry.get())
            if self.dificuldade not in [1, 2, 3]:
                raise ValueError("Dificuldade inválida!")

            # Configura o contador de perguntas respondidas e inicia a primeira pergunta
            self.perguntas_respondidas = 0
            self.fazer_pergunta()

        except ValueError as e:
            # Mostra uma mensagem de erro em caso de entrada inválida
            messagebox.showerror("Erro", str(e))

    def fazer_pergunta(self):
        # Verifica se todas as perguntas foram respondidas
        if self.perguntas_respondidas >= self.num_perguntas:
            # Exibe mensagem de finalização e retorna à tela inicial
            messagebox.showinfo("Fim de Jogo", "Você respondeu todas as perguntas! Obrigado por jogar!")
            self.inicio()
            return

        # Escolhe uma pergunta aleatória com base na dificuldade selecionada
        self.evento, self.data_certa = self.escolher_evento(self.dificuldade)
        self.tentativas = 3  # Define o número inicial de tentativas

        # Limpa a tela e exibe a nova pergunta
        for widget in self.master.winfo_children():
            widget.destroy()

        self.label = tk.Label(self.master, text=f"Pergunta: {self.evento}")
        self.label.pack(pady=20)

        self.mensagem = tk.Label(self.master, text=f"Tentativas restantes: {self.tentativas}")
        self.mensagem.pack(pady=20)

        self.resposta_entry = tk.Entry(self.master)
        self.resposta_entry.pack(pady=10)

        self.checar_button = tk.Button(self.master, text="Checar Resposta", command=self.checar_resposta)
        self.checar_button.pack(pady=10)

    def checar_resposta(self):
        # Obtém a resposta do jogador e verifica se está correta
        tentativa_usuario = self.resposta_entry.get()
        if tentativa_usuario == self.data_certa:
            # Exibe mensagem de sucesso, atualiza o contador e passa para a próxima pergunta
            messagebox.showinfo("Resultado", "Parabéns! Você acertou!")
            self.perguntas_respondidas += 1
            self.fazer_pergunta()
        else:
            # Reduz o número de tentativas em caso de erro
            self.tentativas -= 1
            if self.tentativas > 0:
                # Exibe mensagem informando o número de tentativas restantes
                self.mensagem.config(text=f"Errou! Você ainda tem {self.tentativas} tentativas.")
                self.resposta_entry.delete(0, tk.END)  # Limpa o campo de entrada para nova tentativa
            else:
                # Exibe a resposta correta e passa para a próxima pergunta
                messagebox.showinfo("Resultado", f"Você perdeu! A resposta correta era {self.data_certa}.")
                self.perguntas_respondidas += 1
                self.fazer_pergunta()

    def escolher_evento(self, dificuldade):
        # Escolhe uma pergunta aleatória da lista de eventos com base na dificuldade
        evento = random.choice(list(eventos[dificuldade].items()))
        return evento[0], evento[1]  # Retorna a pergunta e a resposta correta

# Código principal para inicializar a interface gráfica
if __name__ == "__main__":
    root = tk.Tk()  # Cria a janela principal do Tkinter
    jogo = Jogo(root)  # Inicializa o jogo com a janela principal
    root.mainloop()  # Inicia o loop principal do Tkinter para manter a janela aberta
