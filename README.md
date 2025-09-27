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

## 6. Próximos Passos Sugeridos

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

## 7. Integração com Dados Reais (Guia Rápido)

Quando tiver o CSV real:
1. Garantir colunas: `sample_index` (ou `timestamp`) e `ecg`.
2. Criar coluna `regime_change` com 1 nos instantes de início de novo regime (0 caso contrário).
3. Rodar:
```bash
python -m src.streaming_detector --data data/seu_ecg.csv --detector adwin --ma-window 25 --min-gap-samples 100 --param delta=0.01 --tolerance 200
```
4. Ajustar `--tolerance` proporcional ao atraso aceitável (ex: 200 samples = 0.8 s a 250 Hz).

---

## 8. Limitações Atuais

- Sem visualização embutida (apenas métricas numéricas).
- Média móvel não estritamente causal (potencial micro-viés no alinhamento do pico de detecção).
- Sem persistência de hyperparameter search.
- Apenas uma métrica de delay média (sem variância / distribuição completa explicitada).
- Não há distinção entre tipos de mudança (ex: nível vs variância) — poderia classificar pelo sinal pré/pós.

---

## 9. Conclusão

Este baseline fornece uma fundação reproduzível para comparação com seu algoritmo de detecção de mudanças de regime em ECG streaming. A estrutura facilita extensão, logging mais robusto e integração de dados reais. Recomenda-se agora adicionar logging estruturado e visualização para fortalecer a seção experimental da tese.

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
