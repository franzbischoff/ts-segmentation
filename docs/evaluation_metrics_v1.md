# Critérios de Avaliação: Precision, Recall e F1-Score

## 📋 Visão Geral

Este documento descreve em detalhe os critérios utilizados para avaliar a qualidade das detecções de mudanças de regime em sinais de ECG. A implementação está localizada em `src/evaluation.py` e é utilizada por todos os módulos de avaliação do projeto.

## 🔍 Implementação Própria vs Biblioteca

**Importante**: Estamos a calcular **manualmente** o Precision, Recall e F1-Score.

- A biblioteca **scikit-multiflow** fornece apenas os detectores (ADWIN, PageHinkley, DDM)
- As métricas de avaliação são **totalmente implementadas** em `src/evaluation.py`
- O F1-Score é calculado explicitamente como média harmónica em `src/exhaustive_grid_search.py`

## 🎯 Critérios de Classificação

### True Positive (TP)

Uma detecção é considerada **True Positive** quando satisfaz **todos** os seguintes critérios:

1. **Existe um evento ground-truth** no dataset (marcador `regime_change == 1`)
2. A detecção ocorre **dentro de uma janela de tolerância** após o evento real
3. **Condição matemática**: `0 <= (sample_detecção - sample_ground_truth) <= tolerance`
4. O evento ground-truth **não foi previamente matched** por outra detecção
5. Se múltiplas detecções qualificam, escolhe-se a com **menor delay** (mais próxima)

#### Exemplo de Código

```python
# De src/evaluation.py (linhas ~27-34)
candidates = [g for g in gt_indices
              if g not in matched_gt
              and 0 <= ev.sample_index - g <= tolerance]

if candidates:
    # Escolhe o evento ground-truth mais próximo
    best = min(candidates, key=lambda g: ev.sample_index - g)
    matched_gt.add(best)
    tp += 1
```

#### Exemplo Numérico

```
Evento real (ground-truth): sample 10,000
Tolerance: 500 samples (2 segundos a 250 Hz)

Detecção em sample 10,200 → TP ✓ (delay = 200 samples, dentro da janela)
Detecção em sample 10,450 → TP ✓ (delay = 450 samples, ainda dentro)
Detecção em sample 10,550 → FP ✗ (delay = 550 samples, fora da janela)
Detecção em sample 9,950  → FP ✗ (antecipação de -50 samples, não permitido)
```

---

### False Positive (FP)

Uma detecção é considerada **False Positive** quando:

- **NÃO existe nenhum evento ground-truth** dentro da janela de tolerância após a detecção
- **OU** o evento ground-truth mais próximo **já foi matched** por outra detecção anterior

#### Exemplo de Código

```python
# De src/evaluation.py (linha ~35)
else:
    fp += 1
```

#### Cenários Típicos de FP

1. **Ruído do sinal**: Detector reage a artefactos ou variações normais
2. **Transições entre registos**: Mudança de baseline ao concatenar múltiplos pacientes
3. **Parâmetros muito sensíveis**: `delta` muito baixo gera detecções espúrias
4. **Detecção tardia**: Delay > tolerance (passou do prazo)
5. **Detecção antecipada**: Antes do evento começar (impossível em streaming real)

---

### False Negative (FN)

Um evento ground-truth é considerado **False Negative** quando:

- **Nenhuma detecção** foi associada (matched) a esse evento
- Ou seja, eventos reais que o detector **falhou em identificar**

#### Exemplo de Código

```python
# De src/evaluation.py (linha ~37)
fn = len(gt_indices) - len(matched_gt)
```

#### Cenários Típicos de FN

1. **Parâmetros pouco sensíveis**: `delta` muito alto não reage a mudanças sutis
2. **Janela de média móvel grande**: Suavização excessiva mascara o evento
3. **Min-gap muito alto**: Suprime detecções próximas a eventos anteriores
4. **Mudanças graduais**: Transições lentas que não ultrapassam o threshold
5. **Eventos de curta duração**: Regimes muito breves não geram sinal suficiente

---

## 📐 Fórmulas Matemáticas

### Precision (Precisão)

$$
\text{Precision} = \frac{\text{TP}}{\text{TP} + \text{FP}}
$$

**Interpretação**: "Das detecções que fiz, quantas estavam corretas?"

- **Alta Precision**: Poucas detecções incorretas (baixo FP)
- **Baixa Precision**: Muitos falsos alarmes (alto FP)

```python
# De src/evaluation.py (linha ~38)
precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
```

---

### Recall (Sensibilidade)

$$
\text{Recall} = \frac{\text{TP}}{\text{TP} + \text{FN}}
$$

**Interpretação**: "Dos eventos reais que existiam, quantos consegui detectar?"

- **Alto Recall**: Poucos eventos perdidos (baixo FN)
- **Baixo Recall**: Muitos eventos não detectados (alto FN)

```python
# De src/evaluation.py (linha ~39)
recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
```

---

### F1-Score

$$
\text{F1} = 2 \times \frac{\text{Precision} \times \text{Recall}}{\text{Precision} + \text{Recall}}
$$

**Interpretação**: Média harmónica entre Precision e Recall (balanceamento)

- **F1 alto**: Bom equilíbrio entre precisão e sensibilidade
- **F1 baixo**: Pelo menos uma métrica está comprometida

```python
# De src/exhaustive_grid_search.py (linha ~68)
f1 = (2 * precision * recall / (precision + recall)) if (precision + recall) > 0 else 0.0
```

**Nota**: Usamos média harmónica (não aritmética) porque penaliza mais fortemente quando uma das métricas é muito baixa.

---

## ⚙️ Parâmetro Crítico: Tolerance

### Definição

O parâmetro `tolerance` define a **janela de aceitação temporal** para considerar uma detecção como válida.

- **Default**: 500 samples (≈ 2 segundos a 250 Hz)
- **Unidade**: número de samples
- **Direção**: apenas **APÓS** o evento (não aceita antecipações)

### Impacto nos Resultados

```
tolerance = 250 samples (1 segundo)
├─ Mais rigoroso
├─ Menos TPs (muitas detecções caem fora da janela)
├─ Mais FPs (detecções tardias não contam)
└─ Precision pode subir, Recall tende a cair

tolerance = 1000 samples (4 segundos)
├─ Mais permissivo
├─ Mais TPs (janela maior captura mais detecções)
├─ Menos FPs (mais detecções se tornam válidas)
└─ Recall pode subir, Precision tende a cair
```

### Configuração por Comando

```bash
# Tolerance rigoroso (1 segundo)
python -m src.streaming_detector \
  --tolerance 250 \
  --sample-rate 250 \
  ...

# Tolerance permissivo (4 segundos)
python -m src.streaming_detector \
  --tolerance 1000 \
  --sample-rate 250 \
  ...
```

---

## 🔄 Fluxo Completo de Avaliação

### 1. Detecção (src/streaming_detector.py)

```python
# Detector ADWIN processa sinal sample-by-sample
for idx, row in df.iterrows():
    value = row['ecg']
    detector.add_element(value)
    if detector.detected_change():
        events.append(DetectionEvent(
            detector='adwin',
            sample_index=idx,
            time_seconds=idx / sample_rate
        ))
```

### 2. Avaliação (src/evaluation.py)

```python
# Comparar detecções com ground-truth
metrics = evaluate_detections(
    events=events,
    df=df,
    sample_rate=250,
    tolerance=500
)
# Retorna: tp, fp, fn, precision, recall, mean_delay
```

### 3. Cálculo do F1 (src/exhaustive_grid_search.py)

```python
# Extrair métricas
precision = metrics.get('precision', 0.0)
recall = metrics.get('recall', 0.0)

# Calcular F1 manualmente
f1 = (2 * precision * recall / (precision + recall)) if (precision + recall) > 0 else 0.0
```

---

## ⚠️ Considerações Importantes

### 1. Assimetria Temporal (Só Aceita Detecções APÓS)

```python
# Condição: 0 <= delay <= tolerance
0 <= (sample_detecção - sample_ground_truth) <= tolerance
```

**Justificativa**: Em processamento streaming real, é **impossível** detectar um evento antes dele começar. Detecções antecipadas são sempre consideradas FP, mesmo que próximas ao evento.

**Exemplo**:
```
Evento real: sample 10,000
Detecção em 9,995 → FP (antecipação de -5 samples)
Detecção em 10,005 → TP candidato (delay = 5 samples)
```

---

### 2. Estratégia de Matching (Guloso)

O algoritmo processa detecções **ordenadas cronologicamente** e cada detecção procura o evento ground-truth **mais próximo** ainda disponível.

**Implicação**: Uma detecção pode "roubar" um match de outra detecção posterior.

#### Exemplo de Matching Guloso

```
Ground-truth: samples [1000, 2000]
Detecções: [1100, 1900, 2100]

Processo:
1. Detecção 1100 → match com GT 1000 (delay=100) → TP
2. Detecção 1900 → match com GT 2000 (delay=-100, antecipação) → FP
3. Detecção 2100 → GT 2000 já matched → FP

Resultado: 1 TP, 2 FP, 0 FN
```

**Alternativa possível**: Matching ótimo (Hungarian algorithm) — não implementado atualmente.

---

### 3. Impacto do Pré-processamento

As detecções são avaliadas **APÓS** aplicação de:

1. **Média móvel** (`ma_window`): Suaviza o sinal
2. **Min-gap** (`min_gap_samples`): Suprime detecções muito próximas
3. **Derivada** (opcional): Detecta mudanças de gradiente

Estes filtros afetam **quando** as detecções ocorrem, impactando o delay e consequentemente as métricas.

---

### 4. Limitações Conhecidas

#### a) Concatenação de Múltiplos Pacientes

Quando processamos múltiplos registos concatenados (coluna `id`), podem surgir FPs nas transições:

```
Registo A (fim)  |  Registo B (início)
   ... 1.2, 1.1  |  0.8, 0.7, ...
                 ↑
            Mudança de baseline
            (pode gerar FP)
```

**Solução implementada**: `exhaustive_grid_search.py` processa **per-file** (cada `id` separadamente).

#### b) Eventos Muito Próximos

Se dois eventos ground-truth ocorrem com gap < `min_gap_samples`, a segunda detecção pode ser suprimida, gerando FN.

```
Ground-truth: [1000, 2000] samples
min_gap = 1500 samples

Detector gera: [1100, ?]
Segunda detecção suprimida (gap 900 < 1500)
Resultado: 1 TP, 1 FN
```

#### c) Eventos de Curta Duração

Regimes muito breves podem não gerar sinal suficiente para o detector ultrapassar o threshold, especialmente com janelas de média móvel grandes.

---

## 📊 Interpretação de Resultados Típicos

### Cenário 1: Alta Precision, Baixo Recall

```
Precision: 0.85
Recall: 0.30
F1: 0.44
```

**Interpretação**: O detector é **conservador**. Quando deteta algo, geralmente está correto, mas perde muitos eventos reais.

**Possíveis causas**:
- `delta` muito alto (pouco sensível)
- `ma_window` muito grande (suavização excessiva)
- `min_gap` muito alto (suprime detecções válidas)

---

### Cenário 2: Baixa Precision, Alto Recall

```
Precision: 0.25
Recall: 0.80
F1: 0.38
```

**Interpretação**: O detector é **agressivo**. Captura a maioria dos eventos reais, mas gera muitos falsos alarmes.

**Possíveis causas**:
- `delta` muito baixo (hipersensível)
- `ma_window` muito pequeno (não filtra ruído)
- Ruído no sinal ou artefactos frequentes

---

### Cenário 3: Balanceado

```
Precision: 0.60
Recall: 0.65
F1: 0.62
```

**Interpretação**: Compromisso razoável entre precisão e sensibilidade. Típico de parâmetros bem ajustados.

---

### Cenário 4: Ambos Baixos

```
Precision: 0.20
Recall: 0.15
F1: 0.17
```

**Interpretação**: Detector falhando sistematicamente. Pode indicar:
- Parâmetros completamente desajustados
- Sinal muito ruidoso ou atípico
- Eventos ground-truth mal rotulados
- Incompatibilidade entre detector e tipo de mudança

---

## 🎯 Parâmetros Ótimos Encontrados (Baseline)

Segundo `exhaustive_grid_search.py` (385 combinações testadas):

```python
# Melhor configuração global (média de 3 pacientes)
delta = 0.08
ma_window = 175
min_gap_samples = 3000

# Performance: F1 = 0.217 ± 0.202
```

**Comando para reproduzir**:
```bash
python -m src.streaming_detector \
  --data data/afib_paroxysmal_tidy.csv \
  --detector adwin \
  --ma-window 175 \
  --min-gap-samples 3000 \
  --param delta=0.08 \
  --tolerance 500 \
  --sample-rate 250
```

---

## 💡 Sugestões de Melhoria Futura

### 1. Tolerance Adaptativo

```python
# Tolerance baseado na duração esperada do regime
tolerance = min(500, expected_regime_duration * 0.1)
```

### 2. Janela Bilateral

```python
# Aceitar pequenas antecipações (ex: ±50 samples)
-50 <= (sample_detecção - sample_ground_truth) <= 500
```

### 3. Matching Ótimo (Hungarian Algorithm)

```python
from scipy.optimize import linear_sum_assignment

# Encontrar assignment ótimo global entre detecções e ground-truth
cost_matrix = compute_distances(detections, ground_truth)
row_ind, col_ind = linear_sum_assignment(cost_matrix)
```

### 4. Múltiplos Níveis de Tolerance

```python
# Avaliar com três níveis simultaneamente
metrics_strict = evaluate_detections(..., tolerance=250)   # 1s
metrics_medium = evaluate_detections(..., tolerance=500)   # 2s
metrics_loose = evaluate_detections(..., tolerance=1000)   # 4s
```

### 5. Penalização por Delay no F1

```python
# F1 ponderado pelo delay médio
delay_penalty = 1 / (1 + mean_delay / tolerance)
f1_weighted = f1 * delay_penalty
```

---

## 📚 Referências no Código

- **Implementação principal**: `src/evaluation.py` (função `evaluate_detections`)
- **Uso no grid search**: `src/exhaustive_grid_search.py` (linhas 60-80)
- **Uso no detector streaming**: `src/streaming_detector.py` (chamada na linha final)
- **Documentação do projeto**: `README.md` (seção de avaliação)

---

## 🔗 Comandos Úteis

### Testar com diferentes tolerances

```bash
# Teste rigoroso (1 segundo)
python -m src.streaming_detector \
  --data data/small_test.csv \
  --detector adwin \
  --tolerance 250 \
  --param delta=0.01

# Teste permissivo (4 segundos)
python -m src.streaming_detector \
  --data data/small_test.csv \
  --detector adwin \
  --tolerance 1000 \
  --param delta=0.01
```

### Verificar distribuição de delays

```python
import pandas as pd
from src.evaluation import evaluate_detections

# Após executar detecções
metrics = evaluate_detections(events, df, sample_rate=250, tolerance=500)
print(f"Delay médio: {metrics['mean_delay_samples']} samples")
print(f"Delay médio: {metrics['mean_delay_seconds']:.3f} segundos")
```

---

**Documento criado em**: 2025-10-30
**Última atualização**: 2025-10-30
**Versão do código**: Commit atual (main branch)
