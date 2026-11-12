INSERT INTO tarefa (nomeTarefa, descricao, categoria,
                    dataPrazo, prioridade, status)
VALUES
('Trabalho História',
'Capítulo 4 e resumo de 2 páginas',
'Escola', '2026-12-10', 'ALTA', 'Pendente'),

('Lista Matemática',
 'Resolver os problemas da página 112 do livro didático',
 'Escola', '2026-11-18', 'ALTA', 'Pendente'),

('Apresent. Biologia',
 'Preparar os slides sobre fotossíntese em grupo',
 'Escola', '2026-11-25', 'MEDIA', 'Pendente'),

('Redação Português',
 'Escrever um texto dissertativo-argumentativo sobre tecnologia',
 'Escola', '2026-11-22', 'ALTA', 'Concluída'),

('Estudar p/ Física',
 'Revisar leis de Newton e cinemática',
 'Escola', '2026-12-02', 'ALTA', 'Pendente');
 
SELECT * FROM tarefa WHERE categoria = 'Escola';