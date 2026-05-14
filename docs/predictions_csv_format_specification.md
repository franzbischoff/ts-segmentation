# Especificação do Formato CSV `predictions_intermediate.csv`

Este documento descreve o formato exato do ficheiro CSV `predictions_intermediate.csv` usado na pipeline (gerado por `src.generate_predictions`, frequentemente via scripts `scripts/generate_*.sh`, e, no caso de FLOSS, por integração externa em R).

## Estrutura Geral

O CSV deve ter:
- **Separador**: vírgula (`,`)
- **Encoding**: UTF-8
- **Cabeçalho**: linha 1 contém nomes das colunas
- **Index**: NÃO incluir coluna de índice (usar `index=False` em pandas)
- **Aspas**: apenas quando necessário para listas ou strings com vírgulas

## ⚠️ Colunas Opcionais vs Obrigatórias

### ✅ Colunas OBRIGATÓRIAS (mínimo necessário):

1. **Identificação**: `record_id`, `detector`
2. **Parâmetros do detector**: variável por detector (ex: `delta`, `ma_window`, `min_gap_samples`)
3. **Duração do sinal**: `duration_seconds` (usado no cálculo de FP/min)
4. **Ground truth**: `gt_times` (tempos em segundos)
5. **Deteções**: `det_times` (tempos em segundos)
6. **Contagens**: `n_detections`, `n_ground_truth`

### ⚠️ Colunas OPCIONAIS (úteis mas não essenciais):

- `duration_samples` - Útil para metadados, mas pode ser recalculado (`duration_seconds * 250`)
- `processing_time` - Apenas para estatísticas de desempenho de geração
- `error` - Apenas para registar erros durante geração

### ❌ Colunas REDUNDANTES (podem ser omitidas):

- `gt_indices` - Redundante, já temos `gt_times` (conversão: `gt_times = gt_indices / 250`)
- `det_indices` - Redundante, já temos `det_times` (conversão: `det_times = det_indices / 250`)

**Nota**: As especificações abaixo mostram o formato COMPLETO usado pelo Python. No R, você pode omitir as colunas redundantes/opcionais.

## Compatibilidade com a Pipeline Atual

- A pipeline de avaliação usa **nomes de colunas** (não posição), portanto a ordem das colunas **não é requisito funcional**.
- O que precisa estar correto é: nomes das colunas esperadas, tipos compatíveis e listas parseáveis em `gt_times`/`det_times`.
- O formato completo por detector abaixo é uma **referência recomendada** para reprodutibilidade e interoperabilidade, não uma exigência rígida de ordem.

## Formato por Detector

### ADWIN

**Formato completo de referência (14 colunas):**

```
record_id,detector,delta,ma_window,min_gap_samples,duration_samples,duration_seconds,gt_indices,gt_times,det_indices,det_times,n_detections,n_ground_truth,processing_time
```

**Exemplo de linha de dados:**
```
data_101_1.par,adwin,0.005,10,1000,145971,583.884,[70599],[282.396],"[799, 2463, 3839]","[3.196, 9.852, 15.356]",3,1,3.335204839706421
```

---

### Page-Hinkley

**Formato completo de referência (16 colunas):**

```
record_id,detector,lambda_,delta,alpha,ma_window,min_gap_samples,duration_samples,duration_seconds,gt_indices,gt_times,det_indices,det_times,n_detections,n_ground_truth,processing_time
```

**Diferenças em relação ao ADWIN:**
- 3 parâmetros adicionais ANTES de `ma_window`: `lambda_`, `delta`, `alpha`
- Resto da estrutura idêntica

---

### KSWIN

**Formato completo de referência (16 colunas + `error` opcional):**

```
record_id,detector,alpha,window_size,stat_size,ma_window,min_gap_samples,duration_samples,duration_seconds,gt_indices,gt_times,det_indices,det_times,n_detections,n_ground_truth,processing_time,error
```

**Diferenças:**
- 3 parâmetros ANTES de `ma_window`: `alpha`, `window_size`, `stat_size`
- **Coluna opcional no final**: `error` (vazia se não houver erro, ou mensagem de erro se houver)

---

### HDDM_A

**Formato completo de referência (16 colunas):**

```
record_id,detector,drift_confidence,warning_confidence,two_side_option,ma_window,min_gap_samples,duration_samples,duration_seconds,gt_indices,gt_times,det_indices,det_times,n_detections,n_ground_truth,processing_time
```

**Diferenças:**
- 3 parâmetros ANTES de `ma_window`: `drift_confidence`, `warning_confidence`, `two_side_option`

---

### HDDM_W

**Formato completo de referência (17 colunas):**

```
record_id,detector,drift_confidence,warning_confidence,lambda_option,two_side_option,ma_window,min_gap_samples,duration_samples,duration_seconds,gt_indices,gt_times,det_indices,det_times,n_detections,n_ground_truth,processing_time
```

**Diferenças em relação ao HDDM_A:**
- 1 parâmetro adicional: `lambda_option` (entre `warning_confidence` e `two_side_option`)

---

## Descrição Detalhada das Colunas

### Colunas Comuns a Todos os Detectores

| Coluna | Tipo | Obrigatória? | Descrição | Exemplo |
|--------|------|--------------|-----------|---------|
| `record_id` | string | ✅ SIM | Identificador único do ficheiro/sinal | `data_101_1.par` |
| `detector` | string | ✅ SIM | Nome do detector usado | `adwin`, `page_hinkley`, `kswin`, `hddm_a`, `hddm_w`, `floss` |
| `duration_samples` | integer | ⚠️ OPCIONAL | Duração do sinal em número de amostras (pode ser calculado: `duration_seconds * 250`) | `145971` |
| `duration_seconds` | float | ✅ SIM | Duração do sinal em segundos (usado no cálculo de FP/min) | `583.884` |
| `gt_indices` | lista de int | ❌ REDUNDANTE | Índices das mudanças verdadeiras (**pode omitir**, use `gt_times`) | `[70599]` |
| `gt_times` | lista de float | ✅ SIM | Tempos em segundos das mudanças verdadeiras (calculado: `gt_indices / 250`) | `[282.396]` |
| `det_indices` | lista de int | ❌ REDUNDANTE | Índices das deteções (**pode omitir**, use `det_times`) | `[799, 2463, 3839, 5119]` |
| `det_times` | lista de float | ✅ SIM | Tempos em segundos das deteções (calculado: `det_indices / 250`) | `[3.196, 9.852, 15.356, 20.476]` |
| `n_detections` | integer | ✅ SIM | Número total de deteções (deve ser = length(`det_times`)) | `68` |
| `n_ground_truth` | integer | ✅ SIM | Número total de mudanças verdadeiras (deve ser = length(`gt_times`)) | `1` |
| `processing_time` | float | ❌ OPCIONAL | Tempo de processamento em segundos (apenas para estatísticas) | `3.335204839706421` |

**Conversão de Índices para Tempos:**
- `gt_times` (segundos) = `gt_indices` (amostras) / 250 Hz
- `det_times` (segundos) = `det_indices` (amostras) / 250 Hz
- Exemplo: índice 70599 → 70599/250 = 282.396 segundos

**Nota sobre FLOSS**:
- FLOSS é integrado externamente (R/projeto `false.alarm`) e não é produzido por `src/generate_predictions.py`.
- O formato CSV continua o mesmo para consumo da pipeline de avaliação.

### Colunas de Parâmetros Específicos

#### ADWIN
| Coluna | Tipo | Descrição | Valores Típicos |
|--------|------|-----------|-----------------|
| `delta` | float | Confiança do detector | `0.005`, `0.01`, `0.015`, `0.02`, `0.025`, `0.03`, `0.04`, `0.05`, `0.06`, `0.08`, `0.1` |
| `ma_window` | integer | Janela de média móvel | `10`, `25`, `50`, `75`, `100`, `150`, `200`, `250`, `300` |
| `min_gap_samples` | integer | Mínimo de amostras entre deteções | `1000`, `2000`, `3000`, `4000`, `5000` |

#### Page-Hinkley
| Coluna | Tipo | Descrição | Valores Típicos |
|--------|------|-----------|-----------------|
| `lambda_` | integer/float | Threshold (limiar) | `10`, `30`, `50`, `80` |
| `delta` | float | Permissiveness (tolerância) | `0.005`, `0.01`, `0.02`, `0.04` |
| `alpha` | float | Forgetting factor (fator de esquecimento) | `0.9999`, `0.99` |
| `ma_window` | integer | Janela de média móvel | `10`, `50`, `200` |
| `min_gap_samples` | integer | Mínimo de amostras entre deteções | `500`, `1000`, `2000`, `4000` |

#### KSWIN
| Coluna | Tipo | Descrição | Valores Típicos |
|--------|------|-----------|-----------------|
| `alpha` | float | Nível de significância | `0.001`, `0.005`, `0.01`, `0.05` |
| `window_size` | integer | Tamanho da janela de referência | `50`, `100`, `200`, `500` |
| `stat_size` | integer | Tamanho da janela estatística | `20`, `30`, `50`, `100` |
| `ma_window` | integer | Janela de média móvel (1 = sem suavização) | `1`, `10`, `50`, `100` |
| `min_gap_samples` | integer | Mínimo de amostras entre deteções | `500`, `1000`, `2000`, `3000`, `5000` |

#### HDDM_A
| Coluna | Tipo | Descrição | Valores Típicos |
|--------|------|-----------|-----------------|
| `drift_confidence` | float | Nível de confiança para drift | `0.0001`, `0.0005`, `0.001`, `0.005` |
| `warning_confidence` | float | Nível de confiança para aviso | `0.001`, `0.005`, `0.01`, `0.05` |
| `two_side_option` | boolean | Teste bilateral ou unilateral | `True`, `False` |
| `ma_window` | integer | Janela de média móvel (1 = sem suavização) | `1`, `10`, `50`, `100` |
| `min_gap_samples` | integer | Mínimo de amostras entre deteções | `500`, `1000`, `2000`, `3000`, `5000` |

#### HDDM_W
| Coluna | Tipo | Descrição | Valores Típicos |
|--------|------|-----------|-----------------|
| `drift_confidence` | float | Nível de confiança para drift | `0.0001`, `0.0005`, `0.001`, `0.005` |
| `warning_confidence` | float | Nível de confiança para aviso | `0.001`, `0.005`, `0.01`, `0.05` |
| `lambda_option` | float | Fator de ponderação | `0.01`, `0.05`, `0.1`, `0.2` |
| `two_side_option` | boolean | Teste bilateral ou unilateral | `True`, `False` |
| `ma_window` | integer | Janela de média móvel (1 = sem suavização) | `1`, `10`, `50`, `100` |
| `min_gap_samples` | integer | Mínimo de amostras entre deteções | `500`, `1000`, `2000`, `3000`, `5000` |

#### FLOSS (Integração Externa)
| Coluna | Tipo | Descrição | Valores Típicos |
|--------|------|-----------|-----------------|
| `window_size` | integer | Tamanho da janela do FLOSS | `25`, `50`, `100`, ... |
| `regime_threshold` | float | Limiar de mudança de regime | `0.05`, `0.1`, ... |
| `regime_landmark` | float | Landmark para segmentação de regime | `2.0`, `5.0`, ... |
| `min_gap_samples` | integer | Mínimo de amostras entre deteções | `200`, `500`, `1000`, ... |

---

## Formato de Listas em CSV

**IMPORTANTE**: As listas devem ser representadas em formato Python/JSON:

### Listas Curtas (sem vírgulas internas - sem aspas)
```
[70599]
[282.396]
```

### Listas Longas (com vírgulas internas - COM aspas duplas)
```
"[799, 2463, 3839, 5119, 6399]"
"[3.196, 9.852, 15.356, 20.476, 25.596]"
```

### Listas Vazias (quando não há deteções ou ground truth)
```
[]
```

**Regra Geral**: Se a lista contém vírgulas internas, deve estar entre aspas duplas (`"[...]"`). Se não contém vírgulas (lista vazia `[]` ou lista de um elemento `[123]`), não precisa de aspas.

---

## Tipos de Dados Esperados

| Tipo | Formato CSV | Exemplo em Python | Exemplo em R |
|------|-------------|-------------------|--------------|
| string | texto | `"data_101_1.par"` | `"data_101_1.par"` |
| integer | número inteiro | `145971` | `145971L` |
| float | número decimal | `583.884` ou `3.335204839706421` | `583.884` |
| boolean | True/False | `True` ou `False` | `TRUE` ou `FALSE` |
| lista de int | `[1,2,3]` ou `"[1,2,3]"` | `[799, 2463, 3839]` | `c(799, 2463, 3839)` |
| lista de float | `[1.0,2.0]` ou `"[1.0,2.0]"` | `[3.196, 9.852]` | `c(3.196, 9.852)` |

---

## Conversão de Listas (Python → CSV → R)

### Em Python (ao gerar CSV):
```python
import pandas as pd

# Listas são convertidas automaticamente para string
df = pd.DataFrame({
    'det_indices': [[799, 2463, 3839]],
    'det_times': [[3.196, 9.852, 15.356]]
})

# pandas.to_csv() automaticamente adiciona aspas quando necessário
df.to_csv('output.csv', index=False)
```

### No CSV resultante:
```
det_indices,det_times
"[799, 2463, 3839]","[3.196, 9.852, 15.356]"
```

### Em R (ao ler CSV):
```r
library(jsonlite)
library(tidyverse)

# Ler CSV
df <- read_csv('output.csv')

# Converter strings de listas para vetores reais
df <- df %>%
  mutate(
    det_indices = map(det_indices, ~ fromJSON(.x)),
    det_times = map(det_times, ~ fromJSON(.x))
  )
```

**ALTERNATIVA em R sem jsonlite:**
```r
# Parsing manual (mais robusto)
parse_python_list <- function(s) {
  if (is.na(s) || s == "[]") return(numeric(0))
  s <- gsub("\\[|\\]", "", s)  # Remove [ e ]
  as.numeric(strsplit(s, ",")[[1]])
}

df <- df %>%
  mutate(
    det_indices = map(det_indices, parse_python_list),
    det_times = map(det_times, parse_python_list)
  )
```

---

## Validação de Dados

### Regras de Validação Obrigatórias:

1. **`record_id`** nunca pode ser vazio
2. **`detector`** deve ser um de: `adwin`, `page_hinkley`, `kswin`, `hddm_a`, `hddm_w`, `floss`
3. **`duration_seconds`** > 0
4. Se `duration_samples` existir, então `duration_seconds` = `duration_samples / 250` (assumindo 250 Hz)
5. **`n_detections`** = comprimento de `det_times` (e de `det_indices`, se `det_indices` existir)
6. **`n_ground_truth`** = comprimento de `gt_times` (e de `gt_indices`, se `gt_indices` existir)
7. Se `processing_time` existir, `processing_time` >= 0
8. Se existirem, listas `gt_indices` e `det_indices`: valores inteiros >= 0
9. Listas `gt_times` e `det_times`: valores float >= 0
10. **Ordem das colunas**: livre; recomenda-se manter o formato de referência por detector para facilitar auditoria e integração

### Exemplo de Validação em R:
```r
validate_predictions_csv <- function(df, detector_name) {
  # Validações básicas
  stopifnot(!any(is.na(df$record_id)))
  stopifnot(all(df$detector == detector_name))
  stopifnot(all(df$duration_seconds > 0))
  if ("duration_samples" %in% names(df)) {
    stopifnot(all(df$duration_samples > 0))
  }
  if ("processing_time" %in% names(df)) {
    stopifnot(all(df$processing_time >= 0))
  }

  # Validar consistência de listas
  stopifnot(all(map_int(df$det_times, length) == df$n_detections))
  stopifnot(all(map_int(df$gt_times, length) == df$n_ground_truth))
  if ("det_indices" %in% names(df)) {
    stopifnot(all(map_int(df$det_indices, length) == df$n_detections))
  }
  if ("gt_indices" %in% names(df)) {
    stopifnot(all(map_int(df$gt_indices, length) == df$n_ground_truth))
  }

  return(TRUE)
}
```

---

## Exemplo Completo de Conversão em R

### Opção 1: Formato MÍNIMO (Recomendado)

```r
library(tidyverse)
library(jsonlite)

# 1. Preparar dados (apenas colunas essenciais)
predictions_df <- tibble(
  record_id = c("data_101_1.par", "data_102_1.par"),
  detector = "adwin",
  delta = c(0.005, 0.005),
  ma_window = c(10, 10),
  min_gap_samples = c(1000, 2000),
  duration_seconds = c(583.884, 600.0),
  # Apenas gt_times e det_times (SEM índices!)
  gt_times = list(c(282.396), c(300.0)),
  det_times = list(c(3.196, 9.852, 15.356), c(3.2, 10.0)),
  n_detections = c(3, 2),
  n_ground_truth = c(1, 1)
)

# 2. Converter listas para formato Python string
predictions_df <- predictions_df %>%
  mutate(
    gt_times = map_chr(gt_times, ~ toJSON(.x, auto_unbox = FALSE)),
    det_times = map_chr(det_times, ~ toJSON(.x, auto_unbox = FALSE))
  )

# 3. (Opcional) Fixar ordem para reprodutibilidade
column_order <- c(
  "record_id", "detector", "delta", "ma_window", "min_gap_samples",
  "duration_seconds", "gt_times", "det_times",
  "n_detections", "n_ground_truth"
)

predictions_df <- predictions_df %>%
  select(all_of(column_order))

# 4. Salvar como CSV
write_csv(predictions_df, "predictions_intermediate.csv")
```

### Opção 2: Formato COMPLETO (compatível com Python)

```r
library(tidyverse)
library(jsonlite)

# 1. Preparar dados no formato completo
predictions_df <- tibble(
  record_id = c("data_101_1.par", "data_102_1.par"),
  detector = "adwin",
  delta = c(0.005, 0.005),
  ma_window = c(10, 10),
  min_gap_samples = c(1000, 2000),
  duration_samples = c(145971, 150000),
  duration_seconds = c(583.884, 600.0),
  gt_indices = list(c(70599), c(75000)),
  gt_times = list(c(282.396), c(300.0)),  # gt_indices / 250
  det_indices = list(c(799, 2463, 3839), c(800, 2500)),
  det_times = list(c(3.196, 9.852, 15.356), c(3.2, 10.0)),  # det_indices / 250
  n_detections = c(3, 2),
  n_ground_truth = c(1, 1),
  processing_time = c(3.335, 3.4)
)

# 2. Converter listas para formato Python string
predictions_df <- predictions_df %>%
  mutate(
    gt_indices = map_chr(gt_indices, ~ toJSON(.x, auto_unbox = FALSE)),
    gt_times = map_chr(gt_times, ~ toJSON(.x, auto_unbox = FALSE)),
    det_indices = map_chr(det_indices, ~ toJSON(.x, auto_unbox = FALSE)),
    det_times = map_chr(det_times, ~ toJSON(.x, auto_unbox = FALSE))
  )

# 3. (Opcional) Fixar ordem para reprodutibilidade
column_order <- c(
  "record_id", "detector", "delta", "ma_window", "min_gap_samples",
  "duration_samples", "duration_seconds", "gt_indices", "gt_times",
  "det_indices", "det_times", "n_detections", "n_ground_truth",
  "processing_time"
)

predictions_df <- predictions_df %>%
  select(all_of(column_order))

# 4. Salvar como CSV
write_csv(predictions_df, "predictions_intermediate.csv")
```

### Função Helper: Conversão de Índices para Tempos

```r
# Converter índices de amostras para tempos em segundos
convert_indices_to_times <- function(indices, sample_rate = 250) {
  indices / sample_rate
}

# Exemplo de uso:
gt_indices <- c(70599, 150000)
gt_times <- convert_indices_to_times(gt_indices)
# Resultado: [282.396, 600.0]
```

---

## Formato Agregado: `models_aggregated.csv`

O formato agregado é documentado em detalhe na seção
`Especificação do Formato CSV models_aggregated.csv`, mais abaixo neste documento.
Esta seção evita duplicar a especificação para manter uma única fonte textual
sobre colunas, exemplos, NaN e contagens por detector.

## Notas Importantes para o Agente R

1. **Sample Rate**: Os dados de ECG usam 250 Hz (250 amostras/segundo)
   - `duration_seconds = duration_samples / 250.0`
   - `gt_times = gt_indices / 250.0` (conversão de índices para segundos)
   - `det_times = det_indices / 250.0` (conversão de índices para segundos)

2. **Colunas Mínimas Obrigatórias** (para R):
   ```r
   # Apenas estas colunas são ESSENCIAIS:
   c("record_id", "detector",
     "delta", "ma_window", "min_gap_samples",  # parâmetros (variam por detector)
     "duration_seconds",                        # duração do sinal
     "gt_times", "det_times",                   # tempos em segundos (NÃO índices!)
     "n_detections", "n_ground_truth")          # contagens

   # Pode OMITIR:
   # - gt_indices, det_indices (redundantes)
   # - duration_samples (calculável)
   # - processing_time (opcional)
   # - error (opcional)
   ```

3. **Ordem das Colunas**: Não é crítica para a pipeline atual. Ainda assim, usar `select(all_of(column_order))` é recomendado para padronização entre equipas/ferramentas.

4. **Conversão de Listas**: Usar `jsonlite::toJSON()` com `auto_unbox = FALSE` para converter vetores R em listas Python.

5. **Tipos de Dados**:
   - Booleanos: `True`/`False` (Python), não `TRUE`/`FALSE` (R)
   - Converter com: `ifelse(boolean_col, "True", "False")`

6. **Valores Faltantes**: Se não houver deteções ou ground truth, usar listas vazias `[]`, não `NA`.

7. **Coluna `error`**: Opcional para qualquer detector. É preenchida quando ocorre exceção durante geração.

8. **Encoding**: Sempre salvar como UTF-8.

---

## Resumo Rápido por Detector

| Detector | Nº Colunas (completas, sem `error`) | Parâmetros Específicos | Coluna `error` |
|----------|-------------------------------------|------------------------|----------------|
| ADWIN | 14 | `delta`, `ma_window`, `min_gap_samples` | Opcional (em falhas) |
| Page-Hinkley | 16 | `lambda_`, `delta`, `alpha`, `ma_window`, `min_gap_samples` | Opcional (em falhas) |
| KSWIN | 16 | `alpha`, `window_size`, `stat_size`, `ma_window`, `min_gap_samples` | Opcional (em falhas) |
| HDDM_A | 16 | `drift_confidence`, `warning_confidence`, `two_side_option`, `ma_window`, `min_gap_samples` | Opcional (em falhas) |
| HDDM_W | 17 | `drift_confidence`, `warning_confidence`, `lambda_option`, `two_side_option`, `ma_window`, `min_gap_samples` | Opcional (em falhas) |
| FLOSS | 15 | `window_size`, `regime_threshold`, `regime_landmark`, `min_gap_samples` | Opcional (em falhas) |

**No formato completo, as colunas comuns no final** são: `duration_samples`, `duration_seconds`, `gt_indices`, `gt_times`, `det_indices`, `det_times`, `n_detections`, `n_ground_truth`, `processing_time`

---

# Especificação do Formato CSV `models_aggregated.csv`

Este documento descreve o formato do ficheiro CSV gerado por `src/simplify_metrics_for_analysis.py`, que agrega métricas por **combinação única de parâmetros** (modelo).

## Propósito

`models_aggregated.csv` é criado **a partir de** `metrics_comprehensive_with_nab.csv` e é utilizado para:

- **Análise de importância de parâmetros** (ex: SHAP em R)
- **Redução dimensional** dos dados (em vez de métricas por ficheiro, ter por modelo)
- **Preparação de dados compactos** para análises externas de interpretabilidade ou ML

**Diferença fundamental**:
- `predictions_intermediate.csv`: 1 linha = 1 ficheiro ECG × 1 combinação de parâmetros
- `models_aggregated.csv`: 1 linha = 1 combinação de parâmetros ÚNICA (agregado sobre todos os ficheiros)

## Estrutura Geral

O CSV tem:
- **Separador**: vírgula (`,`)
- **Encoding**: UTF-8
- **Cabeçalho**: linha 1 contém nomes das colunas
- **Index**: NÃO incluir coluna de índice
- **Agregação**: Cada linha é média ou mediana das métricas para o modelo em todos os ficheiros

## Geração do Ficheiro

```bash
python -m src.simplify_metrics_for_analysis \
  --input results/<dataset>/<detector>/metrics_comprehensive_with_nab.csv \
  --output results/<dataset>/<detector>/models_aggregated.csv \
  --aggregation mean
```

**Parâmetros opcionais**:
- `--aggregation {mean|median}` — Tipo de agregação (default: `mean`)
- `--add-stats` — Incluir std, min, max além da métrica agregada

## Formato das Colunas

### Estrutura Geral (varia por detector)

```
model_id, [parâmetros específicos do detector...], n_records, [métricas agregadas...]
```

No output padrão atual, o ficheiro tem 20 ou 21 campos agregados após
`n_records` (dependendo da presença de `duration_samples`). O número total de
colunas varia conforme a quantidade de parâmetros do detector (ex.: 26 colunas
para ADWIN, 29 para HDDM_W, sem `--add-stats`).

### Exemplo: ADWIN com 594 modelos

Este exemplo usa os artefatos atuais de `results/afib_paroxysmal/adwin/models_aggregated.csv`.

**Primeiras 6 colunas (ID + parâmetros):**

```
model_id,delta,ma_window,min_gap_samples,n_records
model_1,0.005,10,500,229
model_2,0.005,10,1000,229
model_3,0.005,10,2000,229
...
model_594,0.1,300,5000,229
```

**Campos agregados no output atual padrão:**

```
duration_samples, n_ground_truth, n_detections,
f1_classic, f1_weighted, f3_classic, f3_weighted,
recall_4s, recall_10s, precision_4s, precision_10s,
edd_median_s, edd_p95_s, fp_per_min,
nab_score_standard, nab_score_low_fp, nab_score_low_fn,
tp, fp, fn, tp_weight_sum
```

**Linha de exemplo:**

```
model_1,0.005,10,500,229,180554.47598253275,5.681222707423581,92.51965065502183,0.16524574545244128,0.14841669896430548,0.37059070765798363,0.3306217873592183,0.6325181083722055,0.820378217196224,0.07680042382111923,0.11413107599537244,2.767150684931506,4.5335616438356166,9.140104174388261,-6.726536383913302,-13.941920122556695,-5.3939536848972836,4.331877729257642,83.97379912663756,1.3493449781659388,3.7723114992721984
```

### Descrição Detalhada das Colunas

#### 1. Coluna de Identificação

| Coluna | Tipo | Descrição |
|--------|------|-----------|
| `model_id` | string | ID único do modelo (ex: `model_1`, `model_594`) |

#### 2. Colunas de Parâmetros (variam por detector)

**ADWIN**:
| Coluna | Tipo | Descrição |
|--------|------|-----------|
| `delta` | float | Confiança do detector |
| `ma_window` | integer | Janela de média móvel |
| `min_gap_samples` | integer | Mínimo de amostras entre deteções |

**Page-Hinkley**:
| Coluna | Tipo | Descrição |
|--------|------|-----------|
| `lambda_` | float | Threshold |
| `delta` | float | Permissiveness |
| `alpha` | float | Forgetting factor |
| `ma_window` | integer | Janela de média móvel |
| `min_gap_samples` | integer | Mínimo de amostras entre deteções |

**KSWIN**:
| Coluna | Tipo | Descrição |
|--------|------|-----------|
| `alpha` | float | Nível de significância |
| `window_size` | integer | Tamanho da janela de referência |
| `stat_size` | integer | Tamanho da janela estatística |
| `ma_window` | integer | Janela de média móvel |
| `min_gap_samples` | integer | Mínimo de amostras entre deteções |

**HDDM_A**:
| Coluna | Tipo | Descrição |
|--------|------|-----------|
| `drift_confidence` | float | Nível de confiança para drift |
| `warning_confidence` | float | Nível de confiança para aviso |
| `two_side_option` | boolean | Monitorização bilateral (`True`) ou unilateral (`False`) |
| `ma_window` | integer | Janela de média móvel |
| `min_gap_samples` | integer | Mínimo de amostras entre deteções |

**HDDM_W**:
| Coluna | Tipo | Descrição |
|--------|------|-----------|
| `drift_confidence` | float | Nível de confiança para drift |
| `warning_confidence` | float | Nível de confiança para aviso |
| `lambda_option` | float | Peso da média móvel exponencial |
| `two_side_option` | boolean | Monitorização bilateral (`True`) ou unilateral (`False`) |
| `ma_window` | integer | Janela de média móvel |
| `min_gap_samples` | integer | Mínimo de amostras entre deteções |

#### 3. Coluna de Contagem

| Coluna | Tipo | Descrição | Exemplo |
|--------|------|-----------|---------|
| `n_records` | integer | Número de ficheiros agregados neste modelo | `229` (afib_paroxysmal) |

**Nota**: `n_records` é constante para um dataset mas varia entre datasets (afib=229, malignant=22, vtachy=34)

#### 4. Campos Agregados no Output Atual

No output padrão atual de `src/simplify_metrics_for_analysis.py`, os nomes das colunas agregadas **não** recebem o sufixo `_mean` quando a agregação escolhida é `mean`. O script preserva os nomes originais das colunas e aplica a agregação diretamente ao agrupamento.

Além das métricas propriamente ditas, o CSV agregado também inclui alguns metadados/contagens agregadas.

**Metadados e contagens agregadas**:
| Coluna | Descrição |
|--------|-----------|
| `duration_samples` | Média/mediana da duração do sinal em amostras, quando disponível |
| `n_ground_truth` | Média/mediana de eventos reais por registo |
| `n_detections` | Média/mediana de deteções por registo |

**F-Scores**:
| Coluna | Descrição | Alcance | Agregação |
|--------|-----------|---------|-----------|
| `f1_classic` | F1 clássico agregado | [0, 1] | Média ou Mediana |
| `f1_weighted` | F1 ponderado por latência | [0, 1] | Média ou Mediana |
| `f3_classic` | F3 clássico agregado | [0, 1] | Média ou Mediana |
| `f3_weighted` | F3 ponderado por latência (PRIMÁRIA) | [0, 1] | Média ou Mediana |

**Métricas Temporais**:
| Coluna | Descrição | Alcance | Agregação |
|--------|-----------|---------|-----------|
| `recall_4s` | Recall dentro de 4s | [0, 1] | Média ou Mediana |
| `recall_10s` | Recall dentro de 10s | [0, 1] | Média ou Mediana |
| `precision_4s` | Precision dentro de 4s | [0, 1] | Média ou Mediana |
| `precision_10s` | Precision dentro de 10s | [0, 1] | Média ou Mediana |
| `edd_median_s` | Latência mediana (segundos) | [0, ∞) | Média ou Mediana |
| `edd_p95_s` | Latência p95 (segundos) | [0, ∞) | Média ou Mediana |
| `fp_per_min` | Falsos positivos por minuto | [0, ∞) | Média ou Mediana |

**NAB Scores**:
| Coluna | Descrição | Alcance | Agregação |
|--------|-----------|---------|-----------|
| `nab_score_standard` | NAB Standard agregado | (-∞, +∞) | Média ou Mediana |
| `nab_score_low_fp` | NAB Low FP agregado | (-∞, +∞) | Média ou Mediana |
| `nab_score_low_fn` | NAB Low FN agregado | (-∞, +∞) | Média ou Mediana |

**Contagens de matching agregadas**:
| Coluna | Descrição |
|--------|-----------|
| `tp` | Média/mediana de true positives |
| `fp` | Média/mediana de false positives |
| `fn` | Média/mediana de false negatives |
| `tp_weight_sum` | Soma ponderada agregada dos TP por latência |

### Tratamento de Valores Faltantes

**NaN em métricas**:
- Alguns modelos podem gerar `NaN` em `edd_median_s` ou `edd_p95_s`
  - Causa: modelo não teve nenhum TP em alguns ficheiros
  - Significado: modelo falhou em detectar eventos
- **Decisão**: Manter `NaN` (indica informação crítica: falha de detecção)
- **Agregação**: `pandas` ignora `NaN` em `mean` e `median`; o agregado só permanece `NaN` quando todos os valores do grupo são `NaN` para essa coluna

**Exemplo**:
- FLOSS malignantventricular: ~3,000 modelos (em 25,920 total) têm `NaN` em `edd_median_s`
- Estes modelos não conseguiram detectar eventos a tempo em alguns ficheiros

## Comparação: predictions_intermediate vs models_aggregated

| Aspeto | predictions_intermediate.csv | models_aggregated.csv |
|--------|------------------------------|----------------------|
| **1 linha representa** | 1 ficheiro × 1 parâmetro | 1 combinação de parâmetros (média sobre todos os ficheiros) |
| **Número de linhas** | #ficheiros × #modelos | #modelos |
| **Exemplo ADWIN/afib** | 229 ficheiros × 594 modelos = 136,026 linhas | 594 linhas |
| **Exemplo FLOSS/afib** | 229 ficheiros × 25,920 modelos = 5,935,680 linhas | 25,920 linhas |
| **Contém GT original?** | Sim (gt_indices, gt_times) | Não |
| **Contém detecções?** | Sim (det_indices, det_times) | Não (apenas métricas agregadas) |
| **Colunas de métricas** | Não | Sim (20-21 campos agregados no output padrão) |
| **Uso típico** | Validação manual, debugging | Análise de importância (SHAP), ranking de modelos |
| **Tamanho do ficheiro** | Grande (~100-1000 MB) | Pequeno (~1-10 MB) |
| **Tempo de cálculo** | Rápido (~5-10 min por detector) | Rápido (~30 seg por detector) |

## Quando Usar Cada Um

### Usar `predictions_intermediate.csv` quando:
- Precisa validar detecções num ficheiro específico
- Quer visualizar ground truth vs detecções
- Tem dúvidas sobre um registo específico
- Quer recalcular métricas com diferentes parâmetros

### Usar `models_aggregated.csv` quando:
- Quer comparar performance de diferentes modelos
- Precisa de análise de importância de parâmetros (ex: SHAP)
- Quer ranking de modelos sem ruído de variabilidade por ficheiro
- Prepara dados para análise em R ou ferramentas externas
- Quer datasets compactos para machine learning

## Exemplo de Uso em R

### Carregar e explorar

```r
library(tidyverse)

# Carregar models_aggregated.csv
models <- read_csv("results/afib_paroxysmal/adwin/models_aggregated.csv")

# Verificar estrutura
head(models)
dim(models)  # Ex.: ADWIN/afib = 594 modelos × 26 colunas

# Colunas:
# model_id, delta, ma_window, min_gap_samples, n_records,
# duration_samples, n_ground_truth, n_detections,
# f1_classic, f1_weighted, f3_classic, f3_weighted,
# recall_4s, recall_10s, precision_4s, precision_10s,
# edd_median_s, edd_p95_s, fp_per_min,
# nab_score_standard, nab_score_low_fp, nab_score_low_fn,
# tp, fp, fn, tp_weight_sum
```

### Ranking de modelos

```r
# Top 10 modelos por F3-weighted
top_models <- models %>%
  slice_max(f3_weighted, n = 10) %>%
  select(model_id, delta, ma_window, min_gap_samples, f3_weighted)

print(top_models)
```

### Análise de importância de parâmetros (SHAP-ready)

```r
# Preparar para SHAP
models_for_shap <- models %>%
  select(
    delta, ma_window, min_gap_samples,  # Features
    f3_weighted                          # Target
  ) %>%
  na.omit()  # Remover NaN se houver

# Exportar para R SHAP library
# (ex: com XGBoost ou outro modelo)
```

### Validação de robustez

```r
# Modelos com NaN em EDD → falharam em detectar
problematic_models <- models %>%
  filter(is.na(edd_median_s)) %>%
  nrow()

cat(sprintf(
  "Modelos com falha de detecção: %d / %d (%.1f%%)\n",
  problematic_models, nrow(models), 100 * problematic_models / nrow(models)
))
```

## Notas Importantes

1. **Agregação é média por padrão** — Use `--aggregation median` se preferir robustez a outliers

2. **NaN na agregação** — `mean`/`median` ignoram `NaN`; a métrica agregada só será `NaN` quando todos os valores do grupo forem `NaN`

3. **n_records é informativo** — Diferente entre datasets (229 vs 22 vs 34), útil para ponderação

  Para HDDM_A/HDDM_W, `n_records` deve continuar igual ao número de ficheiros do dataset
  porque `two_side_option` é parte da combinação do modelo e não é agregado por média.

4. **Ordem de parâmetros** — Mesma ordem que em `predictions_intermediate.csv`

5. **Sem duplicatas** — Cada combinação de parâmetros aparece exatamente uma vez

6. **Arquivo compacto** — Ideal para distribuição e análise iterativa em R/Python

---

## Fluxo Completo: predictions → models_aggregated

```
1. generate_predictions.py
   Entrada: data/<dataset>_full.csv
   Saída: results/<dataset>/<detector>/predictions_intermediate.csv
          (1 linha por ficheiro × parâmetro)

2. evaluate_predictions.py
   Entrada: predictions_intermediate.csv
   Saída: results/<dataset>/<detector>/metrics_comprehensive_with_nab.csv
          (métricas calculadas para cada linha)

3. simplify_metrics_for_analysis.py
   Entrada: metrics_comprehensive_with_nab.csv
   Saída: results/<dataset>/<detector>/models_aggregated.csv
          (1 linha por modelo único, agregado)

4. [Opcional] Análise em R (SHAP, ML, etc.)
   Entrada: models_aggregated.csv
   Saída: Relatórios de importância de parâmetros
```

---

## Resumo por Detector

Os valores abaixo refletem os artefatos atuais de `afib_paroxysmal` em `results/<dataset>/<detector>/`.

| Detector | Nº Modelos (afib) | Parâmetros | Linhas em predictions | Linhas em models_aggregated |
|----------|-------------------|------------|----------------------|----------------------------|
| ADWIN | 594 | 3 | 136,026 | 594 |
| Page-Hinkley | 600 | 5 | 137,400 | 600 |
| KSWIN | 1,280 | 5 | 293,120 | 1,280 |
| HDDM_A | 640 | 5 | 146,560 | 640 |
| HDDM_W | 2,560 | 6 | 586,240 | 2,560 |
| FLOSS | 25,920 | 4 | 5,935,680 | 25,920 |
| **TOTAL** | **31,594** | **—** | **7,235,026** | **31,594** |

**Redução de tamanho**: ~230× menos linhas, ~100× menos espaço em disco
