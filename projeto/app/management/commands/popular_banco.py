from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

from app.models import ItemAchado, ItemPerdido, Usuario


SENHA_PADRAO = "123456"

USUARIOS = [
    ("Mariana Costa", "mariana.costa@example.com", "Engenharia de Produção", "2210345", "Aluno"),
    ("Pedro Henrique Almeida", "pedro.almeida@example.com", "Administração", "2311872", "Aluno"),
    ("Júlia Fernandes", "julia.fernandes@example.com", "Design", "2120456", "Aluno"),
    ("Lucas Oliveira", "lucas.oliveira@example.com", "Engenharia de Computação", "2310991", "Aluno"),
    ("Beatriz Rocha", "beatriz.rocha@example.com", "Direito", "2220178", "Aluno"),
    ("Rafael Monteiro", "rafael.monteiro@example.com", "Economia", "2010563", "Aluno"),
    ("Camila Duarte", "camila.duarte@example.com", "Psicologia", "2410237", "Aluno"),
    ("Thiago Barros", "thiago.barros@example.com", "Engenharia Civil", "2110784", "Aluno"),
    ("Ricardo Lemos", "ricardo.lemos@example.com", "Física", "0098123", "Professor"),
    ("Sônia Ribeiro", "sonia.ribeiro@example.com", "Prefeitura do campus", "0076451", "Funcionário"),
]

# (email do dono, titulo, categoria, local, dias atras, descricao, devolvido)
PERDIDOS = [
    ("lucas.oliveira@example.com", "Fone JBL Tune preto", "eletronicos", "Ed. Kennedy, sala 512", 2,
     "Fone sem fio preto, com um adesivo do Botafogo no case. Acho que esqueci na mesa depois da prova de Cálculo II.", False),
    ("pedro.almeida@example.com", "Carteira marrom de couro", "documentos", "Bandejão", 1,
     "Tem minha identidade, um cartão do Bradesco e o RioCard. Se alguém achar me chama por favor!!", False),
    ("beatriz.rocha@example.com", "Garrafa Stanley verde", "utensilios", "Ginásio", 9,
     "Verde-musgo, de 1 litro, com um arranhado na tampa e meu nome escrito embaixo de caneta.", True),
    ("mariana.costa@example.com", "Moletom cinza da PUC", "roupas", "Pilotis, perto da cantina", 3,
     "Moletom cinza com o logo da PUC, tamanho M. Deixei no banco e quando voltei já não tava mais lá.", False),
    ("rafael.monteiro@example.com", "Calculadora HP 12C", "eletronicos", "Ed. Frings, 3º andar", 4,
     "Tem meu nome gravado atrás. Preciso dela pra prova de Matemática Financeira semana que vem :(", False),
    ("mariana.costa@example.com", "Caderno azul de 10 matérias", "material_estudo", "Biblioteca Central", 6,
     "Capa azul com um post-it amarelo. Tem todas as minhas anotações de Fenômenos de Transporte.", False),
    ("camila.duarte@example.com", "Óculos de grau", "roupas", "Ed. Cardeal Leme, sala 102", 2,
     "Armação preta quadrada, dentro de um estojo vermelho. Sem eles eu não enxergo o quadro.", False),
    ("thiago.barros@example.com", "Chave do carro com chaveiro do Flamengo", "outros", "Estacionamento", 5,
     "Duas chaves de casa e a chave do carro (Fiat), presas num chaveirinho do Flamengo.", False),
    ("lucas.oliveira@example.com", "Carregador de notebook Dell", "eletronicos", "RDC, laboratório de informática", 8,
     "Carregador Dell de 65W. Ficou na tomada do lab depois da aula de Programação.", False),
    ("julia.fernandes@example.com", "Guarda-chuva preto", "utensilios", "Ed. da Amizade", 12,
     "Guarda-chuva preto automático, o cabo tá meio quebrado. Esqueci na entrada no dia que choveu muito.", False),
    ("julia.fernandes@example.com", "Case de AirPods com capinha rosa", "eletronicos", "Vila dos Diretórios", 1,
     "Case branco com uma capinha de silicone rosa. Os dois fones estão dentro.", False),
    ("pedro.almeida@example.com", "Livro Cálculo Vol. 1 (Stewart)", "material_estudo", "Biblioteca Central, 4º andar", 15,
     "8ª edição, com várias páginas marcadas a lápis. Meu nome está na primeira folha.", False),
    ("beatriz.rocha@example.com", "Carteirinha da PUC", "documentos", "Pilotis", 7,
     "Carteirinha de estudante no meu nome. Caiu do bolso enquanto eu corria pra aula.", True),
    ("camila.duarte@example.com", "Jaqueta jeans clara", "roupas", "Bosque", 10,
     "Jaqueta jeans clara com um broche de margarida no bolso da frente.", False),
    ("rafael.monteiro@example.com", "Pen drive SanDisk vermelho", "eletronicos", "Ed. Leme, sala de estudos", 3,
     "Pen drive de 32GB, tem a versão final do meu TCC!!! Se acharem me avisem pelo amor de Deus.", False),
    ("julia.fernandes@example.com", "Estojo de pano rosa", "material_estudo", "Ed. Kennedy, 2º andar", 4,
     "Estojo rosa com canetas coloridas, marca-texto e uma borracha em forma de gato.", False),
    ("pedro.almeida@example.com", "Mochila preta da Nike", "outros", "Ginásio, vestiário", 11,
     "Mochila preta com uma toalha e roupa de treino dentro. Nada de valor, mas gosto muito dela.", False),
    ("ricardo.lemos@example.com", "Pasta azul com provas corrigidas", "material_estudo", "Ed. Cardeal Leme, sala dos professores", 2,
     "Pasta plástica azul com as provas da turma 3VA já corrigidas. Preciso devolver para os alunos na sexta.", False),
    ("camila.duarte@example.com", "Kindle com capa marrom", "eletronicos", "Gramado do Solar", 6,
     "Kindle Paperwhite com capa de couro marrom. Estava lendo no gramado e acabei esquecendo.", False),
    ("thiago.barros@example.com", "Crachá do estágio", "documentos", "Bandejão", 1,
     "Crachá com cordão verde. Preciso dele pra entrar no estágio amanhã cedo.", False),
]

# (email de quem achou, nome, categoria, onde encontrou, dias atras, descricao, onde esta agora)
ACHADOS = [
    ("lucas.oliveira@example.com", "Carteirinha de estudante", "documentos", "Pilotis, perto da escada", 7,
     "Carteirinha em nome de Beatriz R. Deixei na prefeitura.", "prefeitura"),
    ("mariana.costa@example.com", "Óculos com estojo vermelho", "roupas", "Ed. Cardeal Leme, sala 102", 1,
     "Achei embaixo de uma carteira no fim da aula. Armação preta.", "coordenacao"),
    ("rafael.monteiro@example.com", "Garrafa térmica azul", "utensilios", "Bandejão", 3,
     "Garrafa azul cheia de adesivos de banda. Tá comigo, é só me chamar.", "comigo"),
    ("sonia.ribeiro@example.com", "Chave com chaveiro de ursinho", "outros", "Estacionamento do Ed. Leme", 4,
     "Uma chave só, presa num chaveiro de pelúcia.", "prefeitura"),
    ("julia.fernandes@example.com", "Fone com fio Samsung", "eletronicos", "Biblioteca Central, 3º andar", 2,
     "Fone branco com fio, estava em cima da mesa de estudo.", "comigo"),
    ("camila.duarte@example.com", "Casaco preto da Adidas", "roupas", "RDC, auditório", 5,
     "Tamanho G, ficou na cadeira depois da palestra de quinta.", "coordenacao"),
    ("pedro.almeida@example.com", "Apostila de Química Geral", "material_estudo", "Ed. Frings, sala 301", 6,
     "Apostila encadernada com várias anotações de caneta azul.", "comigo"),
    ("sonia.ribeiro@example.com", "Guarda-chuva de bolinhas", "utensilios", "Ed. da Amizade, entrada", 12,
     "Guarda-chuva dobrável de bolinhas. Está guardado na prefeitura.", "prefeitura"),
]


class Command(BaseCommand):
    help = "Popula o banco com usuários e itens de exemplo"

    def handle(self, *args, **options):
        agora = timezone.now()

        for nome, email, curso, matricula, perfil in USUARIOS:
            usuario, criado = Usuario.objects.get_or_create(
                email=email,
                defaults={"nome": nome, "curso": curso, "matricula": matricula, "perfil": perfil},
            )
            if criado:
                usuario.set_senha(SENHA_PADRAO)
                usuario.save()

        for email, titulo, categoria, local, dias, descricao, devolvido in PERDIDOS:
            ItemPerdido.objects.get_or_create(
                usuario=Usuario.objects.get(email=email),
                titulo=titulo,
                defaults={
                    "categoria": categoria,
                    "local": local,
                    "data": agora - timedelta(days=dias, hours=dias * 3 % 9),
                    "descricao": descricao,
                    "devolvido": devolvido,
                },
            )

        for email, nome, categoria, local, dias, descricao, onde_esta in ACHADOS:
            ItemAchado.objects.get_or_create(
                usuario=Usuario.objects.get(email=email),
                nome_objeto=nome,
                defaults={
                    "categoria": categoria,
                    "onde_encontrou": local,
                    "data_encontro": agora - timedelta(days=dias, hours=dias * 2 % 7),
                    "descricao": descricao,
                    "onde_esta_agora": onde_esta,
                },
            )

        self.stdout.write(self.style.SUCCESS(
            f"Pronto: {Usuario.objects.count()} usuários, "
            f"{ItemPerdido.objects.count()} itens perdidos e {ItemAchado.objects.count()} achados. "
            f"Senha dos usuários de exemplo: {SENHA_PADRAO}"
        ))
