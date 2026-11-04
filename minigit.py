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

    def criar_branch(self, nome):
        """Cria um ponteiro para o commit atual, gastando um passo."""
        self.__passos = 0
        if nome in self.__branches:
            raise ValueError("A branch ja existe")
        if self.__branches[self.__branch_atual] is None:
            raise ValueError("Nao ha commits para criar a branch")

        self.__branches[nome] = self.__branches[self.__branch_atual]
        self.__passos = 1

    def trocar_branch(self, nome):
        """Move a referencia da branch atual para outra, gastando um passo."""
        self.__passos = 0
        if nome not in self.__branches:
            raise ValueError("Branch inexistente")

        self.__branch_atual = nome
        self.__passos = 1

    @property
    def branch_atual(self):
        """Informa o nome da branch selecionada sem permitir alteracao."""
        return self.__branch_atual

    def mesclar(self, nome):
        """Cria um commit com dois pais e move a branch, gastando dois passos."""
        self.__passos = 0
        if nome not in self.__branches:
            raise ValueError("Branch inexistente")
        if nome == self.__branch_atual:
            raise ValueError("Nao e possivel mesclar a branch atual")

        identificador = f"c{self.__proximo_commit}"
        pais_do_commit = [
            self.__branches[self.__branch_atual],
            self.__branches[nome],
        ]
        self.__pais[identificador] = pais_do_commit
        self.__mensagens[identificador] = f"merge de {nome}"
        self.__proximo_commit += 1
        self.__passos += 1
        self.__branches[self.__branch_atual] = identificador
        self.__passos += 1
        return identificador

    def log(self):
        """Percorre os pais em largura com uma fila e conta cada commit uma vez."""
        self.__passos = 0
        ponta = self.__branches[self.__branch_atual]
        if ponta is None:
            return ()

        fila = deque([ponta])
        visitados = set()
        ordem = []
        while fila:
            commit = fila.popleft()
            if commit in visitados:
                continue

            visitados.add(commit)
            ordem.append(commit)
            self.__passos += 1
            fila.extend(self.__pais[commit])

        return tuple(ordem)

    def buscar(self, texto):
        """Procura mensagens na ordem de criacao e conta cada commit examinado."""
        self.__passos = 0
        for numero in range(1, self.__proximo_commit):
            identificador = f"c{numero}"
            self.__passos += 1
            if texto in self.__mensagens[identificador]:
                return identificador

        return None

    def merges(self):
        """Lista em tupla os commits com mais de um pai, contando os commits existentes."""
        self.__passos = 0
        encontrados = []
        for numero in range(1, self.__proximo_commit):
            identificador = f"c{numero}"
            self.__passos += 1
            if len(self.__pais[identificador]) > 1:
                encontrados.append(identificador)

        return tuple(encontrados)
