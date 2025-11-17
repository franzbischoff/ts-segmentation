Este repositório implementa um baseline de detecção de mudanças de regime (concept drift / change points) em sinais de ECG em fluxo (250 Hz), incluindo: geração sintética, detectores apropriados para time series (PageHinkley, ADWIN, KSWIN, HDDM_A, HDDM_W), avaliação de atraso/precisão, grid search, logging estruturado, integração com dataset real (afib_regimes via scripts convertidos de R) e preprocessamento (`ecg_preprocess.py`) com opção de limitar ficheiros e selecionar classe (paroxysmal/persistent/non_afib). Diretrizes: manter processamento estritamente streaming (sem lookahead), preservar reprodutibilidade (pinned deps), priorizar clareza e modularidade, adicionar melhorias incrementais validadas por execuções rápidas, documentar novos parâmetros no README e evitar adicionar dados grandes ao versionamento (usar `data/` ignorado).

**Nota Importante**: DDM e EDDM foram removidos do projeto por serem inadequados para análise de séries temporais. Estes detectores foram projetados para concept drift em classificação binária (streams de labels), não para detecção de mudanças em valores contínuos.

## Estrutura de Resultados Organizada por Detector

Os resultados estão organizados por detector para facilitar comparações sistemáticas:

```
results/
├── adwin/                          # Detector ADWIN (✅ COMPLETO)
│   ├── predictions_intermediate.csv (126 MB)
│   ├── metrics_comprehensive_with_nab.csv (33 MB)
│   ├── final_report_with_nab.json
│   ├── visualizations/ (9 gráficos PNG)
│   └── README.md                   # Documentação específica do ADWIN
│
├── page_hinkley/                   # Detector Page-Hinkley (🔄 PREPARADO)
│   └── README.md                   # Template e instruções
│
├── kswin/                          # Detector KSWIN (🔄 PREPARADO)
│   └── (a criar após grid search)
│
├── hddm_a/                         # Detector HDDM_A (🔄 PREPARADO)
│   └── (a criar após grid search)
│
├── hddm_w/                         # Detector HDDM_W (🔄 PREPARADO)
│   └── (a criar após grid search)
│
├── comparisons/                    # Comparações entre detectores
│   └── (aguardando implementação de outros detectores)
│
└── README.md                       # Documentação geral da organização
```

### Pipeline Padronizado por Detector

Cada detector segue o mesmo pipeline de 3 passos:

1. **Gerar Predições**: `python -m src.generate_predictions --detector <NAME> --output results/<NAME>/predictions_intermediate.csv`
2. **Avaliar Métricas**: `python -m src.evaluate_predictions --predictions results/<NAME>/predictions_intermediate.csv --metrics-output results/<NAME>/metrics_comprehensive_with_nab.csv --report-output results/<NAME>/final_report_with_nab.json`
3. **Visualizar**: `python -m src.visualize_results --metrics results/<NAME>/metrics_comprehensive_with_nab.csv --output-dir results/<NAME>/visualizations`

### Script de Comparação

Após implementar múltiplos detectores, use:
```bash
python -m src.compare_detectors --detectors adwin page_hinkley kswin hddm_a hddm_w --output results/comparisons/comparative_report.md
```

## Documentação Principal

- **README.md** (raiz) - Documentação geral do projeto, uso, métricas, visualizações
- **results/README.md** - Organização de resultados por detector, workflow padronizado
- **results/adwin/README.md** - Resultados completos do ADWIN, melhores configurações
- **results/page_hinkley/README.md** - Template para Page-Hinkley (a implementar)
- **docs/evaluation_metrics_v1.md** - Documentação detalhada das métricas (F1/F3, NAB, temporal)
- **docs/visualizations_guide.md** - Guia completo de interpretação de gráficos
- **docs/reorganization_summary.md** - Resumo da reorganização por detector
- **docs/nab_comparison_report.md** - Análise comparativa de resultados NAB
- **docs/visualizations_guide.md** - Guia completo de interpretação de gráficos
- **docs/reorganization_summary.md** - Resumo da reorganização por detector
- **docs/nab_comparison_report.md** - Análise comparativa de resultados NAB

## Instruções Importantes
Não crie ficheiros de documentação Markdown adicionais sem antes perguntar ao utilizador. Todas as alterações de documentação devem ser feitas nos ficheiros existentes, a menos que o utilizador solicite explicitamente a criação de novos ficheiros.

## Memória Persistente
Sempre que o utilizador indicar que está a iniciar os trabalhos do dia, consulte o ficheiro `.github/copilot-memory.md` para obter as informações mais recentes sobre o estado do projeto.
Quando o utilizador informar que encerrou os trabalhos do dia, atualize o ficheiro `.github/copilot-memory.md` com as informações mais recentes sobre o estado do projeto.
