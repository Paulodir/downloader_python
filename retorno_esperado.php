<?php

const CATEGORIAS_ANEXOS = [
    1 => 'Requisição de Documentos',
    2 => 'Pedidos',
    3 => 'Titulos',
    4 => 'Uploads do Edital',
    5 => 'Uploads do Candidato',
    6 => 'Isenções',
    7 => 'Condições Especiais',
    8 => 'Solicitações',
    9 => 'Titulos',
    10 => 'Foto do Candidato'
];

echo '{
	"meta": {
		"schema_version": "1.0",
		"request_context": {
			"edital_codigo": "12",'.#id do edital no sistema web
            '"filtro": ['.          #categorias de anexos a serem baixados, conforme: CATEGORIAS_ANEXOS             
				'"8",
				"9"
			],
			"categoria_codigo": [
				8,
				9
			]
		}
	},
	"edital": {
		"codigo": "12",'.#id do edital no sistema web
		'"descricao": "",'. # descrição do edital, caso necessário para organização local dos arquivos
		'"anexos": {'. #listagem de todos os anexos encontrados para o edital, organizados por categoria (categoria_codigo)
            '"1": [ '. #Requisição de Documentos: Modelo antigo onde eram cadastrados documentos a serem solicitados aos candidatos, hoje em desuso
				'{
					"modalidade_codigo": "2517",'.          #id da modalidade de vaga no sistema web
					'"modalidade_descricao": "2517",'.      # Nome da modalidade 
					'"vaga_codigo": "2517",'.               # id do cargo/vaga no sistema web
					'"vaga_descricao": "2517",'.            # Nome do cargo/vaga 
					'"inscricao_codigo": "2517",'.          # id da inscrição no sistema web
					'"inscricao_descricao": "2517",'.       # Nome do Candidato
					'"grupo_codigo": "",'.                  # para essa categoria serásempre vazio
					'"grupo_descricao": "",'.               # para essa categoria será sempre vazio
					'"subgrupo_codigo": "",'.               # para essa categoria será sempre vazio
					'"subgrupo_descricao": "",'.            # para essa categoria será sempre vazio
                    '"documento_codigo": "21",'.            # id do documento solicitado no sistema web
					'"documento_descricao": "Cópia do RG",'.# nome do documento solicitado
					'"anexo_codigo": "2517",'.              # id do arquivo anexado no sistema web
					'"anexo_descricao": "24012025-104040-271119.pdf",'.# Nome do arquivo anexado
					'"url": "https://cdn-hml.testes.net.br/candidato/uploads/8442d9419dba843b9e90dc2965be80975a76f124/24012025-104040-271119.pdf",'.# Link para download do arquivo
					'"bytes": "", '.# tamanho do arquivo em bytes, caso disponível
					'"extensao": "pdf"'.# extensão do arquivo, caso disponível
				'}
			],
            "2": [ '. #Pedidos Fixos: Modelo antigo de pedidos de vaga especial, hoje em desuso
				'{
					"modalidade_codigo": "2517",'.          #id da modalidade de vaga no sistema web
					'"modalidade_descricao": "2517",'.      # Nome da modalidade 
					'"vaga_codigo": "2517",'.               # id do cargo/vaga no sistema web
					'"vaga_descricao": "2517",'.            # Nome do cargo/vaga 
					'"inscricao_codigo": "2517",'.          # id da inscrição no sistema web
					'"inscricao_descricao": "2517",'.       # Nome do Candidato
					'"grupo_codigo": "",'.                  # para essa categoria será sempre 1
					'"grupo_descricao": "",'.               # para essa categoria será sempre Vaga Especial
					'"subgrupo_codigo": "",'.               # para essa categoria será sempre vazio
					'"subgrupo_descricao": "",'.            # para essa categoria será sempre vazio
                    '"documento_codigo": "21",'.            # id do documento solicitado no sistema web
					'"documento_descricao": "Cópia do RG",'.# nome do documento solicitado
					'"anexo_codigo": "2517",'.              # id do arquivo anexado no sistema web
					'"anexo_descricao": "24012025-104040-271119.pdf",'.# Nome do arquivo anexado
					'"url": "https://cdn-hml.testes.net.br/candidato/uploads/8442d9419dba843b9e90dc2965be80975a76f124/24012025-104040-271119.pdf",'.# Link para download do arquivo
					'"bytes": "", '.# tamanho do arquivo em bytes, caso disponível
					'"extensao": "pdf"'.# extensão do arquivo, caso disponível
				'}
			],
            "8": [
				{
					"modalidade_codigo": "2517",
					"modalidade_descricao": "2517",
					"vaga_codigo": "2517",
					"vaga_descricao": "2517",
					"inscricao_codigo": "2517",
					"inscricao_descricao": "2517",
					"grupo_codigo": "2517", 
					"grupo_descricao": "Desejo participar da Vaga especial para PcD",
					"subgrupo_codigo": "2517",
					"subgrupo_descricao": "Desejo participar da Vaga especial para PcD",
					"anexo_codigo": "2517",
					"anexo_descricao": "24012025-104040-271119.pdf",
					"url": "https://cdn-hml.testes.net.br/candidato/uploads/8442d9419dba843b9e90dc2965be80975a76f124/24012025-104040-271119.pdf",
					"bytes": "",
					"extensao": "pdf",
					"raw_payload": {
						"url": "https://cdn-hml.testes.net.br/candidato/uploads/8442d9419dba843b9e90dc2965be80975a76f124/24012025-104040-271119.pdf"
					}
				},
				{
					"modalidade_codigo": "2517",
					"modalidade_descricao": "2517",
					"vaga_codigo": "2517",
					"vaga_descricao": "2517",
					"inscricao_codigo": "2517",
					"inscricao_descricao": "2517",
					"grupo_codigo": "2517",
					"grupo_descricao": "Desejo participar da Vaga especial para PcD",
					"subgrupo_codigo": "2517",
					"subgrupo_descricao": "Desejo participar da Vaga especial para PcD",
					"anexo_codigo": "2517",
					"anexo_descricao": "24012025-104040-271119.pdf",
					"url": "https://cdn-hml.testes.net.br/candidato/uploads/8442d9419dba843b9e90dc2965be80975a76f124/24012025-104040-271119.pdf",
					"bytes": "",
					"extensao": "pdf",
					"raw_payload": {
						"url": "https://cdn-hml.testes.net.br/candidato/uploads/8442d9419dba843b9e90dc2965be80975a76f124/24012025-104040-271119.pdf"
					}
				},
				{
					"modalidade_codigo": "2517",
					"modalidade_descricao": "2517",
					"vaga_codigo": "2517",
					"vaga_descricao": "2517",
					"inscricao_codigo": "2517",
					"inscricao_descricao": "2517",
					"grupo_codigo": "2517",
					"grupo_descricao": "Desejo participar da Vaga especial para PcD",
					"subgrupo_codigo": "2517",
					"subgrupo_descricao": "Desejo participar da Vaga especial para PcD",
					"anexo_codigo": "2517",
					"anexo_descricao": "24012025-104040-271119.pdf",
					"url": "https://cdn-hml.testes.net.br/candidato/uploads/8442d9419dba843b9e90dc2965be80975a76f124/24012025-104040-271119.pdf",
					"bytes": "",
					"extensao": "pdf",
					"raw_payload": {
						"url": "https://cdn-hml.testes.net.br/candidato/uploads/8442d9419dba843b9e90dc2965be80975a76f124/24012025-104040-271119.pdf"
					}
				},
				{
					"modalidade_codigo": "2517",
					"modalidade_descricao": "2517",
					"vaga_codigo": "2517",
					"vaga_descricao": "2517",
					"inscricao_codigo": "2517",
					"inscricao_descricao": "2517",
					"grupo_codigo": "2517",
					"grupo_descricao": "Desejo participar da Vaga especial para PcD",
					"subgrupo_codigo": "2517",
					"subgrupo_descricao": "Desejo participar da Vaga especial para PcD",
					"anexo_codigo": "2517",
					"anexo_descricao": "24012025-104040-271119.pdf",
					"url": "https://cdn-hml.testes.net.br/candidato/uploads/8442d9419dba843b9e90dc2965be80975a76f124/24012025-104040-271119.pdf",
					"bytes": "",
					"extensao": "pdf",
					"raw_payload": {
						"url": "https://cdn-hml.testes.net.br/candidato/uploads/8442d9419dba843b9e90dc2965be80975a76f124/24012025-104040-271119.pdf"
					}
				},
				{
					"modalidade_codigo": "2517",
					"modalidade_descricao": "2517",
					"vaga_codigo": "2517",
					"vaga_descricao": "2517",
					"inscricao_codigo": "2517",
					"inscricao_descricao": "2517",
					"grupo_codigo": "2517",
					"grupo_descricao": "Desejo participar da Vaga especial para PcD",
					"subgrupo_codigo": "2517",
					"subgrupo_descricao": "Desejo participar da Vaga especial para PcD",
					"anexo_codigo": "2517",
					"anexo_descricao": "24012025-104040-271119.pdf",
					"url": "https://cdn-hml.testes.net.br/candidato/uploads/8442d9419dba843b9e90dc2965be80975a76f124/24012025-104040-271119.pdf",
					"bytes": "",
					"extensao": "pdf",
					"raw_payload": {
						"url": "https://cdn-hml.testes.net.br/candidato/uploads/8442d9419dba843b9e90dc2965be80975a76f124/24012025-104040-271119.pdf"
					}
				},
				{
					"modalidade_codigo": "2517",
					"modalidade_descricao": "2517",
					"vaga_codigo": "2517",
					"vaga_descricao": "2517",
					"inscricao_codigo": "2517",
					"inscricao_descricao": "2517",
					"grupo_codigo": "2517",
					"grupo_descricao": "Desejo participar da Vaga especial para PcD",
					"subgrupo_codigo": "2517",
					"subgrupo_descricao": "Desejo participar da Vaga especial para PcD",
					"anexo_codigo": "2517",
					"anexo_descricao": "24012025-104040-271119.pdf",
					"url": "https://cdn-hml.testes.net.br/candidato/uploads/8442d9419dba843b9e90dc2965be80975a76f124/24012025-104040-271119.pdf",
					"bytes": "",
					"extensao": "pdf",
					"raw_payload": {
						"url": "https://cdn-hml.testes.net.br/candidato/uploads/8442d9419dba843b9e90dc2965be80975a76f124/24012025-104040-271119.pdf"
					}
				},
				{
					"modalidade_codigo": "2517",
					"modalidade_descricao": "2517",
					"vaga_codigo": "2517",
					"vaga_descricao": "2517",
					"inscricao_codigo": "2517",
					"inscricao_descricao": "2517",
					"grupo_codigo": "2517",
					"grupo_descricao": "Desejo participar da Vaga especial para PcD",
					"subgrupo_codigo": "2517",
					"subgrupo_descricao": "Desejo participar da Vaga especial para PcD",
					"anexo_codigo": "2517",
					"anexo_descricao": "24012025-104040-271119.pdf",
					"url": "https://cdn-hml.testes.net.br/candidato/uploads/8442d9419dba843b9e90dc2965be80975a76f124/24012025-104040-271119.pdf",
					"bytes": "",
					"extensao": "pdf",
					"raw_payload": {
						"url": "https://cdn-hml.testes.net.br/candidato/uploads/8442d9419dba843b9e90dc2965be80975a76f124/24012025-104040-271119.pdf"
					}
				}
			],
			"9": [
				{
					"modalidade_codigo": "2517",
					"modalidade_descricao": "2517",
					"vaga_codigo": "2517",
					"vaga_descricao": "2517",
					"inscricao_codigo": "2517",
					"inscricao_descricao": "2517",
					"grupo_codigo": "2517",
					"grupo_descricao": "Desejo participar da Vaga especial para PcD",
					"subgrupo_codigo": "2517",
					"subgrupo_descricao": "Desejo participar da Vaga especial para PcD",
					"anexo_codigo": "2517",
					"anexo_descricao": "24012025-104040-271119.pdf",
					"url": "https://cdn-hml.testes.net.br/candidato/uploads/8442d9419dba843b9e90dc2965be80975a76f124/24012025-104040-271119.pdf",
					"bytes": "",
					"extensao": "pdf",
					"raw_payload": {
						"url": "https://cdn-hml.testes.net.br/candidato/uploads/8442d9419dba843b9e90dc2965be80975a76f124/24012025-104040-271119.pdf"
					}
				},
				{
					"modalidade_codigo": "2517",
					"modalidade_descricao": "2517",
					"vaga_codigo": "2517",
					"vaga_descricao": "2517",
					"inscricao_codigo": "2517",
					"inscricao_descricao": "2517",
					"grupo_codigo": "2517",
					"grupo_descricao": "Desejo participar da Vaga especial para PcD",
					"subgrupo_codigo": "2517",
					"subgrupo_descricao": "Desejo participar da Vaga especial para PcD",
					"anexo_codigo": "2517",
					"anexo_descricao": "24012025-104040-271119.pdf",
					"url": "https://cdn-hml.testes.net.br/candidato/uploads/8442d9419dba843b9e90dc2965be80975a76f124/24012025-104040-271119.pdf",
					"bytes": "",
					"extensao": "pdf",
					"raw_payload": {
						"url": "https://cdn-hml.testes.net.br/candidato/uploads/8442d9419dba843b9e90dc2965be80975a76f124/24012025-104040-271119.pdf"
					}
				},
				{
					"modalidade_codigo": "2517",
					"modalidade_descricao": "2517",
					"vaga_codigo": "2517",
					"vaga_descricao": "2517",
					"inscricao_codigo": "2517",
					"inscricao_descricao": "2517",
					"grupo_codigo": "2517",
					"grupo_descricao": "Desejo participar da Vaga especial para PcD",
					"subgrupo_codigo": "2517",
					"subgrupo_descricao": "Desejo participar da Vaga especial para PcD",
					"anexo_codigo": "2517",
					"anexo_descricao": "24012025-104040-271119.pdf",
					"url": "https://cdn-hml.testes.net.br/candidato/uploads/8442d9419dba843b9e90dc2965be80975a76f124/24012025-104040-271119.pdf",
					"bytes": "",
					"extensao": "pdf",
					"raw_payload": {
						"url": "https://cdn-hml.testes.net.br/candidato/uploads/8442d9419dba843b9e90dc2965be80975a76f124/24012025-104040-271119.pdf"
					}
				},
				{
					"modalidade_codigo": "2517",
					"modalidade_descricao": "2517",
					"vaga_codigo": "2517",
					"vaga_descricao": "2517",
					"inscricao_codigo": "2517",
					"inscricao_descricao": "2517",
					"grupo_codigo": "2517",
					"grupo_descricao": "Desejo participar da Vaga especial para PcD",
					"subgrupo_codigo": "2517",
					"subgrupo_descricao": "Desejo participar da Vaga especial para PcD",
					"anexo_codigo": "2517",
					"anexo_descricao": "24012025-104040-271119.pdf",
					"url": "https://cdn-hml.testes.net.br/candidato/uploads/8442d9419dba843b9e90dc2965be80975a76f124/24012025-104040-271119.pdf",
					"bytes": "",
					"extensao": "pdf",
					"raw_payload": {
						"url": "https://cdn-hml.testes.net.br/candidato/uploads/8442d9419dba843b9e90dc2965be80975a76f124/24012025-104040-271119.pdf"
					}
				},
				{
					"modalidade_codigo": "2517",
					"modalidade_descricao": "2517",
					"vaga_codigo": "2517",
					"vaga_descricao": "2517",
					"inscricao_codigo": "2517",
					"inscricao_descricao": "2517",
					"grupo_codigo": "2517",
					"grupo_descricao": "Desejo participar da Vaga especial para PcD",
					"subgrupo_codigo": "2517",
					"subgrupo_descricao": "Desejo participar da Vaga especial para PcD",
					"anexo_codigo": "2517",
					"anexo_descricao": "24012025-104040-271119.pdf",
					"url": "https://cdn-hml.testes.net.br/candidato/uploads/8442d9419dba843b9e90dc2965be80975a76f124/24012025-104040-271119.pdf",
					"bytes": "",
					"extensao": "pdf",
					"raw_payload": {
						"url": "https://cdn-hml.testes.net.br/candidato/uploads/8442d9419dba843b9e90dc2965be80975a76f124/24012025-104040-271119.pdf"
					}
				},
				{
					"modalidade_codigo": "2517",
					"modalidade_descricao": "2517",
					"vaga_codigo": "2517",
					"vaga_descricao": "2517",
					"inscricao_codigo": "2517",
					"inscricao_descricao": "2517",
					"grupo_codigo": "2517",
					"grupo_descricao": "Desejo participar da Vaga especial para PcD",
					"subgrupo_codigo": "2517",
					"subgrupo_descricao": "Desejo participar da Vaga especial para PcD",
					"anexo_codigo": "2517",
					"anexo_descricao": "24012025-104040-271119.pdf",
					"url": "https://cdn-hml.testes.net.br/candidato/uploads/8442d9419dba843b9e90dc2965be80975a76f124/24012025-104040-271119.pdf",
					"bytes": "",
					"extensao": "pdf",
					"raw_payload": {
						"url": "https://cdn-hml.testes.net.br/candidato/uploads/8442d9419dba843b9e90dc2965be80975a76f124/24012025-104040-271119.pdf"
					}
				},
				{
					"modalidade_codigo": "2517",
					"modalidade_descricao": "2517",
					"vaga_codigo": "2517",
					"vaga_descricao": "2517",
					"inscricao_codigo": "2517",
					"inscricao_descricao": "2517",
					"grupo_codigo": "2517",
					"grupo_descricao": "Desejo participar da Vaga especial para PcD",
					"subgrupo_codigo": "2517",
					"subgrupo_descricao": "Desejo participar da Vaga especial para PcD",
					"anexo_codigo": "2517",
					"anexo_descricao": "24012025-104040-271119.pdf",
					"url": "https://cdn-hml.testes.net.br/candidato/uploads/8442d9419dba843b9e90dc2965be80975a76f124/24012025-104040-271119.pdf",
					"bytes": "",
					"extensao": "pdf",
					"raw_payload": {
						"url": "https://cdn-hml.testes.net.br/candidato/uploads/8442d9419dba843b9e90dc2965be80975a76f124/24012025-104040-271119.pdf"
					}
				}
			]
		}
	},
	"raw_payload": {
		"meta": {
			"schema_version": "1.0",
			"descricao": "Estrutura normalizada esperada para alimentar o banco local a partir de uma requisicao da API.",
			"request_context": {
				"edital_codigo": "12",
				"filtro": [
					"solicitacoes",
					"banca"
				],
				"categoria_codigo": [
					5,
					6
				]
			}
		},
		"edital": {
			"codigo": "12",
			"descricao": "",
			"anexos": {
				"5": [
					{
						"modalidade_codigo": "2517",
						"modalidade_descricao": "2517",
						"vaga_codigo": "2517",
						"vaga_descricao": "2517",
						"inscricao_codigo": "2517",
						"inscricao_descricao": "2517",
						"grupo_codigo": "2517",
						"grupo_descricao": "Desejo participar da Vaga especial para PcD",
						"subgrupo_codigo": "2517",
						"subgrupo_descricao": "Desejo participar da Vaga especial para PcD",
						"anexo_codigo": "2517",
						"anexo_descricao": "24012025-104040-271119.pdf",
						"url": "https://cdn-hml.testes.net.br/candidato/uploads/8442d9419dba843b9e90dc2965be80975a76f124/24012025-104040-271119.pdf",
						"bytes": "",
						"extensao": "pdf",
						"raw_payload": {
							"url": "https://cdn-hml.testes.net.br/candidato/uploads/8442d9419dba843b9e90dc2965be80975a76f124/24012025-104040-271119.pdf"
						}
					},
					{
						"modalidade_codigo": "2517",
						"modalidade_descricao": "2517",
						"vaga_codigo": "2517",
						"vaga_descricao": "2517",
						"inscricao_codigo": "2517",
						"inscricao_descricao": "2517",
						"grupo_codigo": "2517",
						"grupo_descricao": "Desejo participar da Vaga especial para PcD",
						"subgrupo_codigo": "2517",
						"subgrupo_descricao": "Desejo participar da Vaga especial para PcD",
						"anexo_codigo": "2517",
						"anexo_descricao": "24012025-104040-271119.pdf",
						"url": "https://cdn-hml.testes.net.br/candidato/uploads/8442d9419dba843b9e90dc2965be80975a76f124/24012025-104040-271119.pdf",
						"bytes": "",
						"extensao": "pdf",
						"raw_payload": {
							"url": "https://cdn-hml.testes.net.br/candidato/uploads/8442d9419dba843b9e90dc2965be80975a76f124/24012025-104040-271119.pdf"
						}
					},
					{
						"modalidade_codigo": "2517",
						"modalidade_descricao": "2517",
						"vaga_codigo": "2517",
						"vaga_descricao": "2517",
						"inscricao_codigo": "2517",
						"inscricao_descricao": "2517",
						"grupo_codigo": "2517",
						"grupo_descricao": "Desejo participar da Vaga especial para PcD",
						"subgrupo_codigo": "2517",
						"subgrupo_descricao": "Desejo participar da Vaga especial para PcD",
						"anexo_codigo": "2517",
						"anexo_descricao": "24012025-104040-271119.pdf",
						"url": "https://cdn-hml.testes.net.br/candidato/uploads/8442d9419dba843b9e90dc2965be80975a76f124/24012025-104040-271119.pdf",
						"bytes": "",
						"extensao": "pdf",
						"raw_payload": {
							"url": "https://cdn-hml.testes.net.br/candidato/uploads/8442d9419dba843b9e90dc2965be80975a76f124/24012025-104040-271119.pdf"
						}
					},
					{
						"modalidade_codigo": "2517",
						"modalidade_descricao": "2517",
						"vaga_codigo": "2517",
						"vaga_descricao": "2517",
						"inscricao_codigo": "2517",
						"inscricao_descricao": "2517",
						"grupo_codigo": "2517",
						"grupo_descricao": "Desejo participar da Vaga especial para PcD",
						"subgrupo_codigo": "2517",
						"subgrupo_descricao": "Desejo participar da Vaga especial para PcD",
						"anexo_codigo": "2517",
						"anexo_descricao": "24012025-104040-271119.pdf",
						"url": "https://cdn-hml.testes.net.br/candidato/uploads/8442d9419dba843b9e90dc2965be80975a76f124/24012025-104040-271119.pdf",
						"bytes": "",
						"extensao": "pdf",
						"raw_payload": {
							"url": "https://cdn-hml.testes.net.br/candidato/uploads/8442d9419dba843b9e90dc2965be80975a76f124/24012025-104040-271119.pdf"
						}
					},
					{
						"modalidade_codigo": "2517",
						"modalidade_descricao": "2517",
						"vaga_codigo": "2517",
						"vaga_descricao": "2517",
						"inscricao_codigo": "2517",
						"inscricao_descricao": "2517",
						"grupo_codigo": "2517",
						"grupo_descricao": "Desejo participar da Vaga especial para PcD",
						"subgrupo_codigo": "2517",
						"subgrupo_descricao": "Desejo participar da Vaga especial para PcD",
						"anexo_codigo": "2517",
						"anexo_descricao": "24012025-104040-271119.pdf",
						"url": "https://cdn-hml.testes.net.br/candidato/uploads/8442d9419dba843b9e90dc2965be80975a76f124/24012025-104040-271119.pdf",
						"bytes": "",
						"extensao": "pdf",
						"raw_payload": {
							"url": "https://cdn-hml.testes.net.br/candidato/uploads/8442d9419dba843b9e90dc2965be80975a76f124/24012025-104040-271119.pdf"
						}
					},
					{
						"modalidade_codigo": "2517",
						"modalidade_descricao": "2517",
						"vaga_codigo": "2517",
						"vaga_descricao": "2517",
						"inscricao_codigo": "2517",
						"inscricao_descricao": "2517",
						"grupo_codigo": "2517",
						"grupo_descricao": "Desejo participar da Vaga especial para PcD",
						"subgrupo_codigo": "2517",
						"subgrupo_descricao": "Desejo participar da Vaga especial para PcD",
						"anexo_codigo": "2517",
						"anexo_descricao": "24012025-104040-271119.pdf",
						"url": "https://cdn-hml.testes.net.br/candidato/uploads/8442d9419dba843b9e90dc2965be80975a76f124/24012025-104040-271119.pdf",
						"bytes": "",
						"extensao": "pdf",
						"raw_payload": {
							"url": "https://cdn-hml.testes.net.br/candidato/uploads/8442d9419dba843b9e90dc2965be80975a76f124/24012025-104040-271119.pdf"
						}
					},
					{
						"modalidade_codigo": "2517",
						"modalidade_descricao": "2517",
						"vaga_codigo": "2517",
						"vaga_descricao": "2517",
						"inscricao_codigo": "2517",
						"inscricao_descricao": "2517",
						"grupo_codigo": "2517",
						"grupo_descricao": "Desejo participar da Vaga especial para PcD",
						"subgrupo_codigo": "2517",
						"subgrupo_descricao": "Desejo participar da Vaga especial para PcD",
						"anexo_codigo": "2517",
						"anexo_descricao": "24012025-104040-271119.pdf",
						"url": "https://cdn-hml.testes.net.br/candidato/uploads/8442d9419dba843b9e90dc2965be80975a76f124/24012025-104040-271119.pdf",
						"bytes": "",
						"extensao": "pdf",
						"raw_payload": {
							"url": "https://cdn-hml.testes.net.br/candidato/uploads/8442d9419dba843b9e90dc2965be80975a76f124/24012025-104040-271119.pdf"
						}
					}
				],
				"6": [
					{
						"modalidade_codigo": "2517",
						"modalidade_descricao": "2517",
						"vaga_codigo": "2517",
						"vaga_descricao": "2517",
						"inscricao_codigo": "2517",
						"inscricao_descricao": "2517",
						"grupo_codigo": "2517",
						"grupo_descricao": "Desejo participar da Vaga especial para PcD",
						"subgrupo_codigo": "2517",
						"subgrupo_descricao": "Desejo participar da Vaga especial para PcD",
						"anexo_codigo": "2517",
						"anexo_descricao": "24012025-104040-271119.pdf",
						"url": "https://cdn-hml.testes.net.br/candidato/uploads/8442d9419dba843b9e90dc2965be80975a76f124/24012025-104040-271119.pdf",
						"bytes": "",
						"extensao": "pdf",
						"raw_payload": {
							"url": "https://cdn-hml.testes.net.br/candidato/uploads/8442d9419dba843b9e90dc2965be80975a76f124/24012025-104040-271119.pdf"
						}
					},
					{
						"modalidade_codigo": "2517",
						"modalidade_descricao": "2517",
						"vaga_codigo": "2517",
						"vaga_descricao": "2517",
						"inscricao_codigo": "2517",
						"inscricao_descricao": "2517",
						"grupo_codigo": "2517",
						"grupo_descricao": "Desejo participar da Vaga especial para PcD",
						"subgrupo_codigo": "2517",
						"subgrupo_descricao": "Desejo participar da Vaga especial para PcD",
						"anexo_codigo": "2517",
						"anexo_descricao": "24012025-104040-271119.pdf",
						"url": "https://cdn-hml.testes.net.br/candidato/uploads/8442d9419dba843b9e90dc2965be80975a76f124/24012025-104040-271119.pdf",
						"bytes": "",
						"extensao": "pdf",
						"raw_payload": {
							"url": "https://cdn-hml.testes.net.br/candidato/uploads/8442d9419dba843b9e90dc2965be80975a76f124/24012025-104040-271119.pdf"
						}
					},
					{
						"modalidade_codigo": "2517",
						"modalidade_descricao": "2517",
						"vaga_codigo": "2517",
						"vaga_descricao": "2517",
						"inscricao_codigo": "2517",
						"inscricao_descricao": "2517",
						"grupo_codigo": "2517",
						"grupo_descricao": "Desejo participar da Vaga especial para PcD",
						"subgrupo_codigo": "2517",
						"subgrupo_descricao": "Desejo participar da Vaga especial para PcD",
						"anexo_codigo": "2517",
						"anexo_descricao": "24012025-104040-271119.pdf",
						"url": "https://cdn-hml.testes.net.br/candidato/uploads/8442d9419dba843b9e90dc2965be80975a76f124/24012025-104040-271119.pdf",
						"bytes": "",
						"extensao": "pdf",
						"raw_payload": {
							"url": "https://cdn-hml.testes.net.br/candidato/uploads/8442d9419dba843b9e90dc2965be80975a76f124/24012025-104040-271119.pdf"
						}
					},
					{
						"modalidade_codigo": "2517",
						"modalidade_descricao": "2517",
						"vaga_codigo": "2517",
						"vaga_descricao": "2517",
						"inscricao_codigo": "2517",
						"inscricao_descricao": "2517",
						"grupo_codigo": "2517",
						"grupo_descricao": "Desejo participar da Vaga especial para PcD",
						"subgrupo_codigo": "2517",
						"subgrupo_descricao": "Desejo participar da Vaga especial para PcD",
						"anexo_codigo": "2517",
						"anexo_descricao": "24012025-104040-271119.pdf",
						"url": "https://cdn-hml.testes.net.br/candidato/uploads/8442d9419dba843b9e90dc2965be80975a76f124/24012025-104040-271119.pdf",
						"bytes": "",
						"extensao": "pdf",
						"raw_payload": {
							"url": "https://cdn-hml.testes.net.br/candidato/uploads/8442d9419dba843b9e90dc2965be80975a76f124/24012025-104040-271119.pdf"
						}
					},
					{
						"modalidade_codigo": "2517",
						"modalidade_descricao": "2517",
						"vaga_codigo": "2517",
						"vaga_descricao": "2517",
						"inscricao_codigo": "2517",
						"inscricao_descricao": "2517",
						"grupo_codigo": "2517",
						"grupo_descricao": "Desejo participar da Vaga especial para PcD",
						"subgrupo_codigo": "2517",
						"subgrupo_descricao": "Desejo participar da Vaga especial para PcD",
						"anexo_codigo": "2517",
						"anexo_descricao": "24012025-104040-271119.pdf",
						"url": "https://cdn-hml.testes.net.br/candidato/uploads/8442d9419dba843b9e90dc2965be80975a76f124/24012025-104040-271119.pdf",
						"bytes": "",
						"extensao": "pdf",
						"raw_payload": {
							"url": "https://cdn-hml.testes.net.br/candidato/uploads/8442d9419dba843b9e90dc2965be80975a76f124/24012025-104040-271119.pdf"
						}
					},
					{
						"modalidade_codigo": "2517",
						"modalidade_descricao": "2517",
						"vaga_codigo": "2517",
						"vaga_descricao": "2517",
						"inscricao_codigo": "2517",
						"inscricao_descricao": "2517",
						"grupo_codigo": "2517",
						"grupo_descricao": "Desejo participar da Vaga especial para PcD",
						"subgrupo_codigo": "2517",
						"subgrupo_descricao": "Desejo participar da Vaga especial para PcD",
						"anexo_codigo": "2517",
						"anexo_descricao": "24012025-104040-271119.pdf",
						"url": "https://cdn-hml.testes.net.br/candidato/uploads/8442d9419dba843b9e90dc2965be80975a76f124/24012025-104040-271119.pdf",
						"bytes": "",
						"extensao": "pdf",
						"raw_payload": {
							"url": "https://cdn-hml.testes.net.br/candidato/uploads/8442d9419dba843b9e90dc2965be80975a76f124/24012025-104040-271119.pdf"
						}
					},
					{
						"modalidade_codigo": "2517",
						"modalidade_descricao": "2517",
						"vaga_codigo": "2517",
						"vaga_descricao": "2517",
						"inscricao_codigo": "2517",
						"inscricao_descricao": "2517",
						"grupo_codigo": "2517",
						"grupo_descricao": "Desejo participar da Vaga especial para PcD",
						"subgrupo_codigo": "2517",
						"subgrupo_descricao": "Desejo participar da Vaga especial para PcD",
						"anexo_codigo": "2517",
						"anexo_descricao": "24012025-104040-271119.pdf",
						"url": "https://cdn-hml.testes.net.br/candidato/uploads/8442d9419dba843b9e90dc2965be80975a76f124/24012025-104040-271119.pdf",
						"bytes": "",
						"extensao": "pdf",
						"raw_payload": {
							"url": "https://cdn-hml.testes.net.br/candidato/uploads/8442d9419dba843b9e90dc2965be80975a76f124/24012025-104040-271119.pdf"
						}
					}
				]
			}
		}
	}
}';