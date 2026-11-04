from collections import deque


class MiniGit:
    """Guarda commits e branches e contabiliza o custo de cada operacao."""

    __slots__ = (
        "__pais",
        "__mensagens",
        "__branches",
        "__branch_atual",
        "__proximo_commit",
        "__passos",
    )

    def __init__(self):
        """Inicia um repositorio vazio; a preparacao nao conta como operacao."""
        self.__pais = {}
        self.__mensagens = {}
        self.__branches = {"main": None}
        self.__branch_atual = "main"
        self.__proximo_commit = 1
        self.__passos = 0

    @property
    def passos(self):
        """Informa os passos gastos pela ultima operacao, sem permitir alteracao."""
        return self.__passos

    def commitar(self, mensagem):
        """Cria um commit e move a branch atual, gastando dois passos."""
        self.__passos = 0
        if not mensagem:
            raise ValueError("A mensagem nao pode ser vazia")

        identificador = f"c{self.__proximo_commit}"
        commit_anterior = self.__branches[self.__branch_atual]
        pais_do_commit = []
        if commit_anterior is not None:
            pais_do_commit.append(commit_anterior)

        self.__pais[identificador] = pais_do_commit
        self.__mensagens[identificador] = mensagem
        self.__proximo_commit += 1
        self.__passos += 1
        self.__branches[self.__branch_atual] = identificador
        self.__passos += 1
        return identificador

    def mensagem(self, commit):
        """Busca a mensagem por chave direta no dicionario, gastando um passo."""
        self.__passos = 0
        if commit not in self.__mensagens:
            raise ValueError("Commit inexistente")

        self.__passos = 1
        return self.__mensagens[commit]

    def pais(self, commit):
        """Devolve uma tupla imutavel de pais, consultando o dicionario em um passo."""
        self.__passos = 0
        if commit not in self.__pais:
            raise ValueError("Commit inexistente")

        self.__passos = 1
        return tuple(self.__pais[commit])
