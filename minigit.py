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
        # Passo 1: registrar o novo commit.
        self.__passos += 1
        # Passo 2: mover o ponteiro da branch atual.
        self.__branches[self.__branch_atual] = identificador
        self.__passos += 1
        return identificador

    def mensagem(self, commit):
        """Busca a mensagem por chave direta no dicionario, gastando um passo."""
        self.__passos = 0
        if commit not in self.__mensagens:
            raise ValueError("Commit inexistente")

        # Passo 1: consultar diretamente a chave.
        self.__passos = 1
        return self.__mensagens[commit]

    def pais(self, commit):
        """Devolve uma tupla imutavel de pais, consultando o dicionario em um passo."""
        self.__passos = 0
        if commit not in self.__pais:
            raise ValueError("Commit inexistente")

        # Passo 1: consultar diretamente a chave.
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
        # Passo 1: criar o novo ponteiro.
        self.__passos = 1

    def trocar_branch(self, nome):
        """Move a referencia da branch atual para outra, gastando um passo."""
        self.__passos = 0
        if nome not in self.__branches:
            raise ValueError("Branch inexistente")

        self.__branch_atual = nome
        # Passo 1: trocar o ponteiro da branch selecionada.
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
        # Passo 1: registrar o commit com seus dois pais.
        self.__passos += 1
        # Passo 2: mover o ponteiro da branch atual.
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
            # Cada commit alcancavel entra uma vez na contagem.
            self.__passos += 1
            fila.extend(self.__pais[commit])

        return tuple(ordem)

    def buscar(self, texto):
        """Procura mensagens na ordem de criacao e conta cada commit examinado."""
        self.__passos = 0
        for numero in range(1, self.__proximo_commit):
            identificador = f"c{numero}"
            # Conta cada mensagem examinada, inclusive a que for encontrada.
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
            # Cada commit existente precisa ser verificado.
            self.__passos += 1
            if len(self.__pais[identificador]) > 1:
                encontrados.append(identificador)

        return tuple(encontrados)


def tentar(acao):
    """Executa uma tentativa e apresenta erros esperados sem interromper o roteiro."""
    try:
        acao()
    except ValueError as erro:
        print("erro:", erro)


def medir(quantidade):
    """Compara o custo do ultimo commit com o custo de percorrer o historico."""
    git = MiniGit()
    for numero in range(quantidade):
        git.commitar(f"commit {numero}")

    passos_commitar = git.passos
    git.log()
    passos_log = git.passos
    return passos_commitar, passos_log


git = MiniGit()
git.commitar("primeiro commit")
print(git.passos)
git.commitar("segundo commit")
git.criar_branch("feature")
print(git.passos)
git.commitar("terceiro commit")
git.trocar_branch("feature")
git.commitar("quarto commit")
git.trocar_branch("main")
git.mesclar("feature")
print(git.pais("c5"))
print(git.log(), git.passos)
print(git.mensagem("c3"), git.passos)
print(git.buscar("quarto"), git.passos)
print(git.merges())
git.trocar_branch("feature")
print(git.log(), git.passos)
git.trocar_branch("main")

tentar(lambda: git.trocar_branch("inexistente"))
tentar(lambda: git.criar_branch("main"))
tentar(lambda: git.mesclar("main"))
tentar(lambda: git.pais("c99"))

print("commits   passos do commitar   passos do log")
for quantidade in (10, 100, 1000):
    passos_commitar, passos_log = medir(quantidade)
    print(f"{quantidade:<10}{passos_commitar:<22}{passos_log}")
