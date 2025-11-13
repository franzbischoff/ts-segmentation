# Time Series Regime Change Detection Baseline

Baseline de detecção de mudanças de regime (concept drift / change point) em um sinal de ECG streaming (250 Hz) usando a biblioteca `scikit-multiflow`.

## Objetivo
Demonstrar um baseline simples que:
1. Lê um sinal de ECG (ou um mock caso real não esteja disponível).
2. Processa o sinal em fluxo (stream) em janelas (chunks) ou amostra a amostra.
3. Usa detectores de mudança (Page Hinkley, ADWIN, DDM etc.).
4. Produz uma lista de timestamps (em segundos e índice de amostra) onde o detector acusou mudança.
5. Compara com metadados de verdade-terreno (ground-truth) de mudanças de regime.

## Estrutura
```
├── data/
│   ├── ecg_signal.csv              # Sinal + metadados (placeholder)
├── src/
│   ├── streaming_detector.py       # Loop principal de detecção
│   ├── detectors.py                # Wrappers utilitários para detectores
│   ├── evaluation.py               # Métricas de atraso e precisão
│   ├── data_loader.py              # Carregamento e normalização
│   └── utils.py                    # Funções auxiliares
├── notebooks/
│   └── exploratory.ipynb           # Exploração opcional (a criar depois)
├── requirements.txt
└── README.md
```

## Formato esperado do dataset
Arquivo CSV `data/ecg_signal.csv` com ao menos as colunas:
- `timestamp` (segundos em ponto flutuante ou índice) OU `sample_index` (inteiro) — usaremos `sample_index` se existir.
- `ecg` valor do sinal bruto (float)
- `regime_change` (0 ou 1) indicando se nesta amostra ocorre o início de um novo regime (ground-truth).

Exemplo (5 linhas):
```
sample_index,ecg,regime_change
0,0.12,0
1,0.11,0
2,0.09,1
3,0.45,0
4,0.47,0
```

## Como funciona a detecção
Para cada nova amostra (ou pequeno batch) alimentamos o detector. Quando o detector sinaliza mudança, registramos:
- `sample_index`
- `time_seconds = sample_index / 250.0`
- `detector` (nome)

---

## 1. Visão Geral da Implementação

Pipeline (arquivo `src/streaming_detector.py`):
1. Carregamento / geração do dataset (`data_loader.load_dataset`).
2. Pré-processamento opcional:
	 - Média móvel (`--ma-window`)
	 - Derivada primeira (`--derivative`) para enfatizar transições rápidas.
3. Alimentação streaming (amostra a amostra) no detector escolhido (`detectors.build_detector`).
4. Pós-processamento: filtro de espaçamento mínimo entre detecções (`--min-gap-samples`).
5. Avaliação das detecções via `evaluation.evaluate_detections`:
	 - Casamento com ground-truth usando tolerância (`--tolerance`).
	 - Cálculo de TP, FP, FN, precisão, recall e atraso médio.
6. Exportação de CSV com eventos: `data/detections_<detector>.csv`.

Arquivos principais:
- `src/data_loader.py`: geração sintética controlável (segmentos, tamanho, shifts cumulativos de baseline, amplitude, ruído).
- `src/detectors.py`: wrappers unificados para PageHinkley, ADWIN, DDM; fácil adicionar outros.
- `src/evaluation.py`: lógica de matching e métricas.
- `src/streaming_detector.py`: CLI + loop principal.
- `src/utils.py`: utilidades simples.

Detecção streaming verdadeira: nenhuma amostra futura é usada; pré-processamentos são causais exceto pela convolução 'same' (média móvel). Para ambiente estritamente online sem lookahead, a média poderia ser implementada via janela deslizante causal (possível melhoria futura).

---

## 2. Detalhes dos Detectores Suportados

| Detector        | Foco principal                      | Parâmetros chave (CLI via `--param k=v`) | Observações |
|-----------------|-------------------------------------|-------------------------------------------|-------------|
| Page Hinkley    | Mudança de média (cumulativa)       | `lambda_`, `delta`, `alpha`               | Sensível ao escalonamento; requer shifts claros |
| ADWIN           | Média adaptativa / janelas dinâmicas| `delta`                                   | Auto-ajusta janela; pode gerar muitos FP se `delta` pequeno |
| DDM             | Desempenho de erro (classificação)  | (sem expostos aqui)                       | Menos adequado sem rótulos de erro de classificação |

Para dados ECG contínuos, ADWIN tende a detectar quando há mudança de nível médio ou dispersão após filtragens.

---

## 3. Uso do CLI

Ativar ambiente virtual:
```bash
source .venv/bin/activate
```

Comando mínimo (gera dados sintéticos se ausente):
```bash
python -m src.streaming_detector --detector adwin
```

Parâmetros principais:
```
--data PATH                # Caminho para CSV real (opcional)
--detector {page_hinkley|adwin|ddm}
--sample-rate INT          # Hz (default 250)
--tolerance INT            # Janela para casar detecção com mudança real
--force-regen              # Regenera sinal sintético (quando sem --data)
--segments INT             # Nº de segmentos sintéticos
--segment-length INT       # Tamanho por segmento
--param k=v                # Repetível para passar parâmetros ao detector
--ma-window INT            # Janela média móvel (suavização)
--derivative               # Usa derivada primeira do sinal
--min-gap-samples INT      # Filtra detecções muito próximas
```

Exemplos:

1) ADWIN com suavização e filtro de espaçamento:
```bash
python -m src.streaming_detector \
	--detector adwin --force-regen \
	--segments 6 --segment-length 800 \
	--ma-window 30 --min-gap-samples 80 \
	--param delta=0.01 --tolerance 120
```

2) Page Hinkley ajustado (se mudanças de média forem fortes):
```bash
python -m src.streaming_detector \
	--detector page_hinkley --force-regen \
	--segments 6 --segment-length 800 \
	--param lambda_=40 --param delta=0.01 --param alpha=0.0001
```

3) Usando derivada (para enfatizar transições rápidas) com ADWIN mais conservador:
```bash
python -m src.streaming_detector \
	--detector adwin --force-regen \
	--segments 6 --segment-length 800 \
	--derivative --ma-window 20 --param delta=0.02 --min-gap-samples 100
```

Saídas:
- Console: métricas agregadas.
- `data/detections_<detector>.csv`: colunas `detector, sample_index, time_seconds`.
- `data/synthetic_ecg.csv`: dataset sintético (caso gerado).

---

## 4. Interpretação dos Resultados

Campos principais nas métricas:
- `tp`: mudanças verdadeiras detectadas (dentro da tolerância).
- `fp`: detecções sem correspondente mudança verdadeira.
- `fn`: mudanças verdadeiras não detectadas.
- `precision`: tp / (tp + fp) – quão “limpas” são as detecções.
- `recall`: tp / (tp + fn) – cobertura das mudanças.
- `mean_delay_samples`: média do (detected_index - true_change_index) para TPs.
- `mean_delay_seconds`: atraso médio em segundos (`mean_delay_samples / sample_rate`).

Balanceamento típico:
- Reduzir `delta` (ADWIN) → mais sensível → aumenta recall mas gera mais falsos positivos.
- Aumentar `min-gap-samples` → agrupa picos próximos → reduz FP mas pode perder mudanças próximas.
- Suavizar (`--ma-window`) → reduz ruído, pode atrasar levemente detecção.
- Derivada (`--derivative`) → destaca transições abruptas, mas pode adicionar ruído em sinais limpos.

Critérios para relatório na tese:
1. Escolher um par (precision, recall) alvo (ex: recall ≥ 0.8 com delay < 0.25 s).
2. Justificar trade-off: diminuição de FP vs atraso ou perda de recall.
3. Mostrar curva ou tabela variando `delta` e `min-gap-samples`.

---

## 5. Recomendações de Configuração Baseline

Para o sinal sintético atual (6 segmentos × 800 samples) um setup razoável de compromisso:
```bash
python -m src.streaming_detector \
	--detector adwin --force-regen \
	--segments 6 --segment-length 800 \
	--ma-window 30 --min-gap-samples 80 \
	--param delta=0.01 --tolerance 120
```
Esse perfil obteve (exemplo observado):
- Recall ≈ 0.8
- Precision ≈ 0.09
- Atraso médio ≈ 55 samples (~0.22 s)

Se precisar mais precisão (menos falsos): subir `min-gap-samples` para 120–150 e talvez `delta=0.015`, aceitando queda de recall.

---

## 6. Métricas de Avaliação

Este projeto implementa três famílias de métricas para avaliação de detecção de mudanças de regime em streaming:

### 6.1. Métricas Clássicas (F1/F3 Classic)

Métricas tradicionais de classificação binária sem consideração temporal:
- **F1-classic**: Média harmônica de precision e recall
- **F3-classic**: Versão ponderada que enfatiza recall (β=3), importante quando não perder eventos é crítico

```
Precision = TP / (TP + FP)
Recall = TP / (TP + FN)
F1 = 2 × (Precision × Recall) / (Precision + Recall)
F3 = 10 × (Precision × Recall) / (9 × Precision + Recall)
```

### 6.2. Métricas Ponderadas por Latência (F1*/F3*)

Métricas que incorporam peso temporal baseado na rapidez da detecção:

**Função de Peso Temporal w(δ)**:
```
w(δ) = {
    1.0,                    se δ ≤ 4s    (peso total - detecção ideal)
    1 - (δ-4)/(10-4),      se 4s < δ ≤ 10s    (decaimento linear)
    0.0,                    se δ > 10s   (peso zero - detecção tardia demais)
}
```

onde δ é a latência de detecção em segundos.

- **F1-weighted (F1*)**: F1 com precision e recall ponderados por w(δ)
- **F3-weighted (F3*)**: F3 com ponderação temporal, **métrica primária** para otimização

**Métricas Auxiliares**:
- **Recall@4s**: Fração de mudanças detectadas dentro de 4 segundos
- **Recall@10s**: Fração de mudanças detectadas dentro de 10 segundos
- **Precision@4s, Precision@10s**: Precisão considerando janelas temporais
- **EDD (Expected Detection Delay)**: Atraso médio/mediano de detecção
- **FP/min**: Taxa de falsos positivos por minuto

**Vantagens**:
- Reflete importância clínica de detecção precoce
- Penaliza detecções tardias mesmo que tecnicamente corretas
- Mais realista para aplicações em tempo real

### 6.3. NAB Score (Numenta Anomaly Benchmark)

Métrica desenvolvida pela Numenta para avaliação de detecção de anomalias em streaming, baseada em função sigmoid que recompensa detecções precoces e penaliza detecções tardias ou falsos positivos.

**Função de Scoring Sigmoid**:
```
S(r) = 2 × sigmoid(-5r) - 1

onde r = posição relativa na janela de anomalia:
  r = -1.0  →  início da janela (score máximo ≈ +0.987)
  r = -0.5  →  meio da janela (score ≈ +0.848)
  r =  0.0  →  fim da janela (score = 0.0)
  r >  0.0  →  após janela / FP (score negativo até -1.0)
```

**Profiles de Aplicação** (Cost Matrix):

1. **Standard** (Balanceado):
   - TP weight: 1.0
   - FP weight: 0.11
   - FN weight: 1.0
   - *Uso*: Avaliação geral, balanço entre precision e recall

2. **Reward Low FP** (Penalizar Falsos Positivos):
   - TP weight: 1.0
   - FP weight: 0.22 (2× penalidade)
   - FN weight: 1.0
   - *Uso*: Aplicações onde alarmes falsos são muito custosos

3. **Reward Low FN** (Penalizar Falsos Negativos):
   - TP weight: 1.0
   - FP weight: 0.055 (1/2 penalidade)
   - FN weight: 2.0 (2× penalidade)
   - *Uso*: Aplicações críticas onde não pode perder eventos

**Cálculo do Score**:
```
NAB Score = Σ(TP scores) + Σ(FP scores) + Σ(FN penalties)

onde:
- TP score = S(r) × tp_weight / max_tp
- FP score = S(r_fp) × fp_weight  (negativo)
- FN penalty = -fn_weight por evento não detectado
```

**Características**:
- Normalizado para comparação entre datasets
- Recompensa detecção antecipada dentro da janela
- Penalidade crescente para FPs mais distantes do evento
- Permite diferentes profiles para diferentes aplicações

**Exemplo de Uso**:
```python
from src.evaluation import calculate_nab_score, NABCostMatrix

nab_result = calculate_nab_score(
    gt_times=[10.0, 30.0],       # Ground truth em segundos
    det_times=[10.5, 29.8],      # Detecções em segundos
    window_width=10.0,            # Janela de 10s após cada GT
    cost_matrix=NABCostMatrix.standard(),
    signal_duration=60.0,
    probation_percent=0.15        # Ignora primeiros 15% para warm-up
)
# Returns: {'nab_score': 1.85, 'tp': 2, 'fp': 0, 'fn': 0}
```

### 6.4. Comparação entre Métricas

| Métrica | Considera Tempo? | Melhor Para | Range de Valores |
|---------|------------------|-------------|------------------|
| F1-classic | ❌ | Avaliação binária básica | [0, 1] |
| F3-classic | ❌ | Enfatizar recall sem latência | [0, 1] |
| F1-weighted | ✅ | Balancear precision/recall com tempo | [0, 1] |
| **F3-weighted** | ✅ | **Otimização primária com recall temporal** | [0, 1] |
| NAB Standard | ✅ | Comparação com benchmarks NAB | ℝ (típico: -2 a +2) |
| NAB Low FP | ✅ | Minimizar alarmes falsos | ℝ (penaliza FP 2×) |
| NAB Low FN | ✅ | Aplicações críticas | ℝ (penaliza FN 2×) |

**Recomendação**:
- Use **F3-weighted** como métrica primária para grid search
- Reporte também **NAB Standard** para comparação com literatura
- Use **NAB Low FP/FN** para análise de trade-offs específicos da aplicação

---

## 7. Próximos Passos Sugeridos

1. Logging Estruturado: salvar JSON com parâmetros + métricas por execução (`results/run_YYYYMMDD_HHMM.json`).
2. Grid Search Automático: script para iterar sobre `delta`, `ma-window`, `min-gap-samples` e consolidar ranking.
3. Visualização Notebook (`notebooks/exploratory.ipynb`): plot do sinal, ground-truth e detecções (linhas verticais).
4. Ensemble de Detectores: combinar ADWIN + PageHinkley (ex: consenso ou votação com janela curta).
5. Métricas Avançadas: distribuição de atrasos (boxplot) e curva Precision–Recall parametrizada por `delta`.
6. Normalização Dinâmica: z-score em janela deslizante causal para reduzir efeito de deriva lenta de amplitude.
7. Ajuste Causal da Média Móvel: substituir convolução 'same' por buffer FIFO para evitar qualquer olhar futuro (rigor metodológico).
8. Integração ECG Real: parsing do dataset verdadeiro (R-peaks, marcações clínicas) e alinhamento de timestamps → conversão para `sample_index` a 250 Hz.
9. Feature Engineering: extrair energia por janela, variação RR (se tiver picos), entropia → alimentar detectores sobre feature agregada.
10. Exportação para Comparação: criar função que gera tabela LaTeX / Markdown com melhores configurações para anexar na tese.
11. Testes Unitários Básicos: validar geração sintética, casamento de detecções e cálculo de atraso.
12. Múltiplas Séries: suportar processamento de vários pacientes concatenando resultados.

---

## 8. Integração com Dados Reais (Guia Rápido)

Quando tiver o CSV real:
1. Garantir colunas: `sample_index` (ou `timestamp`) e `ecg`.
2. Criar coluna `regime_change` com 1 nos instantes de início de novo regime (0 caso contrário).
3. Rodar:
```bash
python -m src.streaming_detector --data data/seu_ecg.csv --detector adwin --ma-window 25 --min-gap-samples 100 --param delta=0.01 --tolerance 200
```
4. Ajustar `--tolerance` proporcional ao atraso aceitável (ex: 200 samples = 0.8 s a 250 Hz).

---

## 9. Limitações Atuais

- Sem visualização embutida (apenas métricas numéricas).
- Média móvel não estritamente causal (potencial micro-viés no alinhamento do pico de detecção).
- Sem persistência de hyperparameter search.
- Apenas uma métrica de delay média (sem variância / distribuição completa explicitada).
- Não há distinção entre tipos de mudança (ex: nível vs variância) — poderia classificar pelo sinal pré/pós.

---

## 10. Conclusão

Este baseline fornece uma fundação reproduzível para comparação com seu algoritmo de detecção de mudanças de regime em ECG streaming. A estrutura facilita extensão, logging mais robusto e integração de dados reais. Recomenda-se agora adicionar logging estruturado e visualização para fortalecer a seção experimental da tese.

---

## 11. Integração com Dataset no Zenodo (Record 6879233)

Para usar um dataset hospedado no Zenodo (ex: record `6879233`):

### Download automático
Foi adicionado script `src/zenodo_download.py` que baixa todos os ficheiros do record.

Exemplo:
```bash
source .venv/bin/activate
python -m src.zenodo_download --record-id 6879233 --out-dir data/zenodo_6879233
```

O script:
1. Consulta `https://zenodo.org/api/records/<record-id>`.
2. Lista ficheiros disponíveis.
3. Faz download streaming (com verificação de tamanho) para `out-dir`.

### Preparação do sinal
Use `src/prepare_dataset.py` para converter um arquivo de sinal para o formato esperado (`sample_index, ecg, regime_change`). Exemplo genérico:
```bash
python -m src.prepare_dataset \
	--input data/zenodo_6879233/SEU_ARQUIVO.csv \
	--output data/ecg_signal.csv \
	--ecg-col signal \
	--timestamp-col timestamp \
	--change-file data/zenodo_6879233/changes.csv \
	--change-col change_flag \
	--sample-rate 250
```

Se não possuir uma coluna de mudança (`regime_change`), pode fornecer um ficheiro de eventos com índices/tempos.

### Mapeamento de colunas
O script tentará:
- Criar `sample_index` sequencial quando só houver timestamp.
- Normalizar o sinal (opção `--zscore`).
- Gerar `regime_change` a partir de uma lista de tempos OU índices (opções `--events-csv`, `--events-col-index`, `--events-col-time`).

### Executar detecção sobre dataset real
```bash
python -m src.streaming_detector --data data/ecg_signal.csv --detector adwin \
	--ma-window 25 --min-gap-samples 100 --param delta=0.01 --tolerance 200
```

### Boas práticas
- Verifique a licença e citação do dataset (no Zenodo a API devolve campos `metadata`).
- Mantenha ficheiros originais intocados (usar subpasta dedicada).
- Se o dataset estiver em múltiplos ficheiros, unifique antes ou rode múltiplas vezes.

---

## 11. Preprocessamento de datasets WFDB com regimes (afib_regimes)

Foi adicionado o script `src/ecg_preprocess.py` que traduz a lógica principal dos scripts R (`find_all_files.R`, `read_ecg.R`, `pre_process.R`) para Python. Ele:

- Descobre ficheiros `.hea` + (`.csv.bz2` sinal) + (`.atr.csv.bz2` anotações) para classes de fibrilação (`persistent_afib`, `paroxysmal_afib`, `non_afib`).
- Lê frequência de amostragem, canais e anotações.
- (Opcional) Faz resample do original (ex.: 200 Hz) para 250 Hz via interpolação linear.
- Extrai índices de mudança de regime a partir dos códigos de anotação (label_store ∈ {28, 32, 33}).
- Limpa eventos duplicados próximos (< 15 samples) e remove eventos muito perto das extremidades (<= 10 samples do início/fim) — conforme `clean_truth` do R.
- Constrói um CSV “tidy” com colunas: `id, sample_index, ecg, regime_change` (1 marca início de novo regime).

### CLI
```
python -m src.ecg_preprocess --root <DIR_RAIZ> \
	--classes paroxysmal_afib \
	--limit-per-class 10 \
	--lead II \
	--resample-to 250 \
	--output data/afib_paroxysmal_tidy.csv
```

Parâmetros principais:
- `--root`: diretório onde estão os `.hea` (ex.: `data/zenodo_6879233/extracted/afib_regimes`).
- `--classes`: lista de classes (ou `all`). Ex.: `paroxysmal_afib`.
- `--limit-per-class`: mini‑teste rápido limitando Nº de ficheiros por classe.
- `--lead`: canal/derivação a extrair (fallback para a primeira coluna se ausente).
- `--resample-to`: frequência alvo (mantém se igual à original).
- `--output`: caminho do CSV final.

### Exemplo (mini‑teste com 10 ficheiros paroxysmal_afib)
```
python -m src.ecg_preprocess \
	--root data/zenodo_6879233/extracted/afib_regimes \
	--classes paroxysmal_afib \
	--limit-per-class 10 \
	--lead II \
	--resample-to 250 \
	--output data/afib_paroxysmal_tidy.csv
```

Depois executar o detector:
```
python -m src.streaming_detector \
	--data data/afib_paroxysmal_tidy.csv \
	--detector adwin \
	--ma-window 25 \
	--min-gap-samples 3000 \
	--param delta=0.01 \
	--tolerance 500 \
	--sample-rate 250
```

### Interpretação inicial
Em um subset de 10 ficheiros foram observados (exemplo) ~46 eventos de verdade e alta taxa de falsos positivos (ADWIN padrão). Isso é esperado porque:
1. Registos diferentes são concatenados — mudanças de baseline entre pacientes podem induzir falsos alarmes.
2. Parâmetro `delta` não foi otimizado para o ruído deste domínio.
3. Falta (por enquanto) pré-processamento mais robusto (derivadas + filtros adaptativos) antes de alimentar o detector.

### Recomendações imediatas
- Rodar por `id` e agregar métricas em vez de concatenar tudo (próxima melhoria planejada).
- Fazer pequena grid de `delta` (ex.: 0.005, 0.01, 0.02, 0.05).
- Ajustar `--min-gap-samples` conforme duração média de segmentos (talvez > 5000 se muitos FP sequenciais).
- Testar `--derivative` + média móvel maior para reduzir drift gradual.

### Estrutura do CSV gerado
```
id,sample_index,ecg,regime_change
data_101_1.par,0,0.012,0
...
```

Onde:
- `id`: identificador do registo (derivado do nome do ficheiro `.hea`).
- `sample_index`: índice da amostra (0-based) após eventual resampling.
- `ecg`: valor flotante da derivação escolhida.
- `regime_change`: 1 quando há início de novo regime; 0 caso contrário.

### Limitações atuais
- Apenas um canal por vez (multi‑lead futuro: armazenar em formato wide ou long com coluna `lead`).
- Códigos de anotação fixos {28,32,33} (tornar parametrizável em versão futura).
- Sem coluna de tempo em segundos (pode ser derivada: `time_s = sample_index / 250`).

---

## Métricas básicas
- Atraso (delay) médio: diferença entre primeira detecção após uma mudança real e o índice verdadeiro.
- Taxa de falsos positivos.
- Cobertura de mudanças reais detectadas (recall de regimes).

## Executar
Instalar dependências e rodar baseline (mock se não tiver dados reais):
```
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m src.streaming_detector --data data/ecg_signal.csv --detector page_hinkley --sample-rate 250
```

Se não existir `data/ecg_signal.csv`, um sinal sintético com regimes será gerado automaticamente em `data/synthetic_ecg.csv`.

## Próximos passos
- Ajustar thresholds dos detectores.
- Adicionar outros detectores (CUSUM, HDDM, EDDM, KSWIN - este de scikit-multiflow / river).
- Criar notebook comparativo.
- Integrar com seu algoritmo proprietário para comparação.

## Referências
- scikit-multiflow: https://scikit-multiflow.github.io/
