# Comparação de Métodos de Agregação (Atualizado 2025-11-25)

**Contexto**: `src.cross_dataset_analysis.py` agora aceita `--min-datasets`. Estamos usando `min_datasets = número de datasets carregados (3)` para evitar configurações “especialistas” que só existem em um dataset.

---

## 🧮 Métodos

| Método | Descrição | Quando usar |
|--------|-----------|-------------|
| **File-Weighted (micro)** | Concatena todas as linhas e calcula a média ponderada pelo nº de ficheiros. `afib_paroxysmal` recebe ~80% do peso. | Para analisar o “teto” possível quando o dataset maior domina ou para comparar com resultados históricos. |
| **True Macro (default)** | Calcula a média por dataset primeiro e depois faz média simples entre datasets, exigindo `n_datasets=3`. | Quando precisamos de configurações que generalizam entre classes de arritmia diferentes. |

---

## 📊 Ranking True Macro (com cobertura garantida)

| Rank | Detector | Score | Std | Comentário |
|------|----------|-------|-----|------------|
| **1** 🥇 | **FLOSS** | **0.3958** | 0.0972 | Ainda campeão; agora com `window=125`. |
| **2** 🥈 | **KSWIN** | **0.2976** | 0.1015 | Pódio consolidado; pequena queda vs relatório anterior. |
| **3** 🥉 | **ADWIN** | **0.2835** | 0.0745 | Novo top-3 após ampliar `min_gap` para 2000. |
| 4 | Page-Hinkley | 0.2625 | 0.0966 | Perdeu 0.12 p.p. quando forçado a `n_datasets=3`. |
| 5 | HDDM_A | 0.2584 | **0.0593** | Melhor robustez absoluta. |
| 6 | HDDM_W | 0.1252 | 0.1552 | Continua impróprio para uso geral. |

---

## 📉 Ranking File-Weighted (referência histórica)

| Rank | Detector | Score | Std | Observação |
|------|----------|-------|-----|------------|
| **1** 🥇 | **FLOSS** | **0.4491** | 0.2244 | Mesma configuração de 24/11 (window=75). |
| 2 | KSWIN | 0.3773 | 0.2114 | Pouca variação. |
| 3 | ADWIN | 0.3629 | 0.2145 | Inclui combinações ausentes nos datasets pequenos. |
| 4 | Page-Hinkley | 0.3345 | 0.2018 | Idem. |
| 5 | HDDM_A | 0.3273 | 0.1944 | Score superior graças ao peso do afib. |
| 6 | HDDM_W | 0.2843 | 0.2567 | Permanece instável. |

---

## 🔍 Principais Diferenciais Após o Filtro

1. **ADWIN e Page-Hinkley** agora aparecem no ranking macro real (antes eram removidos). Seus scores caíram 17–32%, evidenciando a dependência do dataset maior.
2. **FLOSS** manteve a liderança nos dois métodos — prova de que o desempenho não dependia do viés de peso.
3. **Min_gap_samples** divergiu:
   - Macro: ADWIN e HDDM_A → 2000; restante → 1000.
   - File-weighted: praticamente todos mantêm 1000, confirmando que o dataset afib tolera janelas menores entre alertas.
4. **Robustez**: HDDM_A destaca-se (std 0.059). ADWIN vem em seguida (0.0745) e se torna opção generalista aceitável quando não é possível usar FLOSS/KSWIN.

---

## ✅ Recomendações Práticas

1. **Use True Macro como métrica principal** para qualquer decisão de produção ou documentação oficial.
2. **Reporte File-Weighted apenas** como baseline histórico/bibliográfico, deixando claro o viés.
3. **Quando executar o script manualmente**, mantenha:
   ```bash
   python -m src.cross_dataset_analysis \
       --detector <nome> \
       --mode true_macro \
       --min-datasets 3
   ```
4. **Documente a configuração macro** nos READMEs específicos do detector (já atualizado) e nas comparações (`results/comparisons/...`) para evitar regressões.
