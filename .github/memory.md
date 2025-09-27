# Projeto: Streaming ECG Regime Change Detection (Sessão de Trabalho - Memória Persistente)

Este documento resume tudo o que foi feito até agora para permitir continuidade futura mesmo sem o histórico da conversa.

## 1. Objetivo Geral
Criar um baseline reprodutível de detecção de mudanças de regime (concept drift / change points) em sinais de ECG em fluxo (250 Hz), com geração sintética, integração de dados reais (afib_regimes), avaliação de métricas (delay, precision, recall), grid search simples e logging estruturado, mantendo estritamente processamento streaming (sem lookahead) e dependências pinadas.

## 2. Componentes Implementados
- Geração de sinal sintético + ground-truth em `src/data_loader.py`.
- Detectores (PageHinkley, ADWIN, DDM) em `src/detectors.py`.
- Métricas de avaliação (TP/FP/FN, atraso médio) em `src/evaluation.py`.
- Loop de detecção streaming + CLI em `src/streaming_detector.py`.
- Grid search simples com ranking por F1 em `src/grid_search.py`.
- Download de dataset Zenodo (record 6879233) em `src/zenodo_download.py`.
- Preprocessamento simples genérico em `src/prepare_dataset.py` (entrada única + eventos externos).
- Port/parcial de scripts R (`find_all_files.R`, `read_ecg.R`, `pre_process.R`) convertido para Python em `src/ecg_preprocess.py`.
- README expandido (seções de integração real + novo preprocess de regimes).
- Instruções permanentes para assistente em `.github/copilot-instructions.md`.

## 3. Novo Módulo: `ecg_preprocess.py`
Funções principais:
- Descoberta de ficheiros `.hea` filtrando classes (persistent_afib, paroxysmal_afib, non_afib) + limite por classe (`--limit-per-class`).
- Leitura de cabeçalho (freq, nº sinais) + CSV comprimido (`.csv.bz2`) + anotações (`.atr.csv.bz2`).
- Extração de eventos de regime a partir de `label_store ∈ {28,32,33}`.
- Resample opcional (ex.: 200 → 250 Hz) via interpolação linear.
- Limpeza de eventos duplicados próximos (<15 samples) e remoção de bordas (<=10 do início/fim) – fiel ao `clean_truth` do R.
- Construção de CSV tidy: colunas `id, sample_index, ecg, regime_change`.
- Filtro: remove registos sem qualquer evento de regime.

Correções aplicadas:
- Erro inicial: falha ao converter colunas object → float ("Cannot cast array data from dtype('O')...").
- Solução: coerção numérica robusta + detecção de header redundante + preenchimento de NaNs.

## 4. Validação Rápida Realizada
Comando usado (classe única paroxysmal_afib, 10 ficheiros):
```
python -m src.ecg_preprocess \
  --root data/zenodo_6879233/extracted/afib_regimes \
  --classes paroxysmal_afib \
  --limit-per-class 10 \
  --lead II \
  --resample-to 250 \
  --output data/afib_paroxysmal_tidy.csv
```
Resultado:
- Linhas totais: 586,554
- Registos (ids): 10
- Eventos de regime (soma): 46
- Eventos por registo (descr.): min=1, mediana=4, máx=10
- Exemplo primeiro id: ~145,971 samples, 1 evento em posição ~70,599.

Execução do detector ADWIN:
```
python -m src.streaming_detector \
  --data data/afib_paroxysmal_tidy.csv \
  --detector adwin --ma-window 25 \
  --min-gap-samples 3000 --param delta=0.01 \
  --tolerance 500 --sample-rate 250
```
Métricas obtidas (pipeline concatenando todos os ids):
- Detecções: 41 | Ground-truth: 46
- TP=2, FP=39, FN=44
- Precision ≈ 0.049 | Recall ≈ 0.043 | Delay médio ≈ 106 samples (~0.424 s)

Interpretação inicial:
- Muitos FP: provável influência de mudanças de baseline entre registos + delta não ajustado + ausência de features derivadas dentro do fluxo.

## 5. Estrutura Atual dos Principais Arquivos
- `src/streaming_detector.py`: loop streaming + opções de pré-processamento (média móvel, derivada) + min-gap + JSON logging.
- `src/ecg_preprocess.py`: conversão batch dos múltiplos registos WFDB → tidy CSV multi-id.
- `src/grid_search.py`: grid simples (atualmente orientado a dataset único); precisa adaptação multi-id.
- `R/`: scripts originais de referência (muito extensos) — não usados diretamente em runtime Python.

## 6. Decisões & Diretrizes Consolidadas
- Sem lookahead: processar amostra a amostra (condição mantida).
- Reprodutibilidade: dependências pinadas em `requirements.txt`.
- Não versionar dados grandes: pasta `data/` ignorada no `.gitignore`.
- Incrementos pequenos validados por execuções rápidas antes de expandir escopo.
- Documentar cada novo parâmetro no README (feito para ecg_preprocess principal; pendente para extensões futuras).

## 7. Backlog / Próximos Passos Recomendados
Curto prazo:
1. Adicionar coluna `time_seconds` ao CSV tidy (sample_index / fs) – para inspeção temporal.
2. Tornar códigos de anotação configuráveis via CLI (`--label-codes 28 32 33`).
3. Permitir manter registos sem eventos (`--keep-nochange`), útil para FP analysis.
4. Executar detecção por id individualmente e agregar métricas macro/micro.
5. Mini grid search real para ADWIN (`delta`): {0.005, 0.01, 0.02, 0.05} e comparar F1.
6. Opcional: aplicar derivada + normalização incremental (online z-score) antes de detectar.

Médio prazo:
7. Implementar outros detectores (EDDM, HDDM_A, HDDM_W) se suportados pela versão do scikit-multiflow.
8. Métrica de distribuição de atrasos (histograma + percentis) além do delay médio.
9. Adicionar testes unitários mínimos (clean_truth, resample, matching de eventos, build_tidy sem eventos).
10. Exportar métricas agregadas em JSON para ingestão posterior (ex.: dashboard).
11. Extender grid search para multi-run por semente / média dos resultados.
12. Pipeline de CI (lint + testes básicos) e badge no README.

Longo prazo:
13. Suporte multi-lead (wide vs long) e seleção automática de lead com maior SNR.
14. Detecção adaptativa híbrida (ex.: ADWIN sobre derivada + PageHinkley sobre média filtrada).
15. Compressão/segmentação incremental para reduzir custo em sinais muito longos (chunk streaming real).
16. Persistir regime indices crus (pré-limpeza) em JSON para auditoria.

## 8. Pendências Técnicas / Riscos
- Concatenar múltiplos ids pode inflar FP; precisa isolação por registo.
- Limpeza de eventos pode excluir mudanças muito cedo/tarde que façam sentido clinicamente (validar com domínio).
- Resample linear pode introduzir suavização leve; se houver QRS acurado envolvido em sinais curtos, talvez considerar métodos band-limited ou polyphase.

## 9. Comandos Úteis (Resumo)
Geração subset (paroxysmal_afib, 10 ficheiros):
```
python -m src.ecg_preprocess --root data/zenodo_6879233/extracted/afib_regimes \
  --classes paroxysmal_afib --limit-per-class 10 \
  --lead II --resample-to 250 \
  --output data/afib_paroxysmal_tidy.csv
```
Detecção ADWIN:
```
python -m src.streaming_detector --data data/afib_paroxysmal_tidy.csv \
  --detector adwin --ma-window 25 --min-gap-samples 3000 \
  --param delta=0.01 --tolerance 500 --sample-rate 250
```

## 10. Estado Final da Sessão
- Código consistente e executável; preprocess multi-registo funcional.
- README atualizado com seção sobre novo pipeline.
- Instruções de Copilot e memória persistente criadas.
- Próximo passo recomendado: execução por id + ajuste de delta.

---
(Atualizado em: 2025-09-27)
