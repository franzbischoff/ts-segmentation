Este repositório implementa um baseline de detecção de mudanças de regime (concept drift / change points) em sinais de ECG em fluxo (250 Hz), incluindo: geração sintética, detectores (PageHinkley, ADWIN, DDM), avaliação de atraso/precisão, grid search simples, logging estruturado, integração com dataset real (afib_regimes via scripts convertidos de R) e preprocessamento (`ecg_preprocess.py`) com opção de limitar ficheiros e selecionar classe (paroxysmal/persistent/non_afib). Diretrizes: manter processamento estritamente streaming (sem lookahead), preservar reprodutibilidade (pinned deps), priorizar clareza e modularidade, adicionar melhorias incrementais validadas por execuções rápidas, documentar novos parâmetros no README e evitar adicionar dados grandes ao versionamento (usar `data/` ignorado).

## Instruções Importantes
Não crie ficheiros de documentação Markdown adicionais sem antes perguntar ao utilizador. Todas as alterações de documentação devem ser feitas nos ficheiros existentes, a menos que o utilizador solicite explicitamente a criação de novos ficheiros.

## Memória Persistente
Sempre que o utilizador indicar que está a iniciar os trabalhos do dia, consulte o ficheiro `.github/copilot-memory.md` para obter as informações mais recentes sobre o estado do projeto.
Quando o utilizador informar que encerrou os trabalhos do dia, atualize o ficheiro `.github/copilot-memory.md` com as informações mais recentes sobre o estado do projeto.
