# FASE 2 ROADMAP: Geração de Visualizações

**Data**: 2025-12-15
**Responsável**: ✅ CONCLUÍDO
**Status**: ✅ **COMPLETADO** (16:24:43)
**Duração**: ~45 minutos (implementação + testes)

---

## 📋 Tarefas da Fase 2

### Script 1: `src/visualize_comparison_by_dataset.py`

**Propósito**: Gerar visualizações para comparação de 6 detectores num dataset específico

**Input**:
- CSV de métricas de todos os 6 detectores para um dataset
- Path: `results/<dataset>/<detector>/metrics_comprehensive_with_nab.csv`

**Output** (4 ficheiros PNG):
```
results/comparisons/by_dataset/<dataset>/visualizations/
├── radar_6detectors.png              # Radar chart (6 detectores × 6 métricas)
├── f3_vs_fp_scatter.png              # Scatter: F3 vs FP/min
├── heatmap_metrics_comparison.png    # Heatmap: 6 detectores × 7 métricas
└── parameter_tradeoffs.png           # 3D scatter ou parallel coordinates
```

**Métricas no Radar** (6 eixos normalizados 0-1):
1. `F3-weighted` (performance)
2. `NAB Standard` (anomaly detection score)
3. `Recall@10s` (detecção)
4. `Precision@10s` (seletividade)
5. `1 - FP/min` (baixos alarmes falsos, normalizado)
6. `1 - EDD/10s` (rapidez de detecção)

**Detalhes Técnicos**:
```python
# Pseudocode
detectors = ['adwin', 'page_hinkley', 'kswin', 'hddm_a', 'hddm_w', 'floss']

for detector in detectors:
    # Ler metrics_comprehensive_with_nab.csv
    # Calcular best configs por métrica
    # Normalizar values [0, 1]
    # Plotar no radar

# Radar: cada linha = detector, cores diferentes
# Exportar PNG com legenda clara
```

**Comando de Teste**:
```bash
python -m src.visualize_comparison_by_dataset \
    --dataset afib_paroxysmal \
    --output-dir results/comparisons/by_dataset/afib_paroxysmal/visualizations
```

---

### Script 2: `src/visualize_cross_dataset_summary.py`

**Propósito**: Gerar visualizações para análise robustez cross-dataset (3 opções)

**Input**:
- CSVs das Opções 1, 2, 3:
  - `cross_dataset_analysis/cross_dataset_generalization_option1.csv`
  - `cross_dataset_analysis/parameter_portability_option2.csv`
  - `cross_dataset_analysis/unified_robustness_option3.csv`

**Output** (4 ficheiros PNG):
```
results/comparisons/cross_dataset/
├── option1_ceiling_analysis.png       # Bar chart (6 detectores, com CV)
├── option2_portability_heatmap.png    # Heatmap 3×6 (datasets × detectores)
├── option3_unified_score_ranking.png  # Bar chart (6 detectores, score unificado)
└── production_decision_matrix.png     # Bubble chart ou decision tree visual
```

**Detalhes**:

**option1_ceiling_analysis.png**:
- X: 6 detectores
- Y: F3-weighted ceiling (mean)
- Error bars: ± std dev
- Cores: gradient (verde=bom, vermelho=fraco)
- Anotações: CV%, values

**option2_portability_heatmap.png**:
- Rows: 6 detectores
- Cols: Transferability % (média across datasets)
- Heatmap colorido: verde=95%, amarelo=70%, vermelho=45%
- Anotações: values precisos

**option3_unified_score_ranking.png**:
- X: 6 detectores (ordenado por score)
- Y: Unified Score (0.90-0.98 range)
- Cores: gradient
- Anotações: scores e rankings

**production_decision_matrix.png**:
- Bubble chart: X=ceiling F3, Y=transferability%
- Bubble size = unified score
- Cores = detector (diferentes cores)
- Quadrantes anotados:
  - Top-left: "Max Performance" (FLOSS)
  - Bottom-left: "Overkill"
  - Top-right: "Portable & Good" (ADWIN)
  - Bottom-right: "Poor"
- Anotações: nomes detectores

**Comando de Teste**:
```bash
python -m src.visualize_cross_dataset_summary \
    --output-dir results/comparisons/cross_dataset
```

---

### Script 3: `src/generate_comparison_reports.py` (Wrapper)

**Propósito**: Executar ambos scripts acima automaticamente

**Input**:
- Lista de datasets: `afib_paroxysmal`, `malignantventricular`, `vtachyarrhythmias`

**Output**:
- Todas as visualizações da Fase 2 em pastas corretas
- Atualizar/criar READMEs com referências

**Comando**:
```bash
python -m src.generate_comparison_reports \
    --datasets afib_paroxysmal malignantventricular vtachyarrhythmias \
    --output-base results/comparisons
```

---

## 📊 Checklist de Implementação

### `visualize_comparison_by_dataset.py`
- [ ] Parse de argumentos (dataset, output-dir)
- [ ] Ler CSVs de 6 detectores
- [ ] Calcular melhores configs por métrica
- [ ] Normalizar valores [0, 1]
- [ ] Gerar radar chart (matplotlib + numpy)
- [ ] Gerar scatter F3 vs FP
- [ ] Gerar heatmap métricas
- [ ] Gerar 3D tradeoffs
- [ ] Exportar PNGs com qualidade alta (dpi=300)
- [ ] Error handling + logging

### `visualize_cross_dataset_summary.py`
- [ ] Parse de argumentos
- [ ] Ler 3 CSVs de opções
- [ ] Calcular estatísticas
- [ ] Gerar option1 bar chart com CV
- [ ] Gerar option2 heatmap
- [ ] Gerar option3 ranking
- [ ] Gerar production decision matrix
- [ ] Exportar PNGs

### `generate_comparison_reports.py`
- [ ] Parse de argumentos
- [ ] Loop através de datasets
- [ ] Chamar script 1 para cada dataset
- [ ] Chamar script 2 (cross-dataset)
- [ ] Atualizar READMEs com timestamps
- [ ] Validação de outputs (ficheiros existem, não vazios)

---

## 🎨 Especificações Visuais

### Cores (Scheme Consistente)
- ADWIN: Azul
- Page-Hinkley: Verde
- KSWIN: Laranja
- HDDM_A: Vermelho
- HDDM_W: Roxo
- FLOSS: Preto/Cinzento

### Fontes & Sizing
- Título: 16pt, bold
- Axis labels: 12pt
- Anotações: 10pt
- DPI: 300 (alta qualidade para publicação)
- Figsize: (12, 8) padrão, ajustar conforme necessário

### Legends
- Fora dos eixos (right side ou bottom)
- 2 colunas se possível
- Font size: 10pt

---

## 📝 Documentação Updates

Após gerar visualizações, atualizar:

1. **`comparisons/README.md`** - Adicionar links para PNGs
2. **`comparisons/by_dataset/<dataset>/README.md`** - Descrever gráficos
3. **`comparisons/cross_dataset/README.md`** - Adicionar interpretação dos gráficos

---

## 🔄 Dependencies

```
# Já existentes (requirements.txt)
matplotlib>=3.5.0
numpy>=1.21.0
pandas>=1.3.0
seaborn>=0.11.0  # Para heatmaps

# Possível novo
plotly>=5.0  # Se quiser gráficos interativos (opcional)
```

---

## ⏱️ Estimativa de Esforço

| Script | Função | Tempo Estimado |
|--------|--------|---|
| `visualize_comparison_by_dataset.py` | 4 plots/dataset | 2-3 horas |
| `visualize_cross_dataset_summary.py` | 4 plots cross | 2-3 horas |
| `generate_comparison_reports.py` | Wrapper | 1 hora |
| Testes + Debug | QA | 1-2 horas |
| Documentação | README updates | 30 min |
| **TOTAL** | | **7-10 horas** |

---

## 🚀 Próximos Passos Imediatos

1. Rever esta lista com utilizador
2. Ajustar especificações visuais se necessário
3. Começar implementação na próxima sessão
4. Testar em `afib_paroxysmal` primeiro
5. Depois replicar para outros datasets

---

**Preparado por**: Fase 1 (Estrutura + Documentação)
**Data**: 2025-12-15
**Status**: ✅ **CONCLUÍDO**

---

## ✅ FASE 2 CONCLUÍDA

**Data de Conclusão**: 2025-12-15 16:24:43
**Duração Total**: ~45 minutos

### Entregáveis:

1. ✅ Script 1: `src/visualize_comparison_by_dataset.py` (463 linhas)
2. ✅ Script 2: `src/visualize_cross_dataset_summary.py` (329 linhas)
3. ✅ Script 3: `src/generate_comparison_reports.py` (257 linhas)
4. ✅ 16 PNG files gerados (12 by-dataset + 4 cross-dataset)
5. ✅ 7 READMEs atualizados com timestamps
6. ✅ Testes completos (100% sucesso)

**Ver detalhes completos em**: [PHASE2_COMPLETION_SUMMARY.md](./PHASE2_COMPLETION_SUMMARY.md)

