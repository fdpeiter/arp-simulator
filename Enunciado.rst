Trabalho Final - Descrição
TRABALHO FINAL DE REDES DE COMPUTADORES I - 2016/2
Prazo máximo para entrega do trabalho (pelo Moodle): 15/11 às 23:55
O trabalho consiste em desenvolver um simulador de rede. O simulador deve receber como parâmetros de execução o nome de um arquivo de descrição de topologia (conforme formato especificado) e uma lista de nós. O simulador deve apresentar na saída as mensagens enviadas pelos nós e roteadores da topologia conforme o formato estabelecido, considerando o envio de um pacote ICMP Echo Request do primeiro até o último nó da lista e retornando um pacote ICMP Echo Reply para o primeiro nó da lista. A transferência dos pacotes deve respeitar a topologia da rede definida pela arquivo de descrição de topologia. Se existir um loop na topologia, o roteador que chegar ao TTL igual a zero, enviará uma mensagem ICMP Time Exceeded para o último nó que realizou o envio, e o simulador é encerrado.

Formato do arquivo de descrição de topologia
#NODE 
<node_name>,<MAC>,<IP/prefix>,<gateway>
#ROUTER
<router_name>,<num_ports>,<MAC0>,<IP0/prefix>,<MAC1>,<IP1/prefix>,<MAC2>,<IP2/prefix> …
#ROUTERTABLE
<router_name>,<net_dest/prefix>,<nexthop>,<port>
Formato de saída

Pacotes ARP Request: <src_name> box <src_name> : ARP - Who has <dst_IP>? Tell <src_IP>; 
Pacotes ARP Reply: <src_name> => <dst_name> : ARP - <src_IP> is at <src_MAC>;
Pacotes ICMP Echo Request: <src_name> => <dst_name> : ICMP - Echo request (src=<src_IP> dst=<dst_IP> ttl=<TTL>);
Pacotes ICMP Echo Reply: <src_name> => <dst_name> : ICMP - Echo reply (src=<src_IP> dst=<dst_IP> ttl=<TTL>);
Pacotes ICMP Time Exceeded: <src_name> => <dst_name> : ICMP - Time Exceeded (src=<src_IP> dst=<dst_IP> ttl=<TTL>);

Modo de execução do simulador
$ simulador <topologia> <nodo1> <nodo2> <nodo3> …

EXEMPLO:
Arquivo topologia.txt
#NODE 
n1,00:00:00:00:00:01,192.168.0.2/24,192.168.0.1 
n2,00:00:00:00:00:02,192.168.0.3/24,192.168.0.1
n3,00:00:00:00:00:03,192.168.1.2/24,192.168.1.1
n4,00:00:00:00:00:04,192.168.1.3/24,192.168.1.1
#ROUTER
r1,2,00:00:00:00:00:05,192.168.0.1/24,00:00:00:00:00:06,192.168.1.1/24
#ROUTERTABLE
r1,192.168.0.0/24,0.0.0.0,0
r1,192.168.1.0/24,0.0.0.0,1

Exemplos de execução:
$ simulador topologia.txt n1 n2 
n1 box n1 : ARP - Who has 192.168.0.3? Tell 192.168.0.2;
 n2 => n1 : ARP - 192.168.0.3 is at 00:00:00:00:00:02;
n1 => n2 : ICMP - Echo request (src=192.168.0.2 dst=192.168.0.3 ttl=8);
n2 => n1 : ICMP - Echo reply (src=192.168.0.3 dst=192.168.0.2 ttl=8);

$ simulador topologia.txt n1 n3
 n1 box n1 : ARP - Who has 192.168.0.1? Tell 192.168.0.2;
 r1 => n1 : ARP - 192.168.0.1 is at 00:00:00:00:00:05;
n1 => r1 : ICMP - Echo request (src=192.168.0.2 dst=192.168.1.2 ttl=8);
r1 box r1 : ARP - Who has 192.168.1.2? Tell 192.168.1.1;
 n3 => r1 : ARP - 192.168.1.2 is at 00:00:00:00:00:03;
r1 => n3 : ICMP - Echo request (src=192.168.0.2 dst=192.168.1.2 ttl=7);
n3 => r1 : ICMP - Echo reply (src=192.168.1.2 dst=192.168.0.2 ttl=8);
r1 => n1 : ICMP - Echo reply (src=192.168.1.2 dst=192.168.0.2 ttl=7);

$ simulador topologia.txt n1 n2 n3 n4
 n1 box n1 : ARP - Who has 192.168.0.3? Tell 192.168.0.2; 
n2 => n1 : ARP - 192.168.0.3 is at 00:00:00:00:00:02;
n1 => n2 : ICMP - Echo request (src=192.168.0.2 dst=192.168.0.3 ttl=8);
n2 box n2 : ARP - Who has 192.168.0.1? Tell 192.168.0.3;
r1 => n2 : ARP - 192.168.0.1 is at 00:00:00:00:00:05;
n2 => r1 : ICMP - Echo request (src=192.168.0.3 dst=192.168.1.2 ttl=8);
r1 box r1 : ARP - Who has 192.168.1.2? Tell 192.168.1.1;
n3 => r1 : ARP - 192.168.1.2 is at 00:00:00:00:00:03;
r1 => n3 : ICMP - Echo request (src=192.168.0.3 dst=192.168.1.2 ttl=7);
n3 box n3 : ARP - Who has 192.168.1.3? Tell 192.168.1.2;
 n4 => n3 : ARP - 192.168.1.3 is at 00:00:00:00:00:04;
n3 => n4 : ICMP - Echo request (src=192.168.1.2 dst=192.168.1.3 ttl=8);
n4 box n4 : ARP - Who has 192.168.1.1? Tell 192.168.1.3;
r1 => n4 : ARP - 192.168.1.1 is at 00:00:00:00:00:06;
n4 => r1 : ICMP - Echo reply (src=192.168.1.3 dst=192.168.0.2 ttl=8);
r1 box r1 : ARP - Who has 192.168.0.2? Tell 192.168.0.1;
n1 => r1 : ARP - 192.168.0.2 is at 00:00:00:00:00:01;
r1 => n1 : ICMP - Echo reply (src=192.168.1.3 dst=192.168.0.2 ttl=7);

$ simulador topologia.txt n1 n3 n2 n4
 n1 box n1 : ARP - Who has 192.168.0.1? Tell 192.168.0.2;
 r1 => n1 : ARP - 192.168.0.1 is at 00:00:00:00:00:05;
n1 => r1 : ICMP - Echo request (src=192.168.0.2 dst=192.168.1.2 ttl=8);
r1 box r1 : ARP - Who has 192.168.1.2? Tell 192.168.1.1;
n3 => r1 : ARP - 192.168.1.2 is at 00:00:00:00:00:03;
r1 => n3 : ICMP - Echo request (src=192.168.0.2 dst=192.168.1.2 ttl=7);
n3 => r1 : ICMP - Echo request (src=192.168.1.2 dst=192.168.0.3 ttl=8);
r1 box r1 : ARP - Who has 192.168.0.3? Tell 192.168.0.1;
n2 => r1 : ARP - 192.168.0.3 is at 00:00:00:00:00:02;
r1 => n2 : ICMP - Echo request (src=192.168.1.2 dst=192.168.0.3 ttl=7);
n2 => r1 : ICMP - Echo request (src=192.168.0.3 dst=192.168.1.3 ttl=8);
r1 box r1 : ARP - Who has 192.168.1.3? Tell 192.168.1.1;
n4 => r1 : ARP - 192.168.1.3 is at 00:00:00:00:00:04;
r1 => n4 : ICMP - Echo request (src=192.168.0.3 dst=192.168.1.3 ttl=7);
n4 => r1 : ICMP - Echo reply (src=192.168.1.3 dst=192.168.0.2 ttl=8);
r1 => n1 : ICMP - Echo reply (src=192.168.1.3 dst = 192.168.0.2 ttl=7);

Detalhes para construção do simulador:
- TTL inicial dos pacotes IP deve ser igual a 8
- a topologia poderá apresentar loops de roteamento
- a lista de nós de entrada pode ter itens repetidos
- o simulador deve ser executado a partir de um terminal por linha de comando de acordo com o exemplo apresentado - não deve ser necessário utilizar uma IDE para executar o simulador!!!
- o simulador pode ser implementado em qualquer linguagem
- a entrada e saída devem respeitar EXATAMENTE os formatos apresentados
- o formato de saída é baseado na linguagem MsGenny. Sugere-se verificar se a saída está correta através do site https://sverweij.github.io/mscgen_js. Usar o cabeçalho “wordwraparcs=true,hscale=2.0;” para facilitar a visualização.

Itens a serem entregues:
- código fonte e executável
- relatório (em pdf) contendo: (i) detalhes de implementação (linguagem, classes, principais métodos); (ii) descrição de como utilizar o simulador; (iii) limitações do simulador implementado e dificuldades de implementação; (iv) exemplo de execução com 1 topologia composta por no mínimo 2 roteadores e 4 nós

OBSERVAÇÕES
- O trabalho deve ser realizado em grupos de no máximo 2 alunos.
- Não serão aceitos trabalhos atrasados e/ou enviados por e-mail.
- Trabalhos que não compilam ou que não executam não serão avaliados.
- Todos os trabalhos serão analisados e comparados. Caso seja identificada cópia de trabalhos, todos os trabalhos envolvidos receberão nota ZERO!
