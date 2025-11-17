# Especificação do Formato CSV `predictions_intermediate.csv`

Este documento descreve o formato exato do ficheiro CSV gerado pelos scripts `generate_*.sh` para uso com o agente R na conversão de dados.

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

## Formato por Detector

### ADWIN

**Colunas obrigatórias (14 colunas, nesta ordem exata):**

```
record_id,detector,delta,ma_window,min_gap_samples,duration_samples,duration_seconds,gt_indices,gt_times,det_indices,det_times,n_detections,n_ground_truth,processing_time
```

**Exemplo de linha de dados:**
```
data_101_1.par,adwin,0.005,10,1000,145971,583.884,[70599],[282.396],"[799, 2463, 3839]","[3.196, 9.852, 15.356]",3,1,3.335204839706421
```

---

### Page-Hinkley

**Colunas obrigatórias (16 colunas):**

```
record_id,detector,lambda_,delta,alpha,ma_window,min_gap_samples,duration_samples,duration_seconds,gt_indices,gt_times,det_indices,det_times,n_detections,n_ground_truth,processing_time
```

**Diferenças em relação ao ADWIN:**
- 3 parâmetros adicionais ANTES de `ma_window`: `lambda_`, `delta`, `alpha`
- Resto da estrutura idêntica

---

### KSWIN

**Colunas obrigatórias (17 colunas):**

```
record_id,detector,alpha,window_size,stat_size,ma_window,min_gap_samples,duration_samples,duration_seconds,gt_indices,gt_times,det_indices,det_times,n_detections,n_ground_truth,processing_time,error
```

**Diferenças:**
- 3 parâmetros ANTES de `ma_window`: `alpha`, `window_size`, `stat_size`
- **Coluna adicional no final**: `error` (vazia se não houver erro, ou mensagem de erro se houver)

---

### HDDM_A

**Colunas obrigatórias (16 colunas):**

```
record_id,detector,drift_confidence,warning_confidence,two_side_option,ma_window,min_gap_samples,duration_samples,duration_seconds,gt_indices,gt_times,det_indices,det_times,n_detections,n_ground_truth,processing_time
```

**Diferenças:**
- 3 parâmetros ANTES de `ma_window`: `drift_confidence`, `warning_confidence`, `two_side_option`

---

### HDDM_W

**Colunas obrigatórias (17 colunas):**

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
| `detector` | string | ✅ SIM | Nome do detector usado | `adwin`, `page_hinkley`, `kswin`, `hddm_a`, `hddm_w` |
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
| `error` | string | Mensagem de erro (vazia se não houver) | vazio ou `"Error message"` |

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
2. **`detector`** deve ser um de: `adwin`, `page_hinkley`, `kswin`, `hddm_a`, `hddm_w`
3. **`duration_samples`** > 0
4. **`duration_seconds`** > 0 e = `duration_samples / 250` (assumindo 250 Hz)
5. **`n_detections`** = comprimento de `det_indices` = comprimento de `det_times`
6. **`n_ground_truth`** = comprimento de `gt_indices` = comprimento de `gt_times`
7. **`processing_time`** >= 0
8. **Listas `gt_indices` e `det_indices`**: valores inteiros >= 0
9. **Listas `gt_times` e `det_times`**: valores float >= 0
10. **Ordem das colunas**: EXATA conforme especificação do detector

### Exemplo de Validação em R:
```r
validate_predictions_csv <- function(df, detector_name) {
  # Validações básicas
  stopifnot(!any(is.na(df$record_id)))
  stopifnot(all(df$detector == detector_name))
  stopifnot(all(df$duration_samples > 0))
  stopifnot(all(df$duration_seconds > 0))
  stopifnot(all(df$processing_time >= 0))

  # Validar consistência de listas
  stopifnot(all(map_int(df$det_indices, length) == df$n_detections))
  stopifnot(all(map_int(df$det_times, length) == df$n_detections))
  stopifnot(all(map_int(df$gt_indices, length) == df$n_ground_truth))
  stopifnot(all(map_int(df$gt_times, length) == df$n_ground_truth))

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

# 3. Garantir ordem correta das colunas
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

# 3. Garantir ordem correta das colunas
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

3. **Ordem das Colunas**: A ordem EXATA das colunas é crítica se usar formato completo. Usar `select(all_of(column_order))` para garantir.

4. **Conversão de Listas**: Usar `jsonlite::toJSON()` com `auto_unbox = FALSE` para converter vetores R em listas Python.

5. **Tipos de Dados**:
   - Booleanos: `True`/`False` (Python), não `TRUE`/`FALSE` (R)
   - Converter com: `ifelse(boolean_col, "True", "False")`

6. **Valores Faltantes**: Se não houver deteções ou ground truth, usar listas vazias `[]`, não `NA`.

7. **Coluna `error`**: Apenas KSWIN tem esta coluna no formato completo. Pode omitir completamente.

8. **Encoding**: Sempre salvar como UTF-8.

---

## Resumo Rápido por Detector

| Detector | Nº Colunas | Parâmetros Específicos | Tem coluna `error`? |
|----------|------------|------------------------|---------------------|
| ADWIN | 14 | `delta`, `ma_window`, `min_gap_samples` | ❌ |
| Page-Hinkley | 16 | `lambda_`, `delta`, `alpha`, `ma_window`, `min_gap_samples` | ❌ |
| KSWIN | 17 | `alpha`, `window_size`, `stat_size`, `ma_window`, `min_gap_samples` | ✅ |
| HDDM_A | 16 | `drift_confidence`, `warning_confidence`, `two_side_option`, `ma_window`, `min_gap_samples` | ❌ |
| HDDM_W | 17 | `drift_confidence`, `warning_confidence`, `lambda_option`, `two_side_option`, `ma_window`, `min_gap_samples` | ❌ |

**Colunas comuns a todos** (sempre no final): `duration_samples`, `duration_seconds`, `gt_indices`, `gt_times`, `det_indices`, `det_times`, `n_detections`, `n_ground_truth`, `processing_time`
