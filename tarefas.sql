INSERT INTO tarefa (nomeTarefa, descricao, categoria,
                    dataPrazo, prioridade, status)
VALUES
('Trabalho de História',
'Capítulo 4 e resumo de 2 páginas',
'Escola', '2026-12-10', 'ALTA', 'Pendente'),

-- Novas tarefas escolares adicionadas
('Lista de Exercícios de Matemática', 
 'Resolver os problemas da página 112 do livro didático', 
 'Escola', '2026-11-18', 'ALTA', 'Pendente'),

('Apresentação de Biologia', 
 'Preparar os slides sobre fotossíntese em grupo', 
 'Escola', '2026-11-25', 'MÉDIA', 'Pendente'),

('Redação de Português', 
 'Escrever um texto dissertativo-argumentativo sobre tecnologia', 
 'Escola', '2026-11-22', 'ALTA', 'Concluído'),

('Estudar para a Prova de Física', 
 'Revisar leis de Newton e cinemática', 
 'Escola', '2026-12-02', 'ALTA', 'Pendente');
 
SELECT * FROM tarefa WHERE categoria = 'Escola';