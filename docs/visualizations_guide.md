# Guia de Visualizações do Grid Search

Este documento descreve as visualizações geradas pelo script `src/visualize_results.py` para análise dos resultados do grid search de parâmetros.

## Geração das Visualizações

```bash
python -m src.visualize_results \
    --metrics results/metrics_comprehensive_with_nab.csv \
    --output-dir results/visualizations
```

## Gráficos Produzidos

### 1. Precision-Recall Scatter Plots
**Arquivo**: `pr_scatter_plots.png`

**Descrição**: Dois painéis lado a lado mostrando trade-offs Precision vs Recall.

**Detalhes**:
- **Painel Esquerdo**: Recall@4s vs Precision@4s (janela de 4 segundos)
- **Painel Direito**: Recall@10s vs Precision@10s (janela de 10 segundos)
- Cada ponto = uma combinação (delta, ma_window, min_gap_samples)
- Cor do ponto = Score F3-weighted (escala viridis: roxo→verde→amarelo)
- Estrela vermelha = melhor configuração F3-weighted

**Como interpretar**:
- Ideal: canto superior direito (alta precision + alta recall)
- Cores quentes (amarelo/verde) indicam melhores F3 scores
- Comparar janelas 4s vs 10s mostra impacto de tolerância temporal
- Clusters de pontos revelam regiões viáveis do espaço de parâmetros

**Uso típico**:
Primeira visualização para entender landscape geral de performance e identificar se há trade-off claro ou configurações dominantes.

---

### 2. Pareto Front
**Arquivo**: `pareto_front.png`

**Descrição**: Fronteira de Pareto para otimização multi-objetivo.

**Detalhes**:
- **Eixo X**: Recall@10s (↑ melhor)
- **Eixo Y**: Falsos Positivos por minuto (↓ melhor)
- Pontos pequenos cinza/coloridos = soluções dominadas
- Pontos grandes com borda vermelha = soluções Pareto-ótimas
- Linha tracejada vermelha conecta a fronteira

**Como interpretar**:
- Soluções na fronteira são não-dominadas (não há outra solução melhor em ambos objetivos)
- "Joelho da curva" = melhor compromisso balanceado
- Escolha na fronteira depende da aplicação:
  - Alta recall + tolerância a FP → ponto à direita
  - Baixo FP + recall moderado → ponto à esquerda
- Número de soluções Pareto-ótimas indicado no canto superior esquerdo

**Uso típico**:
Identificar conjunto de configurações ótimas para diferentes cenários clínicos/operacionais.

---

### 3. Parameter Heatmaps
**Arquivos**:
- `heatmap_f3-weighted.png`
- `heatmap_nab-score-standard.png`
- `heatmap_recall-10s.png`
- `heatmap_fp-per-min.png`

**Descrição**: Mapas de calor 2D mostrando efeito de delta × ma_window.

**Detalhes**:
- **Linhas**: Valores de `delta` (threshold do detector)
- **Colunas**: Valores de `ma_window` (janela média móvel)
- **Painéis**: Diferentes valores de `min_gap_samples` (top 3)
- **Cor**: Valor da métrica (vermelho→amarelo→verde para maximize; invertido para FP/min)
- **Anotações**: Valor numérico em cada célula

**Como interpretar**:
- Regiões quentes = melhores configurações
- Gradientes suaves = robustez (pequenas variações não afetam muito)
- Picos isolados = configuração frágil (evitar)
- Comparar painéis mostra interação com min_gap_samples

**Uso típico**:
Fine-tuning de parâmetros após identificar região promissora. Verificar se configuração ótima é robusta ou sensível.

---

### 4. Score Distributions
**Arquivo**: `score_distributions.png`

**Descrição**: Quatro box plots comparando distribuições de métricas.

**Detalhes**:
- **Painel Superior Esquerdo**: F1/F3 Weighted vs Classic
- **Painel Superior Direito**: NAB Standard/Low FP/Low FN
- **Painel Inferior Esquerdo**: Recall@4s vs Recall@10s
- **Painel Inferior Direito**: FP/min (eixo esquerdo, azul) e EDD (eixo direito, vermelho)

**Como interpretar**:
- Caixa central = quartis (Q1, mediana, Q3)
- Bigodes = extensão até 1.5×IQR
- Pontos externos = outliers
- Mediana (linha central) = valor típico
- Altura da caixa = variabilidade entre configurações

**Comparações úteis**:
- F-weighted vs F-classic: impacto da ponderação temporal
- NAB profiles: sensibilidade a FP vs FN
- Recall@4s vs @10s: benefício de janela maior
- FP/min vs EDD: trade-off velocidade vs alarmes falsos

**Uso típico**:
Entender variabilidade e centralidade das métricas. Identificar se há configurações outliers excepcionalmente boas/más.

---

### 5. 3D Trade-off Surface
**Arquivo**: `3d_tradeoff.png`

**Descrição**: Scatter plot 3D mostrando trade-off triplo.

**Detalhes**:
- **Eixo X**: Recall@10s (↑ melhor)
- **Eixo Y**: Falsos Positivos por minuto (↓ melhor)
- **Eixo Z**: EDD median em segundos (↓ melhor)
- **Cor**: Score F3-weighted
- **Estrela vermelha**: Melhor configuração F3

**Como interpretar**:
- Ideal: alto X, baixo Y, baixo Z (canto frontal inferior direito)
- Clusters 3D revelam configurações similares
- Cores quentes em posições favoráveis = configurações excelentes
- Visualização rotativa ajuda a identificar relações escondidas

**Uso típico**:
Análise exploratória avançada quando trade-offs binários não são suficientes. Identificar se existe "sweet spot" no espaço 3D.

---

### 6. Parameter Sensitivity
**Arquivo**: `parameter_sensitivity.png`

**Descrição**: Gráficos de linha mostrando sensibilidade de métricas a parâmetros.

**Detalhes**:
- **Layout**: 2 linhas × 3 colunas
- **Linhas**: F3-weighted (cima) e Recall@10s (baixo)
- **Colunas**: delta / ma_window / min_gap_samples
- **Linha**: Média da métrica
- **Área sombreada**: ± 1 desvio padrão
- **Eixo X log-scale**: Para ma_window (valores variam ordem de magnitude)

**Como interpretar**:
- **Inclinação acentuada**: Parâmetro tem forte impacto (crítico para tuning)
- **Linha plana**: Parâmetro tem pouco efeito (robusto)
- **Área sombreada ampla**: Alta variabilidade entre ficheiros/pacientes
- **Picos/vales**: Valores ótimos do parâmetro

**Insights típicos**:
- `delta`: Geralmente trade-off (baixo → alta recall + alto FP)
- `ma_window`: Pode ter ponto ótimo (muito baixo = ruído, muito alto = atraso)
- `min_gap_samples`: Reduz FP mas pode reduzir recall se mudanças próximas

**Uso típico**:
Entender mecanismo de cada parâmetro. Priorizar tuning dos parâmetros com maior impacto. Validar se comportamento é monotônico ou tem máximo local.

---

## Workflow Recomendado de Análise

### 1. Visão Geral (10 min)
1. Abrir `pr_scatter_plots.png` → Entender trade-offs básicos
2. Abrir `score_distributions.png` → Ver ranges e variabilidade
3. Abrir `pareto_front.png` → Identificar quantas soluções viáveis

### 2. Exploração de Parâmetros (20 min)
4. Abrir `parameter_sensitivity.png` → Identificar parâmetros críticos
5. Abrir `heatmap_f3-weighted.png` → Localizar regiões ótimas
6. Comparar heatmaps de diferentes métricas → Verificar consenso

### 3. Análise Avançada (15 min)
7. Abrir `3d_tradeoff.png` → Visualizar trade-offs complexos
8. Abrir `heatmap_nab-score-standard.png` → Comparar com F3
9. Consultar `pareto_front.png` novamente → Selecionar configuração final

### 4. Validação e Decisão (10 min)
10. Listar top 3-5 configurações da fronteira de Pareto
11. Verificar robustez nos heatmaps (regiões amplas vs picos isolados)
12. Considerar requisitos da aplicação (FP vs FN criticality)
13. Documentar escolha final com justificativa

---

## Interpretação de Cores

**Mapas de Calor**:
- Verde/Amarelo: Bom (para métricas a maximizar)
- Vermelho/Laranja: Mau
- Invertido para FP/min (vermelho = alto FP = mau)

**Scatter Plots**:
- Viridis (roxo→azul→verde→amarelo): Score F3
  - Roxo/azul: Scores baixos
  - Verde/amarelo: Scores altos

**Box Plots**:
- Azul: FP/min
- Vermelho/coral: EDD
- Padrão matplotlib para outros

---

## Personalização

Para modificar visualizações, edite `src/visualize_results.py`:

**Adicionar nova métrica ao heatmap**:
```python
# Na função plot_parameter_heatmaps(), adicionar à lista metrics
metrics.append(('sua_metrica_mean', 'Título da Métrica'))
```

**Mudar esquema de cores**:
```python
# Trocar 'viridis' por 'RdYlGn', 'coolwarm', 'plasma', etc.
cmap='RdYlGn'
```

**Ajustar DPI para publicação**:
```python
# Aumentar DPI para imagens de alta resolução
plt.savefig(output_path, dpi=600, bbox_inches='tight')
```

**Desabilitar gráfico específico**:
```python
# Comentar linha no main()
# plot_3d_tradeoff(df, output_dir)
```

---

## Requisitos Técnicos

**Dependências**:
- matplotlib >= 3.10
- seaborn >= 0.12
- pandas >= 1.5
- numpy >= 1.23

**Recursos**:
- ~500 MB RAM (para 113k avaliações)
- ~30 segundos de processamento
- ~4.5 MB de imagens PNG (300 DPI)

**Formatos de Saída**:
- PNG (default, 300 DPI)
- Para vetorial: trocar `.png` por `.svg` ou `.pdf`

---

## Perguntas Frequentes

**P: Por que alguns gráficos mostram @4s e outros @10s?**
R: 4s e 10s são janelas de tolerância temporal definidas nas métricas F-weighted. 4s = detecção ideal, 10s = aceitável.

**P: O que significa um score NAB negativo?**
R: Em dados streaming com ruído, scores NAB negativos são comuns. Foco deve ser na **comparação relativa** entre configurações (menos negativo = melhor).

**P: Como escolher entre melhor F3 e melhor NAB?**
R: F3-weighted é otimizado para recall com peso temporal. NAB é mais sensível a FP. Se FP são críticos, preferir NAB Low FP. Para não perder eventos, usar F3 ou NAB Low FN.

**P: Quantas configurações Pareto-ótimas são normais?**
R: Depende do grid. Com 495 combinações, ter 10-50 soluções na fronteira é típico. Menos que 5 sugere poucos trade-offs reais.

**P: Posso comparar visualizações de diferentes datasets?**
R: Sim, mas escalas podem variar. Recomenda-se normalizar eixos ou usar mesma faixa de cores para comparação justa.

---

## Exemplos de Insights

**Cenário 1: Heatmap mostra "ilha" de scores altos**
→ Configuração muito específica (frágil). Testar com mais variações ao redor.

**Cenário 2: Pareto front é linear**
→ Trade-off claro e proporcional entre Recall e FP. Escolha depende linearmente da tolerância.

**Cenário 3: Pareto front tem "joelho" pronunciado**
→ Ponto de mudança de regime no trade-off. Configuração no joelho geralmente é ótima.

**Cenário 4: Parameter sensitivity mostra linha plana para delta**
→ Detector não é sensível a delta no range testado. Expandir range ou testar outro detector.

**Cenário 5: 3D plot mostra cluster isolado com cores quentes**
→ Região ótima clara. Investigar quais parâmetros levam a esse cluster.

---

## Referências

- Seaborn heatmaps: https://seaborn.pydata.org/generated/seaborn.heatmap.html
- Matplotlib 3D: https://matplotlib.org/stable/gallery/mplot3d/
- Pareto optimization: https://en.wikipedia.org/wiki/Pareto_efficiency
- NAB scoring: https://github.com/numenta/NAB

---

**Última atualização**: 2025-11-13
**Versão**: 1.0
